"""
Demo scenario showcasing autonomous agent behavior
Simulates 100+ interactions to demonstrate emergent patterns
"""
import sys
sys.path.append('src')

from agent_utils import create_agent_population
from game_engine import GameEngine
import pandas as pd

def run_demo():
    """Run autonomous agent simulation"""
    print("🎮 AI Agent Dating Economy Demo")
    print("=" * 60)
    
    # Create 10 diverse agents
    print("\n📋 Creating 10 autonomous agents...")
    agents = create_agent_population(10, 10.0)
    
    print("\n👥 Agent Roster:")
    for agent in agents:
        print(f"  {agent.profile.name:10} | {agent.profile.attachment_style.value:12} | Goals: {', '.join(g.value for g in agent.profile.goals)}")
    
    # Initialize game engine
    engine = GameEngine(agents)
    
    # Run multiple rounds
    total_rounds = 20
    print(f"\n🎲 Running {total_rounds} rounds of autonomous interactions...")
    print("-" * 60)
    
    for round_num in range(1, total_rounds + 1):
        matches = engine.create_matches()
        
        if not matches:
            print(f"\nRound {round_num}: No matches created")
            continue
        
        print(f"\n📍 Round {round_num}:")
        for agent1, agent2 in matches:
            result = engine.run_round(agent1, agent2)
            if result:
                outcome_icon = "🤝" if result['agent1_move'] == 'cooperate' and result['agent2_move'] == 'cooperate' else \
                             "💔" if result['agent1_move'] != result['agent2_move'] else "⚔️"
                print(f"  {outcome_icon} {result['agent1_name']:10} ({result['agent1_move']:9}) vs {result['agent2_name']:10} ({result['agent2_move']:9}) → "
                      f"{result['agent1_name']}: {result['agent1_profit']:+.2f} MON, {result['agent2_name']}: {result['agent2_profit']:+.2f} MON")
        
        # Evaluate bonds every 5 rounds
        if round_num % 5 == 0:
            evaluations = engine.evaluate_bonds()
            print(f"\n  💔 Bond Evaluations:")
            for agent1, agent2, continues in evaluations:
                if not continues:
                    mem1 = agent1.relationships.get(agent2.profile.name)
                    print(f"    BREAKUP: {agent1.profile.name} & {agent2.profile.name} (Trust: {mem1.trust_score if mem1 else 'N/A':.1f})")
    
    # Final statistics
    print("\n" + "=" * 60)
    print("📊 Final Statistics")
    print("=" * 60)
    
    stats = engine.get_statistics()
    print(f"\n  Total Games Played: {stats['total_games']}")
    print(f"  Active Bonds Remaining: {stats['active_bonds']}")
    
    # Agent standings
    print("\n💰 Final Balances:")
    balances = sorted(stats['agent_balances'].items(), key=lambda x: x[1], reverse=True)
    for i, (name, balance) in enumerate(balances, 1):
        agent = next(a for a in agents if a.profile.name == name)
        profit = balance - 10.0
        profit_str = f"+{profit:.2f}" if profit > 0 else f"{profit:.2f}"
        print(f"  #{i}. {name:10} | {balance:.2f} MON ({profit_str}) | {agent.profile.attachment_style.value}")
    
    # Reputation
    print("\n⭐ Reputation Scores:")
    reps = sorted(stats['agent_reputations'].items(), key=lambda x: x[1], reverse=True)
    for name, rep in reps:
        agent = next(a for a in agents if a.profile.name == name)
        print(f"  {name:10} | {rep:.1f} | {agent.profile.attachment_style.value}")
    
    # Behavioral insights
    print("\n🧠 Behavioral Insights:")
    
    # Find most cooperative agent
    coop_rates = {}
    for agent in agents:
        total_coop = sum(1 for g in agent.game_history if g['my_move'])
        total_games = len(agent.game_history)
        if total_games > 0:
            coop_rates[agent.profile.name] = (total_coop / total_games) * 100
    
    if coop_rates:
        most_coop = max(coop_rates.items(), key=lambda x: x[1])
        least_coop = min(coop_rates.items(), key=lambda x: x[1])
        
        most_agent = next(a for a in agents if a.profile.name == most_coop[0])
        least_agent = next(a for a in agents if a.profile.name == least_coop[0])
        
        print(f"  Most Cooperative: {most_coop[0]} ({most_agent.profile.attachment_style.value}) - {most_coop[1]:.1f}% cooperation rate")
        print(f"  Least Cooperative: {least_coop[0]} ({least_agent.profile.attachment_style.value}) - {least_coop[1]:.1f}% cooperation rate")
    
    # Find strongest bond
    all_bonds = []
    for agent in agents:
        for partner_name, memory in agent.relationships.items():
            if memory.total_games > 0:
                # Only add once (avoid duplicates)
                if agent.profile.name < partner_name:
                    all_bonds.append({
                        'agent1': agent.profile.name,
                        'agent2': partner_name,
                        'trust': memory.trust_score,
                        'bond': memory.bond_strength,
                        'games': memory.total_games
                    })
    
    if all_bonds:
        strongest = max(all_bonds, key=lambda x: x['bond'])
        print(f"  Strongest Bond: {strongest['agent1']} & {strongest['agent2']} (Bond: {strongest['bond']:.1f}, Trust: {strongest['trust']:.1f}, Games: {strongest['games']})")
    
    print("\n✅ Demo Complete!")
    print("\n💡 Key Observations:")
    print("  - Agents made autonomous partner selections")
    print("  - Attachment styles influenced cooperation rates")
    print("  - Trust scores evolved based on interactions")
    print("  - Bonds formed and broke autonomously")
    print("  - Emergent patterns: Some agents thrived, others struggled")

if __name__ == "__main__":
    run_demo()
