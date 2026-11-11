# Join the Deltanium network — public vouchers

Use a **one-shot voucher** below to register a community **Store** or **Block Creator** node against production Central API:

**https://api.deltanium.com**

Each code works **once**. After a successful register, Central marks it used. Prefer Store codes for storage nodes and Blocker codes for block creators (they share the same DB pool).

> Public vouchers are first-come, first-served. Do not reuse a code after someone else has registered with it.

## Store node vouchers

| # | Voucher |
|---|--------|
| 1 | `PUBLIC-STORE-01-41A6E1BA` |
| 2 | `PUBLIC-STORE-02-23CDBA0F` |
| 3 | `PUBLIC-STORE-03-ABB4D5BB` |
| 4 | `PUBLIC-STORE-04-663F7AB2` |
| 5 | `PUBLIC-STORE-05-E0391BC5` |
| 6 | `PUBLIC-STORE-06-437E3A4A` |
| 7 | `PUBLIC-STORE-07-A32B6207` |
| 8 | `PUBLIC-STORE-08-C17C54B2` |
| 9 | `PUBLIC-STORE-09-FD02D517` |
| 10 | `PUBLIC-STORE-10-0FBD713C` |

### Register a Store node

1. Clone [deltanium-store](https://github.com/dlvstudio/deltanium-store) (+ [deltanium-core](https://github.com/dlvstudio/deltanium-core) as sibling for build).
2. Point the node at Central and set a **public HTTPS endpoint** clients can reach.
3. Set voucher (env / secrets — never commit real codes into tracked config if you fork privately):

```bash
export CENTRAL_API_URL="https://api.deltanium.com"
export NODE_ENDPOINT="https://your-store.example.com"
export STORE_VOUCHER="PUBLIC-STORE-01-41A6E1BA"   # pick an unused code
```

Or call Central directly:

```bash
curl -sS -X POST "https://api.deltanium.com/api/storenode/register" \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "https://your-store.example.com",
    "voucher": "PUBLIC-STORE-01-41A6E1BA",
    "publicKey": "<your-node-compressed-or-hex-pubkey>"
  }'
```

Confirm discovery:

```bash
curl -sS "https://api.deltanium.com/api/storenode/list"
```

## Block Creator vouchers

| # | Voucher |
|---|--------|
| 1 | `PUBLIC-BLOCKER-01-2EE10206` |
| 2 | `PUBLIC-BLOCKER-02-B1620275` |
| 3 | `PUBLIC-BLOCKER-03-AEB62F59` |
| 4 | `PUBLIC-BLOCKER-04-EEC32BCE` |
| 5 | `PUBLIC-BLOCKER-05-8064551E` |

### Register a Block Creator node

1. Clone [deltanium-blocker](https://github.com/dlvstudio/deltanium-blocker).
2. See [REGISTRATION.md](https://github.com/dlvstudio/deltanium-blocker/blob/main/REGISTRATION.md).
3. Example:

```bash
export CENTRAL_API_URL="https://api.deltanium.com"
export NODE_ENDPOINT="https://your-blocker.example.com"
export VOUCHER="PUBLIC-BLOCKER-01-2EE10206"
# INTERNAL_API_TOKEN must match Central (ask maintainers if running a public blocker)
dotnet run
```

Or:

```bash
curl -sS -X POST "https://api.deltanium.com/api/BlockCreatorNode/register" \
  -H "Content-Type: application/json" \
  -d '{
    "endpoint": "https://your-blocker.example.com",
    "voucher": "PUBLIC-BLOCKER-01-2EE10206",
    "publicKey": "<your-node-pubkey>"
  }'
```

> Block creators that pull transactions need the shared `INTERNAL_API_TOKEN` with Central. Registration alone does not publish that secret.

## Machine-readable batch

[`vouchers/public-join-2026-11.json`](vouchers/public-join-2026-11.json)

## Related production hosts

| Service | URL |
|---------|-----|
| Landing | https://deltanium.com |
| App | https://app.deltanium.com |
| Central API | https://api.deltanium.com |
| Reference stores | https://store-1.deltanium.com · https://store-2.deltanium.com |
| Reference blocker | https://blocker-1.deltanium.com |
