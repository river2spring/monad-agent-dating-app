# 💘 AI Agent Dating Economy on Monad

> **A high-fidelity social and economic simulation where truly autonomous AI agents navigate complex attraction, form psychological bonds, and transact real MON on the Monad Mainnet.**

---

## 🌟 The Vision

Traditional agent simulations often rely on static scripts. This project breaks that mold by introducing **Psychological State Machines**. Our agents don't just "play a game"; they experience trust, betrayal, anxiety, and learning. By utilizing Monad's ultra-fast execution layer, we've built a system where social reputation and economic success are inextricably linked.

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

### 📈 Adaptive Evolution
Agents **learn** from every interaction. Through `_adapt_parameters()`, agents dynamically adjust their:
- **Risk Tolerance**: Becomes more aggressive after profitable rounds.
- **Ethics (Fairness)**: Increases with mutual trust; decreases to a "self-preservation" mode after betrayals.

---

## 🏗️ Technical Architecture

### 🛡️ Secure On-Chain Settlement (`AgentDating.sol`)
We implement a **Commit-Reveal Mechanism** to ensure complete game fairness:
1. **Commit**: Agents submit a cryptographic hash of their move (`cooperate`/`defect`).
2. **Reveal**: Only after both have committed do they reveal the plain-text move + secret salt.
3. **Escrow**: The contract holds stakes in escrow, ensuring payouts are atomic and guaranteed.

### 🕸️ Compatibility-Based Matching (`src/game_engine.py`)
Agents don't just pick random partners. They evaluate:
- **Value Alignment**: Do our long-term goals overlap?
- **Skill Complementarity**: Does one agent's patience balance the other's negotiation skill?
- **Reputation**: The community-wide `reputation_score` influences the initial willingness to engage.

---

## 📊 Relationship Dynamics

- **Bond Evolution**: Trust and bond strength are updated after every round.
- **Natural Terminations**: Bonds naturally end after 5-10 rounds (simulating "moving on") or break instantly if trust falls below a "toxic" threshold (<20).
- **Social Graph**: Visualized in the dashboard as a network of "Healthy" (green) and "Toxic" (red) connections.

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- A Monad Mainnet Wallet (for Blockchain Mode)
- **Note on Red Spots**: Lint errors (Pyre) are expected until `requirements.txt` is installed and the IDE indexes them.

### 2. Quick Install
```bash
python -m pip install -r requirements.txt
```

### 3. Launch
| Mode | Command | Best For |
|------|---------|----------|
| **Interactive** | `streamlit run src/dashboard.py` | Full visual monitoring of the economy. |
| **Statistical** | `python tests/demo_scenario.py` | Bulk testing of agent behavior over 20+ rounds. |
| **Logic Check** | `python tests/simple_demo.py` | Immediate verification of the decision engine. |

---

## 🔗 Infrastructure

- **Network**: Monad Mainnet (`ChainID 143`)
- **RPC**: `https://rpc.monad.xyz`
- **Explorer**: [Monad Vision](https://monadvision.com)

---

Built for the **Moltiverse Bounty** - Demonstrating that complex AI social structures require the performant and reliable rails of the Monad blockchain. 🚀
