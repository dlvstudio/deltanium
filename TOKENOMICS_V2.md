# Deltanium economic model v2 (D credit)

Status: **proposal** — supersedes [TOKENOMICS.md](TOKENOMICS.md) (v1) once accepted.
Related: [VOUCHERS.md](VOUCHERS.md) · [README.md](README.md)

v1 set the right principles (no mint on register, fiat buys existing D, fees pay for real work). v2 keeps them and fixes what makes v1 unworkable in practice: community nodes cannot cash out, fees never reach nodes, storage is priced far below cost, and the ledger the chain is supposed to secure lives only in Central's database.

---

## 0. What changes from v1

| Topic | v1 | v2 |
|-------|----|----|
| What D is | Hard-capped utility coin | **Prepaid service credit pegged to VND** (1 D = 1 VND; display unit 1 DLT = 1,000,000 D). Hard cap kept as a technical max supply, not a selling point |
| Fiat from top-ups | 85% unallocated, 10% platform, 5% reserve | **Fully backed**: the D-value of every top-up goes to a segregated **backing reserve** |
| On-ramp fee | Flat 15% | **3% bank transfer / VietQR**, 5% card, app-store price tiers for in-app purchase |
| Cash-out | None | **Redemption for nodes and creators** (KYC, 1% fee) |
| Fee split | Documented 70/20/10, implemented 100% → treasury | **Implemented per fee type** (§5) |
| Storage price | 0.01 D/GB-month at the old 1 D = 1,000 VND (≈ 10 VND, 10–60× below cost) | **800 D/GB-month per replica**, minimum fee per contract |
| Storage payment | Paid upfront to node | **Escrow, released monthly on passing proof-of-storage** |
| OpenEnded contract | One-time fee, deleted after 1 year | Replaced by **auto-renew from balance** |
| Bandwidth (reads) | Unpaid | Included quota + metered egress |
| Free tier | "Small quota" (undefined) | **Quota, not D**: 200 MB stored, 2 GB egress / month for verified users |
| Node admission | Voucher only | Voucher **+ bond** in D, slashable |
| Demand for D | Spending only | **Subscriptions (PRE), tips** — creators earn D |
| Genesis | 40% seeded, 60% not on ledger | **100% on ledger** in labelled accounts |
| Source of truth | Central MySQL | Ledger root anchored in blocks → later balances validated by blockers |

**Units (applied to v1 and code):** base unit **D**, **1 D = 1 VND** (`Economics:VndPerD = 1`). Display unit **Deltanium (DLT)**, **1 DLT = 1,000,000 D** (`Economics:DPerDlt`). Ledger, API and contracts always use D; the App shows large balances in DLT, e.g. `1,25 DLT (1.250.000 D)`. With the v1 15% fee, 1,000 VND buys 850 D.

---

## 1. Principles

1. **D is a credit for using the network, not an investment.** The price is fixed in VND so users and node operators can plan costs.
2. **Every circulating D is backed 1:1 by VND** in a segregated reserve, published monthly.
3. **Nobody mints by using the network.** D leaves the treasury only when it is bought, or when someone pays fiat into the reserve for it (grants, subsidies).
4. **Whoever does the work gets the fee**: Store nodes for storage and bandwidth, Block Creators for transactions, creators for content.
5. **Those who earn D can cash it out.** Users who only buy and spend D cannot redeem it. That keeps D a closed-loop credit for consumers.
6. **Verifiable**: the ledger is anchored on chain, and reserve and treasury balances are public.

---

## 2. Supply and accounts

- Max supply: **10,000,000 DLT = 10^13 D** (≈ 10,000 billion VND). **All of it** is credited at genesis to labelled accounts, so the ledger always sums to the cap.
- **Circulating D** = all D outside the issuance accounts below. This is the number the reserve must back.

| Account | Initial | Can release D when… |
|---------|--------:|---------------------|
| `treasury:issuance` | 10^13 D (10,000,000 DLT) | A top-up is paid, or fiat is deposited into the reserve for a grant or subsidy |
| `treasury:network-fund` | 0 D | Receives its fee share (§5). Pays free-tier and node subsidies |
| `treasury:protocol-ops` | 0 D | Receives its fee share (§5). Converted to company revenue by redeeming |
| `escrow:<contractId>` | 0 D | Storage escrow, released per epoch (§6) |
| `bond:<nodePubKey>` | 0 D | Node bond, slashable (§8) |

