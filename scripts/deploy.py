"""
Deploy AgentDating contract to Monad testnet
"""
import sys
import os
sys.path.append('src')

from web3 import Web3
from dotenv import load_dotenv
import json

def deploy_contract():
    """Deploy the contract to Monad testnet"""
    load_dotenv()
    
    print("Deploying AgentDating Contract to Monad Testnet")
    print("=" * 60)
    
    # Load configuration
    rpc_url = os.getenv('MONAD_RPC_URL')
    private_key = os.getenv('PRIVATE_KEY')
    
    if not rpc_url or not private_key:
        print("Missing configuration!")
        print("   Please set MONAD_RPC_URL and PRIVATE_KEY in .env file")
        return
    
    # Connect to Monad
    print("\nConnecting to Monad testnet...")
    print(f"   RPC: {rpc_url}")
    
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    
    if not w3.is_connected():
        print("Failed to connect to Monad testnet")
        print("   Please check your RPC URL")
        return
    
    print("Connected to Monad testnet")
    
    # Load account
    account = w3.eth.account.from_key(private_key)
    print(f"\nDeploying from: {account.address}")
    
    # Check balance
    balance = w3.eth.get_balance(account.address)
    balance_eth = w3.from_wei(balance, 'ether')
    print(f"   Balance: {balance_eth:.4f} MON")
    
    if balance == 0:
        print("\nInsufficient balance!")
        print("   Please get testnet MON from faucet")
        return
    
    # Load contract
    print("\nLoading contract ABI and bytecode...")
    
    contract_json_path = 'contracts/AgentDating.json'
    if not os.path.exists(contract_json_path):
        print(f"Contract JSON not found at {contract_json_path}")
        print("   Please run: python scripts/setup_contracts.py")
        return
    
    with open(contract_json_path, 'r') as f:
        contract_json = json.load(f)
    
    # Create contract instance
    Contract = w3.eth.contract(
        abi=contract_json['abi'],
        bytecode=contract_json['bytecode']
    )
    
    print("Contract loaded")
    
    # Build deployment transaction
    print("\nBuilding deployment transaction...")
    
    try:
        transaction = Contract.constructor().build_transaction({
            'from': account.address,
            'nonce': w3.eth.get_transaction_count(account.address),
            'gas': 3000000,
            'gasPrice': w3.eth.gas_price
        })
        
        estimated_gas = w3.eth.estimate_gas(transaction)
        gas_cost = w3.from_wei(estimated_gas * transaction['gasPrice'], 'ether')
        
        print(f"   Estimated gas: {estimated_gas}")
        print(f"   Gas cost: ~{gas_cost:.6f} MON")
        
    except Exception as e:
        print(f"Failed to build transaction: {e}")
        return
    
    # Sign and send
    print("\nSigning and sending transaction...")
    
    try:
        signed_txn = w3.eth.account.sign_transaction(transaction, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        print(f"   Transaction hash: {tx_hash.hex()}")
        print("   ⏳ Waiting for confirmation...")
        
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        if receipt.status == 1:
            print("\nContract deployed successfully!")
            print(f"\n📍 Contract Address: {receipt.contractAddress}")
            print(f"   Block number: {receipt.blockNumber}")
            print(f"   Gas used: {receipt.gasUsed}")
            
            # Update .env file
            print("\n💾 Updating .env with contract address...")
            env_path = '.env'
            
            # Read existing .env
            env_lines = []
            if os.path.exists(env_path):
                with open(env_path, 'r') as f:
                    env_lines = f.readlines()
            
            # Update or add CONTRACT_ADDRESS
            found = False
            for i, line in enumerate(env_lines):
                if line.startswith('CONTRACT_ADDRESS='):
                    env_lines[i] = f'CONTRACT_ADDRESS={receipt.contractAddress}\n'
                    found = True
                    break
            
            if not found:
                env_lines.append(f'\nCONTRACT_ADDRESS={receipt.contractAddress}\n')
            
            with open(env_path, 'w') as f:
                f.writelines(env_lines)
            
            print("env updated")
            
            print("\n" + "=" * 60)
            print("Deployment Complete!")
            print("\nNext steps:")
            print("  1. View on explorer (if available)")
            print("  2. Run simulation: python tests/demo_scenario.py")
            print("  3. Start dashboard: streamlit run src/dashboard.py")
            
        else:
            print("\nTransaction failed!")
            print(f"   Status: {receipt.status}")
            
    except Exception as e:
        print(f"\nDeployment failed: {e}")

if __name__ == "__main__":
    deploy_contract()
