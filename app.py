import streamlit as st
import pandas as pd
import time
import hashlib
from datetime import datetime

# --- IBM CARBON THEME CONFIGURATION ---
st.set_page_config(
    page_title="IBM watsonx Governance | Sentinel",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- CUSTOM CSS (THE ENTERPRISE LOOK) ---
st.markdown("""
    <style>
    /* IBM Carbon Dark Theme Overrides */
    .stApp {
        background-color: #161616; /* Carbon Gray 100 */
        color: #f4f4f4;
    }
    
    /* Metrics Cards */
    div[data-testid="stMetric"] {
        background-color: #262626; /* Carbon Gray 90 */
        border: 1px solid #393939;
        padding: 15px;
        border-radius: 0px; /* IBM Square style */
        border-left: 5px solid #0f62fe; /* IBM Blue Accent */
    }
    
    /* Inputs */
    .stTextInput > div > div > input {
        background-color: #262626;
        color: white;
        border: 1px solid #525252;
        border-radius: 0px;
    }
    
    /* Buttons */
    div.stButton > button {
        background-color: #0f62fe;
        color: white;
        border-radius: 0px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    div.stButton > button:hover {
        background-color: #0353e9;
    }

    /* Success/Error Boxes */
    .success-box {
        padding: 1rem;
        background-color: #24a148; /* Support Green */
        color: white;
        margin-bottom: 1rem;
    }
    .error-box {
        padding: 1rem;
        background-color: #da1e28; /* Support Red */
        color: white;
        margin-bottom: 1rem;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'IBM Plex Sans', sans-serif;
        font-weight: 300;
    }
    </style>
""", unsafe_allow_html=True)

# --- BACKEND LOGIC (The "Completeness" Proof) ---
def sentinel_check(text):
    # Simulated Watson NLU Logic
    risk_keywords = ["password", "admin", "secret", "drop table", "ignore instructions"]
    for word in risk_keywords:
        if word in text.lower():
            return False, word
    return True, None

def log_transaction(user_input, status, risk=None):
    if "audit_log" not in st.session_state:
        st.session_state.audit_log = []
    
    entry = {
        "Timestamp": datetime.now().strftime("%H:%M:%S"),
        "Event_ID": hashlib.sha256(user_input.encode()).hexdigest()[:8],
        "Input_Snippet": user_input[:25] + "..." if len(user_input) > 25 else user_input,
        "Risk_Flag": risk if risk else "None",
        "Action": status
    }
    # Prepend to show newest first
    st.session_state.audit_log.insert(0, entry)

# --- UI LAYOUT ---

# 1. TOP HEADER (The "Brand")
col_logo, col_title = st.columns([1, 10])
with col_title:
    st.title("IBM watsonx | Aletheia Sentinel")
    st.caption("Autonomous Governance Layer for Agentic Workflows")

st.markdown("---")

# 2. KPI DASHBOARD (The "Efficiency" Proof)
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
with kpi1:
    st.metric("System Status", "ONLINE", delta="Active", delta_color="normal")
with kpi2:
    st.metric("Governance Policy", "STRICT-V4", delta="Enforced")
with kpi3:
    if "audit_log" not in st.session_state: st.session_state.audit_log = []
    violation_count = len([x for x in st.session_state.audit_log if x["Action"] == "BLOCKED"])
    st.metric("Threats Blocked", f"{violation_count}", delta="Real-time", delta_color="inverse")
with kpi4:
    st.metric("Agent Latency", "12ms", delta="-2ms")

st.markdown("---")

# 3. MAIN WORKSPACE (Split View)
col_agent, col_audit = st.columns([6, 4])

# --- LEFT COLUMN: AGENT INTERFACE ---
with col_agent:
    st.subheader("🤖 Orchestrate Agent Interaction")
    
    # Chat Container
    chat_container = st.container(height=400)
    
    # Initialize Chat
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Aletheia Sentinel active. I am monitoring for policy violations."}]

    # Display History
    with chat_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    # Input Area
    prompt = st.chat_input("Enter command for watsonx Agent...")
    
    if prompt:
        # Show User Input
        st.session_state.messages.append({"role": "user", "content": prompt})
        with chat_container:
            with st.chat_message("user"):
                st.write(prompt)
        
        # --- SENTINEL INTERVENTION ---
        with chat_container:
            with st.status("🛡️ Sentinel is scanning input...", expanded=True) as status:
                time.sleep(1.2) # Dramatic "Processing" Pause
                is_safe, risk = sentinel_check(prompt)
                
                if not is_safe:
                    # BLOCKED PATH
                    status.update(label="🚨 POLICY VIOLATION DETECTED", state="error")
                    error_msg = f"**BLOCKED:** Input contains prohibited content: `{risk}`."
                    st.markdown(f"<div class='error-box'>{error_msg}</div>", unsafe_allow_html=True)
                    
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
                    log_transaction(prompt, "BLOCKED", risk)
                    
                else:
                    # APPROVED PATH
                    status.update(label="✅ GOVERNANCE CHECK PASSED", state="complete")
                    success_msg = "Request authorized. Forwarding to Orchestrate Agent..."
                    st.markdown(f"<div class='success-box'>{success_msg}</div>", unsafe_allow_html=True)
                    
                    # Simulate Agent Reply
                    time.sleep(1)
                    agent_reply = f"I have successfully executed your request: '{prompt}'"
                    st.session_state.messages.append({"role": "assistant", "content": agent_reply})
                    st.markdown(agent_reply)
                    
                    log_transaction(prompt, "APPROVED", None)

# --- RIGHT COLUMN: FORENSICS LEDGER ---
with col_audit:
    st.subheader("🔒 Immutable Audit Ledger")
    st.caption("Live feed from IBM Cloudant (Simulated)")
    
    if st.session_state.audit_log:
        df = pd.DataFrame(st.session_state.audit_log)
        st.dataframe(
            df, 
            hide_index=True, 
            use_container_width=True,
            column_config={
                "Risk_Flag": st.column_config.TextColumn(
                    "Risk Level",
                    help="Detected Policy Violation",
                    validate="^(?!None$).*$", # Highlight if not None
                ),
                "Action": st.column_config.TextColumn(
                    "Decision",
                    width="small"
                )
            }
        )
    else:
        st.info("No events logged. Waiting for agent activity...")
        
    st.markdown("### Architecture")
    st.code("User -> Sentinel(NLU) -> [Gate] -> Agent -> Cloudant", language="bash")