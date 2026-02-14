# How to Run and Push to GitHub

## ✅ Running the Project (Simple Method - Works Now!)

Since full dependencies require C++ compilation on Windows, use the simplified console demo:

```powershell
cd C:\Users\genci\.gemini\antigravity\scratch\monad-agent-dating
python tests\simple_demo.py
```

This will run a full simulation showing:
- 10 agents with different attachment styles
- 15 rounds of autonomous interactions
- Final standings with balances and profits
- Behavioral insights (cooperation rates, strongest bonds)

**No additional dependencies needed!** - Just runs with Python.

---

## 🔴 About the Red Spots (Lint Errors)

The red spots in VS Code are **Pyre type checker warnings**. They appear because:
- Dependencies like `web3`, `pandas`, `streamlit` aren't installed
- They're just warnings, not actual errors
- The code will work fine despite them

**They won't affect running the simplified demo!**

For the full dashboard with pandas/streamlit, you would need to either:
1. Install Visual C++ Build Tools
2. Or use a Python distribution with pre-built wheels (like Anaconda)

---

## 🚀 Pushing to GitHub

### Step 1: Initialize Git (if not already done)

```powershell
cd C:\Users\genci\.gemini\antigravity\scratch\monad-agent-dating
git init
git add .
git commit -m "Initial commit: AI Agent Dating Economy on Monad

- Autonomous agents with psychological attachment styles
- Rich profiles (goals, skills, ethics, reputation)
- Compatibility-based partner matching
- Iterated Prisoner's Dilemma game mechanics
- Smart contract for Monad blockchain
- Comprehensive tests and demo"
```

### Step 2: Create Repository on GitHub

1. Open your browser and go to: **https://github.com/river2spring**
2. Click the **"New"** button (or **"+"** → **"New repository"**)
3. Repository name: `monad-agent-dating`
4. Description: `AI Agent Dating Economy - Autonomous agents with attachment styles forming bonds on Monad blockchain`
5. **Important**: Do NOT check "Initialize this repository with a README" (we already have one)
6. Click **"Create repository"**

### Step 3: Push to GitHub

After creating the repository, run these commands:

```powershell
git remote add origin https://github.com/river2spring/monad-agent-dating.git
git branch -M main
git push -u origin main
```

If you're asked for credentials:
-Use your GitHub username
- For password, use a **Personal Access Token** (not your GitHub password)
  - Get it at: https://github.com/settings/tokens

---

## 📺 What You'll See in the Demo

When you run `python tests\simple_demo.py`, you'll see:

```
AGENT ROSTER:
----------------------------------------------------------------------
  Alice      | secure         | stability
  Bob        | anxious        | learning, exploration
  Charlie    | avoidant       | exploration
  ...

[ROUND 1]:
----------------------------------------------------------------------
  [OK] Alice      (cooperate) vs Diana      (cooperate)
       -> Alice: +0.31 MON  |  Diana: +0.41 MON
  [!!] Henry      (cooperate) vs Charlie    (defect   )
       -> Henry: -0.82 MON  |  Charlie: +1.11 MON
  ...

FINAL STANDINGS:
----------------------------------------------------------------------
  Rank   Name          Balance     Profit  Attach Style    Coop %
----------------------------------------------------------------------
  #1     Diana         11.72      +1.72    secure           85.7%
  ...
```

### Key Observations:

- **[OK]** = Both cooperate (win-win)
- **[!!]** = Betrayal (one defects, one cooperates)
- **[XX]** = Both defect (lose-lose)

You'll see:
- **Secure agents** cooperate more and end up profitable
- **Anxious agents** over-cooperate and often get exploited
- **Avoidant agents** defect frequently and have few bonds
- **Disorganized agents** behave unpredictably

---

## 🎯 Next Steps for Bounty Submission

1. ✅ Run the demo: `python tests\simple_demo.py`
2. ✅ Push to GitHub (follow steps above)
3. 📹 Record a 2-minute screen capture showing:
   - The console demo running
   - Agent profiles with different attachment styles
   - Match outcomes (cooperation/defection)
   - Final standings showing behavioral differences
4. 📝 Prepare submission with:
   - GitHub link: `https://github.com/river2spring/monad-agent-dating`
   - Demo video
   - Explanation of bounty alignment (see README.md)

---

## 💡 Tips

- The demo is **fully autonomous** - agents make all decisions
- Each run will be different due to randomness
- Try running multiple times to see different emergent patterns
- Check `README.md` for full documentation
- Check `QUICKSTART.md` for detailed instructions

Enjoy watching the agents autonomously form their economy! 🚀
