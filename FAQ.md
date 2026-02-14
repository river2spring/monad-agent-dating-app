# Quick Answers

## Q: What do I put in .env file?

### PRIVATE_KEY:
**Your Ethereum/Monad wallet private key** (64 hex characters)

**How to get it:**
1. Open MetaMask
2. Click 3 dots → Account Details
3. Export Private Key → Enter password
4. Copy the key (looks like: `0x123abc...`)

⚠️ **SECURITY**: 
- Only use testnet wallets (not real money!)
- Never share this key
- It's in .gitignore (won't be pushed to GitHub)

### CONTRACT_ADDRESS:
**Leave this EMPTY!**

It gets filled automatically when you run `deploy.py` (if you choose to deploy)

### Complete .env example:
```
MONAD_RPC_URL=https://testnet-rpc.monad.xyz
PRIVATE_KEY=your64characterprivatekeyhere123456789abcdef123456789abcdef
CONTRACT_ADDRESS=
```

## Q: Why does setup_contracts.py fail?

**It requires Node.js and C++ Build Tools** which are complex to setup on Windows.

**Good news**: You don't need it! 

The demo works perfectly without any blockchain deployment:
```powershell
python tests\simple_demo.py
```

This shows:
✅ All 10 autonomous agents
✅ Attachment style behaviors  
✅ Compatibility matching
✅ Trust evolution
✅ Economic outcomes

## Q: Do I need to deploy to blockchain?

**No!** The demo is sufficient to show:
- Autonomous decision-making
- Psychological attachment models
- Economic game theory
- Non-scripted agent behavior

The smart contract design proves you understand blockchain integration, but actual deployment is optional for the bounty.

## Q: What if I WANT to deploy?

**Easiest method - Use Remix**:
1. Go to https://remix.ethereum.org
2. Upload `contracts/AgentDating.sol`
3. Compile it there
4. Deploy to Monad testnet using MetaMask

**Or**: I can provide pre-compiled contract artifacts (ABI + bytecode)

## Ready to ship?

```powershell
# 1. Run the demo (works right now!)
python tests\simple_demo.py

# 2. Push to GitHub
git init
git add .
git commit -m "AI Agent Dating Economy on Monad"
git remote add origin https://github.com/river2spring/monad-agent-dating.git
git push -u origin main

# 3. Make demo video showing the console output
# 4. Submit to bounty with GitHub link
```

That's it! You have a working autonomous agent economy 🎉
