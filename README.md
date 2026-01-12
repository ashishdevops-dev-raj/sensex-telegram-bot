# 📊 SENSEX & NIFTY Auto Telegram Trading Bot

An automated **Python + GitHub Actions** bot that posts **daily SENSEX & NIFTY option setups** (CE / PE) to a Telegram channel based on **EMA20 / EMA50 trend logic**.

> ⚠️ **Educational purpose only. Not financial advice.**

---

## 🚀 Features

* ✅ Live **SENSEX & NIFTY 50** data (Yahoo Finance)
* ✅ Automatic **EMA20 / EMA50** trend detection
* ✅ Auto ATM strike calculation
* ✅ CE / PE enabled based on daily trend
* ✅ Sideways market filter
* ✅ Telegram channel auto-post
* ✅ Fully serverless (GitHub Actions cron)

---

## 🧠 Strategy Logic

### Trend Detection

| Condition            | Trend       | Option Bias |
| -------------------- | ----------- | ----------- |
| Spot > EMA20 > EMA50 | Bullish 📈  | CE only     |
| Spot < EMA20 < EMA50 | Bearish 📉  | PE only     |
| Otherwise            | Sideways ⚖️ | No trade    |

### Strike Calculation

* **SENSEX** → nearest 100
* **NIFTY** → nearest 50

---

## 📦 Project Structure

```
sensex-telegram-bot/
├── sensex_auto_ce_pe.py
├── requirements.txt
├── .github/
│   └── workflows/
│       └── sensex.yml
└── README.md
```

---

## 🛠️ Step 1: Clone Repository

```bash
git clone https://github.com/your-username/sensex-telegram-bot.git
cd sensex-telegram-bot
```

---

## 🐍 Step 2: Python Script

Main file: `sensex_auto_ce_pe.py`

This script:

* Fetches daily SENSEX & NIFTY data
* Calculates EMA20 & EMA50
* Determines CE / PE bias
* Sends formatted message to Telegram

---

## 📄 Step 3: requirements.txt

Create `requirements.txt`

```
yfinance
requests
```

---

## 📢 Step 4: Create Telegram Channel

1. Open Telegram → **Create New Channel**
2. Choose **Public or Private**
3. Add a clear **Disclaimer** (VERY IMPORTANT)

### 📌 Example Disclaimer

```
Educational purposes only.
No buy/sell recommendation.
Markets involve risk.
```

Save your **Channel ID**:

* Public channel → `@yourchannelname`
* Private channel → numeric ID like `-1001234567890`

---

## 🤖 Step 5: Create Telegram Bot

1. Open Telegram → search **@BotFather**

2. Run `/start`

3. Run `/newbot`

4. Set bot name & username

5. Copy the **BOT TOKEN**

6. Add the bot as **Admin** in your Telegram channel

7. Open Telegram → search **@BotFather**

8. Run `/start`

9. Run `/newbot`

10. Copy the **BOT TOKEN**

---

## 📢 Step 5: Create Telegram Channel

1. Create a Telegram Channel
2. Add your bot as **Admin**
3. Copy Channel ID

   * Public: `@channelname`
   * Private: numeric ID (e.g. `-1001234567890`)

---

## ⚙️ Step 6: Automation (Hourly Posting)

You have **3 good automation options**:

### ✅ Option 1: GitHub Actions (Recommended)

* Free
* Reliable
* No server needed

### ✅ Option 2: VPS + Cron Job

* Use AWS / DigitalOcean / Oracle Free Tier
* Best for high-frequency posting

### ✅ Option 3: Railway / Render Scheduler

* Easy UI
* Limited free tier

👉 This project uses **GitHub Actions**.

---

## 🔐 Step 7: Add GitHub Secrets

Go to:

**GitHub Repo → Settings → Secrets → Actions**

Add:

| Name         | Value               |
| ------------ | ------------------- |
| `BOT_TOKEN`  | Telegram Bot Token  |
| `CHANNEL_ID` | Telegram Channel ID |

---

## ⚙️ Step 7: GitHub Actions Workflow

Create file:

```
.github/workflows/sensex.yml
```

```yaml
name: SENSEX NIFTY Telegram Bot

on:
  schedule:
    - cron: "30 13 * * 1-5"   # 7:00 PM IST
  workflow_dispatch:

jobs:
  run-bot:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repo
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'

      - name: Install dependencies
        run: pip install -r requirements.txt

      - name: Run bot
        env:
          BOT_TOKEN: ${{ secrets.BOT_TOKEN }}
          CHANNEL_ID: ${{ secrets.CHANNEL_ID }}
        run: python sensex_auto_ce_pe.py
```

---

## ⏰ Cron Timing (IST)

| Cron            | Time (IST) |
| --------------- | ---------- |
| `30 13 * * 1-5` | 7:00 PM    |
| `0 4 * * 1-5`   | 9:30 AM    |

> GitHub uses **UTC time**

---

## 📩 Sample Telegram Output

```
📊 SENSEX DAILY SETUP
Spot: 83,878
EMA20: 84,784 | EMA50: 84,815
Trend: BEARISH 📉

SENSEX 83900 PE
BUY BELOW 300
SL 360
TGT 220 / 180

📊 NIFTY DAILY SETUP
Spot: 21,820
EMA20: 22,050 | EMA50: 22,180
Trend: SIDEWAYS ⚖️

Market is SIDEWAYS
Option buying not recommended
```

---

## 🧪 Manual Test (Optional)

```bash
export BOT_TOKEN=your_token
export CHANNEL_ID=your_channel
python sensex_auto_ce_pe.py
```

---

## 🚀 Future Enhancements

* ATR based SL / Target
* BankNifty & FinNifty
* Market hours filter
* Holiday detection
* Trade log CSV
* Multi-timeframe trend

---

## 📚 Disclaimer

This project is for **learning & automation practice only**.
The author is **not responsible** for financial losses.

---

## ⭐ Support

If this helped you:

* ⭐ Star the repository
* 🍴 Fork it
* 🧠 Modify & learn

Happy Trading & Coding 🚀
