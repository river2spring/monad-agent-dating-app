# 🚀 Quick Start Guide

## About the Red Spots (Lint Errors)

The red spots you see in the code are **lint errors from Pyre** - they're completely normal and expected! They appear because:
- The Python packages aren't installed yet
- Once you run `pip install -r requirements.txt`, the errors will disappear

These are just warnings from the IDE's type checker and won't prevent the code from running.

## Running the Project

### Step 1: Install Dependencies

Open a terminal in the project directory and run:

```powershell
# Windows
python -m pip install -r requirements.txt

# This installs:
# - web3 (blockchain integration)
# - streamlit (dashboard)
# - pandas (data management)
# - plotly (visualizations)
# - networkx (relationship graphs)
# - python-dotenv (environment config)
# - eth-account (wallet management)
```

**Note**: Installation may take 3-5 minutes.

### Step 2: Run the Simulation

Once dependencies are installed, start the interactive dashboard:

```powershell
# Option 1: Using the quick start script
python scripts\run_simulation.py

# Option 2: Run streamlit directly
python -m streamlit run src\dashboard.py
```

This will:
1. Open your browser automatically
2. Show the interactive dashboard
3. Display 10 agents with different personalities

### Step 3: Interact with the Dashboard

In the dashboard:
- Click **"Run Single Round"** to execute one set of matches
- Enable **"Auto-Run"** toggle to continuously simulate
- Watch agents autonomously form bonds and break up
- See trust scores evolve in real-time
- Observe the relationship network graph

### Step 4: Run the Demo Scenario (Optional)

To see a command-line simulation with statistics:

```powershell
python tests\demo_scenario.py
```

This runs 20 rounds and shows:
- Match outcomes
- Final balances and profits
- Cooperation rates by attachment style
- Strongest bonds formed

## Pushing to GitHub

### Quick Method (Using Git Commands)

1. **Initialize git** (if not already done):
   ```powershell
   cd C:\Users\genci\.gemini\antigravity\scratch\monad-agent-dating
   git init
   ```

2. **Add all files**:
   ```powershell
   git add .
   git commit -m "Initial commit: AI Agent Dating Economy on Monad"
   ```

3. **Create a new repository on GitHub**:
   - Go to https://github.com/river2spring
   - Click "New repository"
   - Name: `monad-agent-dating`
   - **Do NOT** check "Initialize with README" (we already have one)
   - Click "Create repository"

4. **Push to GitHub**:
   ```powershell
   git remote add origin https://github.com/river2spring/monad-agent-dating.git
   git branch -M main
   git push -u origin main
   ```

### Alternative: Using GitHub Desktop (If Installed)

1. Open GitHub Desktop
2. File → Add Local Repository
3. Choose: `C:\Users\genci\.gemini\antigravity\scratch\monad-agent-dating`
4. Publish repository
5. Name: `monad-agent-dating`
6. Push to GitHub

## What You'll See When Running

### Agent Profiles Tab
- 10 agents with unique personalities
- Color-coded by attachment style:
  - 🟢 Green = Secure
  - 🟡 Yellow = Anxious
  - 🔴 Red = Avoidant
  - ⚫ Gray = Disorganized
- Each shows: balance, reputation, emotional state, skills, ethics

### Relationship Network Tab
- Interactive graph of agent connections
- Green edges = healthy relationships (high trust)
- Red edges = toxic relationships (low trust)
- Hover over edges to see compatibility metrics

### Match Feed Tab
- Real-time scrolling list of game outcomes
- 🤝 = cooperation
- ❌ = defection
- Green text = profit, Red text = loss

### Leaderboard Tab
- Rankings by balance and reputation
- Total profits/losses
- Games played

## Expected Behaviors

When you run the simulation, you'll notice:

**Secure Agents** (Green):
- Form stable bonds
- High cooperation rates
- Profitable over time

**Anxious Agents** (Yellow):
- Over-cooperate initially
- Dramatic reactions to betrayal
- Cycle through partners frequently

**Avoidant Agents** (Red):
- Low cooperation rates
- Few lasting relationships
- Protect their balance but miss cooperation gains

**Disorganized Agents** (Gray):
- Unpredictable, chaotic behavior
- High variance in outcomes

## Troubleshooting

**Error: "No module named 'streamlit'"**
- Solution: Run `python -m pip install -r requirements.txt`

**Error: "pip is not recognized"**
- Solution: Use `python -m pip` instead of `pip`

**Dashboard doesn't open automatically**
- Solution: Check the terminal for the URL (usually `http://localhost:8501`)
- Open it manually in your browser

**Port already in use**
- Solution: Run `python -m streamlit run src\dashboard.py --server.port 8502`

## Next Steps

1. **Local Simulation**: Run dashboard and observe agent behaviors
2. **Monad Testnet Deployment** (optional):
   - Get Monad testnet RPC URL
   - Get testnet MON from faucet
   - Run `python scripts\setup_contracts.py`
   - Run `python scripts\deploy.py`
3. **Record Demo Video**: Screen capture the dashboard running
4. **Submit to Bounty**: Package with transaction hashes

## Files Overview

- `src/agent.py` - Autonomous agent with decision-making logic
- `src/game_engine.py` - Orchestrates matches and bonds
- `src/dashboard.py` - Streamlit UI
- `src/blockchain.py` - Web3 integration (for testnet deployment)
- `contracts/AgentDating.sol` - Smart contract
- `tests/test_agents.py` - Unit tests
- `tests/demo_scenario.py` - Command-line simulation
- `README.md` - Full documentation

Enjoy watching the agents autonomously form their dating economy! 🎉
