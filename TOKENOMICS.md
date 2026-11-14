# Deltanium economic model (D coin)

Status: **design target** for the live MVP network.  
D is the **utility credit** of the Deltanium network (storage, transaction fees, later tips / node incentives). It is **not** marketed as a redeemable 1:1 bank stablecoin.

Related: [VOUCHERS.md](VOUCHERS.md) (node join) · [README.md](README.md) (repos & production hosts)

---

## 1. Principles

1. **Hard-capped supply** — fixed at genesis. No mint when a user registers or tops up.
2. **Fiat → D is a purchase from treasury** — existing D is transferred; supply does not increase.
3. **Fees fund work** — users pay Store / Block Creator (and later Router / other) nodes in D for real services.
4. **Team & investors are not a per-top-up tax** — they are paid via **vesting + company revenue**, not a visible cut labeled “investor” on every deposit.
5. **Transparency** — treasury addresses, remaining inventory, and fee schedule are publishable.

---

## 2. Genesis allocation

Total supply (hard cap): **10,000,000 DLT** = **`10_000_000_000_000 D`** (10^13 D).

**Units:** base unit **D** with **1 D = 1 VND**; display unit **Deltanium (DLT)** with **1 DLT = 1,000,000 D** (= 1,000,000 VND). Ledger and API amounts are always in D.

| Bucket | Share | Purpose |
|--------|------:|---------|
| Network treasury | 40% | Sell to users on fiat on-ramp; bootstrap node subsidies; incident reserve |
| Ecosystem / grants | 15% | Partners, bounties, growth (time-locked / vested) |
| Team + developers | 20% | 2–4 year vesting, 6–12 month cliff |
| Investors | 15% | Per investment agreements, vested |
| Community / liquidity | 10% | Future DEX/pools and controlled campaigns |

**Rules**

- Investor and salary spend come from **equity / company fiat revenue / unlocked vesting**, not from minting.
- Unsold treasury D stays in a **public treasury wallet**.

---

## 3. Fiat on-ramp (user buys D)

### Posted quote (example)

| | |
|--|--|
| Reference rate | **1 VND → 1 D** (before fee); 1 DLT = 1,000,000 D |
| Platform fee | **15%** |
| User receives | **850 D** per 1,000 VND paid (0.85 DLT per 1,000,000 VND) |

UI must show: reference rate, fee %, **D credited**, and order id.

### Fiat split (per 1,000 VND received)

| Destination | Share of fiat | Notes |
|-------------|--------------:|-------|
| User’s D purchase | 85% | Treasury sends **850 D** to the user’s pubkey |
| Platform (operating company) | 10% | Cash: Central hosting, support, legal, engineering payroll |
| Network reserve | 5% | Held as fiat and/or D in a **public network treasury** for protocol needs |

There is **no** separate “investor %” on each top-up.

### Anti-inflation

- Top-up **never mints**.
- Only **transfers** D from treasury → user (and optional reserve accounting).

### Trust checklist for on-ramp

1. Legal entity receives fiat (PSP / bank); receipts + ToS.
2. Public **treasury** pubkey / address and remaining D inventory.
3. Each paid order maps to an on-chain (or ledger) **D credit tx**.
4. Refund policy if D is not credited within a stated window.
5. Later: third-party on-ramps / DEX so Central holds less fiat over time.

---

## 4. In-network cash flow (D after purchase)

Users spend D for services (storage contracts, tx fees, later tips).

Suggested fee split on **protocol service fees** (tunable by governance later):

| Recipient | Share | Role |
|-----------|------:|------|
| Service nodes (Store / Blocker / …) | ~70% | Pay for real work |
| Burn or network treasury | ~20% | Sink / long-term reserve |
| Protocol ops | ~10% | Documented Central / protocol cost |

**Nodes earn D from fees**, not from inflationary registration rewards.

---

## 5. New users & free tier

| Event | D granted |
|-------|-----------|
| Account registration | **0 D** |
| Optional free tier | Small **storage / message quota** subsidized by treasury (not a farmable airdrop) |
| Real usage beyond quota | Requires fiat top-up → D |

---

## 6. Implementation status

Central API now exposes a **wallet ledger** (MySQL tables `wallet_accounts`, `wallet_ledger`, `topup_orders`; JSON fallback under `wallet-data/`):

| Endpoint | Auth | Purpose |
|----------|------|---------|
| `GET /api/wallet/economics` | public | Cap, fee %, treasury balance |
| `GET /api/wallet/balance` | signed user | Balance for caller |
| `GET /api/wallet/ledger` | signed user | Recent ledger rows |
| `POST /api/wallet/transfer` | signed user | P2P D transfer |
| `POST /api/wallet/topup` | signed user | Create pending fiat order (quote) |
| `POST /api/wallet/topup/complete` | Super Admin sig on TopUp SignPayload | Build network TopUp → blockers → then credit ledger |
| `GET /api/wallet/admin/topups` | `X-Internal-Token` | List orders (+ `signPayload` for pending) |
| `POST /api/wallet/admin/topup/approve` | Internal token + Super Admin on SignPayload | Same finalize path as complete |

**Network TopUp tx (blocker):**
- `Type=TopUp`, `Id=orderId`, `From=Central pubkey`, `To=buyer`
- `SignPayload` signed by **Central** + **Super Admin** (`signature` + `superAdminSignature`)
- Blocker requires `CENTRAL_API_PUBLIC_KEY` and `SUPER_ADMIN_PUBLIC_KEY`
- Wallet ledger credit runs **only after** at least one blocker accepts (or 409 duplicate)

- Genesis seeds **40% hard cap** into treasury account `deltanium-treasury` on first boot.
- `Economics:EnforceFees` defaults to **false** so existing flows keep working until balances are funded.
- App Profile → **Wallet** shows balance and creates top-up orders.
- Ops UI: `https://api.deltanium.com/admin/topup.html`
- Prod: API + each blocker need `SUPER_ADMIN_PUBLIC_KEY`; Super Admin keeps private key offline.

Still to do: automate fiat PSP, enforce non-zero fees on storage/tx, node payout split, public dashboard UI.

---

## 7. Parameter summary (defaults)

| Parameter | Default |
|-----------|---------|
| Total supply | 10,000,000 DLT = 10^13 D (hard cap) |
| Units | 1 D = 1 VND; 1 DLT = 1,000,000 D |
| Minimum top-up | 10,000 VND |
| Register grant | 0 D |
| On-ramp fee | 15% |
| User D per 1,000 VND at 15% fee | 850 D |
| Fiat to platform | 10% of payment |
| Fiat/D to network reserve | 5% of payment |
| Service fee to nodes | ~70% |
| Service fee burn/treasury | ~20% |
| Service fee protocol | ~10% |

Parameters may change with a published version bump; genesis cap should not.

---

## 8. One-line summary

**Hard-capped D → sold from treasury for fiat → ~15% transparent platform/network fee on purchase → in-network D pays nodes for work; team and investors are funded by vesting and company revenue, not by minting or a hidden per-deposit investor tax.**
