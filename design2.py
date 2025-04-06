import streamlit as st
import yfinance as yf
import pandas as pd
import time

# Page config
st.set_page_config(layout="wide")

from streamlit_autorefresh import st_autorefresh



# -------------------- Auto Refresh Every 60 Seconds --------------------
st_autorefresh(interval=60000, key="refresh")

# Custom CSS for styling
st.markdown("""
<style>
    body {
        background-color: #f0ebf8;
    }
    .main-container {
        display: flex;
        flex-direction: row;
        background: linear-gradient(135deg, #e4dcf5, #f2f0fc);
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
    }
    .left-pane, .center-pane, .right-pane {
        padding: 1.5rem;
        border-radius: 15px;
        height: 75vh;
        overflow-y: auto;
    }
    .left-pane {
        background-color: #ffffffaa;
        width: 20%;
        margin-right: 1rem;
    }
    .center-pane {
        background-color: #f8f5ff;
        width: 55%;
        margin-right: 1rem;
    }
    .right-pane {
        background-color: #ffffffaa;
        width: 25%;
    }
    .title-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 0;
    }
    .title-text {
        font-size: 2rem;
        font-weight: 700;
        color: #4b2e83;
    }
    .chat-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #4b2e83;
        margin-bottom: 0.5rem;
    }
    .stock-box {
        background-color: #f3eaff;
        padding: 0.75rem;
        margin-bottom: 0.5rem;
        border-radius: 10px;
    }
    .stock-symbol {
        font-weight: 600;
        color: #5d3a9b;
    }
</style>
""", unsafe_allow_html=True)

# Title bar
with st.container():
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown('<div class="title-text">💼 Your Financial Assistant</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div style="font-size: 2rem;">👧</div>', unsafe_allow_html=True)  # change to 👦 if gender is boy

# Layout with three sections
st.markdown('<div class="main-container">', unsafe_allow_html=True)

# Left Pane: Navigation or new chat
with st.container():
    st.markdown('<div class="left-pane">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header">📂 Menu</div>', unsafe_allow_html=True)
    if st.button("🆕 New Chat"):
        st.session_state.chat_history = []
    st.write("Other Features Coming Soon...")
    st.markdown('</div>', unsafe_allow_html=True)

# Center Pane: Chat
with st.container():
    st.markdown('<div class="center-pane">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header">🧠 Chat</div>', unsafe_allow_html=True)

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    user_input = st.text_input("Ask me anything about finance or investing:", key="chat_input")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "text": user_input})
        st.session_state.chat_history.append({"role": "assistant", "text": "Processing your question..."})

    for message in st.session_state.chat_history:
        if message["role"] == "user":
            st.markdown(f"🧑‍💬 **You:** {message['text']}")
        else:
            st.markdown(f"🤖 **Assistant:** {message['text']}")

    st.markdown('</div>', unsafe_allow_html=True)

# Right Pane: Live Stock Updates
with st.container():
    st.markdown('<div class="right-pane">', unsafe_allow_html=True)
    st.markdown('<div class="chat-header">📊 Live NIFTY 50 Stocks</div>', unsafe_allow_html=True)

    stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS"]
    for symbol in stocks:
        try:
            data = yf.download(symbol, period="1d", interval="1m")
            if not data.empty:
                price = data["Close"].iloc[-1]
                change = data["Close"].iloc[-1] - data["Open"].iloc[0]
                color = "green" if change >= 0 else "red"
                st.markdown(f"""
                <div class="stock-box">
                    <span class="stock-symbol">{symbol.split('.')[0]}</span><br>
                    ₹{round(price, 2)} <span style='color:{color};'>({round(change, 2)})</span>
                </div>
                """, unsafe_allow_html=True)
        except:
            st.markdown(f"Failed to fetch data for {symbol}")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# Auto-refresh every 60 seconds
st_autorefresh = st.empty()
st_autorefresh.write(f"Last updated: {time.strftime('%H:%M:%S')}")