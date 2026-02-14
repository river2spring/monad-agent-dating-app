"""
Test suite for agent autonomy and decision-making
"""
import pytest
from src.agent import Agent, AgentProfile, AttachmentStyle, Goal
import random

def create_test_agent(name="TestAgent", attachment=AttachmentStyle.SECURE):
    """Helper to create test agent"""
    profile = AgentProfile(
        name=name,
        attachment_style=attachment,
        goals=[Goal.PROFIT],
        risk_tolerance=0.5,
        ethics_fairness=0.5,
        ethics_reciprocity=0.7,
        skill_negotiation=0.5,
        skill_patience=0.5,
        skill_adaptability=0.5,
        preferred_partner_goals=[Goal.STABILITY],
        preferred_trust_threshold=50.0
    )
    return Agent(profile, initial_balance=100.0)

def test_attachment_styles_produce_different_behaviors():
    """Test that different attachment styles lead to different decisions"""
    # Create agents with different attachment styles
    secure = create_test_agent("Secure", AttachmentStyle.SECURE)
    anxious = create_test_agent("Anxious", AttachmentStyle.ANXIOUS)
    avoidant = create_test_agent("Avoidant", AttachmentStyle.AVOIDANT)
    
    # Run many trials to see behavioral differences
    secure_coop_count = 0
    anxious_coop_count = 0
    avoidant_coop_count = 0
    
    trials = 100
    for _ in range(trials):
        if secure.decide_move(anxious, 1.0):
            secure_coop_count += 1
        if anxious.decide_move(secure, 1.0):
            anxious_coop_count += 1
        if avoidant.decide_move(secure, 1.0):
           avoidant_coop_count += 1
    
    # Secure should cooperate most, avoidant least
    assert secure_coop_count > avoidant_coop_count, \
        f"Secure ({secure_coop_count}) should cooperate more than Avoidant ({avoidant_coop_count})"
    
    # Anxious should cooperate a lot initially
    assert anxious_coop_count > avoidant_coop_count, \
        f"Anxious ({anxious_coop_count}) should cooperate more than Avoidant ({avoidant_coop_count})"

def test_trust_affects_cooperation():
    """Test that trust score affects cooperation probability"""
    agent = create_test_agent()
    partner = create_test_agent("Partner")
    
    # Manually set high trust
    agent.relationships[partner.profile.name] = type('obj', (object,), {
        'partner_name': partner.profile.name,
        'trust_score': 90.0,
        'total_games': 5,
        'times_cooperated': 5,
        'times_defected': 0,
        'times_betrayed': 0,
        'times_exploited': 0,
        'bond_strength': 80.0,
        'total_earnings': 10.0,
        'last_interaction_outcome': 'cooperated'
    })()
    
    high_trust_coop = sum(agent.decide_move(partner, 1.0) for _ in range(100))
    
    # Manually set low trust
    agent.relationships[partner.profile.name].trust_score = 10.0
    agent.relationships[partner.profile.name].last_interaction_outcome = 'defected'
    
    low_trust_coop = sum(agent.decide_move(partner, 1.0) for _ in range(100))
    
    assert high_trust_coop > low_trust_coop, \
        f"High trust ({high_trust_coop}) should lead to more cooperation than low trust ({low_trust_coop})"

def test_betrayal_reduces_trust():
    """Test that betrayal reduces trust score"""
    agent = create_test_agent()
    partner = create_test_agent("Partner")
    
    # Simulate initial cooperation
    agent.update_after_game(partner, True, True, 1.0, 1.5)
    initial_trust = agent.relationships[partner.profile.name].trust_score
    
    # Simulate betrayal (agent cooperates, partner defects)
    agent.update_after_game(partner, True, False, 1.0, 0.0)
    betrayal_trust = agent.relationships[partner.profile.name].trust_score
    
    assert betrayal_trust < initial_trust, \
        f"Trust after betrayal ({betrayal_trust}) should be less than initial ({initial_trust})"

