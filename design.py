import streamlit as st


# -------------------- Page Config --------------------
st.set_page_config(page_title="Your Financial Assistant", layout="wide")
import yfinance as yf
from streamlit_extras.let_it_rain import rain
from streamlit_autorefresh import st_autorefresh



# -------------------- Auto Refresh Every 60 Seconds --------------------
st_autorefresh(interval=60000, key="refresh")



# -------------------- Custom CSS --------------------
st.markdown("""
    <style>
        .title-bar {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 1rem 2rem;
            background-color: #f0f2f6;
            border-bottom: 1px solid #ccc;
        }

        .left-title {
            font-size: 1.5rem;
            font-weight: bold;
        }

        .new-chat-btn {
            background-color: #4CAF50;
            color: white;
            padding: 0.4rem 1rem;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            margin-left: 1rem;
        }

        .user-icon {
            font-size: 2rem;
            margin-right: 1rem;
        }

        .stock-box {
            font-size: 0.95rem;
            background-color: #ffffff;
            padding: 0.5rem;
            margin-bottom: 0.4rem;
            border-radius: 8px;
            box-shadow: 0 1px 2px rgba(0,0,0,0.1);
        }

        .stock-section {
            padding: 1rem;
            background-color: #f9f9f9;
            height: 100%;
            overflow-y: auto;
        }

        .main-area {
            padding: 2rem;
        }

    </style>
""", unsafe_allow_html=True)

# -------------------- Top Bar --------------------
with st.container():
    st.markdown('<div class="title-bar">', unsafe_allow_html=True)

    col1, col2 = st.columns([5, 1])

    with col1:
        st.markdown('<span class="left-title">💼 Your Financial Assistant</span>', unsafe_allow_html=True)
        if st.button("🆕 New Chat", use_container_width=False):
            st.experimental_rerun()

    with col2:
        gender = st.radio("You are:", ["Boy", "Girl"], horizontal=True, label_visibility="collapsed")
        icon = "👦" if gender == "Boy" else "👧"
        st.markdown(f'<span class="user-icon">{icon}</span>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Layout Columns --------------------
left_col, right_col = st.columns([3, 1])

# -------------------- Left: Main Chat Area --------------------
with left_col:
    st.markdown('<div class="main-area">', unsafe_allow_html=True)

    user_name = st.text_input("👤 What’s your name?")
    if user_name:
        st.markdown(f"### 👋 Hello {user_name}, how may I help you today?")

    st.markdown('</div>', unsafe_allow_html=True)

# -------------------- Right: Live Stock Updates --------------------
with right_col:
    st.markdown("### 📈 Nifty 50 Live Updates")

    nifty50_tickers = {
        "RELIANCE": "RELIANCE.NS",
        "TCS": "TCS.NS",
        "HDFCBANK": "HDFCBANK.NS",
        "INFY": "INFY.NS",
        "ICICIBANK": "ICICIBANK.NS"
    }

    for company, ticker in nifty50_tickers.items():
        try:
            stock_data = yf.download(ticker, period="2d", interval="1d", progress=False)
            if len(stock_data) >= 2:
                prev_price = stock_data["Close"].iloc[-2]
                current_price = stock_data["Close"].iloc[-1]
                change = current_price - prev_price
                pct_change = (change / prev_price) * 100

                if change > 0:
                    arrow = "🔼"
                    color = "green"
                elif change < 0:
                    arrow = "🔽"
                    color = "red"
                else:
                    arrow = "⏸️"
                    color = "gray"

                st.markdown(
                    f"<div class='stock-box'><strong>{company}</strong>: "
                    f"<span style='color:{color};'>₹{current_price:.2f} {arrow} "
                    f"({change:+.2f}, {pct_change:+.2f}%)</span></div>",
                    unsafe_allow_html=True
                )
            else:
                st.write(f"{company}: Data not available")
        except Exception as e:
            st.write(f"{company}: Error fetching data")
