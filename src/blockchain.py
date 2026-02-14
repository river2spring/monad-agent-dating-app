"""
Blockchain integration with Monad testnet for agent transactions
"""
from web3 import Web3
from typing import Optional, Dict, Tuple
import json
import hashlib
import secrets

class BlockchainIntegration:
    """Handles all Monad blockchain interactions"""
    
    def __init__(self, rpc_url: str, private_key: str, contract_address: Optional[str] = None):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.private_key = private_key
        self.account = self.w3.eth.account.from_key(private_key)
        self.contract_address = contract_address
        self.contract = None
        
        # Load contract ABI
        with open('contracts/AgentDating.json', 'r') as f:
            contract_json = json.load(f)
            self.contract_abi = contract_json['abi']
        
        if contract_address:
            self.contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=self.contract_abi
            )
    
    def deploy_contract(self) -> str:
        """Deploy the AgentDating contract to Monad testnet"""
        with open('contracts/AgentDating.json', 'r') as f:
            contract_json = json.load(f)
        
        Contract = self.w3.eth.contract(
            abi=contract_json['abi'],
            bytecode=contract_json['bytecode']
        )
        
        # Build transaction
        transaction = Contract.constructor().build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 3000000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        # Sign and send
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        self.contract_address = receipt.contractAddress
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(receipt.contractAddress),
            abi=self.contract_abi
        )
        
        return receipt.contractAddress
    
    def create_game(self, agent1_address: str, agent2_address: str, stake_wei: int) -> int:
        """Create a new game on-chain"""
        transaction = self.contract.functions.createGame(
            Web3.to_checksum_address(agent2_address)
        ).build_transaction({
            'from': Web3.to_checksum_address(agent1_address),
            'value': stake_wei,
            'nonce': self.w3.eth.get_transaction_count(Web3.to_checksum_address(agent1_address)),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        # Extract game ID from logs
        logs = self.contract.events.GameCreated().process_receipt(receipt)
        if logs:
            return logs[0]['args']['gameId']
        
        return None
    
    def join_game(self, game_id: int, agent2_address: str, stake_wei: int) -> str:
        """Agent 2 joins the game with their stake"""
        transaction = self.contract.functions.joinGame(game_id).build_transaction({
            'from': Web3.to_checksum_address(agent2_address),
            'value': stake_wei,
            'nonce': self.w3.eth.get_transaction_count(Web3.to_checksum_address(agent2_address)),
            'gas': 150000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return tx_hash.hex()
    
    def commit_move(self, game_id: int, agent_address: str, cooperate: bool) -> Tuple[str, str]:
        """Commit a move using hash (returns tx_hash and salt for reveal)"""
        # Generate random salt
        salt = secrets.token_hex(32)
        
        # Create hash
        move_hash = Web3.solidity_keccak(['bool', 'string'], [cooperate, salt])
        
        transaction = self.contract.functions.commitMove(game_id, move_hash).build_transaction({
            'from': Web3.to_checksum_address(agent_address),
            'nonce': self.w3.eth.get_transaction_count(Web3.to_checksum_address(agent_address)),
            'gas': 100000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return (tx_hash.hex(), salt)
    
    def reveal_move(self, game_id: int, agent_address: str, cooperate: bool, salt: str) -> str:
        """Reveal a move"""
        transaction = self.contract.functions.revealMove(
            game_id, cooperate, salt
        ).build_transaction({
            'from': Web3.to_checksum_address(agent_address),
            'nonce': self.w3.eth.get_transaction_count(Web3.to_checksum_address(agent_address)),
            'gas': 200000,
            'gasPrice': self.w3.eth.gas_price
        })
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        return tx_hash.hex()
    
    def get_game(self, game_id: int) -> Dict:
        """Get game details from contract"""
        game = self.contract.functions.getGame(game_id).call()
        return {
            'agent1': game[0],
            'agent2': game[1],
            'stake1': game[2],
            'stake2': game[3],
            'settled': game[10],
            'agent1_cooperated': game[8],
            'agent2_cooperated': game[9]
        }
    
    def get_balance(self, address: str) -> float:
        """Get MON balance of address"""
        balance_wei = self.w3.eth.get_balance(Web3.to_checksum_address(address))
        return self.w3.from_wei(balance_wei, 'ether')
    
    def fund_agent(self, agent_address: str, amount_eth: float) -> str:
        """Send MON to agent address"""
        transaction = {
            'to': Web3.to_checksum_address(agent_address),
            'value': self.w3.to_wei(amount_eth, 'ether'),
            'gas': 21000,
            'gasPrice': self.w3.eth.gas_price,
            'nonce': self.w3.eth.get_transaction_count(self.account.address)
        }
        
        signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        return tx_hash.hex()
    
    def simulate_game_offchain(self, agent1_move: bool, agent2_move: bool, 
                               stake1: float, stake2: float) -> Tuple[float, float]:
        """Simulate game payoffs without touching blockchain (for dashboard simulation)"""
        # This matches the smart contract logic
        if agent1_move and agent2_move:
            return (stake1 * 1.5, stake2 * 1.5)
        elif not agent1_move and not agent2_move:
            return (stake1 * 0.5, stake2 * 0.5)
        elif not agent1_move and agent2_move:
            return (stake1 * 2.5, 0)
        else:
            return (0, stake2 * 2.5)
