# Join the Deltanium network — public vouchers

**Step-by-step guide:** https://deltanium.com/node-setup.html

Use a **one-shot voucher** below to register a community **Store** or **Block Creator** node against production Central API:

**https://api.deltanium.com**

Each code works **once**. Prefer Store codes for storage nodes and Blocker codes for block creators (they share the same DB pool).

## How joining works

1. **Register.** On first start the node creates its key and sends a registration **signed with that key** (the easiest way is the
   [installer](https://deltanium.com/node-setup.html)). Central answers `202` with status `awaiting_payment`. The voucher is checked but **not spent yet**.
2. **Pay the registration fee: 100,000 VND**, by bank transfer or PayPal, with the transfer note Central gives (`NODE…`).
   The node log, the installer and `GET https://api.deltanium.com/api/noderegistration/<node public key>` show the amount, account and note.
3. **Super Admin approval.** The Super Admin matches the payment and signs the approval. Only then is the voucher spent.
4. **Activation.** Central checks that the node answers on its address (HTTPS or DLTP) and activates it. Until it answers, it stays `approved`
   and Central retries every few minutes. Node lists only show nodes that are online.

> Public vouchers are first-come, first-served, but a code is spent only by an approved, paid registration: registering many fake nodes
> cannot burn the list. If someone else's approved registration used your code first, pick another one.

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
export NodeRegistration__ApiUrl="https://api.deltanium.com"
export NodeRegistration__Endpoint="https://your-store.example.com"   # public HTTPS URL of your node
export CentralApi__BaseUrl="https://api.deltanium.com"
export STORE_VOUCHER="PUBLIC-STORE-01-41A6E1BA"   # pick an unused code
```

> The Store reads `NodeRegistration__Endpoint`, not `NODE_ENDPOINT`. Without it the node registers its local address.

Calling `/api/storenode/register` by hand is not enough any more: the body must be signed with the node key (`timestamp`, `signature`). Let the node register itself.

Then pay the fee (see **How joining works**) and wait for approval. Confirm discovery:

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
export VOUCHER="PUBLIC-BLOCKER-01-2EE10206"   # pick an unused code
export CENTRAL_API_PUBLIC_KEY="0390329609c78fff2cd895cb3faf30b1fa868085da0e89dbeeff642258773c9191"
export SUPER_ADMIN_PUBLIC_KEY="021fd57c80fd85156c307e2f1c0bc278ea0eeabac930835ab989803ee2d77165f7"
dotnet run -c Release
```

Check both keys against [NODE_KEYS.md](NODE_KEYS.md).

Calling `/api/BlockCreatorNode/register` by hand is not enough any more: the body must be signed with the node key. Let the node register itself.


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
