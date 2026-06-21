import streamlit as st
from groq import Groq
import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="Auto Money Assistant", page_icon="💰", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .stApp { background-color: #0f1117; }
    .metric-card { background: linear-gradient(135deg, #1e2130, #252b3b); border: 1px solid #2d3450; border-radius: 16px; padding: 20px; text-align: center; margin-bottom: 10px; }
    .metric-label { font-size: 13px; color: #8b9cc8; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 8px; }
    .metric-value { font-size: 28px; font-weight: 700; color: #ffffff; }
    .metric-sub { font-size: 12px; margin-top: 6px; }
    .green { color: #4ade80; }
    .red { color: #f87171; }
    .amber { color: #fbbf24; }
    .chat-bubble-user { background: #2d3450; border-radius: 16px 16px 4px 16px; padding: 12px 16px; margin: 8px 0; margin-left: 20%; color: #e2e8f0; font-size: 14px; }
    .chat-bubble-ai { background: #1a2035; border: 1px solid #2d3450; border-radius: 16px 16px 16px 4px; padding: 12px 16px; margin: 8px 0; margin-right: 20%; color: #e2e8f0; font-size: 14px; }
    .ai-label { font-size: 11px; color: #4285f4; font-weight: 600; margin-bottom: 6px; }
    .section-header { font-size: 16px; font-weight: 600; color: #c7d2fe; border-bottom: 1px solid #2d3450; padding-bottom: 8px; margin-bottom: 16px; }
    div[data-testid="stSidebar"] { background-color: #0d1020; border-right: 1px solid #2d3450; }
    .stButton > button { background: #4285f4; color: white; border: none; border-radius: 10px; font-weight: 600; width: 100%; }
    .stButton > button:hover { background: #2b6de8; }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def get_sample_data():
    transactions = [
        {"date": "2026-04-18", "name": "Salary Deposit",    "category": "Income",        "amount":  3200.00},
        {"date": "2026-04-17", "name": "Grocery Store",     "category": "Food & Dining", "amount":   -94.50},
        {"date": "2026-04-16", "name": "Electricity Bill",  "category": "Utilities",     "amount":   -68.00},
        {"date": "2026-04-15", "name": "Netflix",           "category": "Subscriptions", "amount":   -15.49},
        {"date": "2026-04-14", "name": "Zomato Order",      "category": "Food & Dining", "amount":   -22.00},
        {"date": "2026-04-13", "name": "Uber Ride",         "category": "Transport",     "amount":   -18.00},
        {"date": "2026-04-12", "name": "Amazon Purchase",   "category": "Shopping",      "amount":   -45.00},
        {"date": "2026-04-11", "name": "Restaurant Dinner", "category": "Food & Dining", "amount":   -60.00},
        {"date": "2026-04-10", "name": "Gym Membership",    "category": "Health",        "amount":   -30.00},
        {"date": "2026-04-09", "name": "Spotify",           "category": "Subscriptions", "amount":   -11.99},
        {"date": "2026-04-08", "name": "Petrol",            "category": "Transport",     "amount":   -40.00},
        {"date": "2026-04-07", "name": "Coffee Shop",       "category": "Food & Dining", "amount":   -12.00},
        {"date": "2026-04-06", "name": "Cloud Storage",     "category": "Subscriptions", "amount":   -28.00},
        {"date": "2026-04-05", "name": "Movie Tickets",     "category": "Entertainment", "amount":   -25.00},
        {"date": "2026-04-04", "name": "Pharmacy",          "category": "Health",        "amount":   -18.50},
        {"date": "2026-04-03", "name": "Internet Bill",     "category": "Utilities",     "amount":   -55.00},
        {"date": "2026-04-02", "name": "Rent Payment",      "category": "Housing",       "amount":  -900.00},
        {"date": "2026-04-01", "name": "Savings Transfer",  "category": "Savings",       "amount":  -340.00},
    ]
    budgets = {
        "Food & Dining": {"budget": 500,  "spent": 188.50},
        "Housing":       {"budget": 900,  "spent": 900.00},
        "Transport":     {"budget": 200,  "spent": 58.00},
        "Subscriptions": {"budget": 60,   "spent": 55.48},
        "Entertainment": {"budget": 150,  "spent": 25.00},
        "Shopping":      {"budget": 100,  "spent": 45.00},
        "Health":        {"budget": 80,   "spent": 48.50},
        "Utilities":     {"budget": 150,  "spent": 123.00},
        "Savings":       {"budget": 500,  "spent": 340.00},
    }
    return transactions, budgets

def build_system_prompt(transactions, budgets, balance, total_spent, total_saved):
    txn_text = "\n".join([
        f"  - {t['date']}: {t['name']} | {t['category']} | {'+' if t['amount'] > 0 else ''}${t['amount']:.2f}"
        for t in transactions
    ])
    budget_lines = []
    for cat, info in budgets.items():
        pct = f"{100 * info['spent'] / info['budget']:.0f}% used"
        status = "OVER" if info['spent'] > info['budget'] else pct
        budget_lines.append(f"  - {cat}: ${info['spent']:.0f} spent / ${info['budget']} budget ({status})")
    budget_text = "\n".join(budget_lines)

    return f"""You are an expert agentic AI personal finance manager called "Auto Money Assistant".
You have full access to the user's financial data for April 2026. Always reference specific numbers.

=== FINANCIAL SNAPSHOT ===
Current Balance: ${balance:,.2f}
Total Spent This Month: ${total_spent:,.2f}
Total Saved This Month: ${total_saved:,.2f}
Monthly Income: $3,200.00

=== BUDGET STATUS ===
{budget_text}

=== RECENT TRANSACTIONS ===
{txn_text}

=== YOUR ROLE ===
- Analyse spending patterns using the real data above
- Give specific, actionable advice with exact dollar amounts
- Identify overspending, savings opportunities, unusual transactions
- Be concise (under 150 words per response), direct, and helpful
- Use bullet points when listing multiple items
- Always be encouraging and constructive
"""

def chat_with_groq(api_key, system_prompt, messages):
    client = Groq(api_key=api_key)
    groq_messages = [{"role": "system", "content": system_prompt}]
    for m in messages:
        groq_messages.append({"role": m["role"], "content": m["content"]})
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=groq_messages,
        max_tokens=1000
    )
    return response.choices[0].message.content

# ─── Session State ────────────────────────────────────────────────────────────
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "api_key" not in st.session_state:
    st.session_state.api_key = os.getenv("GROQ_API_KEY", "")

# ─── Load Data ────────────────────────────────────────────────────────────────
transactions, budgets = get_sample_data()
df = pd.DataFrame(transactions)
df["amount_abs"] = df["amount"].abs()

income      = df[df["amount"] > 0]["amount"].sum()
expenses    = df[df["amount"] < 0]["amount"].abs().sum()
savings     = budgets["Savings"]["spent"]
balance     = 4820.00
total_spent = expenses - savings

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 Auto Money Assistant")
    st.markdown("*Powered by Groq (Free)*")
    st.markdown("---")

    api_key = st.text_input("Groq API Key", type="password", value=st.session_state.api_key, placeholder="gsk_...")
    if api_key:
        st.session_state.api_key = api_key
        st.success("API key saved ✓")

    st.markdown("🔑 Get free key → [console.groq.com](https://console.groq.com)")
    st.markdown("---")
    st.markdown("### Quick Actions")

    for qp in ["Where am I overspending?", "How can I save $500 this month?",
                "Analyse my subscriptions", "Give me a 3-month savings plan",
                "What are my biggest expenses?", "Am I on track with my budget?"]:
        if st.button(qp, key=f"qp_{qp}"):
            st.session_state.pending_prompt = qp

    st.markdown("---")
    st.caption("Built with Python + Streamlit + Groq API.")

# ─── Main ─────────────────────────────────────────────────────────────────────
st.markdown("# 💰 Auto Money Assistant")
st.caption("Your agentic AI personal finance manager — April 2026")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Balance</div><div class="metric-value">${balance:,.0f}</div><div class="metric-sub green">▲ $340 this month</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Spent</div><div class="metric-value">${total_spent:,.0f}</div><div class="metric-sub red">82% of budget</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Saved</div><div class="metric-value">${savings:,.0f}</div><div class="metric-sub amber">Goal: $500/mo</div></div>', unsafe_allow_html=True)
with col4:
    st.markdown(f'<div class="metric-card"><div class="metric-label">Income</div><div class="metric-value">${income:,.0f}</div><div class="metric-sub green">Salary deposit</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "💳 Transactions", "🤖 AI Assistant"])

with tab1:
    left, right = st.columns(2)
    with left:
        st.markdown('<div class="section-header">Budget vs Spending</div>', unsafe_allow_html=True)
        budget_df = pd.DataFrame([
            {"Category": cat, "Budget": info["budget"], "Spent": info["spent"]}
            for cat, info in budgets.items()
        ])
        colors = ["#f87171" if r["Spent"] >= r["Budget"] else "#4285f4" for _, r in budget_df.iterrows()]
        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(x=budget_df["Spent"], y=budget_df["Category"], orientation="h", marker_color=colors, text=[f"${v:.0f}" for v in budget_df["Spent"]], textposition="outside"))
        fig_bar.add_trace(go.Bar(x=budget_df["Budget"], y=budget_df["Category"], orientation="h", marker_color="rgba(255,255,255,0.08)", text=[f"/${v:.0f}" for v in budget_df["Budget"]], textposition="outside"))
        fig_bar.update_layout(barmode="overlay", height=340, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#c7d2fe", margin=dict(l=0,r=60,t=10,b=10), showlegend=False, xaxis=dict(showgrid=False,zeroline=False,showticklabels=False), yaxis=dict(showgrid=False))
        st.plotly_chart(fig_bar, use_container_width=True)

    with right:
        st.markdown('<div class="section-header">Spending by Category</div>', unsafe_allow_html=True)
        expense_df = df[df["amount"] < 0].copy()
        expense_df["amount_abs"] = expense_df["amount"].abs()
        cat_totals = expense_df.groupby("category")["amount_abs"].sum().reset_index()
        fig_pie = px.pie(cat_totals, values="amount_abs", names="category", color_discrete_sequence=px.colors.sequential.Plasma_r, hole=0.5)
        fig_pie.update_layout(height=340, paper_bgcolor="rgba(0,0,0,0)", font_color="#c7d2fe", margin=dict(l=0,r=0,t=10,b=10), legend=dict(font=dict(color="#8b9cc8", size=11)))
        fig_pie.update_traces(textposition="inside", textfont_color="white")
        st.plotly_chart(fig_pie, use_container_width=True)

    st.markdown('<div class="section-header">Daily Spending Trend</div>', unsafe_allow_html=True)
    daily = expense_df.groupby("date")["amount_abs"].sum().reset_index().sort_values("date")
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=daily["date"], y=daily["amount_abs"], fill="tozeroy", fillcolor="rgba(66,133,244,0.15)", line=dict(color="#4285f4", width=2), mode="lines+markers", marker=dict(color="#4285f4", size=6)))
    fig_line.update_layout(height=220, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font_color="#c7d2fe", margin=dict(l=0,r=0,t=10,b=10), xaxis=dict(showgrid=False,color="#8b9cc8"), yaxis=dict(showgrid=True,gridcolor="#1e2130",color="#8b9cc8"), showlegend=False)
    st.plotly_chart(fig_line, use_container_width=True)

with tab2:
    st.markdown('<div class="section-header">All Transactions — April 2026</div>', unsafe_allow_html=True)
    cat_filter = st.selectbox("Filter by category", ["All"] + sorted(df["category"].unique().tolist()))
    filtered = df if cat_filter == "All" else df[df["category"] == cat_filter]
    display_df = filtered.copy()
    display_df["Amount"] = display_df["amount"].apply(lambda x: f"🟢 +${x:.2f}" if x > 0 else f"🔴 -${abs(x):.2f}")
    display_df = display_df.rename(columns={"date": "Date", "name": "Description", "category": "Category"})[["Date", "Description", "Category", "Amount"]]
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Transactions", len(filtered))
    c2.metric("Total Income",   f"${filtered[filtered['amount'] > 0]['amount'].sum():,.2f}")
    c3.metric("Total Expenses", f"${filtered[filtered['amount'] < 0]['amount'].abs().sum():,.2f}")

with tab3:
    st.markdown('<div class="section-header">🤖 Chat with your AI Finance Manager</div>', unsafe_allow_html=True)

    if not st.session_state.api_key:
        st.warning("👈 Add your **Groq API key** in the sidebar. Get one free at https://console.groq.com")
    else:
        for msg in st.session_state.chat_history:
            if msg["role"] == "user":
                st.markdown(f'<div class="chat-bubble-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="chat-bubble-ai"><div class="ai-label">🤖 Auto Money Assistant (Groq)</div>{msg["content"]}</div>', unsafe_allow_html=True)

        pending = st.session_state.pop("pending_prompt", None)
        user_input = st.chat_input("Ask about your finances...")
        prompt = pending or user_input

        if prompt:
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            st.markdown(f'<div class="chat-bubble-user">{prompt}</div>', unsafe_allow_html=True)
            with st.spinner("Analysing your finances..."):
                try:
                    system_prompt = build_system_prompt(transactions, budgets, balance, total_spent, savings)
                    reply = chat_with_groq(st.session_state.api_key, system_prompt, st.session_state.chat_history)
                    st.session_state.chat_history.append({"role": "assistant", "content": reply})
                    st.markdown(f'<div class="chat-bubble-ai"><div class="ai-label">🤖 Auto Money Assistant (Groq)</div>{reply}</div>', unsafe_allow_html=True)
                except Exception as e:
                    err = str(e)
                    if "invalid_api_key" in err.lower() or "api key" in err.lower() or "authentication" in err.lower():
                        st.error("Invalid API key. Please check your Groq API key.")
                    else:
                        st.error(f"Error: {err}")

        if st.session_state.chat_history:
            if st.button("🗑️ Clear Chat"):
                st.session_state.chat_history = []
                st.rerun()