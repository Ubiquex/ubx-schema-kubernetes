# ubx-schema-kubernetes

A real, frozen, versioned Kubernetes provider schema snapshot -- the pinnable
distribution artifact `ubx-provider-dynamic` and `ubiquex` resolve a
`[providers.kubernetes]` entry against, with zero network calls at schema
resolution time (see `provider/acquireschema.go` in `ubiquex`, and
`internal/snapshot`'s own doc comment in `ubx-provider-dynamic`).

## What's here

- `snapshot.json` -- the real, committed snapshot. Generated from
  Kubernetes' own live OpenAPI/Swagger description
  (`https://raw.githubusercontent.com/kubernetes/kubernetes/release-1.37/api/openapi-spec/swagger.json`)
  via `ubx-provider-dynamic --generate-snapshot`, unchanged from what that
  binary wrote. Committed at the repo root, not release-only, so a real
  reviewer sees the real diff on every version bump.
- `.github/workflows/hash-watch.yml` -- runs weekly (and on manual
  dispatch), regenerates a fresh snapshot from the live spec, and opens a
  PR if the mechanically-derived version (`internal/snapshot`'s own
  `DiffLevel`/`NextVersion`, not a hand-picked bump) moved. Never
  auto-merges.
- `.github/workflows/publish.yml` -- manual dispatch only. Cuts a real
  GitHub Release tagged `v<version>` (matching `snapshot.json`'s own
  committed version) carrying exactly two assets: `snapshot.json` and
  `SHA256SUMS`.

## Consuming a real, published version

In `ubiquex`, pin a stack's `[providers.kubernetes]` entry:

```toml
[providers.kubernetes]
source  = "ubiquex/kubernetes"
version = "0.1.0"
```

`provider.AcquireSchema` resolves that to
`github.com/ubiquex/ubx-schema-kubernetes`'s own release tagged `v0.1.0`,
downloads `snapshot.json`, verifies it against `SHA256SUMS`, and caches it
at `~/.ubx/schemas/ubiquex/kubernetes/0.1.0/` -- every subsequent
resolution reads the verified local cache, no network involved.

## Versioning

One real, mechanically-derived semver number, not hand-picked: a brand new
resource type or a field that gained write access bumps MINOR; a resource
type or field that disappeared, or a field that lost write access, bumps
MAJOR; a pure description-text change bumps PATCH; an identical spec bumps
nothing at all. See `internal/snapshot/diff.go` in `ubx-provider-dynamic`
for the real rule.
