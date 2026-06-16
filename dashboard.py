import streamlit as st
import pandas as pd
import os
import json
from dotenv import load_dotenv
from community_database.models import init_db, Community, Post, Campaign
from crews.discovery_crew import DiscoveryCrew
from crews.content_crew import ContentCrew
from crews.orchestrator_crew import HierarchicalOrchestrator
from sqlalchemy.orm import sessionmaker

load_dotenv()

# Page config
st.set_page_config(page_title="🇪🇬 Egyptian Growth Specialist Dashboard", layout="wide")
st.title("🇪🇬 Egyptian Omnichannel Growth Specialist")

# DB Initialization
db_url = os.getenv("DATABASE_URL", "sqlite:///community_database/growth_specialist.db")
Session = init_db(db_url)

# Helper to refresh session
def get_session():
    return Session

st.sidebar.header("Control Center")
mode = st.sidebar.radio("Navigate to:", ["Communities", "Approvals", "Active Campaigns", "Run Crews", "Model Settings"])

if mode == "Communities":
    st.header("Discovered Egyptian Communities")
    session = get_session()
    communities = session.query(Community).all()
    
    if communities:
        data = []
        for c in communities:
            data.append({
                "ID": c.id,
                "Name": c.name,
                "Platform": c.platform,
                "Governorate": c.governorate,
                "Audience Size": c.audience_size,
                "Status": c.status,
                "URL": c.url
            })
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        # Action: Approve/Prohibit
        st.subheader("Update Community Status")
        col1, col2, col3 = st.columns(3)
        with col1:
            c_id = st.number_input("Community ID", min_value=1, step=1)
        with col2:
            new_status = st.selectbox("New Status", ["Approved", "Needs Review", "Prohibited"])
        with col3:
            if st.button("Update Status"):
                comm = session.query(Community).filter_by(id=c_id).first()
                if comm:
                    comm.status = new_status
                    session.commit()
                    st.success(f"Updated {comm.name} to {new_status}")
                    st.rerun()
                else:
                    st.error("Community not found")
    else:
        st.info("No communities discovered yet. Run the Discovery Crew!")

elif mode == "Approvals":
    st.header("Content Approvals (Egyptian Arabic)")
    session = get_session()
    pending_posts = session.query(Post).filter_by(status="Needs Approval").all()
    
    if pending_posts:
        for p in pending_posts:
            with st.expander(f"Post ID: {p.id} | Language: {p.language}"):
                st.write("**Content Preview:**")
                st.info(p.content)
                if p.image_url:
                    st.image(p.image_url, caption="Generated AI Image")
                if p.video_url:
                    st.video(p.video_url)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button(f"Approve Post {p.id}", key=f"app_{p.id}"):
                        p.status = "Approved"
                        session.commit()
                        st.success("Post Approved!")
                        st.rerun()
                with col2:
                    if st.button(f"Reject Post {p.id}", key=f"rej_{p.id}"):
                        p.status = "Rejected"
                        session.commit()
                        st.warning("Post Rejected")
                        st.rerun()
    else:
        st.info("No posts pending approval.")

elif mode == "Active Campaigns":
    st.header("ERPNext Campaigns Mirror")
    session = get_session()
    campaigns = session.query(Campaign).all()
    if campaigns:
        st.table([{"Name": c.name, "Objectives": c.objectives, "Status": c.status} for c in campaigns])
    else:
        st.info("No campaigns synced from ERPNext yet.")

elif mode == "Run Crews":
    st.header("Trigger AI Micro-Crews")
    
    tabs = st.tabs(["Master Orchestrator", "Legacy Discovery", "Legacy Content"])
    
    with tabs[0]:
        st.subheader("🚀 Omnichannel Hierarchical Orchestrator")
        st.write("Spawns isolated teams for Facebook, WhatsApp, Telegram, and Forums to run a unified campaign.")
        objective = st.text_area("Campaign Objective", placeholder="e.g., Promote our new Cairo branch furniture collection to real estate groups and wholesale buyers.")
        if st.button("Launch Orchestrator"):
            if not objective:
                st.error("Please provide a campaign objective.")
            else:
                with st.spinner("Master Orchestrator is coordinating platform teams..."):
                    orchestrator = HierarchicalOrchestrator()
                    result = orchestrator.run_omnichannel_campaign(objective)
                    st.success("Orchestration Complete!")
                    st.write(result)

    with tabs[1]:
        st.subheader("Discovery Crew (Single Platform)")
        topic = st.text_input("Topic", value="Real Estate")
        platform = st.selectbox("Platform Focus", ["Facebook Groups", "WhatsApp", "Telegram", "Forums"])
        if st.button("Start Discovery"):
            with st.spinner("Discovery Crew is searching..."):
                crew = DiscoveryCrew()
                result = crew.run(topic, platform)
                st.success("Discovery Complete!")
                st.write(result)
                
    with tabs[2]:
        st.subheader("Content Crew (Single Community)")
        gov = st.text_input("Governorate", value="Alexandria")
        c_url = st.text_input("Target Community URL")
        if st.button("Generate Content"):
            if not c_url:
                st.error("Please provide a target community URL")
            else:
                with st.spinner("Content Crew is drafting..."):
                    crew = ContentCrew()
                    result = crew.run(gov, c_url)
                    st.success("Content Drafted!")
                    st.write(result)

elif mode == "Model Settings":
    st.header("🤖 AI Model Configuration")
    st.write("Assign providers and models to the specialized platform teams.")
    
    config_file = "agent_models.json"
    if os.path.exists(config_file):
        with open(config_file, "r") as f:
            config = json.load(f)
    else:
        config = {}
        
    providers = ["openai", "kimi", "gemini", "anthropic", "mistral", "cohere"]
    
    # Define the new expanded agent list
    agent_categories = {
        "Core Management": ["Orchestrator Manager", "Media Director", "Audience Intelligence"],
        "Facebook Team": ["Facebook Strategist", "Facebook Copywriter"],
        "WhatsApp Team": ["WhatsApp Manager", "WhatsApp Writer"],
        "Telegram Team": ["Telegram Specialist", "Telegram Writer"],
        "Forums Team": ["Forum Researcher", "Forum Writer"]
    }
    
    new_config = {}
    
    for category, agents in agent_categories.items():
        with st.expander(f"⚙️ {category}", expanded=True):
            for agent in agents:
                st.markdown(f"**{agent}**")
                col1, col2 = st.columns(2)
                
                current_prov = config.get(agent, {}).get("provider", "openai")
                current_mod = config.get(agent, {}).get("model", "gpt-4-turbo")
                
                try:
                    prov_idx = providers.index(current_prov)
                except ValueError:
                    prov_idx = 0
                
                with col1:
                    prov = st.selectbox(f"Provider for {agent}", providers, index=prov_idx, key=f"prov_{agent}")
                with col2:
                    mod = st.text_input(f"Model for {agent}", value=current_mod, key=f"mod_{agent}")
                    
                new_config[agent] = {"provider": prov, "model": mod}
    
    if st.button("Save Configuration", type="primary"):
        with open(config_file, "w") as f:
            json.dump(new_config, f, indent=4)
        st.success("Configuration saved! The Hierarchical Orchestrator will use these settings.")
