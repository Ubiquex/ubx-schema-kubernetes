#!/usr/bin/env python3
"""Fail if the committed snapshot pins an out-of-date ubx-provider-dynamic.

WHY THIS EXISTS. A snapshot records which binary generated it, and every
`ubx sdk gen` fetches exactly that binary. So the stamp decides what a
consumer actually runs, long after the snapshot was cut.

On 2026-09-07 that went wrong quietly (UBI-241). The Monday scheduled
run cut snapshot PRs across six schema repos at 11:00, stamping
ubx-provider-dynamic 1.0.13. At 14:12 v1.1.0 was released, changing
which data sources the binary derives. Nothing rechecked the six open
PRs. Merging any of them would have pinned a pre-fix binary
permanently, regenerated the SDKs to byte-identical output, and
published releases claiming a fix that had not shipped.

The failure mode is a merge that looks completely normal. This turns it
into a visible one.

DELIBERATELY A WARNING ON main, A FAILURE ON A PULL REQUEST. A committed
snapshot legitimately lags the newest binary most of the time, and
failing main for that would be noise. A snapshot being *proposed* right
now is a different thing: it should be cut against what is current, and
if it is not, re-cutting costs one dispatch.
"""

from __future__ import annotations

import json
import os
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LATEST = "https://api.github.com/repos/Ubiquex/ubx-provider-dynamic/releases/latest"


def parse(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in v.strip().lstrip("v").split(".") if p.isdigit())


def main() -> int:
    manifest = json.loads((ROOT / "manifest.json").read_text())
    stamped = manifest.get("generated_by_binary_version") or manifest.get("min_binary_version")
    if not stamped:
        print("manifest.json records no generating binary version at all", file=sys.stderr)
        return 1

    req = urllib.request.Request(LATEST, headers={"Accept": "application/vnd.github+json"})
    if tok := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {tok}")
    try:
        latest = json.load(urllib.request.urlopen(req, timeout=30))["tag_name"]
    except Exception as err:  # noqa: BLE001
        # Never fail a build because GitHub was unreachable. The guard is
        # worth having; it is not worth blocking on an API blip.
        print(f"could not read the latest ubx-provider-dynamic release ({err}); skipping", file=sys.stderr)
        return 0

    if parse(stamped) >= parse(latest):
        print(f"ok: snapshot pins ubx-provider-dynamic {stamped}, latest is {latest}")
        return 0

    on_pr = os.environ.get("GITHUB_EVENT_NAME") == "pull_request"
    where = "This snapshot" if on_pr else "The committed snapshot"
    print(
        f"{where} pins ubx-provider-dynamic {stamped}, but {latest} is released.\n"
        f"Every `ubx sdk gen` against it would run {stamped}, so anything the newer\n"
        f"release changed about what the binary derives would not reach consumers.",
        file=sys.stderr if on_pr else sys.stdout,
    )
    if on_pr:
        print(
            "\nRe-cut it: dispatch hash-watch.yml, which builds from the latest release.\n"
            "If the regeneration reports no change, the release changed behaviour rather\n"
            "than content, and the dispatch needs force_binary_version_bump.",
            file=sys.stderr,
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
