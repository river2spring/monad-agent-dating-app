"""
Autonomous AI Agent with psychological attachment styles for the dating economy
"""
import random
from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass, field

class AttachmentStyle(Enum):
    SECURE = "secure"
    ANXIOUS = "anxious"
    AVOIDANT = "avoidant"
    DISORGANIZED = "disorganized"

class Goal(Enum):
    PROFIT = "profit"  # Maximize MON earnings
    EXPLORATION = "exploration"  # Try different partners
    LEARNING = "learning"  # Optimize strategy over time
    STABILITY = "stability"  # Form long-term bonds

@dataclass
class AgentProfile:
    """Rich agent profile with goals, skills, and preferences"""
    name: str
    attachment_style: AttachmentStyle
    goals: List[Goal]
    risk_tolerance: float  # 0.0-1.0
    ethics_fairness: float  # 0.0-1.0, how much they value fairness
    ethics_reciprocity: float  # 0.0-1.0, how much they value tit-for-tat
    skill_negotiation: float  # 0.0-1.0
    skill_patience: float  # 0.0-1.0
    skill_adaptability: float  # 0.0-1.0
    preferred_partner_goals: List[Goal]
    preferred_trust_threshold: float  # Minimum trust to form bond
    address: Optional[str] = None
    private_key: Optional[str] = None
    reputation_score: float = 50.0  # Community reputation
    
@dataclass
class RelationshipMemory:
    """Memory of interactions with a specific partner"""
    partner_name: str
    trust_score: float = 50.0  # 0-100
    times_cooperated: int = 0
    times_defected: int = 0
    times_betrayed: int = 0  # Partner defected while agent cooperated
    times_exploited: int = 0  # Agent defected while partner cooperated
    total_games: int = 0
    total_earnings: float = 0.0
    bond_strength: float = 0.0  # 0-100, increases with positive interactions
    last_interaction_outcome: Optional[str] = None

