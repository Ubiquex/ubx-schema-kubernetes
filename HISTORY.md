# HISTORY.md — narrative archive

> Consulted only when a session needs to know why a decision was made, not on
> every open. For what's current, read `STATE.md` instead.

This file is new as of UBI-183 (2026-08-27). Real history predating it lives
in `ubiquex`'s own `HISTORY.md` (search `UBI-182`, `UBI-194`) and in this
repo's own real `git log`/merged-PR history, which is authoritative for what
actually shipped and when.

## Real, known decisions worth carrying forward

**First real published version was `1.0.0`, not `0.1.0`.** This repo's own
first `publish.yml` dispatch used `0.1.0` (`ubx-provider-dynamic`'s own
generic default for a first-ever snapshot at the time). The founder corrected
this before this repo's own Stage E work: a schema snapshot's version
communicates what changed in the vendor's own API surface, not artifact
maturity — there is no pre-1.0 phase for something complete on first publish.
The erroneous `v0.1.0` release was deleted (confirmed gone via `gh release
view` and a direct tag-ref API 404, not just the delete command's exit
status) and `manifest.json`'s own version hand-corrected before republishing
as `v1.0.0`. `ubx-provider-dynamic`'s own `NextVersion("", ...)` default was
fixed at the root afterward so this wasn't a one-off correction repeated by
hand for every other schema repo.

**`kubernetes_ds`'s own real published type-name prefix bug.** `v2.0.0`'s
real, published release asset served every data-source type under the wrong
`kubernetes_ds_` prefix instead of the intended, shared `kubernetes_` prefix —
correct COUNT (116), wrong NAMES, a class of bug a count-only check would
never catch. Fixed at the source; this repo's own live pinned test
(`ubiquex`'s `cli/dynamicprovider_pinned_live_test.go`) checks specific,
hand-picked type names AND that no returned name anywhere carries the wrong
prefix, specifically because of this incident.

**`v3.0.0 -> v3.0.1`: a real `min_binary_version`-only bump, zero API drift**
(UBI-194, 2026-08-27). See `ubx-provider-dynamic`'s own `HISTORY.md` for the
full story — `AssembleGroup`'s version-derivation logic didn't originally
account for a `min_binary_version` transition with no content change, so the
first attempt at this regeneration was silently discarded by this repo's own
`hash-watch.yml` "is this newer" gate. Fixed at the source, re-run for real.