**Team and investors:** in v2 they are paid with **equity and company fiat revenue (protocol-ops share, platform fees), not D**. A pegged, backed credit has no upside to vest. Unbacked team D would also drain the reserve the moment it is redeemed. If a floating token is introduced later (§12), allocations are decided then.

**Returning D to issuance:** when D flows back to `treasury:issuance` (for example from a refund), it stops circulating and the matching VND in the reserve becomes free. That freed VND goes to the network fund.

---

## 3. On-ramp (user buys D)

Reference rate: **1 D = 1 VND** (`Economics:VndPerD`); 1 DLT = 1,000,000 D.

| Channel | Fee | User pays | User receives | Note |
|---------|----:|----------:|--------------:|------|
| Bank transfer / VietQR (web) | 3% | 100,000 VND | **97,000 D** | Default; fee covers payment provider + ops |
| Card (web) | 5% | 100,000 VND | **95,000 D** | Card processing cost |
| In-app purchase (iOS / Android) | Store fee passed through | Store price tier | Shown before purchase | App-store fee 15–30% is the store's, not Deltanium's |

Minimum top-up: **10,000 VND**.

### Where the fiat goes (web transfer, per 100,000 VND)

| Destination | Amount | Rule |
|-------------|-------:|------|
| **Backing reserve** (segregated account) | 97,000 VND | Always equals the D credited × 1 VND |
| Platform (company) | 3,000 VND | Payment provider costs + operations |

The UI must show the reference rate, the fee, D credited, and the order id. This is unchanged from v1.

### TopUp transaction

The v1 flow stays the same: `Type=TopUp` signed by Central and Super Admin, accepted by a blocker before the ledger is credited. v2 adds one field, `reserveDepositRef`: the bank or payment-provider reference of the fiat deposit, so each TopUp can be matched to a reserve statement.

---

## 4. Redemption (cash-out)

| | |
|--|--|
| Who | Registered Store / Block Creator operators, and creators with paid subscriptions (§9). **KYC required** |
| Rate | 1 D → 1 VND, minus **1%** fee (to platform) |
| Minimum | 100,000 D (0.1 DLT) |
| Schedule | Weekly batch payout to a verified bank account |
| Source | Backing reserve |
| Safeguard | If the reserve ratio drops below 100%, redemptions queue until it is restored, and the shortfall is published |

Regular users cannot redeem. A failed or uncredited top-up is still refunded as in v1.

---

## 5. Fees and how they are split

All splits are config values (`Economics:FeeSplit:*`), and every split leg is written as its own ledger row.

| Fee type | Who pays | Service node | Network fund | Protocol ops |
|----------|----------|-------------:|-------------:|-------------:|
| Storage (§6) | Uploader | **80%** to Store nodes holding replicas, pro rata | 10% | 10% |
| Bandwidth overage (§7) | Uploader | **85%** to the Store that served it | 5% | 10% |
| Transaction fee | Sender, or sponsored (§10) | **80%** to the Block Creator of the block | 10% | 10% |
| Subscription / tip (§9) | Reader | **90%** to the creator | 3% (to Stores serving the content) | 7% |

The network fund pays for the free tier, bootstrap subsidies for new nodes, and incident refunds. Its balance and outflows are public.

**Transaction fee default:** 1 D (1 VND) per non-sponsored tx. With the peg and Central-scheduled blockers there is no fee market. Mempool ordering by fee is kept only as a tiebreaker.

---

## 6. Storage pricing and escrow

### Price

| Parameter | Default | Config key |
|-----------|---------|-----------|
| Base price | **800 D per GB-month per replica** (≈ 800 VND) | `StorageNode:Pricing:BasePricePerGBPerMonth` |
| Minimum fee per contract | **10 D** | `StorageNode:Pricing:MinContractFee` |
| Replication factor | 2 (paid per replica) | `REPLICATION_FACTOR` |

Formula: `fee = max(MinContractFee, price × sizeGB × months × replicas)`.

Store nodes may set a price within **±50%** of the base. The App picks nodes by price × reliability.

**Example:** a 2 MB photo post, 2 replicas, 12 months:
`0.00195 GB × 12 × 800 × 2 ≈ 37.5 D ≈ 37.5 VND`.

### Contract types

| Type | Behaviour |
|------|-----------|
| `TimeFixed` | Paid for N months upfront into escrow. Deleted after expiry plus a 30-day grace period unless renewed |
| `AutoRenew` (replaces `OpenEnded`) | Renews monthly from the uploader's balance. If the balance is short: 30-day grace period with notices, then deletion |

