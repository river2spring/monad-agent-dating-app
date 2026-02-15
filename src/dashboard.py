"""
Streamlit dashboard for visualizing autonomous agent dating economy
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import networkx as nx
from typing import List
import time
import os
from dotenv import load_dotenv

from agent import Agent, AttachmentStyle
from game_engine import GameEngine
from agent_utils import create_agent_population, get_agent_summary, get_relationship_summary
from blockchain import BlockchainIntegration

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Agent Dating Economy",
    page_icon="💘",
    layout="wide"
)

# Initialize session state
if 'blockchain' not in st.session_state:
    rpc_url = os.getenv("MONAD_RPC_URL", "https://rpc.monad.xyz")
    private_key = os.getenv("PRIVATE_KEY", "")
    contract_address = os.getenv("CONTRACT_ADDRESS", "")
    
    if private_key:
        st.session_state.blockchain = BlockchainIntegration(rpc_url, private_key, contract_address)
    else:
        st.session_state.blockchain = None

if 'agents' not in st.session_state:
    st.session_state.agents = create_agent_population(10, 10.0)
    st.session_state.engine = GameEngine(st.session_state.agents, st.session_state.blockchain)
    st.session_state.round_count = 0
    st.session_state.auto_run = False
    st.session_state.blockchain_mode = False
    st.session_state.funding_hashes = []
    st.session_state.blockchain_mode = False

# Title and header
st.title("💘 AI Agent Dating Economy on Monad")
st.markdown("**Autonomous agents with attachment styles forming bonds through iterated Prisoner's Dilemma**")

# Sidebar controls
with st.sidebar:
    st.header("🎮 Controls")
    
    if st.button("▶️ Run Single Round", use_container_width=True):
        matches = st.session_state.engine.create_matches()
        for agent1, agent2 in matches:
            result = st.session_state.engine.run_round(agent1, agent2)
            if result:
                st.session_state.round_count += 1
        st.rerun()
    
    st.session_state.auto_run = st.toggle("🔄 Auto-Run", value=st.session_state.auto_run)
    
    # Blockchain Mode Toggle and Sync
    if st.session_state.blockchain:
        new_mode = st.toggle("⛓️ Blockchain Mode (Monad Mainnet)", value=st.session_state.blockchain_mode)
        
        # Trigger sync on toggle change
        if new_mode != st.session_state.blockchain_mode:
            st.session_state.blockchain_mode = new_mode
            st.session_state.engine.blockchain = st.session_state.blockchain if new_mode else None
            
            if new_mode:
                with st.spinner("Initial balance sync..."):
                    for agent in st.session_state.agents:
                        try:
                            balance_wei = st.session_state.blockchain.w3.eth.get_balance(agent.profile.address)
                            agent.balance = float(st.session_state.blockchain.w3.from_wei(balance_wei, 'ether'))
                        except: pass
            st.rerun()
        
        if st.session_state.blockchain_mode:
            st.info(f"Connected to Contract: {st.session_state.blockchain.contract_address[:10]}...")
            
            # Balance Sync for Blockchain Mode
            if st.button("🔄 Sync On-Chain Balances", use_container_width=True):
                with st.spinner("Fetching balances..."):
                    for agent in st.session_state.agents:
                        try:
                            balance_wei = st.session_state.blockchain.w3.eth.get_balance(agent.profile.address)
                            agent.balance = float(st.session_state.blockchain.w3.from_wei(balance_wei, 'ether'))
                        except Exception as e:
                            st.error(f"Failed to sync for {agent.profile.name}: {e}")
                st.success("Balances synchronized!")
                st.rerun()

            if st.button("💰 Fund Agents (MON)", use_container_width=True):
                st.session_state.funding_hashes = [] # Clear previous hashes
                with st.status("Distributing MON to agents...") as status:
                    for i, agent in enumerate(st.session_state.agents):
                        try:
                            status.update(label=f"Broadcasting to {agent.profile.name} ({i+1}/{len(st.session_state.agents)})...")
                            tx_hash = st.session_state.blockchain.fund_agent(agent.profile.address, 0.1)
                            st.session_state.funding_hashes.append({
                                'name': agent.profile.name,
                                'hash': tx_hash
                            })
                            st.write(f"✅ {agent.profile.name}: Confirmed ([View](https://monadvision.com/tx/{tx_hash}))")
                        except Exception as e:
                            st.error(f"❌ Failed to fund {agent.profile.name}: {e}")
                    status.update(label="Funding Complete!", state="complete")
                    status.update(label="Funding complete!", state="complete")
                st.success("Agents funding process finished!")
            
            # Display Funding Hashes
            if st.session_state.funding_hashes:
                with st.expander("📝 Recent Funding Transactions", expanded=True):
                    for item in st.session_state.funding_hashes:
                        st.markdown(f"**{item['name']}:** [`{item['hash'][:20]}...`](https://monadvision.com/tx/{item['hash']})")
    else:
        st.warning("⚠️ No Private Key found in .env. Blockchain Mode disabled.")
    
    if st.button("🔄 Reset Simulation", use_container_width=True):
        st.session_state.agents = create_agent_population(10, 10.0)
        st.session_state.engine = GameEngine(st.session_state.agents)
        st.session_state.round_count = 0
        st.rerun()
    
    st.divider()
    st.metric("Total Rounds", st.session_state.round_count)
    st.metric("Total Games", len(st.session_state.engine.match_history))
    st.metric("Active Bonds", len(st.session_state.engine.active_bonds))

# Main dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs(["👥 Agent Profiles", "🕸️ Relationship Network", "📊 Match Feed", "🏆 Leaderboard", "📈 Analytics"])

with tab1:
# ... (lines 100-153)
    st.header("Agent Profiles")
    
    # Attachment style colors
    style_colors = {
        'secure': '#28a745',
        'anxious': '#ffc107',
        'avoidant': '#dc3545',
        'disorganized': '#6c757d'
    }
    
    # Display agents in grid
    cols = st.columns(2)
    for idx, agent in enumerate(st.session_state.agents):
        with cols[idx % 2]:
            summary = get_agent_summary(agent)
            color = style_colors[summary['attachment']]
            
            with st.container(border=True):
                st.markdown(f"### {summary['name']}")
                st.markdown(f"<div style='background-color: {color}; padding: 5px; border-radius: 5px; text-align: center; color: white; font-weight: bold;'>{summary['attachment'].upper()}</div>", unsafe_allow_html=True)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("💰 Balance", f"{summary['balance']:.2f} MON")
                    st.metric("⭐ Reputation", f"{summary['reputation']:.1f}")
                    st.metric("😊 Emotional State", f"{summary['emotional_state']:.1f}")
                with col2:
                    st.metric("🎯 Goals", ", ".join(summary['goals']))
                    st.metric("🎲 Risk Tolerance", f"{summary['risk_tolerance']:.2f}")
                    st.metric("🎮 Total Games", summary['total_games'])
                
                # Skills
                st.markdown("**Skills:**")
                cols_skills = st.columns(3)
                with cols_skills[0]:
                    st.progress(summary['skill_negotiation'], text=f"Negotiation {summary['skill_negotiation']:.2f}")
                with cols_skills[1]:
                    st.progress(summary['skill_patience'], text=f"Patience {summary['skill_patience']:.2f}")
                with cols_skills[2]:
                    st.progress(summary['skill_adaptability'], text=f"Adaptability {summary['skill_adaptability']:.2f}")
                
                # Ethics
                st.markdown("**Ethics:**")
                cols_ethics = st.columns(2)
                with cols_ethics[0]:
                    st.caption(f"Fairness: {summary['ethics_fairness']:.2f}")
                with cols_ethics[1]:
                    st.caption(f"Reciprocity: {summary['ethics_reciprocity']:.2f}")
                
                # Wallet Info
                st.markdown("**Wallet:**")
                st.code(f"{summary['address']}", language="text")

with tab2:
    st.header("Relationship Network")
    
    # Build network graph
    G = nx.Graph()
    
    # Add nodes
    for agent in st.session_state.agents:
        summary = get_agent_summary(agent)
        G.add_node(summary['name'], 
                  attachment=summary['attachment'],
                  balance=summary['balance'])
    
    # Add edges for relationships
    edge_data = []
    for agent in st.session_state.agents:
        for partner_name, memory in agent.relationships.items():
            if memory.total_games > 0:
                # Only add edge once
                if agent.profile.name < partner_name:
                    G.add_edge(agent.profile.name, partner_name,
                             weight=memory.bond_strength,
                             trust=memory.trust_score,
                             games=memory.total_games)
    
    if len(G.edges()) > 0:
        # Create network visualization
        pos = nx.spring_layout(G, k=0.5, iterations=50)
        
        # Create edge traces
        edge_traces = []
        for edge in G.edges(data=True):
            x0, y0 = pos[edge[0]]
            x1, y1 = pos[edge[1]]
            
            weight = edge[2].get('weight', 0)
            trust = edge[2].get('trust', 50)
            
            # Color based on relationship health
            if trust > 70:
                color = 'green'
            elif trust > 40:
                color = 'orange'
            else:
                color = 'red'
            
            edge_trace = go.Scatter(
                x=[x0, x1, None],
                y=[y0, y1, None],
                mode='lines',
                line=dict(width=weight/10, color=color),
                hoverinfo='text',
                text=f"Trust: {trust:.1f}<br>Bond: {weight:.1f}<br>Games: {edge[2].get('games', 0)}",
                showlegend=False
            )
            edge_traces.append(edge_trace)
        
        # Create node trace
        node_x = []
        node_y = []
        node_text = []
        node_color = []
        
        for node in G.nodes():
            x, y = pos[node]
            node_x.append(x)
            node_y.append(y)
            
            data = G.nodes[node]
            attachment = data.get('attachment', 'unknown')
            balance = data.get('balance', 0)
            
            node_text.append(f"{node}<br>Attachment: {attachment}<br>Balance: {balance:.2f}")
            node_color.append(style_colors.get(attachment, '#000000'))
        
        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode='markers+text',
            text=[G.nodes[node] for node in G.nodes()],
            textposition="top center",
            marker=dict(
                size=30,
                color=node_color,
                line=dict(width=2, color='white')
            ),
            hovertext=node_text,
            hoverinfo='text',
            showlegend=False
        )
        
        # Create figure
        fig = go.Figure(data=edge_traces + [node_trace])
        fig.update_layout(
            showlegend=False,
            hovermode='closest',
            margin=dict(b=0,l=0,r=0,t=0),
            xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
            height=600
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No relationships formed yet. Run some rounds to see the network!")

with tab3:
    st.header("Live Match Feed")
    
    if st.session_state.engine.match_history:
        # Show recent matches
        recent = st.session_state.engine.match_history[-20:][::-1]
        
        for match in recent:
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    st.markdown(f"**{match['agent1_name']}**")
                    move_icon = "🤝" if match['agent1_move'] == 'cooperate' else "❌"
                    st.markdown(f"{move_icon} {match['agent1_move'].upper()}")
                    if 'agent1_reason' in match:
                        st.caption(f"💭 {match['agent1_reason']}")
                    profit_color = "green" if match['agent1_profit'] > 0 else "red"
                    st.markdown(f"<span style='color: {profit_color}; font-weight: bold;'>{match['agent1_profit']:+.2f} MON</span>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div style='text-align: center;'>⚔️<br>VS</div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"**{match['agent2_name']}**")
                    move_icon = "🤝" if match['agent2_move'] == 'cooperate' else "❌"
                    st.markdown(f"{move_icon} {match['agent2_move'].upper()}")
                    if 'agent2_reason' in match:
                        st.caption(f"💭 {match['agent2_reason']}")
                    profit_color = "green" if match['agent2_profit'] > 0 else "red"
                    st.markdown(f"<span style='color: {profit_color}; font-weight: bold;'>{match['agent2_profit']:+.4f} MON</span>", unsafe_allow_html=True)
                
                st.caption(f"Round {match['bond_rounds']} of their bond")
                
                # Show Blockchain Details
                # Show if we have a game_id OR any tx_hashes (like a failed create)
                if 'game_id' in match or ('tx_hashes' in match and match['tx_hashes']):
                    game_label = f"Game #{match['game_id']}" if 'game_id' in match else "Failed On-chain Attempt"
                    st.markdown(f"⛓️ **{game_label}**")
                    if 'tx_hashes' in match:
                        hashes = match['tx_hashes']
                        # Show primary hashes directly
                        h1, h2, h3 = st.columns(3)
                        with h1:
                            st.caption(f"**Create:** [`{hashes.get('create', 'N/A')[:10]}...`](https://testnet.monadexplorer.com/tx/{hashes.get('create', '')})")
                        with h2:
                            st.caption(f"**Join:** [`{hashes.get('join', 'N/A')[:10]}...`](https://testnet.monadexplorer.com/tx/{hashes.get('join', '')})")
                        with h3:
                            st.caption(f"**Reveals:** [1](https://testnet.monadexplorer.com/tx/{hashes.get('reveal1', '')}) | [2](https://testnet.monadexplorer.com/tx/{hashes.get('reveal2', '')})")
                        
                        # Full details still available in expander if needed
                        with st.expander("🔍 Full Transaction Trail"):
                            st.markdown(f"**Commit 1:** [`{hashes.get('commit1', 'N/A')[:15]}`](https://testnet.monadexplorer.com/tx/{hashes.get('commit1', '')})")
                            st.markdown(f"**Commit 2:** [`{hashes.get('commit2', 'N/A')[:15]}`](https://testnet.monadexplorer.com/tx/{hashes.get('commit2', '')})")
                        
                        if 'error' in match:
                            st.error(f"Transaction Error: {match['error']}")
                elif 'on_chain' in match:
                    st.markdown("⛓️ **On-chain Transaction Verified**")
    else:
        st.info("No games played yet!")

with tab4:
    st.header("Leaderboard")
    
    # Create leaderboard data
    leaderboard_data = []
    for agent in st.session_state.agents:
        summary = get_agent_summary(agent)
        leaderboard_data.append(summary)
    
    df = pd.DataFrame(leaderboard_data)
    
    # Sort by balance
    df_sorted = df.sort_values('balance', ascending=False)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 By Balance")
        for idx, row in df_sorted.iterrows():
            with st.container(border=True):
                cols = st.columns([3, 2, 2])
                with cols[0]:
                    st.markdown(f"**{row['name']}** ({row['attachment']})")
                with cols[1]:
                    st.metric("Balance", f"{row['balance']:.2f} MON")
                with cols[2]:
                    st.metric("Profit", f"{row['total_profit']:+.2f} MON")
    
    with col2:
        st.subheader("⭐ By Reputation")
        df_rep = df.sort_values('reputation', ascending=False)
        for idx, row in df_rep.iterrows():
            with st.container(border=True):
                cols = st.columns([3, 2, 2])
                with cols[0]:
                    st.markdown(f"**{row['name']}** ({row['attachment']})")
                with cols[1]:
                    st.metric("Reputation", f"{row['reputation']:.1f}")
                with cols[2]:
                    st.metric("Games", row['total_games'])

with tab5:
    st.header("📈 System Analytics")
    
    if st.session_state.engine.match_history:
        history_df = pd.DataFrame(st.session_state.engine.match_history)
        
        # 1. Cooperation Rate over time
        st.subheader("🤝 Global Cooperation Rate")
        history_df['combined_coop'] = history_df.apply(
            lambda x: (1 if x['agent1_move'] == 'cooperate' else 0) + (1 if x['agent2_move'] == 'cooperate' else 0), axis=1
        ) / 2
        
        # Calculate rolling cooperation rate
        window = max(1, len(history_df) // 5)
        history_df['rolling_coop'] = history_df['combined_coop'].rolling(window=window).mean()
        
        fig_coop = px.line(history_df, y='rolling_coop', title=f"Global Cooperation Trend (Rolling Window: {window})")
        fig_coop.update_layout(yaxis_range=[0, 1])
        st.plotly_chart(fig_coop, use_container_width=True)
        
        # 2. Trust Distribution by Attachment Style
        st.subheader("🛡️ Trust by Attachment Style")
        trust_data = []
        for agent in st.session_state.agents:
            for partner_name, memory in agent.relationships.items():
                if memory.total_games > 0:
                    trust_data.append({
                        'Agent': agent.profile.name,
                        'Style': agent.profile.attachment_style.value,
                        'Trust': memory.trust_score
                    })
        
        if trust_data:
            trust_df = pd.DataFrame(trust_data)
            fig_trust = px.box(trust_df, x='Style', y='Trust', color='Style', 
                              points="all", title="Trust Score Distribution by Attachment Style")
            st.plotly_chart(fig_trust, use_container_width=True)
            
            # 3. Learning Visibility: Ethics Evolving
            st.subheader("🧠 Adaptive Learning: Ethics Evolution")
            ethics_data = []
            for agent in st.session_state.agents:
                ethics_data.append({
                    'Agent': agent.profile.name,
                    'Style': agent.profile.attachment_style.value,
                    'Fairness': agent.profile.ethics_fairness
                })
            ethics_df = pd.DataFrame(ethics_data)
            fig_ethics = px.bar(ethics_df, x='Agent', y='Fairness', color='Style', 
                               title="Current Ethics (Fairness) Level (Learned from experience)")
            st.plotly_chart(fig_ethics, use_container_width=True)
        else:
            st.info("Play more games to see trust distribution analysis.")
    else:
        st.info("No data yet. Run some rounds to see analytics!")

# Auto-run logic
if st.session_state.auto_run:
    # Run a round automatically
    matches = st.session_state.engine.create_matches()
    for agent1, agent2 in matches:
        result = st.session_state.engine.run_round(agent1, agent2)
        if result:
            st.session_state.round_count += 1
    
    time.sleep(1)
    st.rerun()
