# ubx-schema-kubernetes

A real, frozen, versioned Kubernetes provider schema snapshot -- the pinnable
distribution artifact `ubx-provider-dynamic` and `ubiquex` resolve a
single `[providers.kubernetes]` entry against, with zero network calls at
schema resolution time (see `provider/acquireschema.go` in `ubiquex`, and
`internal/snapshot`'s own doc comment in `ubx-provider-dynamic`). The
resource/data-source split below is a real, internal discovery-time
detail -- one pin resolves both.

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

In `ubiquex`, one real pin resolves the whole group -- both real members
(`kubernetes` resource mode, `kubernetes_ds` data-source mode) are served
together from the SAME launch, the SAME real download:

```toml
[providers.kubernetes]
source  = "ubiquex/kubernetes"
version = "3.0.0"
```

`provider.AcquireSchema`'s own cache-by-source+version resolves ONE real
download and ONE extracted cache directory
(`~/.ubx/schemas/ubiquex/kubernetes/3.0.0/`) -- the launched process
merges every real member of the group (`internal/snapshot.MergeOpenAPIGroup`)
into one served schema, `ResourceSchemas` and `DataSourceSchemas`
together, exactly like a real, hand-written Terraform provider already
looks from the outside.

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

`v3.0.0` (`kubernetes` resource content unchanged, `kubernetes_ds` a
real, breaking content correction) is UBI-182's own resource/
data-source collapse, landing here twice over: (1) `hash-watch.yml`'s
own driving config collapses from two `[dynamic_providers.*]` tables to
one (`config.Provider.DataSources`' own doc comment, ubx-provider-dynamic),
matching the identical collapse ubiquex's own `sdk/providers/.ubx/config`
went through for every provider. (2) A real, live bug surfaced while
regenerating under that collapse: the wire_name fix that corrected
`kubernetes_ds`'s own type-name prefixes (`kubernetes_ds_*` -> the
intended, shared `kubernetes_*`) had been merged into this repo's own
`main` branch but never actually republished -- `v2.0.0`'s real release
asset kept serving the old, wrong prefixes the whole time. `v3.0.0` is
the first real release to carry the fix.