### Escrow and proof-of-storage

1. When the contract is signed, the fee moves from the uploader to `escrow:<contractId>`, not to the node.
2. At upload, the App registers each file's **chunk Merkle root** together with `register-replicas`.
3. Each epoch (1 day), Central (later: Inspector nodes) sends each holder a random challenge `(fileId, chunkIndex, nonce)`. The Store must return the chunk and its Merkle proof within 30 s.
4. At month end, per replica:
   - pass rate ≥ 95% → full monthly share released (split as in §5)
   - 80–95% → released pro rata to the pass rate. The remainder stays in escrow
   - < 80% → nothing released, the bond is slashed (§8), the replica is moved to another node, and the remaining escrow follows the file
5. If a file is lost on every replica, the remaining escrow is refunded to the uploader. Bonds and the network fund cover the rest.

---

## 7. Bandwidth (reads)

- Every storage contract includes **egress quota = 10× the stored size per month**. For example, a 2 MB post comes with 20 MB/month of reads.
- Beyond the quota: **300 D per GB** (≈ 300 VND), charged to the uploader's balance. The uploader can set a monthly cap. When the cap is reached, content is served to subscribers only.
- Stores submit signed per-`fileId` egress reports each epoch. Central cross-checks them against client-signed download receipts (sampled).

---

## 8. Node bond and slashing

| Node | Minimum bond | Notes |
|------|-------------:|-------|
| Store | 100,000 D + 50,000 D per 100 GB committed | Locked in `bond:<pubkey>` |
| Block Creator | 500,000 D | |

Vouchers stay as the admission gate. The bond is what makes a node financially accountable.

| Event | Slash |
|-------|------:|
| Monthly proof-of-storage pass rate < 80% | 10% of bond |
| Missing a scheduled block, or > 24 h downtime (blocker) | 5% |
| Provably invalid block or forged report | 100%, node removed |

Slashed D goes 50% to affected users (refunds) and 50% to the network fund. Central weights blocker selection by `uptime × bond`. A bond can be withdrawn 30 days after the node leaves.

**Bootstrap:** the network fund may lend bonds to the first community nodes (the voucher holders in [VOUCHERS.md](VOUCHERS.md)) and recover them from those nodes' earnings.

---

## 9. Creator economy (demand for D)

This is the main reason to hold D, and it builds on PRE, which Deltanium already has:

- **Paid subscriptions:** a creator sets a monthly price in D. Paying subscribers get rekeys for the `subscribers:YYYY-MM` policy tag. This extends the existing `followers:YYYY` epoch tags. Not renewing means no rekey for the next epoch; content already decrypted stays readable.
- **Tips:** one-off D transfers attached to a post or comment.
- Split as in §5 (90% to the creator). Creators who pass KYC can redeem (§4).

The cycle becomes: **readers pay creators → creators and uploaders pay infrastructure → nodes cash out**.

---

## 10. Free tier and anti-spam

| Item | Free quota (verified email or phone) |
|------|------------------|
| Storage | 200 MB (replication included) |
| Egress | 2 GB / month |
| Social actions (follow, like, comment, chat) | Free, rate-limited |

- The free tier is a **quota, not a D grant**, so it cannot be farmed or transferred.
- The network fund pays nodes for free-tier usage at normal rates. That D is backed because the network fund only spends D that came from fees or from fiat deposited into the reserve.
- **Sponsored transactions:** Central's sponsor account pays the transaction fee for free-tier social actions, so users never need D just to interact.
- Cost estimate: 0.2 GB-replica × 800 D ≈ **160 D (≈ 160 VND) per fully used free account per month**. The 2 GB egress is the included 10× quota (§7), so it costs nothing extra. 10,000 such accounts ≈ 1.6M VND/month.

---

## 11. Making the ledger verifiable

| Phase | Mechanism |
|-------|-----------|
| **A (now)** | Each block carries `ledgerRoot`: the Merkle root of the `wallet_ledger` rows since the previous block, plus `balancesRoot` for all accounts. Anyone can check that Central did not rewrite history |
| **B** | Blockers keep account state (balance + nonce) and **reject** `Transfer` / fee / escrow transactions that lack funds. The MySQL ledger becomes a cache rebuilt from blocks |
| **C** | Inspector nodes take over the proof-of-storage challenges and the egress audit from Central |

**Monthly proof-of-reserve report:** circulating D, reserve VND (bank statement attested by a third party), reserve ratio, network fund flows, and the slashing log.

