# Deltanium network public keys

Public keys of the network's root signers and of every node the Deltanium team runs. Use them to check
that a signature really comes from the network. These are **public keys only** — private keys never
leave their machines (the Super Admin private key is kept offline).

Live values: [deltanium.com/nodes.html](https://deltanium.com/nodes.html) · `GET https://api.deltanium.com/api/explorer/keys`
· `GET https://api.deltanium.com/api/explorer/nodes`. If anything here disagrees with the live API,
treat it as a red flag and report it.

All keys are compressed secp256k1 public keys (33 bytes, hex).

## Mainnet (`mainnet`)

### Root keys

| Role | Endpoint | Public key | Signs |
|------|----------|------------|-------|
| Central API | https://api.deltanium.com | `0390329609c78fff2cd895cb3faf30b1fa868085da0e89dbeeff642258773c9191` | Network decisions, Store access tokens, version attestations |
| Super Admin | — (offline) | `021fd57c80fd85156c307e2f1c0bc278ea0eeabac930835ab989803ee2d77165f7` | Second signature on top-ups, redemptions and slashing |

### Block Creators

| Node | Public key |
|------|------------|
| https://blocker-1.deltanium.com | `0200f8829ee2396f13e271b91ac1bd3f8abf493fa455a567c374d0f0960a9bb19b` |

### Stores

| Node | Public key |
|------|------------|
| https://store-1.deltanium.com | `0377ca93ec5d80938149d7cd115103af7c0df58ae304aba8ec63206a57a6aa681f` |
| https://store-2.deltanium.com | `02de754903d8572ad0930aa7db4e16beb221e33312dcf67e56129e1f04b67e5671` |

## Testnet (`deltanium-test`)

Signatures are bound to the network, so testnet keys can never authorize anything on mainnet.

### Root keys

| Role | Endpoint | Public key |
|------|----------|------------|
| Central API | https://testnet-api.deltanium.com | `025a49d61f45a4905d25659235c63390ee815bb9323db5154fbe8a42b67be7c802` |
| Super Admin | — (offline) | `02dced09e78d9622135c723c0641069b0bf4cf62d05184fb47a6292f6c2e106780` |

### Block Creators

| Node | Public key |
|------|------------|
| https://testnet-blocker-1.deltanium.com | `03002a50ff6df683d8600e2295d6cb99a3925dd195f454964e6e12e1052367c2f7` |

### Stores

| Node | Public key |
|------|------------|
| https://testnet-store-1.deltanium.com | `038125070af76df1cb2717a77d1f8341d9d0a991a14a3c362bb81860298b739d2e` |
| https://testnet-store-2.deltanium.com | `028b5553d0a5a15c649a0eb29be9b7eb3923ce245c441cc15d74577f3d2b11d0b8` |

## Community nodes

Nodes registered by the community with a [public voucher](VOUCHERS.md) appear on the live Nodes page
and in `GET /api/explorer/nodes`. Open a pull request to add yours here.

## Check a key yourself

```bash
# Root keys (Central + Super Admin)
curl -s https://api.deltanium.com/api/explorer/keys

# Every active Block Creator and Store, with its public key
curl -s https://api.deltanium.com/api/explorer/nodes

# A node's own build and network
curl -s https://blocker-1.deltanium.com/api/version
```
