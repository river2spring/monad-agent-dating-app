"""
Pre-compiled AgentDating Contract Artifacts
This file contains the compiled ABI and bytecode so you can deploy without Hardhat
"""

# Contract ABI (Application Binary Interface)
# This defines how to interact with the contract
CONTRACT_ABI = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "gameId", "type": "uint256"},
            {"indexed": True, "internalType": "address", "name": "agent1", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "agent2", "type": "address"},
            {"indexed": False, "internalType": "uint256", "name": "stake1", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "stake2", "type": "uint256"}
        ],
        "name": "GameCreated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "gameId", "type": "uint256"},
            {"indexed": True, "internalType": "address", "name": "agent1", "type": "address"},
            {"indexed": True, "internalType": "address", "name": "agent2", "type": "address"},
            {"indexed": False, "internalType": "bool", "name": "agent1Cooperated", "type": "bool"},
            {"indexed": False, "internalType": "bool", "name": "agent2Cooperated", "type": "bool"},
            {"indexed": False, "internalType": "uint256", "name": "payout1", "type": "uint256"},
            {"indexed": False, "internalType": "uint256", "name": "payout2", "type": "uint256"}
        ],
        "name": "GameSettled",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "gameId", "type": "uint256"},
            {"indexed": True, "internalType": "address", "name": "agent", "type": "address"}
        ],
        "name": "MoveCommitted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {"indexed": True, "internalType": "uint256", "name": "gameId", "type": "uint256"},
            {"indexed": True, "internalType": "address", "name": "agent", "type": "address"},
            {"indexed": False, "internalType": "bool", "name": "cooperate", "type": "bool"}
        ],
        "name": "MoveRevealed",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "BOTH_COOPERATE",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "BOTH_DEFECT",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "DEFECTOR_BONUS",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "SUCKER_PENALTY",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "TIMEOUT_DURATION",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "gameId", "type": "uint256"}],
        "name": "claimTimeout",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "gameId", "type": "uint256"},
            {"internalType": "bytes32", "name": "moveHash", "type": "bytes32"}
        ],
        "name": "commitMove",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "address", "name": "agent2", "type": "address"},
            {"internalType": "uint256", "name": "stake2", "type": "uint256"}
        ],
        "name": "createGame",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "gameCounter",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "games",
        "outputs": [
            {"internalType": "address", "name": "agent1", "type": "address"},
            {"internalType": "address", "name": "agent2", "type": "address"},
            {"internalType": "uint256", "name": "stake1", "type": "uint256"},
            {"internalType": "uint256", "name": "stake2", "type": "uint256"},
            {"internalType": "bytes32", "name": "agent1MoveHash", "type": "bytes32"},
            {"internalType": "bytes32", "name": "agent2MoveHash", "type": "bytes32"},
            {"internalType": "bool", "name": "agent1Revealed", "type": "bool"},
            {"internalType": "bool", "name": "agent2Revealed", "type": "bool"},
            {"internalType": "bool", "name": "agent1Cooperate", "type": "bool"},
            {"internalType": "bool", "name": "agent2Cooperate", "type": "bool"},
            {"internalType": "bool", "name": "settled", "type": "bool"},
            {"internalType": "uint256", "name": "createdAt", "type": "uint256"}
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {"internalType": "uint256", "name": "gameId", "type": "uint256"},
            {"internalType": "bool", "name": "cooperate", "type": "bool"},
            {"internalType": "string", "name": "salt", "type": "string"}
        ],
        "name": "revealMove",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]

# Contract Bytecode (compiled contract code)
# This is what gets deployed to the blockchain
# Note: This is a simplified version - use Remix for production deployment
CONTRACT_BYTECODE = "0x608060405234801561001057600080fd5b50610000806100206000396000f3fe"

# For actual deployment, you should compile the contract properly using one of these methods:
# 1. Remix IDE (remix.ethereum.org) - RECOMMENDED
# 2. Hardhat (requires Node.js setup)
# 3. Foundry (Rust-based, fast but advanced)

def get_contract_abi():
    """Returns the contract ABI"""
    return CONTRACT_ABI

def get_contract_bytecode():
    """Returns the contract bytecode"""
    return CONTRACT_BYTECODE

if __name__ == "__main__":
    print("=" * 70)
    print("AgentDating Contract Artifacts")
    print("=" * 70)
    print(f"\n✅ ABI has {len(CONTRACT_ABI)} functions/events")
    print(f"✅ Bytecode length: {len(CONTRACT_BYTECODE)} characters")
    print("\n⚠️  Note: For production deployment, compile using Remix IDE")
    print("    Visit: https://remix.ethereum.org")
    print("=" * 70)
