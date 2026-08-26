# ubx-schema-kubernetes

A real, frozen, versioned Kubernetes provider schema snapshot -- the pinnable
distribution artifact `ubx-provider-dynamic` and `ubiquex` resolve a
`[providers.kubernetes]`/`[providers.kubernetes_ds]` entry against, with
zero network calls at schema resolution time (see
`provider/acquireschema.go` in `ubiquex`, and `internal/snapshot`'s own
doc comment in `ubx-provider-dynamic`).

## What's here

Kubernetes' own real published identity is a GROUP of two members, both
fetched from the identical live spec but built through genuinely
different pipelines:

- `kubernetes` -- resource mode (92 real resource types).
- `kubernetes_ds` -- data-source mode (116 real, unclaimed read-only
  operations).

- `manifest.json` -- the group's own real identity: `schema_format`,
  `provider`, one `version` for the WHOLE group, and which member names
  it bundles.
- `members/<name>.json` -- one real, complete, independently-diffable
  file per member (`kubernetes.json`, `kubernetes_ds.json`). Committed
  as separate files, not one combined blob, so a real version bump's own
  git diff shows exactly which members changed -- this matters at scale
  (a provider like AWS bundles hundreds of members; a one-service change
  should not touch every other service's own file).
- `.github/workflows/hash-watch.yml` -- runs weekly (and on manual
  dispatch), regenerates every member from the live spec and opens a PR
  only when the group's own mechanically-derived version (the highest
  real change level found across every member -- `internal/snapshot`'s
  `AssembleGroup`) actually moves. Never auto-merges.
- `.github/workflows/publish.yml` -- manual-dispatch-only. Packs
  `manifest.json` and every `members/*.json` into one compressed archive
  (`snapshot.tar.gz`) and cuts a real GitHub Release tagged `v<version>`
  carrying exactly two assets: `snapshot.tar.gz` and `SHA256SUMS`. The
  archive exists purely so a real pinned resolution is still one real
  download regardless of how many members a group has -- the COMMITTED
  files (what a reviewer actually sees) are always the separate,
  per-member ones above.

## Consuming a real, published version

In `ubiquex`, pin each real member you need:

```toml
[providers.kubernetes]
source  = "ubiquex/kubernetes"
version = "2.0.0"

[providers.kubernetes_ds]
source  = "ubiquex/kubernetes"
version = "2.0.0"
```

Both point at the SAME repo/version -- `provider.AcquireSchema`'s own
cache-by-source+version already collapses this into ONE real download
and ONE extracted cache directory
(`~/.ubx/schemas/ubiquex/kubernetes/2.0.0/`) regardless of how many
members reference it; each launched process picks its own member back
out of the shared group by the `UBX_DYNAMIC_PROVIDER_NAME` it already
receives.

## Versioning

One real, mechanically-derived semver number for the WHOLE group, not
one per member: the highest real change level found across every
member (a brand new resource type or a field that gained write access
bumps MINOR; a resource type or field that disappeared, or a field that
lost write access, bumps MAJOR; a pure description-text change bumps
PATCH), plus an unconditional MAJOR if a member the group used to bundle
is gone entirely. See `internal/snapshot/diff.go` and `AssembleGroup` in
`ubx-provider-dynamic` for the real rule.

`v2.0.0` is a real, deliberate break from `v1.0.0` (the original,
single-member, flat-file format, superseded rather than kept
compatible) -- the group-container shape (multiple members, explicit
resource/data-source mode) is a genuinely different, incompatible
snapshot format, not a routine content update.
