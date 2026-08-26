# Deltanium

Decentralized social network on a custom blockchain, with encrypted storage and Proxy Re-Encryption (PRE).

Public repositories live under [github.com/dlvstudio](https://github.com/dlvstudio).

## Repositories

| Repository | Role | Default port |
|------------|------|----------------|
| [deltanium-core](https://github.com/dlvstudio/deltanium-core) | Crypto, BIP39, Umbral PRE (Rust FFI) | — |
| [deltanium-api](https://github.com/dlvstudio/deltanium-api) | Central coordinator: users, follow graph, store/blocker registry, PRE rekeys | 5002 |
| [deltanium-store](https://github.com/dlvstudio/deltanium-store) | Encrypted content storage node | 5001 |
| [deltanium-blocker](https://github.com/dlvstudio/deltanium-blocker) | Block creator: mempool, blocks, validation | 5003 |
| [deltanium-app](https://github.com/dlvstudio/deltanium-app) | Flutter client (iOS / Android / macOS / web) | — |
| [deltanium-user](https://github.com/dlvstudio/deltanium-user) | .NET client library and demos | — |
| [deltanium-landing](https://github.com/dlvstudio/deltanium-landing) | Marketing site | — |

## Local setup (short)

1. Copy example config where needed:
   - `deltanium-api/vouchers.json.example` → `vouchers.json`
   - Central API creates `central_keys.json` on first run
   - Store and Blocker create `node_info.json` on first registration (keep this file private)
2. Run API, then Store, then Blocker, then the Flutter app.
3. Point the app at `http://127.0.0.1:5002/api` (`CENTRAL_API_BASE`).

Do not commit `central_keys.json`, `node_info.json`, `users.json`, chat data, or any mnemonic / private key.

## Status

Prototype / MVP. Persistence is file-based JSON, not a production database. Inspector and Router nodes are not implemented yet.
