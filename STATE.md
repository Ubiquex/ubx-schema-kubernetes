# STATE.md — current state

> Rewritten, not appended, as the LAST act of every session. See `HISTORY.md`
> for the narrative.

## In flight

Nothing in flight as of 2026-08-27.

## Blocked

Nothing blocked. Zero open PRs.

## Current release

Latest published: `v3.0.1` (verify directly — `gh api
repos/Ubiquex/ubx-schema-kubernetes/releases/tags/v3.0.1` — don't trust this
file if it's gone stale). 2 members (`kubernetes` resource, `kubernetes_ds`
data-source). Carries a real `min_binary_version` (`1.0.1`) — a pinned
`[providers.kubernetes]` resolution does NOT need `ubiquex`'s own bootstrap
fallback anymore; confirmed live, zero-network, against this exact release.

## Before touching anything

- Never self-merge here. See `CLAUDE.md`.
- If regenerating: build `ubx-provider-dynamic` from ITS OWN latest real
  release tag, not a local checkout or `main` HEAD, or the new snapshot loses
  its real `min_binary_version` (see `CLAUDE.md`).
