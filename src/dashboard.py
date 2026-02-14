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

from agent import Agent, AttachmentStyle
from game_engine import GameEngine
from agent_utils import create_agent_population, get_agent_summary, get_relationship_summary

# Page configuration
st.set_page_config(
    page_title="AI Agent Dating Economy",
    page_icon="💘",
    layout="wide"
)

# Initialize session state
if 'agents' not in st.session_state:
    st.session_state.agents = create_agent_population(10, 10.0)
    st.session_state.engine = GameEngine(st.session_state.agents)
    st.session_state.round_count = 0
    st.session_state.auto_run = False

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
tab1, tab2, tab3, tab4 = st.tabs(["👥 Agent Profiles", "🕸️ Relationship Network", "📊 Match Feed", "🏆 Leaderboard"])

with tab1:
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
                    profit_color = "green" if match['agent1_profit'] > 0 else "red"
                    st.markdown(f"<span style='color: {profit_color}; font-weight: bold;'>{match['agent1_profit']:+.2f} MON</span>", unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<div style='text-align: center;'>⚔️<br>VS</div>", unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"**{match['agent2_name']}**")
                    move_icon = "🤝" if match['agent2_move'] == 'cooperate' else "❌"
                    st.markdown(f"{move_icon} {match['agent2_move'].upper()}")
                    profit_color = "green" if match['agent2_profit'] > 0 else "red"
                    st.markdown(f"<span style='color: {profit_color}; font-weight: bold;'>{match['agent2_profit']:+.2f} MON</span>", unsafe_allow_html=True)
                
                st.caption(f"Round {match['bond_rounds']} of their bond")
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

# Auto-run logic
if st.session_state.auto_run:
    time.sleep(1)
    st.rerun()
