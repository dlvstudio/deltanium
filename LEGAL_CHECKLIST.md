# Legal checklist for TOKENOMICS_V2

**This is not legal advice.** It is the list of questions to put to a Vietnamese lawyer before real money flows through Deltanium, and the code switches that depend on each answer. The laws named below are starting points for counsel to confirm. Check which version is in force and how it applies to Deltanium; do not rely on this list for that.

Everything that touches money ships **switched off** or in a reversible state:

| Switch | Default | Turns on |
|--------|---------|----------|
| `Economics:EnforceFees` | `false` | Users actually pay storage, bandwidth and tx fees |
| `Economics:P2PTransfer:Enabled` | `true` | `POST /api/wallet/transfer` between users (tips and subscriptions are separate) |
| `Economics:Redemption:*` + payee KYC (`admin/payee`) | no payees | Creators and nodes cashing D out to VND |
| `Economics:Bond:Enforce` | `false` | Nodes must lock D as a bond to operate |
| Top-up channels `Economics:OnRampFee:*` | transfer, card, iap | Selling D for VND |

## 1. What D is

- [ ] Can D be treated as a **prepaid service credit / platform points** rather than e-money or a payment instrument? Key facts: it is pegged 1 D = 1 VND, sold only by Deltanium, spent on Deltanium services, and not redeemable by ordinary users.
- [ ] Does selling D for VND make Deltanium a **payment intermediary or e-wallet provider** that needs a State Bank of Vietnam licence? Rules on non-cash payments to check: Decree 52/2024/ND-CP and its amendments.
- [ ] Does the "DLT" display unit (1 DLT = 1,000,000 D) or the on-chain ledger make D a **digital asset / crypto-asset** under the digital-technology-industry law and the crypto-asset pilot framework? If so, what follows? Deltanium has no exchange, no floating price, and no trading.
- [ ] What may the product and marketing **call** D? Wording to avoid: "token", "coin", "investment", "yield".

## 2. Peer-to-peer transfer

- [ ] Is open user-to-user transfer allowed for a service credit? If not, set `Economics:P2PTransfer:Enabled=false`; tips and subscriptions keep working.
- [ ] Are **tips and subscriptions** (a user paying a creator, Deltanium keeping 10%) a marketplace or e-commerce activity, and if so which obligations apply?

## 3. Redemption (D → VND)

- [ ] Can **creators and node operators** cash out D? On what contractual basis: payment for services rendered to Deltanium, or revenue share?
- [ ] What KYC is required, and at what thresholds? Today the code requires a verified payee and a minimum of 100,000 D, and a Super Admin signature before a payout counts as paid.
- [ ] What anti-money-laundering duties apply (AML law and implementing rules): suspicious-transaction reporting, record keeping, limits?
- [ ] Is a 1% redemption fee allowed? Is a weekly payout schedule allowed?

## 4. Reserve and refunds

- [ ] Must the 1:1 VND backing reserve sit in a **segregated or escrow account**? Must it be audited? The public `/api/wallet/reserve` endpoint and the Inspector make it observable, but they are not a legal guarantee.
- [ ] What **refund policy** must top-up terms offer for unused D? What happens to D if the user deletes their account or Deltanium shuts down?
- [ ] Do the top-up fees (3% transfer, 5% card, store fee for in-app purchase) need to be disclosed in a particular way?

## 5. Tax and accounting

- [ ] Is D sold but not yet spent a **deferred revenue liability**? When is VAT due: at sale or at use?
- [ ] Must Deltanium **withhold personal income tax** on creator and node payouts? Check platform withholding rules for e-commerce and digital platforms.
- [ ] How should D paid to Stores and Blockers be invoiced?

## 6. Node operators

- [ ] Are Store and Blocker operators **contractors** of Deltanium? What contract covers bonds, slashing (10% for failed storage proofs) and the 30-day withdrawal delay?
- [ ] Is slashing a bond an enforceable **contractual penalty**? Is there a cap?

## 7. Data and privacy

- [ ] Do storage proofs, egress receipts and on-chain value transactions publish **personal data**? Public keys, amounts and timestamps are visible to Blockers and Inspectors. Check the personal-data-protection law and decree.
- [ ] Is a **cross-border** transfer assessment needed if Store or Blocker nodes run outside Vietnam?

## 8. Consumer terms

- [ ] Prepare terms of service covering the free tier, what happens when storage expires (30-day grace, then refund of the unused escrow), bandwidth caps, and the paywall on subscriber-only content.
- [ ] Is a separate notice needed when a user's file becomes `Lost` (every replica failed) and the remaining escrow is refunded?

## Sign-off

| Item | Counsel answer | Date | Switch changed |
|------|----------------|------|----------------|
| D classification | | | |
| P2P transfer | | | `Economics:P2PTransfer:Enabled` |
| Redemption + KYC/AML | | | payees, `Economics:Redemption:*` |
| Reserve and refunds | | | |
| Tax | | | |
| Node contracts | | | `Economics:Bond:Enforce` |
| Turn on fees | | | `Economics:EnforceFees` |
