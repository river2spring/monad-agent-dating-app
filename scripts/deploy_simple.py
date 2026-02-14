"""
Simplified Deployment Script for Monad Testnet
Uses pre-compiled artifacts or Remix-compiled artifacts
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from web3 import Web3
    from eth_account import Account
    from dotenv import load_dotenv
except ImportError:
    print("=" * 70)
    print("❌ Missing required packages!")
    print("=" * 70)
    print("\nPlease install:")
    print("  pip install web3 eth-account python-dotenv")
    print()
    sys.exit(1)

def load_contract_artifacts():
    """Load contract ABI and bytecode"""
    contracts_dir = Path(__file__).parent.parent / "contracts"
    
    # Try to load from Remix-generated files first
    abi_file = contracts_dir / "AgentDating_abi.json"
    bytecode_file = contracts_dir / "AgentDating_bytecode.txt"
    
    if abi_file.exists() and bytecode_file.exists():
        print("📦 Loading artifacts from Remix compilation...")
        with open(abi_file, 'r') as f:
            abi_content = f.read().strip()
            if abi_content.startswith('[') and abi_content != '[\n  // Paste the ABI from Remix here\n]':
                abi = json.loads(abi_content)
                with open(bytecode_file, 'r') as bf:
                    bytecode = bf.read().strip()
                    if not bytecode.startswith('//'):
                        return abi, bytecode
    
    # Fall back to pre-compiled artifacts
    print("📦 Loading pre-compiled artifacts...")
    try:
        from contracts.artifacts import get_contract_abi, get_contract_bytecode
        return get_contract_abi(), get_contract_bytecode()
    except Exception as e:
        print(f"❌ Error loading artifacts: {e}")
        print("\n💡 Please compile the contract first:")
        print("   python scripts/setup_contracts.py")
        sys.exit(1)

def deploy_contract():
    """Deploy the AgentDating contract to Monad testnet"""
    
    print("=" * 70)
    print("🚀 DEPLOYING AgentDating CONTRACT TO MONAD TESTNET")
    print("=" * 70)
    print()
    
    # Load environment variables
    load_dotenv()
    
    rpc_url = os.getenv('MONAD_RPC_URL')
    private_key = os.getenv('PRIVATE_KEY')
    
    if not rpc_url:
        print("❌ Error: MONAD_RPC_URL not set in .env file")
        print("\n💡 Create a .env file with:")
        print("   MONAD_RPC_URL=https://testnet-rpc.monad.xyz")
        print("   PRIVATE_KEY=your_private_key_here")
        return
    
    if not private_key:
        print("❌ Error: PRIVATE_KEY not set in .env file")
        print("\n💡 Get your private key from MetaMask:")
        print("   1. Click 3 dots → Account Details")
        print("   2. Export Private Key → Enter password")
        print("   3. Copy and paste into .env file")
        return
    
    # Clean private key
    if private_key.startswith('0x'):
        private_key = private_key[2:]
    
    print(f"🔗 Connecting to Monad testnet...")
    print(f"   RPC: {rpc_url}")
    
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not w3.is_connected():
            print(f"❌ Failed to connect to {rpc_url}")
            print("\n💡 Check that:")
            print("   1. The RPC URL is correct")
            print("   2. You have internet connection")
            print("   3. Monad testnet is running")
            return
        
        print("✅ Connected to Monad testnet!")
        
        # Get account
        account = Account.from_key(private_key)
        print(f"\n👤 Deployer address: {account.address}")
        
        # Check balance
        balance = w3.eth.get_balance(account.address)
        balance_eth = w3.from_wei(balance, 'ether')
        print(f"💰 Balance: {balance_eth} MON")
        
        if balance == 0:
            print("\n⚠️  Warning: Your balance is 0 MON!")
            print("   You need testnet MON to deploy contracts.")
            print("\n💡 Get testnet MON from Monad faucet:")
            print("   - Check Monad Discord")
            print("   - Or Monad documentation")
            return
        
        # Load contract artifacts
        abi, bytecode = load_contract_artifacts()
        
        print(f"\n📄 Contract loaded:")
        print(f"   ABI entries: {len(abi)}")
        print(f"   Bytecode length: {len(bytecode)} characters")
        
        # Create contract instance
        Contract = w3.eth.contract(abi=abi, bytecode=bytecode)
        
        # Build deployment transaction
        print("\n🔨 Building deployment transaction...")
        
        nonce = w3.eth.get_transaction_count(account.address)
        
        # Estimate gas
        try:
            gas_estimate = Contract.constructor().estimate_gas({'from': account.address})
            print(f"   Estimated gas: {gas_estimate}")
        except Exception as e:
            print(f"   ⚠️  Could not estimate gas: {e}")
            gas_estimate = 3000000  # Fallback
        
        # Build transaction
        transaction = Contract.constructor().build_transaction({
            'from': account.address,
            'nonce': nonce,
            'gas': gas_estimate + 100000,  # Add buffer
            'gasPrice': w3.eth.gas_price,
        })
        
        # Sign transaction
        print("✍️  Signing transaction...")
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
        
        # Send transaction
        print("📤 Sending transaction to network...")
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        print(f"   Transaction hash: {tx_hash.hex()}")
        
        # Wait for receipt
        print("⏳ Waiting for confirmation...")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        
        if receipt['status'] == 1:
            contract_address = receipt['contractAddress']
            print("\n" + "=" * 70)
            print("✅ CONTRACT DEPLOYED SUCCESSFULLY!")
            print("=" * 70)
            print(f"\n📍 Contract Address: {contract_address}")
            print(f"🔗 Transaction: {tx_hash.hex()}")
            print(f"⛽ Gas Used: {receipt['gasUsed']}")
            
            # Update .env file
            env_path = Path(__file__).parent.parent / ".env"
            
            if env_path.exists():
                # Read existing .env
                with open(env_path, 'r') as f:
                    lines = f.readlines()
                
                # Update CONTRACT_ADDRESS line
                updated = False
                for i, line in enumerate(lines):
                    if line.startswith('CONTRACT_ADDRESS='):
                        lines[i] = f'CONTRACT_ADDRESS={contract_address}\n'
                        updated = True
                        break
                
                if not updated:
                    lines.append(f'\nCONTRACT_ADDRESS={contract_address}\n')
                
                # Write back
                with open(env_path, 'w') as f:
                    f.writelines(lines)
                
                print(f"\n✅ Updated .env file with contract address")
            else:
                print(f"\n💡 Add this to your .env file:")
                print(f"   CONTRACT_ADDRESS={contract_address}")
            
            print("\n" + "=" * 70)
            print("🎉 DEPLOYMENT COMPLETE!")
            print("=" * 70)
            print("\nNext steps:")
            print("1. Test the contract: python scripts/test_contract.py")
            print("2. Run simulation with blockchain: python src/dashboard.py")
            print()
            
        else:
            print("\n❌ Transaction failed!")
            print(f"   Receipt: {receipt}")
    
    except Exception as e:
        print(f"\n❌ Deployment failed: {e}")
        print("\n💡 Troubleshooting:")
        print("   - Check your RPC URL is correct")
        print("   - Ensure you have enough MON for gas")
        print("   - Verify private key is correct")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    deploy_contract()