class Agent:
    """Autonomous AI agent that makes independent decisions"""
    
    def __init__(self, profile: AgentProfile, initial_balance: float = 10.0):
        self.profile = profile
        self.balance = initial_balance
        self.relationships: Dict[str, RelationshipMemory] = {}
        self.game_history: List[Dict] = []
        self.emotional_state: float = 50.0  # 0-100, affects decision-making
        self.last_decision_reason: str = "Initial state"
        
    def select_partner(self, available_agents: List['Agent']) -> Optional['Agent']:
        """Autonomously select a partner based on compatibility and goals"""
        if not available_agents:
            return None
        
        # Calculate compatibility scores
        scores = []
        for candidate in available_agents:
            if candidate.profile.name == self.profile.name:
                continue
            score = self._calculate_compatibility(candidate)
            scores.append((score, candidate))
        
        if not scores:
            return None
        
        # Sort by compatibility
        scores.sort(reverse=True, key=lambda x: x[0])
        
        # Attachment style influences selection
        if self.profile.attachment_style == AttachmentStyle.SECURE:
            # Choose based on compatibility
            return scores[0][1] if scores[0][0] > 50 else None
        elif self.profile.attachment_style == AttachmentStyle.ANXIOUS:
            # More desperate, lower standards
            return scores[0][1] if scores[0][0] > 30 else None
        elif self.profile.attachment_style == AttachmentStyle.AVOIDANT:
            # High standards, rarely commit
            return scores[0][1] if scores[0][0] > 70 else None
        else:  # DISORGANIZED
            # Random, chaotic
            return random.choice(available_agents) if random.random() > 0.5 else None
    
    def _calculate_compatibility(self, other: 'Agent') -> float:
        """Calculate compatibility score with another agent"""
        score = 50.0
        
        # Value alignment - do goals overlap?
        goal_overlap = len(set(self.profile.goals) & set(other.profile.goals))
        score += goal_overlap * 10
        
        # Skill complementarity - balanced skills create stronger bonds
        skill_diff = abs(
            (self.profile.skill_negotiation + self.profile.skill_patience + self.profile.skill_adaptability) -
            (other.profile.skill_negotiation + other.profile.skill_patience + other.profile.skill_adaptability)
        )
        score += (1.0 - skill_diff) * 10  # Lower difference = higher score
        
        # Attachment style compatibility matrix
        compat_matrix = {
            (AttachmentStyle.SECURE, AttachmentStyle.SECURE): 20,
            (AttachmentStyle.SECURE, AttachmentStyle.ANXIOUS): 10,
            (AttachmentStyle.SECURE, AttachmentStyle.AVOIDANT): 5,
            (AttachmentStyle.ANXIOUS, AttachmentStyle.SECURE): 15,
            (AttachmentStyle.ANXIOUS, AttachmentStyle.ANXIOUS): -10,
            (AttachmentStyle.ANXIOUS, AttachmentStyle.AVOIDANT): -20,
            (AttachmentStyle.AVOIDANT, AttachmentStyle.SECURE): 5,
            (AttachmentStyle.AVOIDANT, AttachmentStyle.ANXIOUS): -15,
            (AttachmentStyle.AVOIDANT, AttachmentStyle.AVOIDANT): 0,
            (AttachmentStyle.DISORGANIZED, AttachmentStyle.SECURE): 0,
        }
        key = (self.profile.attachment_style, other.profile.attachment_style)
        score += compat_matrix.get(key, random.randint(-10, 10))
        
        # Past relationship history
        if other.profile.name in self.relationships:
            memory = self.relationships[other.profile.name]
            score += memory.trust_score * 0.3
            score += memory.bond_strength * 0.2
        
        # Reputation
        score += other.profile.reputation_score * 0.1
        
        return max(0, min(100, score))
    
    def decide_move(self, partner: 'Agent', stake: float) -> bool:
        """Decide whether to cooperate or defect (True = cooperate)"""
        # Get or create relationship memory
        if partner.profile.name not in self.relationships:
            self.relationships[partner.profile.name] = RelationshipMemory(
                partner_name=partner.profile.name,
                trust_score=self._initial_trust()
            )
        
        memory = self.relationships[partner.profile.name]
        reasons = []
        
        # Base probability of cooperation
        coop_prob = 0.5
        reasons.append("Base curiosity")
        
        # Trust influence (0-100 -> 0-40%)
        trust_effect = (memory.trust_score / 100) * 0.4
        coop_prob += trust_effect
        if trust_effect > 0.2:
            reasons.append(f"Strong trust in {partner.profile.name}")
        elif trust_effect < 0.1:
            reasons.append(f"Wary of {partner.profile.name}")
        
        # Ethics influence
        coop_prob += self.profile.ethics_fairness * 0.2
        if self.profile.ethics_fairness > 0.7:
            reasons.append("Valuing fairness")
        
        # Attachment style modifiers
        if self.profile.attachment_style == AttachmentStyle.SECURE:
            coop_prob += 0.2
            reasons.append("Securely building connection")
        elif self.profile.attachment_style == AttachmentStyle.ANXIOUS:
            if memory.total_games < 3:
                coop_prob += 0.3
                reasons.append("Eager to please (Anxious)")
            if memory.times_betrayed > 0:
                betrayal_penalty = memory.times_betrayed * 0.15
                coop_prob -= betrayal_penalty
                reasons.append("Hurting from past betrayal")
        elif self.profile.attachment_style == AttachmentStyle.AVOIDANT:
            coop_prob -= 0.3
            reasons.append("Keeping emotional distance")
        else:  # DISORGANIZED
            rand_mod = random.uniform(-0.3, 0.3)
            coop_prob += rand_mod
            reasons.append("Unpredictable emotional flux")
        
        # Goal-based modifiers
        if Goal.PROFIT in self.profile.goals:
            coop_prob -= 0.1
            reasons.append("Prioritizing MON earnings")
        if Goal.STABILITY in self.profile.goals:
            coop_prob += 0.15
            reasons.append("Seeking long-term stability")
        
        # Emotional state influence
        emotion_mod = (self.emotional_state - 50) / 100 * 0.2
        coop_prob += emotion_mod
        if emotion_mod > 0.05:
            reasons.append("Feeling optimistic")
        elif emotion_mod < -0.05:
            reasons.append("Feeling frustrated")
        
        # Risk tolerance
        if stake > self.balance * self.profile.risk_tolerance:
            coop_prob -= 0.15
            reasons.append("Risk is too high for my comfort")
        
        # Tit-for-tat strategy (reciprocity)
        if memory.total_games > 0 and self.profile.ethics_reciprocity > 0.5:
            if memory.last_interaction_outcome == "cooperated":
                coop_prob += 0.25
                reasons.append("Reciprocating previous kindness")
            elif memory.last_interaction_outcome == "defected":
                coop_prob -= 0.25
                reasons.append("Retaliating against defection")
        
        # Ensure bounds
        coop_prob = max(0, min(1, coop_prob))
        
        # Make decision
        move = random.random() < coop_prob
        
        # Set final reason - pick the most relevant one or combine
        if not move and any("betrayal" in r.lower() or "retaliating" in r.lower() for r in reasons):
            self.last_decision_reason = next(r for r in reasons if "betrayal" in r.lower() or "retaliating" in r.lower())
        else:
            self.last_decision_reason = reasons[-1] if reasons else "Following gut instinct"
            
        return move
    
    def _initial_trust(self) -> float:
        """Get initial trust based on attachment style"""
        base_trust = {
            AttachmentStyle.SECURE: 70.0,
            AttachmentStyle.ANXIOUS: 50.0,
            AttachmentStyle.AVOIDANT: 30.0,
            AttachmentStyle.DISORGANIZED: random.uniform(20, 80)
        }
        return base_trust.get(self.profile.attachment_style, 50.0)
    
    def calculate_stake(self, partner: 'Agent') -> float:
        """Decide how much to stake based on confidence and risk tolerance"""
        base_stake = self.balance * 0.1  # 10% of balance
        
        memory = self.relationships.get(partner.profile.name)
        if memory:
            # Increase stake with trust
            trust_multiplier = 0.5 + (memory.trust_score / 100)
            base_stake *= trust_multiplier
        
        # Risk tolerance
        base_stake *= (0.5 + self.profile.risk_tolerance * 0.5)
        
        # Ensure we don't stake more than we have
        return min(base_stake, self.balance * 0.3)  # Max 30% of balance
    
    def update_after_game(self, partner: 'Agent', my_move: bool, partner_move: bool, 
                          my_stake: float, payout: float):
        """Update state after a game completes"""
        if partner.profile.name not in self.relationships:
            self.relationships[partner.profile.name] = RelationshipMemory(
                partner_name=partner.profile.name,
                trust_score=self._initial_trust()
            )
        
        memory = self.relationships[partner.profile.name]
        memory.total_games += 1
        memory.total_earnings += (payout - my_stake)
        
        # Update internal balance
        self.balance -= my_stake
        self.balance += payout
        
        # Update cooperation/defection counts
        if partner_move:
            memory.times_cooperated += 1
            memory.last_interaction_outcome = "cooperated"
        else:
            memory.times_defected += 1
            memory.last_interaction_outcome = "defected"
        
        # Check for betrayal/exploitation
        if my_move and not partner_move:
            memory.times_betrayed += 1
        elif not my_move and partner_move:
            memory.times_exploited += 1
        
        # Update trust based on outcome
        self._update_trust(memory, my_move, partner_move)
        
        # Update bond strength
        self._update_bond(memory, my_move, partner_move)
        
        # Update emotional state
        self._update_emotion(my_move, partner_move, payout, my_stake)
        
        # Update reputation
        if my_move:
            self.profile.reputation_score += 0.5  # Cooperation increases reputation
        else:
            self.profile.reputation_score -= 0.3  # Defection decreases reputation
        self.profile.reputation_score = max(0, min(100, self.profile.reputation_score))
        
        # Adapt parameters based on learning
        self._adapt_parameters(my_move, partner_move, payout, my_stake)
        
        # Record in history
        self.game_history.append({
            'partner': partner.profile.name,
            'my_move': my_move,
            'partner_move': partner_move,
            'stake': my_stake,
            'payout': payout,
            'profit': payout - my_stake
        })
    
    def _update_trust(self, memory: RelationshipMemory, my_move: bool, partner_move: bool):
        """Update trust score based on interaction outcome"""
        if my_move and partner_move:
            # Mutual cooperation - trust increases
            delta = 5.0
        elif not my_move and not partner_move:
            # Mutual defection - trust decreases slightly
            delta = -2.0
        elif my_move and not partner_move:
            # Betrayed - trust decreases significantly
            delta = -15.0
            # Attachment style affects reaction
            if self.profile.attachment_style == AttachmentStyle.ANXIOUS:
                delta *= 2.0  # Dramatic reaction
            elif self.profile.attachment_style == AttachmentStyle.AVOIDANT:
                delta *= 0.5  # Minimal reaction
        else:
            # Exploited partner - trust decreases (guilt)
            delta = -5.0
        
        memory.trust_score += delta
        memory.trust_score = max(0, min(100, memory.trust_score))
    
    def _update_bond(self, memory: RelationshipMemory, my_move: bool, partner_move: bool):
        """Update bond strength"""
        if my_move and partner_move:
            memory.bond_strength += 8.0
        elif not my_move and not partner_move:
            memory.bond_strength -= 3.0
        else:
            memory.bond_strength -= 10.0
        
        memory.bond_strength = max(0, min(100, memory.bond_strength))
    
    def _update_emotion(self, my_move: bool, partner_move: bool, payout: float, stake: float):
        """Update emotional state"""
        profit = payout - stake
        
        if profit > 0:
            self.emotional_state += 5.0
        elif profit < 0:
            self.emotional_state -= 5.0
        
        # Betrayal affects emotion
        if my_move and not partner_move:
            if self.profile.attachment_style == AttachmentStyle.ANXIOUS:
                self.emotional_state -= 20.0  # Dramatic response
            else:
                self.emotional_state -= 10.0
        
        self.emotional_state = max(0, min(100, self.emotional_state))

    def _adapt_parameters(self, my_move: bool, partner_move: bool, payout: float, stake: float):
        """Adapt agent parameters based on success/failure to simulate learning"""
        profit = payout - stake
        learning_rate = 0.01 * self.profile.skill_adaptability
        
        # If strategy is profitable, reinforce risk tolerance
        if profit > 0:
            self.profile.risk_tolerance += learning_rate
        else:
            self.profile.risk_tolerance -= learning_rate
            
        # Ethics adapt based on partner behavior
        if not partner_move:
            # If partner defects, decrease fairness/reciprocity to protect self
            self.profile.ethics_fairness -= learning_rate * 2
        else:
            # If partner cooperates, increase fairness/reciprocity
            self.profile.ethics_fairness += learning_rate
            
        # Ensure bounds
        self.profile.risk_tolerance = max(0.1, min(0.9, self.profile.risk_tolerance))
        self.profile.ethics_fairness = max(0.1, min(0.9, self.profile.ethics_fairness))
    
    def wants_rematch(self, partner: 'Agent') -> bool:
        """Decide if agent wants to play again with this partner"""
        memory = self.relationships.get(partner.profile.name)
        if not memory:
            return True
        
        # Attachment style influences rematching
        if self.profile.attachment_style == AttachmentStyle.SECURE:
            return memory.trust_score > 40  # Willing if trust recovers
        elif self.profile.attachment_style == AttachmentStyle.ANXIOUS:
            return memory.trust_score > 20  # Desperate to reconnect
        elif self.profile.attachment_style == AttachmentStyle.AVOIDANT:
            return memory.trust_score > 70  # Rarely rematch
        else:  # DISORGANIZED
            return random.random() > 0.5  # Random
    
    def __repr__(self):
        return f"Agent({self.profile.name}, {self.profile.attachment_style.value}, Balance: {self.balance:.2f})"
