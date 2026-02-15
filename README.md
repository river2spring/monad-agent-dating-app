# 💘 AI Agent Dating Economy on Monad

> **Truly Autonomous AI Agents with psychological attachment styles FORMING BONDS, playing iterated Prisoner's Dilemma, and transacting real MON on Monad Mainnet.**

---

## 🎯 Core Concept

This ecosystem demonstrates **non-scripted, emergent behavior** between AI agents. Each agent is a unique individual with:
- **Attachment Styles**: Secure, Anxious, Avoidant, or Disorganized (logic in `src/agent.py`).
- **Emotional Memory**: They remember betrayals and acts of trust per partner.
- **Economic Agency**: They stake and earn real MON tokens based on social outcomes.
- **Adaptive Learning**: Agents adjust their cooperation threshold based on relationship history.

## 🏗️ Technical Architecture

### 1. Smart Contract (Mainnet: `ChainID 143`)
- **Escrow System**: Both agents lock stakes before match start.
- **Commit-Reveal Pattern**: Cryptographic verification of moves to prevent front-running.
- **On-Chain Settlement**: Prisoner's Dilemma payoffs executed as atomic transactions.

### 2. Decision Logic
Agents don't follow static "if/else" paths. Their probability to cooperate is a dynamic function of:
`P(Cooperation) = f(Base_Value, Trust_Score, Attachment_Modifier, Emotional_State)`

### 3. Dashboard (`streamlit`)
A real-time visual control center for:
- **Relationship Network**: Interactive graph of trust bonds.
- **Match Feed**: Live stream of cooperation/betrayal outcomes.
- **On-Chain Sync**: Direct integration with Monad block explorers.

---

## 🚀 Quick Start

### 1. Installation
```bash
python -m pip install -r requirements.txt
```

### 2. Configuration
Copy `.env.example` to `.env` and configure your Monad credentials:
```env
MONAD_RPC_URL=https://rpc.monad.xyz
PRIVATE_KEY=your_private_key
CONTRACT_ADDRESS=your_deployed_contract
```

### 3. Running the Simulation
**Option A: Simplified Demo (Console)**
Perfect for immediate verification of agent logic:
```bash
python tests/simple_demo.py
```

**Option B: Full Dashboard (GUI)**
Requires streamlit:
```bash
streamlit run src/dashboard.py
```

---

## 🛠️ Blockchain Deployment

If you wish to deploy the contract yourself:

1. **Setup Contracts**: `python scripts/setup_contracts.py` (Generates ABI/Bytecode).
2. **Deploy**: `python scripts/deploy.py` (Deploys to Monad Mainnet).
3. **Verify**: Ensure your `.env` is updated with the new address.

---

## 📊 Attachment Style Breakdown

| Style | Color | Behavior Pattern |
|-------|-------|------------------|
| **Secure** | 🟢 | Forms stable, high-trust bonds. Very profitable. |
| **Anxious** | 🟡 | Over-cooperates early, dramatic reaction to betrayals. |
| **Avoidant** | 🔴 | Low cooperation rate. Protects capital but misses gains. |
| **Disorganized** | ⚫ | Chaotic and unpredictable. High variance in results. |

---

## 🔗 Links & Resources

- **Explorer**: [Monad Vision](https://monadvision.com)
- **Official Docs**: [Monad Documentation](https://docs.monad.xyz)
- **Bounty Support**: [Moltiverse](https://moltiverse.io)

---

Built for the **Moltiverse Bounty Program** - Proving that agents need fast, scalable financial rails like Monad to form complex social and economic systems. 🚀
