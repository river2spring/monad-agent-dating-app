# 💘 Agent Dating Economy on Monad

> **A high-fidelity social and economic simulation where truly autonomous agents navigate complex attraction, form psychological bonds, and transact real MON on the Monad Mainnet.**

---

## 🔗 Live Application & Proof of Work

- **Live Dashboard**: [https://dashboardpy-ephqohxyabxyj9qq2nm3go.streamlit.app/](https://dashboardpy-ephqohxyabxyj9qq2nm3go.streamlit.app/)
- **Verified Contract**: [0x327... (Monad Vision)](https://monadvision.com) *(Replace with actual deployed address if different)*
- **On-Chain Evidence (Mainnet Funding Hashes)**:
  - `0x4005afa8acaa5ede2bc7af7be1580824762d408cb30f504e68415ca5f2aaa472`
  - `0xbd8a4c7c3b796f4b76fad9f56b20ccee597270d6d76383e01d7b438569e998f6`
  - `0x1210053a12747ea2478d9ac6eeb5eed208bbab3e21ea1cb92d5277b71cdc9e2c`

---

## 🧠 The Agent "Brain" (`src/agent.py`)

Every agent operates on a nuanced multidimensional decision matrix. Their behavior is influenced by:

### 🎭 Psychological Attachment Styles
- **🟢 Secure**: Builds steady trust, recovers quickly from conflict, and prioritizes long-term stability.
- **🟡 Anxious**: Highly cooperative early on but hypersensitive to betrayal (2x emotional impact). Frequently cycles through partners.
- **🔴 Avoidant**: Prioritizes capital preservation over social bonds. Maintains high cooperation thresholds.
- **⚫ Disorganized**: Chaotic and unpredictable; moves are driven by erratic internal "emotional flux."

### 🎯 Goal-Oriented Agency
Agents aren't just trying to win; they have distinct life goals:
- **Profit**: Maximize MON earnings.
- **Exploration**: Seek out diverse partner profiles.
- **Learning**: Optimize social strategies over time.
- **Stability**: Prioritize bond strength over immediate payouts.

---

## 🛡️ Agentic Blockchain Architecture

Our agents are **first-class on-chain citizens**. The system is not a centralized script; it is a decentralized orchestration.

### 📡 Real-Time Broadcasting
- **Autonomous Transactions**: Agents own their own private keys and independently sign/broadcast transactions via the `BlockchainIntegration` layer.
- **Direct Connection**: The system connects directly via `Web3.py` to the Monad Mainnet RPC.
- **Sovereign Actions**: Every `createGame`, `joinGame`, `commitMove`, and `revealMove` is a signed transaction originating from an agent's individual wallet.

### 🛡️ Smart Contract Judicial Layer (`AgentDating.sol`)
We implement a **Commit-Reveal Mechanism** to ensure complete game fairness:
1. **Commit**: Agents submit a cryptographic hash of their move. This prevents "front-running" or "move-sniffing."
2. **Reveal**: Only after both have committed do they reveal the plain-text move + secret salt.
3. **Escrow**: The contract holds stakes in escrow, ensuring payouts are atomic and guaranteed.

---

## 🧪 Testing & Validation

The project includes a robust test suite covering core logic and simulation edge cases.

### 🛠️ Coverage
- **Decision Engine**: `tests/test_agents.py` verifies that attachment styles, trust levels, and past betrayals correctly influence move probability.
- **Blockchain Mocks**: Unit tests use isolated object mocks for relationship memory to test agent decisions without requiring a live node.
- **Simulation Stress**: `tests/demo_scenario.py` runs 20+ round high-fidelity simulations to observe behavioral evolution.

### 🏃 How to Run Tests
```bash
# Run unit tests
pytest tests/test_agents.py -v

# Run the long-term demo scenario
python tests/demo_scenario.py
```

---

## 🔐 Security & Configuration

### 🔑 Private Key Management
- **Secure Provisioning**: Private keys are **never** hardcoded. They are loaded exclusively from the `.env` file or Streamlit Secrets.
- **Agent Sovereignty**: The simulation generates separate internal wallets for each agent during initialized population to prevent main wallet exposure.

### ⚙️ RPC Configuration
Modify your `.env` to point to the desired network:
```ini
# Monad Mainnet
MONAD_RPC_URL=https://rpc.monad.xyz
CHAIN_ID=143
```

---

## 🚀 Impact & Behavior Evolution

**Is the on-chain logic real?** Yes. Every reward and penalty is settled on the Monad blockchain.
**Does behavior evolve?** Yes. Through `_adapt_parameters()`, agents learning from their environment. A "Secure" agent betrayed multiple times will eventually evolve a "self-preservation" ethics mode, proving that the social environment on Monad directly shapes agentic psychology.

Built for the **Moltiverse Hackathon** 🚀
