import os
import yfinance as yf
import requests
import datetime

# ---- Secrets from GitHub Actions ----
BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHANNEL_ID = os.environ.get("CHANNEL_ID")

if not BOT_TOKEN or not CHANNEL_ID:
    raise ValueError("Missing BOT_TOKEN or CHANNEL_ID")

# ---- Helper: Trend Calculation ----
def get_trend(symbol, strike_round):
    ticker = yf.Ticker(symbol)
    df = ticker.history(period="3mo", interval="1d")

    df["EMA20"] = df["Close"].ewm(span=20).mean()
    df["EMA50"] = df["Close"].ewm(span=50).mean()

    latest = df.iloc[-1]
    spot = round(latest["Close"], 2)
    ema20 = round(latest["EMA20"], 2)
    ema50 = round(latest["EMA50"], 2)

    if spot > ema20 and ema20 > ema50:
        trend = "BULLISH 📈"
        bias = "CE"
    elif spot < ema20 and ema20 < ema50:
        trend = "BEARISH 📉"
        bias = "PE"
    else:
        trend = "SIDEWAYS ⚖️"
        bias = "BOTH"

    atm = round(spot / strike_round) * strike_round

    return spot, ema20, ema50, trend, bias, atm

# ---- Fetch Trends ----
sensex = get_trend("^BSESN", 100)
nifty = get_trend("^NSEI", 50)

# ---- Static Levels (example placeholders) ----
levels = {
    "CE": {"buy": 320, "sl": 260, "t1": 380, "t2": 450},
    "PE": {"buy": 300, "sl": 360, "t1": 220, "t2": 180},
}

# ---- Build Message Block ----
def build_message(name, data):
    spot, ema20, ema50, trend, bias, atm = data

    header = f"""
📊 {name} DAILY SETUP
🕒 {datetime.datetime.now().strftime("%d %b %Y | %I:%M %p")}
📈 Spot: {spot}
📐 EMA20: {ema20} | EMA50: {ema50}
🧭 Trend: {trend}
"""

    if bias == "CE":
        l = levels["CE"]
        return header + f"""
{name} {atm} CE
BUY ABOVE {l['buy']}
SL {l['sl']}
TGT {l['t1']} / {l['t2']}
"""
    elif bias == "PE":
        l = levels["PE"]
        return header + f"""
{name} {atm} PE
BUY BELOW {l['buy']}
SL {l['sl']}
TGT {l['t1']} / {l['t2']}
"""
    else:
        return header + """
Market is SIDEWAYS ⚖️
Option buying not recommended
"""

# ---- Final Telegram Message ----
message = (
    build_message("SENSEX", sensex)
    + "\n\n"
    + build_message("NIFTY", nifty)
    + """

"""
)

# ---- Send to Telegram ----
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
payload = {"chat_id": CHANNEL_ID, "text": message}
requests.post(url, data=payload)