---

## 12. Later: floating token (optional, not v2)

A freely traded, hard-capped token only makes sense after phases B and C, when Central is no longer a single point of control, and only after legal clearance. If it is introduced, the D credit stays as the pegged unit for paying for services, and the token is used for staking and governance.

---

## 13. Legal posture (to confirm with counsel before enabling fees)

- D is a **prepaid service credit**: sold for VND, spent on Deltanium services, and redeemable only by service providers and creators under contract and KYC.
- Peer-to-peer transfer between regular users may be **limited to tips and subscriptions** if counsel advises against open P2P transfer.
- The reserve sits in a segregated account, under top-up terms of service with a refund policy.
- Regulation of digital assets, e-wallets and payment intermediaries in Vietnam must be reviewed before the redemption and P2P features are switched on.
- The questions for counsel, and the config switch each answer controls, are in [LEGAL_CHECKLIST.md](LEGAL_CHECKLIST.md). Open P2P transfer can be turned off with `Economics:P2PTransfer:Enabled=false`.

---

## 14. Implementation status

Everything below is in code. Fees stay off (`Economics:EnforceFees=false`) until the rollout step.

| Section | Where it lives |
|---------|----------------|
| §0 Units, cap, genesis | `appsettings.json` → `Economics` (`VndPerD=1`, `DPerDlt=1000000`, `HardCap=10^13`, 100% seeded into issuance); App `lib/utils/d_format.dart` |
| §3 Top-up channels, backing reserve | `WalletService.CreateTopUpOrderAsync(channel)` with transfer 3%, card 5%, iap 0; reserve = D credited × `VndPerD`; `GET /api/wallet/reserve` (public); App top-up dialog with a channel picker and a live preview |
| §4 Fee splits | `WalletService.SettleFeeAsync` + `ApplyMovesAsync` (atomic, one ledger row per leg) into `treasury:network-fund`, `treasury:protocol-ops` and node accounts |
| §5–6 Storage escrow, AutoRenew, grace | `EconomicsService.OpenStorageEscrowAsync` / `SettleDueAsync`; `register-replicas` takes `months`, `contractType`, `blocks`; `GET /api/storedfile/quote`, `GET /api/storedfile/contract/{fileId}`; the App quotes before upload and sends block hashes |
| §6 Proof-of-storage | Central `RunChallengesAsync` → Store `POST /api/proof/challenge` (sha256 of a random block); monthly release ≥95% full, 80–95% pro rata, <80% nothing + 10% bond slash |
| §7 Bandwidth | Store `EgressTracker` + `POST /api/proof/egress/drain`; Central `RecordEgressAsync` (10× quota, 300 D/GB, uploader cap via `POST /api/wallet/egress-cap`) |
| §8 Bonds, slashing, blocker selection | `api/wallet/bond/*`, `admin/slash`, 30-day withdrawal delay, bond-weighted `PickBlockerAsync`, Store list filtered when `Bond:Enforce=true` |
| §9 Creators | `SubscriptionController` (plan, subscribe, status, subscribers, tip); `fetch-rekey` / `validate-token` gate `subscribers:YYYY-MM` on payment; App: tip and subscribe buttons, "Subscribers only" post option, subscriber rekey sync at login |
| §9 Redemption | `POST /api/wallet/redeem` (KYC payee, 1%, minimum 100,000 D, queued when the reserve ratio is below 1); paid only with a Super Admin signature |
| §10 Free tier, sponsored txs | 200 MB paid by the network fund (needs email); social txs sponsored, 120/hour limit; `TransactionController` returns 402/429 |
| §11 Ledger anchors (phase A) | `CreateAnchorAsync` (Merkle roots of ledger rows and balances) → block slot → `Block.LedgerAnchorSeq/LedgerRoot/BalancesRoot`; `GET /api/wallet/anchors` |
| Background jobs | `EconomicsWorker` (challenges daily; egress, settlement and bond withdrawals every `Worker:IntervalMinutes`) |
| §11 phase B: Blockers check value moves | Central mirrors every transfer and tip on chain as a `Transfer` / `Donate` tx that carries the user's own signed HTTP request (`ValueNetworkTx`). The Blocker (`Services/Ledger/BalanceCheckService.cs`) checks three things. (1) The signed request names exactly this amount and recipient. (2) The balance at the latest anchor before the move is proven by a Merkle path (`GET /api/wallet/anchors/{seq}/balance-proof/{account}`) to the `BalancesRoot` already in its chain. (3) That balance, minus the user's other on-chain moves since the anchor, covers the amount. A reused signature is rejected as a replay. Mode `LEDGER_BALANCE_CHECK` = `off` / `warn` (default) / `enforce` |
| §11 phase C: Inspector | `deltanium-inspector/` (anyone can run it). It replays every published ledger row and checks the rows against the roots the Blockers committed. It catches: rewritten or hidden rows, gaps between anchors, balances edited outside the ledger, minting outside genesis, supply above the hard cap, and negative balances. Exit code 1 on any error. `BalancesRoot` is now the replay of the ledger (one snapshot per anchor); Central logs `LiveMismatchAccounts` when live balances drift from it |
| §7 Reader-signed egress receipts | The App routes block downloads through `BlockHttp.get`. Every 60 s it signs `EGRESS\|origin\|reader\|ts\|sha256(items)` per Store and posts it to `{store}/api/proof/egress/receipt`. The Store forwards receipts with its counters. With `Economics:Bandwidth:ReceiptMode=require`, Central bills min(Store count, receipted bytes). A receipt only counts if: the signature is valid, it names this Store's origin, it is recent, it is not a duplicate, and it covers blocks Central knows |
| §6 Automatic re-replication | When a replica fails proofs, Central (`RepairEscrowAsync`, worker job `repair`) picks a new bonded Store. It copies the Store metadata rows and every encrypted block from a healthy replica, checking each block against the hash the App registered. It challenges the new copy, then adds the placement. `TargetReplicas` keeps the paid-for count; settlement pays per target replica. History: `GET /api/wallet/admin/replications`. Switch: `Economics:Storage:AutoRepair` |
| §13 Legal | [LEGAL_CHECKLIST.md](LEGAL_CHECKLIST.md): questions for counsel, each tied to the switch it controls |

