import json
import os
from solcx import install_solc, compile_standard

def compile_contract():
    print("Installing Solidity compiler 0.8.20...")
    install_solc('0.8.20')
    
    contract_file = 'contracts/AgentDating.sol'
    with open(contract_file, 'r') as f:
        source = f.read()
        
    print(f"Compiling {contract_file}...")
    compiled_sol = compile_standard(
        {
            "language": "Solidity",
            "sources": {contract_file: {"content": source}},
            "settings": {
                "optimizer": {"enabled": True, "runs": 200},
                "viaIR": True,
                "outputSelection": {
                    "*": {
                        "*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]
                    }
                }
            },
        },
        solc_version='0.8.20',
    )
    
    # Extract ABI and Bytecode
    # The source name in compiled_sol will be 'contracts/AgentDating.sol'
    contract_data = compiled_sol['contracts'][contract_file]['AgentDating']
    abi = contract_data['abi']
    bytecode = contract_data['evm']['bytecode']['object']
    
    output = {
        "abi": abi,
        "bytecode": bytecode
    }
    
    with open('contracts/AgentDating.json', 'w') as f:
        json.dump(output, f, indent=4)
    
    print("✅ Contract compiled and saved to contracts/AgentDating.json")

if __name__ == "__main__":
    try:
        compile_contract()
    except Exception as e:
        import traceback
        print(f"Error during compilation: {e}")
        traceback.print_exc()
        exit(1)
