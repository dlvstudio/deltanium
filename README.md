# Deltanium

Decentralized social network on a custom blockchain, with encrypted storage and Proxy Re-Encryption (PRE).

Public repositories live under [github.com/dlvstudio](https://github.com/dlvstudio).

## Production

| Service | URL |
|---------|-----|
| Landing | [https://deltanium.com](https://deltanium.com) · [https://www.deltanium.com](https://www.deltanium.com) |
| App (Flutter web) | [https://app.deltanium.com](https://app.deltanium.com) |
| Central API | [https://api.deltanium.com](https://api.deltanium.com) (`/api` base for clients) |
| Store node 1 | [https://store-1.deltanium.com](https://store-1.deltanium.com) |
| Store node 2 | [https://store-2.deltanium.com](https://store-2.deltanium.com) |
| Block creator 1 | [https://blocker-1.deltanium.com](https://blocker-1.deltanium.com) |

## Repositories

| Repository | Role | Production | Local port |
|------------|------|------------|------------|
| [deltanium-core](https://github.com/dlvstudio/deltanium-core) | Crypto, BIP39, Umbral PRE (Rust FFI) | — | — |
| [deltanium-api](https://github.com/dlvstudio/deltanium-api) | Central coordinator: users, follow graph, store/blocker registry, PRE rekeys | [api.deltanium.com](https://api.deltanium.com) | 5002 |
| [deltanium-store](https://github.com/dlvstudio/deltanium-store) | Encrypted content storage node | [store-1](https://store-1.deltanium.com) · [store-2](https://store-2.deltanium.com) | 5001 |
| [deltanium-blocker](https://github.com/dlvstudio/deltanium-blocker) | Block creator: mempool, blocks, validation | [blocker-1.deltanium.com](https://blocker-1.deltanium.com) | 5003 |
| [deltanium-app](https://github.com/dlvstudio/deltanium-app) | Flutter client (iOS / Android / macOS / web) | [app.deltanium.com](https://app.deltanium.com) | — |
| [deltanium-landing](https://github.com/dlvstudio/deltanium-landing) | Marketing site | [deltanium.com](https://deltanium.com) | — |

## Local setup (short)

1. **Secrets (never commit):**
   - API: User Secrets / `ConnectionStrings:Default`; optional `CENTRAL_*_KEY` or `~/.deltanium/central_keys.json`
   - Shared: `INTERNAL_API_TOKEN` on API + Store + Blocker
   - Store: `STORE_VOUCHER`; Blocker: `VOUCHER` (one-shot; consumed atomically)
   - JSON examples only: `vouchers.json.example`, `central_keys.json.example`
2. Run API, then Store, then Blocker, then the Flutter app.
3. Point the app at `http://127.0.0.1:5002/api` (`CENTRAL_API_BASE`).
4. Optional N-of-M: `--dart-define=REPLICATION_FACTOR=2` (default). App uploads full replicas to N stores and calls `POST /api/storedfile/register-replicas`.

Do not commit `central_keys.json`, `node_info.json`, `users.json`, `vouchers.json`, chat data, or any mnemonic / private key.

## License

Public repositories are released under the **MIT License** (same family as Bitcoin Core). See each repo’s `LICENSE` file.

## Status

Live MVP on the hosts above. Persistence prefers **MySQL**; JSON remains a local fallback. Content distribution is **N-of-M full replicas** orchestrated by the app (Central API indexes placements). Inspector and Router nodes are not implemented yet. Architecture overview: `deltanium-app/ARCHITECT.MD`.
