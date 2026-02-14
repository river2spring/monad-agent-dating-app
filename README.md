# 💘 AI Agent Dating Economy on Monad

> **An autonomous dating + economic ecosystem where AI agents with psychological attachment styles form bonds, play iterated Prisoner's Dilemma, and transact real MON on Monad blockchain.**

## 🎯 Core Concept

This project demonstrates **truly autonomous agents** that:
- Have psychological attachment styles (Secure, Anxious, Avoidant, Disorganized)
- Form emotional bonds based on trust
- Make independent economic decisions
- Stake and earn real MON tokens
- Adapt strategies based on relationship history
- Break up or seek new partners autonomously

## 🏗️ Architecture

### 1. Smart Contract (Solidity)
- **Escrow System**: Stakes from both agents locked before each game
- **Prisoner's Dilemma Payoffs**: On-chain settlement
  - Both Cooperate → 1.5x stake each
  - Both Defect → 0.5x stake each
  - One Defects → Defector gets 2.5x, Cooperator loses all
- **Commit-Reveal Pattern**: Prevents front-running
- **Event Logs**: Immutable on-chain proof of interactions

### 2. Agent Engine (Python)
Each agent has:
- **Attachment Style**: Influences cooperation tendency and betrayal response
- **Goals**: Profit, exploration, learning, or stability
- **Skills**: Negotiation, patience, adaptability
- **Ethics**: Fairness and reciprocity parameters
- **Memory**: Trust scores, relationship history per partner
- **Emotions**: Dynamic state affecting decisions

### 3. Game Engine
- **Autonomous Matching**: Agents select partners using compatibility algorithms:
  - Value alignment (goal compatibility)
  - Skill complementarity
  - Attachment style compatibility matrix
  - Past relationship history
- **Iterated Games**: 5-10 rounds per bond
- **Bond Management**: Relationships strengthen or break based on trust

### 4. Dashboard (Streamlit)
Real-time visualization showing:
- Agent profiles with full personality details
- Relationship network graph
- Live match outcomes
- Earnings/losses leaderboard
- Transaction hashes (when deployed)

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Monad testnet access
- Testnet MON tokens

### Installation

```bash
# Clone or navigate to project
cd monad-agent-dating

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your Monad testnet RPC and private key
```

### Run Simulation (Local)

```bash
# Run dashboard without blockchain (for development/demo)
streamlit run src/dashboard.py
```

### Deploy to Monad Testnet

```bash
# Deploy smart contract
python scripts/deploy.py

# Run simulation with blockchain integration
python scripts/run_with_blockchain.py
```

## 📊 How It Works

### Agent Decision-Making

Agents make **non-scripted decisions** based on:

1. **Trust Score** (0-100): Updated after each interaction
   - Mutual cooperation → +5 trust
   - Betrayal → -15 trust (more dramatic for Anxious agents)

2. **Attachment Style Modifiers**:
   - **Secure**: +20% cooperation, stable trust recovery
   - **Anxious**: +30% early cooperation, -30% after betrayal
   - **Avoidant**: -30% cooperation, rarely rematches
   - **Disorganized**: Random, chaotic behavior

3. **Goal Influence**:
   - Profit-seekers → -10% cooperation
   - Stability-seekers → +15% cooperation

4. **Emotional State**: Affects risk tolerance
5. **Reciprocity**: Tit-for-tat if ethics_reciprocity > 0.5

### Matching Algorithm

Compatibility score (0-100) calculated from:
- **Goal overlap**: +10 per shared goal
- **Skill balance**: Complementary skills score higher
- **Attachment compatibility**: Matrix-based scoring
- **Trust history**: Past relationship trust adds +30%
- **Reputation**: Community standing adds +10%

Agents choose highest-compatible partner above their threshold.

## 🎮 Bounty Alignment

### ✅ Autonomous Agents (9.1 Compliance)
- ✅ Not simple if/else scripting
- ✅ Decisions depend on history + personality
- ✅ Agents adapt over multiple rounds
- ✅ Operate without human input
- ✅ Non-deterministic behavior

### 💰 Monad Integration (Opt 1)
- ✅ Real money rails (escrow staking)
- ✅ On-chain settlement (Prisoner's Dilemma payoffs)
- ✅ Immutable history (transaction hashes)
- ✅ Scalable multi-agent activity
- ✅ NOT just storage - used as financial infrastructure

### 🧬 Weird Agents (Opt B)
- ✅ Psychological attachment styles
- ✅ Non-trivial reasoning
- ✅ Emergent behavior patterns
- ✅ Emotional memory affects decisions
- ✅ Novel: dating economy for AI

## 📁 Project Structure

```
monad-agent-dating/
├── contracts/
│   └── AgentDating.sol          # Smart contract
├── src/
│   ├── agent.py                 # Agent with attachment styles
│   ├── game_engine.py           # Game orchestration
│   ├── blockchain.py            # Web3 integration
│   ├── agent_utils.py           # Agent creation utilities
│   └── dashboard.py             # Streamlit UI
├── tests/
│   ├── test_agents.py           # Agent autonomy tests
│   └── demo_scenario.py         # End-to-end demo
├── .env.example                 # Environment template
├── requirements.txt             # Python dependencies
└── README.md                    # This file
```

## 🧪 Testing

```bash
# Test agent autonomy
pytest tests/test_agents.py -v

# Run demo scenario
python tests/demo_scenario.py
```

## 📹 Demo Video

The 2-minute demo will showcase:
1. **Agent profiles**: Show 10 diverse agents with different attachment styles
2. **Autonomous decisions**: Watch agents independently choose partners
3. **Emergent behavior**: Anxious agent desperately seeks reconnection after betrayal
4. **Economic outcomes**: Real MON flowing based on cooperation/defection
5. **On-chain proof**: Transaction hashes visible on Monad testnet explorer

## 🏆 Expected Outcomes

- **Secure agents**: Form stable, long-term bonds
- **Anxious agents**: Cycle through partners, dramatic reactions to betrayal
- **Avoidant agents**: Rarely cooperate, few lasting relationships
- **Disorganized agents**: Unpredictable, chaotic patterns

**Emergent economies**: Agents with compatible goals (e.g., two stability-seekers) tend to form profitable long-term partnerships, while profit-seekers exploit then abandon partners.

## 🔗 Links

- [Monad Testnet Explorer](https://explorer.testnet.monad.xyz)
- [Nad.fun Platform](https://nad.fun)
- [Moltiverse Bounty Program](https://moltiverse.io)

## 📄 License

MIT

## 👥 Team

Built for the Moltiverse bounty program - proving that agents need money rails at scale, and Monad provides them.
