"""
Game engine that orchestrates iterated Prisoner's Dilemma games between agents
"""
import random
from typing import List, Dict, Tuple, Optional, Any, TYPE_CHECKING
from agent import Agent, Goal, AttachmentStyle

if TYPE_CHECKING:
    from blockchain import BlockchainIntegration

class GameEngine:
    """Orchestrates autonomous agent interactions"""
    
    def __init__(self, agents: List[Agent], blockchain: Optional['BlockchainIntegration'] = None):
        self.agents = agents
        self.blockchain = blockchain
        self.active_bonds: Dict[Tuple[str, str], int] = {}  # (agent1, agent2) -> rounds_played
        self.match_history: List[Dict] = []
        
    def create_matches(self) -> List[Tuple[Agent, Agent]]:
        """Autonomously pair agents based on compatibility"""
        matches = []
        available = self.agents.copy()
        random.shuffle(available)
        
        # First, let agents choose partners
        used = set()
        for agent in available:
            if agent.profile.name in used:
                continue
            
            potential_partners = [a for a in available if a.profile.name not in used 
                                 and a.profile.name != agent.profile.name]
            partner = agent.select_partner(potential_partners)
            
            if partner:
                matches.append((agent, partner))
                used.add(agent.profile.name)
                used.add(partner.profile.name)
        
        # Random pairing for remaining agents
        remaining = [a for a in available if a.profile.name not in used]
        while len(remaining) >= 2:
            agent1 = remaining.pop(0)
            agent2 = remaining.pop(0)
            matches.append((agent1, agent2))
        
        return matches
    
    def run_round(self, agent1: Agent, agent2: Agent) -> Optional[Dict]:
        """Run a single game round between two agents"""
        # Agents decide stakes
        stake1 = float(agent1.calculate_stake(agent2))
        stake2 = float(agent2.calculate_stake(agent1))
        
        # Gas Reservation & Small Stakes logic for Blockchain Mode
        if self.blockchain and self.blockchain.contract:
            GAS_BUFFER = 0.02
            MAX_ON_CHAIN_STAKE = 0.005
            
            # Reserve gas buffer
            available1 = float(max(0.0, agent1.balance - GAS_BUFFER))
            available2 = float(max(0.0, agent2.balance - GAS_BUFFER))
            
            # Cap stake and ensure it doesn't exceed available balance after gas buffer
            stake1 = float(min(stake1, available1, MAX_ON_CHAIN_STAKE))
            stake2 = float(min(stake2, available2, MAX_ON_CHAIN_STAKE))
        else:
            # Standard balance checks for off-chain or initial logic
            stake1 = float(min(stake1, float(agent1.balance)))
            stake2 = float(min(stake2, float(agent2.balance)))
        
        if stake1 <= 0 or stake2 <= 0:
            return None  # Can't play
        
        # Agents make independent decisions
        move1 = agent1.decide_move(agent2, stake1)
        move2 = agent2.decide_move(agent1, stake2)
        
        tx_details: Dict[str, Any] = {}
        
        # On-chain execution if blockchain mode is active
        if self.blockchain and self.blockchain.contract:
            try:
                # 1. Create Game (Agent 1)
                print(f"⛓️ Broadcasting create_game (Agent 1: {agent1.profile.name})...")
                stake_wei = self.blockchain.w3.to_wei(stake1, 'ether')
                game_id, tx_create = self.blockchain.create_game(agent1.profile.private_key, agent2.profile.address, stake_wei)
                
                # Record the hash immediately so it's visible even on failure
                tx_details['tx_hashes'] = {'create': tx_create}
                
                # CRITICAL: Validate Game ID before proceeding
                if game_id is None:
                    raise Exception("Game creation failed on-chain (Transaction might have reverted or no Game ID in logs)")
                
                print(f"✅ Game Created: ID #{game_id}")
                tx_details['game_id'] = game_id
                
                # 2. Join Game (Agent 2)
                print(f"⛓️ Broadcasting join_game (Agent 2: {agent2.profile.name})...")
                stake2_wei = self.blockchain.w3.to_wei(stake2, 'ether')
                tx_join = self.blockchain.join_game(game_id, agent2.profile.private_key, stake2_wei)
                tx_details['tx_hashes']['join'] = tx_join
                print("✅ Join Confirmed")
                
                # 3. Commit Moves (Both)
                print(f"⛓️ Broadcasting commit_move (Agent 1: {agent1.profile.name})...")
                tx_commit1, salt1 = self.blockchain.commit_move(game_id, agent1.profile.private_key, move1)
                print(f"⛓️ Broadcasting commit_move (Agent 2: {agent2.profile.name})...")
                tx_commit2, salt2 = self.blockchain.commit_move(game_id, agent2.profile.private_key, move2)
                tx_details['tx_hashes']['commit1'] = tx_commit1
                tx_details['tx_hashes']['commit2'] = tx_commit2
                print("✅ Commits Confirmed")
                
                # 4. Reveal Moves (Both)
                print(f"⛓️ Broadcasting reveal_move (Agent 1: {agent1.profile.name})...")
                tx_reveal1 = self.blockchain.reveal_move(game_id, agent1.profile.private_key, move1, salt1)
                print(f"⛓️ Broadcasting reveal_move (Agent 2: {agent2.profile.name})...")
                tx_reveal2 = self.blockchain.reveal_move(game_id, agent2.profile.private_key, move2, salt2)
                tx_details['tx_hashes']['reveal1'] = tx_reveal1
                tx_details['tx_hashes']['reveal2'] = tx_reveal2
                print("✅ Reveals Confirmed")
                
                # 5. Get Final Results from Contract
                game_result = self.blockchain.get_game(game_id)
                tx_details['on_chain'] = True
                
                # Payouts
                payout1, payout2 = self._calculate_payoffs(move1, move2, stake1, stake2)
                
            except Exception as e:
                print(f"Blockchain transaction failed: {e}")
                tx_details['error'] = str(e)
                # Fallback or record failure
                # If game_id was None, we didn't actually start an on-chain game
                payout1, payout2 = 0, 0 # No payout if it failed to start
                if 'game_id' not in tx_details:
                    # Off-chain fallback if user wants to keep sim moving, 
                    # but for this request we want robustness, so we record the failure
                    pass
        else:
            # Calculate payoffs based on Prisoner's Dilemma
            payout1, payout2 = self._calculate_payoffs(move1, move2, stake1, stake2)
        
        # Update agents
        agent1.update_after_game(agent2, move1, move2, stake1, payout1)
        agent2.update_after_game(agent1, move2, move1, stake2, payout2)
        
        # Record match
        bond_key = tuple(sorted([agent1.profile.name, agent2.profile.name]))
        self.active_bonds[bond_key] = self.active_bonds.get(bond_key, 0) + 1
        
        result = {
            'agent1_name': agent1.profile.name,
            'agent2_name': agent2.profile.name,
            'agent1_move': 'cooperate' if move1 else 'defect',
            'agent2_move': 'cooperate' if move2 else 'defect',
            'agent1_reason': agent1.last_decision_reason,
            'agent2_reason': agent2.last_decision_reason,
            'agent1_stake': stake1,
            'agent2_stake': stake2,
            'agent1_payout': payout1,
            'agent2_payout': payout2,
            'agent1_profit': payout1 - stake1,
            'agent2_profit': payout2 - stake2,
            'bond_rounds': self.active_bonds[bond_key],
            **tx_details
        }
        
        self.match_history.append(result)
        return result
    
    def _calculate_payoffs(self, move1: bool, move2: bool, stake1: float, stake2: float) -> Tuple[float, float]:
        """Calculate Prisoner's Dilemma payoffs"""
        if move1 and move2:
            # Both cooperate: (3, 3) - each gets 1.5x stake
            return (stake1 * 1.5, stake2 * 1.5)
        elif not move1 and not move2:
            # Both defect: (1, 1) - each gets 0.5x stake
            return (stake1 * 0.5, stake2 * 0.5)
        elif not move1 and move2:
            # Agent1 defects, Agent2 cooperates: (5, 0)
            return (stake1 * 2.5, 0)
        else:
            # Agent1 cooperates, Agent2 defects: (0, 5)
            return (0, stake2 * 2.5)
    
    def evaluate_bonds(self) -> List[Tuple[Agent, Agent, bool]]:
        """Evaluate which bonds should continue"""
        evaluations = []
        
        # Create a list of bond keys to avoid dictionary size change during iteration
        bond_keys = list(self.active_bonds.keys())
        
        for (name1, name2) in bond_keys:
            rounds = self.active_bonds[(name1, name2)]
            agent1 = next(a for a in self.agents if a.profile.name == name1)
            agent2 = next(a for a in self.agents if a.profile.name == name2)
            
            # Decide if bond continues
            # Bond breaks if:
            # 1. Either agent doesn't want rematch
            # 2. Trust is too low
            # 3. Played too many rounds (5-10)
            
            wants_continue = True
            
            if rounds >= random.randint(5, 10):
                wants_continue = False  # Natural end
            
            if not agent1.wants_rematch(agent2) or not agent2.wants_rematch(agent1):
                wants_continue = False
            
            # Check trust levels
            mem1 = agent1.relationships.get(agent2.profile.name)
            mem2 = agent2.relationships.get(agent1.profile.name)
            
            if mem1 and mem1.trust_score < 20:
                wants_continue = False
            if mem2 and mem2.trust_score < 20:
                wants_continue = False
            
            evaluations.append((agent1, agent2, wants_continue))
            
            if not wants_continue:
                # Break bond
                del self.active_bonds[(name1, name2)]
        
        return evaluations
    
    def get_statistics(self) -> Dict:
        """Get summary statistics"""
        return {
            'total_games': len(self.match_history),
            'active_bonds': len(self.active_bonds),
            'agent_balances': {a.profile.name: a.balance for a in self.agents},
            'agent_reputations': {a.profile.name: a.profile.reputation_score for a in self.agents}
        }
