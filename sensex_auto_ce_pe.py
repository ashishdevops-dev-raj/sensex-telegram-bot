import os
import yfinance as yf
import requests
import datetime

# ---- Read secrets from GitHub Actions ----
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

# ---- Safety check ----
if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError("Missing BOT_TOKEN or CHANNEL_ID in environment variables")

# ---- Fetch daily Sensex data ----
sensex = yf.Ticker("^BSESN")
df = sensex.history(period="3mo", interval="1d")

# ---- EMA calculation ----
df["EMA20"] = df["Close"].ewm(span=20).mean()
df["EMA50"] = df["Close"].ewm(span=50).mean()

latest = df.iloc[-1]
spot = round(latest["Close"], 2)
ema20 = round(latest["EMA20"], 2)
ema50 = round(latest["EMA50"], 2)

# ---- Determine Daily Trend ----
if spot > ema20 and ema20 > ema50:
    trend = "BULLISH 📈"
    bias = "CE"
elif spot < ema20 and ema20 < ema50:
    trend = "BEARISH 📉"
    bias = "PE"
else:
    trend = "SIDEWAYS ⚖️"
    bias = "BOTH"

# ---- ATM Strike Calculation ----
atm_strike = round(spot / 100) * 100

# ---- Option Levels (Example / Placeholder) ----
ce_buy = 320
ce_sl = 260
ce_tgt1 = 380
ce_tgt2 = 450

pe_buy = 300
pe_sl = 360
pe_tgt1 = 220
pe_tgt2 = 180

# ---- Generate Message Based on Trend ----
if bias == "CE":
    message = f"""
📊 SENSEX {atm_strike} CE SETUP

🕒 {datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")}
📈 Spot: {spot}
📐 EMA20: {ema20} | EMA50: {ema50}
🧭 Trend: {trend}

BUY ABOVE {ce_buy}
SL {ce_sl}
TGT {ce_tgt1} / {ce_tgt2}

"""
elif bias == "PE":
    message = f"""
📊 SENSEX {atm_strike} PE SETUP

🕒 {datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")}
📈 Spot: {spot}
📐 EMA20: {ema20} | EMA50: {ema50}
🧭 Trend: {trend}

BUY BELOW {pe_buy}
SL {pe_sl}
TGT {pe_tgt1} / {pe_tgt2}

"""
else:  # Sideways
    message = f"""
📊 SENSEX {atm_strike} SETUP

🕒 {datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")}
📈 Spot: {spot}
📐 EMA20: {ema20} | EMA50: {ema50}
🧭 Trend: {trend}

Market is sideways ⚖️
Option trading not recommended

"""

# ---- Send to Telegram ----
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {
    "chat_id": CHANNEL_ID,
    "text": message
}
requests.post(url, data=payload)
