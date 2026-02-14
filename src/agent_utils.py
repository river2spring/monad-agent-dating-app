"""
Utility functions for creating and managing agents
"""
import random
from typing import List
from agent import Agent, AgentProfile, AttachmentStyle, Goal

def create_agent_population(num_agents: int = 10, initial_balance: float = 10.0) -> List[Agent]:
    """Create a diverse population of agents with varying profiles"""
    
    names = [
        "Alice", "Bob", "Charlie", "Diana", "Eve", 
        "Frank", "Grace", "Henry", "Iris", "Jack"
    ]
    
    agents = []
    
    # Ensure diversity in attachment styles (at least 2 of each)
    attachment_distribution = [
        AttachmentStyle.SECURE, AttachmentStyle.SECURE, AttachmentStyle.SECURE,
        AttachmentStyle.ANXIOUS, AttachmentStyle.ANXIOUS, AttachmentStyle.ANXIOUS,
        AttachmentStyle.AVOIDANT, AttachmentStyle.AVOIDANT,
        AttachmentStyle.DISORGANIZED, AttachmentStyle.DISORGANIZED
    ]
    random.shuffle(attachment_distribution)
    
    for i in range(min(num_agents, len(names))):
        # Random goals (1-3 goals per agent)
        num_goals = random.randint(1, 3)
        goals = random.sample(list(Goal), num_goals)
        
        # Create profile with varied attributes
        profile = AgentProfile(
            name=names[i],
            attachment_style=attachment_distribution[i],
            goals=goals,
            risk_tolerance=random.uniform(0.2, 0.9),
            ethics_fairness=random.uniform(0.3, 0.9),
            ethics_reciprocity=random.uniform(0.4, 1.0),
            skill_negotiation=random.uniform(0.3, 0.9),
            skill_patience=random.uniform(0.3, 0.9),
            skill_adaptability=random.uniform(0.3, 0.9),
            preferred_partner_goals=random.sample(list(Goal), random.randint(1, 2)),
            preferred_trust_threshold=random.uniform(30, 70),
            reputation_score=random.uniform(40, 60)
        )
        
        agents.append(Agent(profile, initial_balance))
    
    return agents

def get_agent_summary(agent: Agent) -> dict:
    """Get a summary of agent state for display"""
    return {
        'name': agent.profile.name,
        'attachment': agent.profile.attachment_style.value,
        'goals': [g.value for g in agent.profile.goals],
        'balance': round(agent.balance, 2),
        'reputation': round(agent.profile.reputation_score, 1),
        'emotional_state': round(agent.emotional_state, 1),
        'risk_tolerance': round(agent.profile.risk_tolerance, 2),
        'ethics_fairness': round(agent.profile.ethics_fairness, 2),
        'ethics_reciprocity': round(agent.profile.ethics_reciprocity, 2),
        'skill_negotiation': round(agent.profile.skill_negotiation, 2),
        'skill_patience': round(agent.profile.skill_patience, 2),
        'skill_adaptability': round(agent.profile.skill_adaptability, 2),
        'total_games': len(agent.game_history),
        'total_profit': round(sum(g['profit'] for g in agent.game_history), 2),
        'active_relationships': len(agent.relationships)
    }

def get_relationship_summary(agent: Agent, partner_name: str) -> dict:
    """Get summary of relationship between two agents"""
    if partner_name not in agent.relationships:
        return None
    
    memory = agent.relationships[partner_name]
    return {
        'partner': partner_name,
        'trust': round(memory.trust_score, 1),
        'bond_strength': round(memory.bond_strength, 1),
        'total_games': memory.total_games,
        'cooperations': memory.times_cooperated,
        'defections': memory.times_defected,
        'betrayals': memory.times_betrayed,
        'total_earnings': round(memory.total_earnings, 2),
        'cooperation_rate': round(memory.times_cooperated / memory.total_games * 100, 1) if memory.total_games > 0 else 0
    }
