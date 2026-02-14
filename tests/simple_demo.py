"""
Simple console-based demo that doesn't require pandas/streamlit/plotly
Run this to test the agent logic without dependencies
"""
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from agent import Agent, AgentProfile, AttachmentStyle, Goal
from game_engine import GameEngine
import random

def create_simple_agents(num_agents=10):
    """Create agents without using agent_utils (which imports pandas)"""
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", 
             "Frank", "Grace", "Henry", "Iris", "Jack"]
    
    attachment_styles = [
        AttachmentStyle.SECURE, AttachmentStyle.SECURE, AttachmentStyle.SECURE,
        AttachmentStyle.ANXIOUS, AttachmentStyle.ANXIOUS, AttachmentStyle.ANXIOUS,
        AttachmentStyle.AVOIDANT, AttachmentStyle.AVOIDANT,
        AttachmentStyle.DISORGANIZED, AttachmentStyle.DISORGANIZED
    ]
    random.shuffle(attachment_styles)
    
    agents = []
    for i in range(num_agents):
        num_goals = random.randint(1, 3)
        goals = random.sample(list(Goal), num_goals)
        
        profile = AgentProfile(
            name=names[i],
            attachment_style=attachment_styles[i],
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
        
        agents.append(Agent(profile, initial_balance=10.0))
    
    return agents

def main():
    print("=" * 70)
    print("AI AGENT DATING ECONOMY - CONSOLE DEMO")
    print("=" * 70)
    print("\nThis simplified demo tests the core agent logic without needing")
    print("pandas, streamlit, or plotly (which require C++ compilation on Windows)")
    print()
    
    # Create agents
    print("[*] Creating 10 autonomous agents...\n")
    agents = create_simple_agents(10)
    
    print("AGENT ROSTER:")
    print("-" * 70)
    for agent in agents:
        goals_str = ", ".join(g.value for g in agent.profile.goals)
        print(f"  {agent.profile.name:10} | {agent.profile.attachment_style.value:14} | {goals_str}")
    
    # Initialize game engine
    engine = GameEngine(agents)
    
    # Run simulation
    num_rounds = 15
    print(f"\n[*] Running {num_rounds} rounds of autonomous agent interactions...")
    print("=" * 70)
    
    for round_num in range(1, num_rounds + 1):
        matches = engine.create_matches()
        
        if not matches:
            continue
        
        print(f"\n[ROUND {round_num}]:")
        print("-" * 70)
        
        for agent1, agent2 in matches:
            result = engine.run_round(agent1, agent2)
            if result:
                # Format output
                a1 = result['agent1_name']
                a2 = result['agent2_name']
                m1 = result['agent1_move']
                m2 = result['agent2_move']
                p1 = result['agent1_profit']
                p2 = result['agent2_profit']
                
                # Choose symbol
                if m1 == 'cooperate' and m2 == 'cooperate':
                    symbol = "[OK]"
                elif m1 != m2:
                    symbol = "[!!]"
                else:
                    symbol = "[XX]"
                
                print(f"  {symbol} {a1:10} ({m1:9}) vs {a2:10} ({m2:9})")
                print(f"       -> {a1}: {p1:+.2f} MON  |  {a2}: {p2:+.2f} MON")
        
        # Evaluate bonds every 5 rounds
        if round_num % 5 == 0:
            evaluations = engine.evaluate_bonds()
            breakups = [e for e in evaluations if not e[2]]
            
            if breakups:
                print(f"\n  [BOND BREAKUPS]:")
                for agent1, agent2, _ in breakups:
                    mem1 = agent1.relationships.get(agent2.profile.name)
                    trust = mem1.trust_score if mem1 else 0
                    print(f"     {agent1.profile.name} & {agent2.profile.name} (Trust: {trust:.1f})")
    
    # Final statistics
    print("\n" + "=" * 70)
    print("FINAL STATISTICS")
    print("=" * 70)
    
    stats = engine.get_statistics()
    print(f"\n  Total Games Played: {stats['total_games']}")
    print(f"  Bonds Remaining: {stats['active_bonds']}")
    
    # Sort agents by balance
    agent_data = [(a.profile.name, a.balance, a.profile.attachment_style.value, 
                   sum(1 for g in a.game_history if g['my_move']) / len(a.game_history) * 100 if a.game_history else 0)
                  for a in agents]
    agent_data.sort(key=lambda x: x[1], reverse=True)
    
    print("\n[FINAL STANDINGS]:")
    print("-" * 70)
    print(f"  {'Rank':<6} {'Name':<12} {'Balance':>10} {'Profit':>10} {'Attach Style':<14} {'Coop %':>8}")
    print("-" * 70)
    
    for i, (name, balance, style, coop_rate) in enumerate(agent_data, 1):
        profit = balance - 10.0
        profit_str = f"+{profit:.2f}" if profit > 0 else f"{profit:.2f}"
        print(f"  #{i:<5} {name:<12} {balance:>10.2f} {profit_str:>10} {style:<14} {coop_rate:>7.1f}%")
    
    print("\n" + "=" * 70)
    print("BEHAVIORAL INSIGHTS:")
    print("-" * 70)
    
    # Most/least cooperative
    if agent_data:
        by_coop = sorted(agent_data, key=lambda x: x[3], reverse=True)
        most_coop = by_coop[0]
        least_coop = by_coop[-1]
        
        print(f"  Most Cooperative:  {most_coop[0]:<12} ({most_coop[2]:<14}) {most_coop[3]:.1f}% coop rate")
        print(f"  Least Cooperative: {least_coop[0]:<12} ({least_coop[2]:<14}) {least_coop[3]:.1f}% coop rate")
    
    # Find strongest bond
    all_bonds = []
    for agent in agents:
        for partner_name, memory in agent.relationships.items():
            if memory.total_games > 0 and agent.profile.name < partner_name:
                all_bonds.append((agent.profile.name, partner_name, memory.bond_strength, 
                                memory.trust_score, memory.total_games))
    
    if all_bonds:
        strongest = max(all_bonds, key=lambda x: x[2])
        print(f"  Strongest Bond:    {strongest[0]} & {strongest[1]}")
        print(f"                     Bond: {strongest[2]:.1f}  Trust: {strongest[3]:.1f}  Games: {strongest[4]}")
    
    print("\n[*] Demo Complete!")
    print("\n[KEY OBSERVATIONS]:")
    print("  [+] Agents made autonomous partner selections")
    print("  [+] Attachment styles influenced cooperation rates")
    print("  [+] Trust scores evolved based on interactions")
    print("  [+] Bonds formed and broke autonomously")
    print("  [+] Emergent patterns: Some agents thrived, others struggled")
    print("\n" + "=" * 70)

if __name__ == "__main__":
    main()