**Known limits**

- Phase B only sees value moves that are mirrored on chain: transfers and tips. Storage, bandwidth and subscription payments show up at the next anchor, so a Blocker's check is a second line of defence. Central's own ledger is still what blocks overspending.
- An anchor's `UpToInclusive` comes from Central's anchor list; it is not committed in the block. The Inspector checks that every row falls inside its anchor's window, so lying about the window shows up there.
- A reader can withhold receipts, and the Store then goes unpaid for that traffic. That is why `ReceiptMode` defaults to `off` until App versions that sign receipts are widespread.
- Repair copies the owner's metadata rows for the file. Shared copies registered under other file ids are not copied.
- Legal answers have to come from a lawyer; the checklist only frames the questions.

**Rollout:** turn on `Economics:EnforceFees=true` **together with** the free tier and sponsored txs, so existing users are not suddenly blocked. Then turn on `Bond:Enforce`, `LEDGER_BALANCE_CHECK=enforce` on Blockers once anchors are flowing, and `Bandwidth:ReceiptMode=require` once most readers sign receipts. Run the Inspector continuously.

---

## 15. Parameter summary

| Parameter | v2 default |
|-----------|-----------|
| Peg | 1 D = 1 VND; 1 DLT = 1,000,000 D |
| Max supply | 10,000,000 DLT = 10^13 D (100% on ledger at genesis) |
| Register grant | 0 D (free tier is quota) |
| On-ramp fee | 3% transfer / 5% card / store tier for in-app purchase |
| Minimum top-up | 10,000 VND |
| Backing reserve | 100% of circulating D |
| Redemption | Nodes + creators, 1% fee, minimum 100,000 D, weekly |
| Storage price | 800 D / GB-month / replica, minimum 10 D per contract |
| Egress | 10× stored size per month included, then 300 D / GB |
| Tx fee | 1 D (social actions sponsored) |
| Storage split | 80 node / 10 network fund / 10 ops |
| Bandwidth split | 85 node / 5 network fund / 10 ops |
| Tx split | 80 blocker / 10 network fund / 10 ops |
| Creator split | 90 creator / 3 network fund / 7 ops |
| Store bond | 100,000 D + 50,000 D per 100 GB |
| Blocker bond | 500,000 D |
| Proof-of-storage | Daily challenge; ≥ 95% pass rate → full release |

## 16. One-line summary

**D is a VND-pegged, fully backed service credit: users buy it cheaply, spend it on storage, bandwidth and creators; escrow and storage proofs make sure nodes are paid only for work they actually do; nodes and creators can cash out; and the ledger is anchored on chain so none of this depends on trusting Central's database.**
