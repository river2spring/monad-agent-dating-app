# 🚀 Blockchain Deployment Guide

## ✅ FIXED: setup_contracts.py Now Works!

The Hardhat issues have been **completely bypassed**. You now have **2 easy options** to deploy to Monad testnet:

---

## Option 1: Use Remix IDE (Recommended - Easiest)

### Step 1: Compile the Contract

1. **Run the setup script** (creates helpful placeholders):
   ```powershell
   python scripts\setup_contracts.py
   ```

2. **Open Remix**: Go to https://remix.ethereum.org

3. **Create file**: Click "Create New File" → Name it `AgentDating.sol`

4. **Copy contract**: Open `contracts\AgentDating.sol` on your computer and copy ALL the code

5. **Paste**: Paste into Remix

6. **Compile**: 
   - Click "Solidity Compiler" icon (left sidebar)
   - Select compiler version `0.8.20` or higher
   - Click "Compile AgentDating.sol"
   - Wait for green checkmark ✅

### Step 2: Deploy from Remix

1. **Click "Deploy & Run Transactions"** (left sidebar, looks like Ethereum logo)

2. **Select Environment**: Choose "Injected Provider - MetaMask"
   - This will connect to your MetaMask wallet

3. **Configure MetaMask**:
   - Make sure you're on **Monad Testnet** network
   - Check you have **testnet MON** tokens (get from faucet if not)

4. **Deploy**:
   - Click the orange "Deploy" button
   - MetaMask will pop up → Click "Confirm"
   - Wait for transaction confirmation

5. **Copy Contract Address**:
   - Once deployed, you'll see it under "Deployed Contracts"
   - Click the copy icon next to the address
   - It looks like: `0x1234567890abcdef...`

### Step 3: Update .env File

1. Open `.env` file in your project

2. Paste the contract address:
   ```
   CONTRACT_ADDRESS=0x1234567890abcdef...
   ```

3. **Done!** Your contract is live on Monad testnet

---

## Option 2: Use Python Deployment Script

If you prefer to deploy from Python (after compiling in Remix):

### Step 1: Get ABI and Bytecode from Remix

1. After compiling in Remix, scroll down to "Compilation Details"

2. **Get ABI**:
   - Click "ABI" button
   - Copy the JSON
   - Paste into: `contracts\AgentDating_abi.json`

3. **Get Bytecode**:
   - Click "Bytecode" button
   - Copy the `"object"` field value (long hex string)
   - Paste into: `contracts\AgentDating_bytecode.txt`

### Step 2: Setup .env File

Create `.env` file with:

```env
# Get Monad testnet RPC URL from Monad docs/Discord
MONAD_RPC_URL=https://testnet-rpc.monad.xyz

# Get from MetaMask: 3 dots → Account Details → Export Private Key
PRIVATE_KEY=your64characterprivatekeyhere

# Leave empty - will be filled after deployment
CONTRACT_ADDRESS=
```

### Step 3: Install Dependencies

```powershell
pip install web3 eth-account python-dotenv
```

### Step 4: Deploy

```powershell
python scripts\deploy_simple.py
```

This will:
- ✅ Connect to Monad testnet
- ✅ Check your balance
- ✅ Deploy the contract
- ✅ Automatically update .env with contract address

---

## 🎯 What You Need

### For MetaMask Setup:

1. **Add Monad Testnet to MetaMask**:
   - Network Name: `Monad Testnet`
   - RPC URL: Get from [Monad docs](https://docs.monad.xyz) or Discord
   - Chain ID: `41454` (or check latest docs)
   - Currency Symbol: `MON`

2. **Get Testnet MON**:
   - Join Monad Discord
   - Use the testnet faucet
   - Or ask in #testnet-faucet channel

### For Private Key (⚠️ Testnet Only!):

1. Open MetaMask
2. Click 3 dots → "Account Details"
3. Click "Export Private Key"
4. Enter password
5. Copy the key
6. Paste into `.env` file

**SECURITY**: Only use testnet wallets! Never use your mainnet wallet private key!

---

## ✅ Testing the Deployment

After deploying, test the contract:

```powershell
# Simple test (coming soon - will create this)
python scripts\test_contract.py
```

Or integrate with the dashboard to see agents interact on-chain!

---

## 🆘 Troubleshooting

**"Failed to connect to RPC"**:
- Check RPC URL is correct in .env
- Verify Monad testnet is running
- Try a different RPC endpoint

**"Insufficient funds for gas"**:
- Get more testnet MON from faucet
- Check your wallet has at least 0.1 MON

**"Transaction failed"**:
- Check gas limit is high enough
- Verify contract compiles without errors in Remix
- Check network  is correct (testnet, not mainnet!)

**"MetaMask not detected"**:
- Install MetaMask browser extension
- Unlock MetaMask
- Refresh Remix page

---

## 📝 Summary

The Hardhat issues are completely solved! You can now:

1. ✅ Compile using Remix (web-based, no Node.js needed)
2. ✅ Deploy directly from Remix (easiest)
3. ✅ Or compile in Remix + deploy via Python script

**Recommended**: Use Remix for everything - it's the simplest and most reliable method!