def test_anxious_reacts_more_strongly_to_betrayal():
    """Test that anxious agents have stronger reactions to betrayal"""
    secure = create_test_agent("Secure", AttachmentStyle.SECURE)
    anxious = create_test_agent("Anxious", AttachmentStyle.ANXIOUS)
    partner = create_test_agent("Partner")
    
    # Establish baseline trust
    secure.relationships[partner.profile.name] = type('obj', (object,), {
        'partner_name': partner.profile.name,
        'trust_score': 70.0,
        'times_cooperated': 0,
        'times_defected': 0,
        'times_betrayed': 0,
        'times_exploited': 0,
        'total_games': 0,
        'bond_strength': 50.0,
        'total_earnings': 0.0,
        'last_interaction_outcome': None
    })()
    
    anxious.relationships[partner.profile.name] = type('obj', (object,), {
        'partner_name': partner.profile.name,
        'trust_score': 70.0,
        'times_cooperated': 0,
        'times_defected': 0,
        'times_betrayed': 0,
        'times_exploited': 0,
        'total_games': 0,
        'bond_strength': 50.0,
        'total_earnings': 0.0,
        'last_interaction_outcome': None
    })()
    
    # Simulate betrayal
    secure.update_after_game(partner, True, False, 1.0, 0.0)
    anxious.update_after_game(partner, True, False, 1.0, 0.0)
    
    secure_trust_drop = 70.0 - secure.relationships[partner.profile.name].trust_score
    anxious_trust_drop = 70.0 - anxious.relationships[partner.profile.name].trust_score
    
    assert anxious_trust_drop > secure_trust_drop, \
        f"Anxious trust drop ({anxious_trust_drop}) should be greater than Secure ({secure_trust_drop})"

def test_decisions_are_non_deterministic():
    """Test that agents don't always make the same decision given same inputs"""
    agent = create_test_agent()
    partner = create_test_agent("Partner")
    
    # Run same scenario many times
    decisions = [agent.decide_move(partner, 1.0) for _ in range(50)]
    
    # Should have some variation (not all True or all False)
    assert len(set(decisions)) > 1, \
        "Agent should show non-deterministic behavior, not all same decisions"

def test_compatibility_scoring():
    """Test that compatibility calculation produces reasonable scores"""
    # Create agents with very compatible profiles
    agent1 = create_test_agent("Agent1", AttachmentStyle.SECURE)
    agent1.profile.goals = [Goal.STABILITY, Goal.LEARNING]
    
    agent2 = create_test_agent("Agent2", AttachmentStyle.SECURE)
    agent2.profile.goals = [Goal.STABILITY, Goal.LEARNING]
    
    # Create incompatible agent
    agent3 = create_test_agent("Agent3", AttachmentStyle.AVOIDANT)
    agent3.profile.goals = [Goal.PROFIT]
    
    compat_high = agent1._calculate_compatibility(agent2)
    compat_low = agent1._calculate_compatibility(agent3)
    
    assert compat_high > compat_low, \
        f"Compatible agents ({compat_high}) should score higher than incompatible ({compat_low})"

def test_agent_wants_rematch_depends_on_attachment():
    """Test that rematch willingness varies by attachment style"""
    partner = create_test_agent("Partner")
    
    # Create relationship with medium trust (55)
    def create_memory(agent, trust=55.0):
        agent.relationships[partner.profile.name] = type('obj', (object,), {
            'partner_name': partner.profile.name,
            'trust_score': trust,
            'times_cooperated': 5,
            'times_defected': 5,
            'times_betrayed': 2,
            'times_exploited': 0,
            'total_games': 10,
            'bond_strength': 40.0,
            'total_earnings': 2.0,
            'last_interaction_outcome': 'cooperated'
        })()
    
    secure = create_test_agent("Secure", AttachmentStyle.SECURE)
    anxious = create_test_agent("Anxious", AttachmentStyle.ANXIOUS)
    avoidant = create_test_agent("Avoidant", AttachmentStyle.AVOIDANT)
    
    create_memory(secure)
    create_memory(anxious)
    create_memory(avoidant)
    
    # With trust=55, Secure and Anxious should want rematch, but not Avoidant (needs 70+)
    assert secure.wants_rematch(partner), "Secure should want rematch with trust=55"
    assert anxious.wants_rematch(partner), "Anxious should want rematch with trust=55"
    assert not avoidant.wants_rematch(partner), "Avoidant should NOT want rematch with trust=55"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
