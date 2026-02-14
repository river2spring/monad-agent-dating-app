from web3 import Web3
from dotenv import load_dotenv
import os

def verify_and_update():
    load_dotenv()
    rpc_url = os.getenv('MONAD_RPC_URL')
    tx_hash = 'c756b2e002babbd7f206784e8927b41b074f65bd08b46adc2759abdb9d2addab'
    
    w3 = Web3(Web3.HTTPProvider(rpc_url))
    print(f"Waiting for receipt for {tx_hash}...")
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    if receipt.status == 1:
        contract_address = receipt.contractAddress
        print(f"Success! Contract Address: {contract_address}")
        
        env_path = '.env'
        with open(env_path, 'r') as f:
            lines = f.readlines()
            
        with open(env_path, 'w') as f:
            for line in lines:
                if line.startswith('CONTRACT_ADDRESS='):
                    f.write(f'CONTRACT_ADDRESS={contract_address}\n')
                else:
                    f.write(line)
        print(".env updated.")
    else:
        print("Transaction failed.")

if __name__ == "__main__":
    verify_and_update()
