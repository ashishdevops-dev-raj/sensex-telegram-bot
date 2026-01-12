import os
import yfinance as yf
import requests
import datetime

# ======================================================
# 🔐 Environment Variables
# ======================================================
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError("BOT_TOKEN or CHANNEL_ID missing")

# ======================================================
# 📊 Fetch index trend safely (no crash)
# ======================================================
def get_index_trend(symbol, strike_step):
    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="4mo", interval="1d")

        if df.empty or len(df) < 50:
            return {"error": "No data available"}

        df["EMA20"] = df["Close"].ewm(span=20).mean()
        df["EMA50"] = df["Close"].ewm(span=50).mean()

        latest = df.iloc[-1]
        spot = round(float(latest["Close"]), 2)
        ema20 = round(float(latest["EMA20"]), 2)
        ema50 = round(float(latest["EMA50"]), 2)

        if spot > ema20 and ema20 > ema50:
            trend = "BULLISH 📈"
            bias = "CE"
        elif spot < ema20 and ema20 < ema50:
            trend = "BEARISH 📉"
            bias = "PE"
        else:
            trend = "SIDEWAYS ⚖️"
            bias = "NONE"

        atm = round(spot / strike_step) * strike_step

        return {
            "spot": spot,
            "ema20": ema20,
            "ema50": ema50,
            "trend": trend,
            "bias": bias,
            "atm": atm
        }

    except Exception as e:
        return {"error": str(e)}

# ======================================================
# 📈 Fetch SENSEX & NIFTY
# ======================================================
sensex = get_index_trend("^BSESN", 100)
nifty  = get_index_trend("^NSEI", 50)

# ======================================================
# 🎯 Option Levels (static placeholders)
# ======================================================
CE = {"buy": 320, "sl": 260, "t1": 380, "t2": 450}
PE = {"buy": 300, "sl": 360, "t1": 220, "t2": 180}

# ======================================================
# 🧩 Build Telegram message block
# ======================================================
def build_block(name, data):
    if "error" in data:
        return f"""
📊 {name} DAILY SETUP
❌ Data unavailable
Yahoo Finance issue
"""

    header = f"""
📊 {name} DAILY SETUP
🕒 {datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")}
📈 Spot: {data['spot']}
📐 EMA20: {data['ema20']} | EMA50: {data['ema50']}
🧭 Trend: {data['trend']}
"""

    if data["bias"] == "CE":
        return header + f"""
{name} {data['atm']} CE
BUY ABOVE {CE['buy']}
SL {CE['sl']}
TGT {CE['t1']} / {CE['t2']}
"""
    elif data["bias"] == "PE":
        return header + f"""
{name} {data['atm']} PE
BUY BELOW {PE['buy']}
SL {PE['sl']}
TGT {PE['t1']} / {PE['t2']}
"""
    else:
        return header + """
Market is SIDEWAYS ⚖️
Option buying not recommended
"""

# ======================================================
# 📩 Final Message
# ======================================================
message = (
    build_block("SENSEX", sensex)
    + "\n\n"
    + build_block("NIFTY", nifty)
    + """

⚠️ Educational purpose only
Not a buy/sell recommendation
"""
)

# ======================================================
# 🚀 Send to Telegram
# ======================================================
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHANNEL_ID,
    "text": message
}

requests.post(url, data=payload)
