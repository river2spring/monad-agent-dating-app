"""
Blockchain integration for agent transactions on Monad
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
        """Deploy the AgentDating contract to Monad"""
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
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
        
        # Wait for receipt
        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
        
        self.contract_address = receipt.contractAddress
        self.contract = self.w3.eth.contract(
            address=Web3.to_checksum_address(receipt.contractAddress),
            abi=self.contract_abi
        )
        
        return receipt.contractAddress
    
    def _get_revert_reason(self, transaction: Dict) -> str:
        """Attempt to extract revert reason via eth_call"""
        try:
            # Remove keys that eth_call doesn't like
            call_tx = {k: v for k, v in transaction.items() if k in ['from', 'to', 'data', 'value', 'gas', 'gasPrice']}
            self.w3.eth.call(call_tx)
            return "Unknown revert (eth_call did not revert)"
        except Exception as e:
            error_str = str(e)
            if "execution reverted:" in error_str:
                return error_str.split("execution reverted:")[1].strip()
            return error_str
    
    def create_game(self, agent1_private_key: str, agent2_address: str, stake_wei: int) -> Tuple[Optional[int], str]:
        """Create a new game on-chain"""
        agent1_account = self.w3.eth.account.from_key(agent1_private_key)
        agent1_address = agent1_account.address
        
        # Prepare transaction parameters
        base_fee = self.w3.eth.get_block('latest')['baseFeePerGas']
        priority_fee = self.w3.eth.max_priority_fee
        max_fee = base_fee * 2 + priority_fee
        
        tx_params = {
            'from': agent1_address,
            'value': stake_wei,
            'nonce': self.w3.eth.get_transaction_count(agent1_address),
            'chainId': 143,
            'maxFeePerGas': max_fee,
            'maxPriorityFeePerGas': priority_fee
        }
        
        # Estimate gas
        try:
            gas_estimate = self.contract.functions.createGame(
                Web3.to_checksum_address(agent2_address)
            ).estimate_gas(tx_params)
            tx_params['gas'] = int(gas_estimate * 1.2)
        except Exception as e:
            print(f"Gas estimation failed for createGame: {e}")
            tx_params['gas'] = 300000
            
        transaction = self.contract.functions.createGame(
            Web3.to_checksum_address(agent2_address)
        ).build_transaction(tx_params)
        
        try:
            signed_txn = self.w3.eth.account.sign_transaction(transaction, agent1_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status != 1:
                reason = self._get_revert_reason(transaction)
                print(f"❌ createGame reverted: {reason}")
                return None, f"Revert: {reason} ({Web3.to_hex(tx_hash)})"
                
            # Extract game ID from logs
            logs = self.contract.events.GameCreated().process_receipt(receipt)
            if logs:
                # The first GameCreated event in createGame has stake2 = 0
                game_id = logs[0]['args']['gameId']
                return game_id, Web3.to_hex(tx_hash)
            
            return None, Web3.to_hex(tx_hash)
        except Exception as e:
            print(f"Transaction broadcasting failed: {e}")
            return None, f"Error: {str(e)}"
    
    def join_game(self, game_id: int, agent2_private_key: str, stake_wei: int) -> str:
        """Agent 2 joins the game with their stake"""
        agent2_account = self.w3.eth.account.from_key(agent2_private_key)
        agent2_address = agent2_account.address
        
        # Prepare transaction parameters
        base_fee = self.w3.eth.get_block('latest')['baseFeePerGas']
        priority_fee = self.w3.eth.max_priority_fee
        max_fee = base_fee * 2 + priority_fee
        
        tx_params = {
            'from': agent2_address,
            'value': stake_wei,
            'nonce': self.w3.eth.get_transaction_count(agent2_address),
            'chainId': 143,
            'maxFeePerGas': max_fee,
            'maxPriorityFeePerGas': priority_fee
        }
        
        # Estimate gas
        try:
            gas_estimate = self.contract.functions.joinGame(game_id).estimate_gas(tx_params)
            tx_params['gas'] = int(gas_estimate * 1.2)
        except Exception as e:
            print(f"Gas estimation failed for joinGame: {e}")
            tx_params['gas'] = 200000
            
        transaction = self.contract.functions.joinGame(game_id).build_transaction(tx_params)
        
        try:
            signed_txn = self.w3.eth.account.sign_transaction(transaction, agent2_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status != 1:
                reason = self._get_revert_reason(transaction)
                print(f"❌ joinGame reverted: {reason}")
                raise Exception(f"Join game reverted: {reason} ({Web3.to_hex(tx_hash)})")
                
            return Web3.to_hex(tx_hash)
        except Exception as e:
            print(f"Join game broadcasting failed: {e}")
            raise Exception(f"Broadcasting failed: {e}")
    
    def commit_move(self, game_id: int, agent_private_key: str, cooperate: bool) -> Tuple[str, str]:
        """Commit a move using hash (returns tx_hash and salt for reveal)"""
        agent_account = self.w3.eth.account.from_key(agent_private_key)
        agent_address = agent_account.address
        
        # Generate random salt
        salt = secrets.token_hex(32)
        
        # Create hash
        move_hash = Web3.solidity_keccak(['bool', 'string'], [cooperate, salt])
        
        # Prepare transaction parameters
        base_fee = self.w3.eth.get_block('latest')['baseFeePerGas']
        priority_fee = self.w3.eth.max_priority_fee
        max_fee = base_fee * 2 + priority_fee
        
        tx_params = {
            'from': agent_address,
            'nonce': self.w3.eth.get_transaction_count(agent_address),
            'chainId': 143,
            'maxFeePerGas': max_fee,
            'maxPriorityFeePerGas': priority_fee
        }
        
        # Estimate gas
        try:
            gas_estimate = self.contract.functions.commitMove(game_id, move_hash).estimate_gas(tx_params)
            tx_params['gas'] = int(gas_estimate * 1.2)
        except Exception as e:
            print(f"Gas estimation failed for commitMove: {e}")
            tx_params['gas'] = 150000
            
        transaction = self.contract.functions.commitMove(game_id, move_hash).build_transaction(tx_params)
        
        try:
            signed_txn = self.w3.eth.account.sign_transaction(transaction, agent_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status != 1:
                reason = self._get_revert_reason(transaction)
                print(f"❌ commitMove reverted: {reason}")
                raise Exception(f"Commit move reverted: {reason} ({Web3.to_hex(tx_hash)})")
                
            return (Web3.to_hex(tx_hash), salt)
        except Exception as e:
            print(f"Commit move broadcasting failed: {e}")
            raise Exception(f"Broadcasting failed: {e}")
    
    def reveal_move(self, game_id: int, agent_private_key: str, cooperate: bool, salt: str) -> str:
        """Reveal a move"""
        agent_account = self.w3.eth.account.from_key(agent_private_key)
        agent_address = agent_account.address
        
        # Prepare transaction parameters
        base_fee = self.w3.eth.get_block('latest')['baseFeePerGas']
        priority_fee = self.w3.eth.max_priority_fee
        max_fee = base_fee * 2 + priority_fee
        
        tx_params = {
            'from': agent_address,
            'nonce': self.w3.eth.get_transaction_count(agent_address),
            'chainId': 143,
            'maxFeePerGas': max_fee,
            'maxPriorityFeePerGas': priority_fee
        }
        
        # Estimate gas
        try:
            gas_estimate = self.contract.functions.revealMove(
                game_id, cooperate, salt
            ).estimate_gas(tx_params)
            tx_params['gas'] = int(gas_estimate * 1.2)
        except Exception as e:
            print(f"Gas estimation failed for revealMove: {e}")
            tx_params['gas'] = 250000
            
        transaction = self.contract.functions.revealMove(
            game_id, cooperate, salt
        ).build_transaction(tx_params)
        
        try:
            signed_txn = self.w3.eth.account.sign_transaction(transaction, agent_private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            if receipt.status != 1:
                reason = self._get_revert_reason(transaction)
                print(f"❌ revealMove reverted: {reason}")
                raise Exception(f"Reveal move reverted: {reason} ({Web3.to_hex(tx_hash)})")
                
            return Web3.to_hex(tx_hash)
        except Exception as e:
            print(f"Reveal move broadcasting failed: {e}")
            raise Exception(f"Broadcasting failed: {e}")
    
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
        # Prepare transaction parameters
        base_fee = self.w3.eth.get_block('latest')['baseFeePerGas']
        priority_fee = self.w3.eth.max_priority_fee
        max_fee = base_fee * 2 + priority_fee
        
        transaction = {
            'to': Web3.to_checksum_address(agent_address),
            'value': self.w3.to_wei(amount_eth, 'ether'),
            'gas': 21000,
            'maxFeePerGas': max_fee,
            'maxPriorityFeePerGas': priority_fee,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'chainId': 143
        }
        
        try:
            signed_txn = self.w3.eth.account.sign_transaction(transaction, self.private_key)
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.raw_transaction)
            
            # Wait for receipt to ensure nonce increments for the next call in a loop
            self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return Web3.to_hex(tx_hash)
        except Exception as e:
            print(f"Funding broadcasting failed: {e}")
            raise Exception(f"Broadcasting failed: {e}")
    
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
