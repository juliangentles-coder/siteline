# Coinbase 1h Momentum Alerts → Telegram

Scans every online USD/USDC Coinbase product once an hour and pings your
Telegram when a coin gains >7% in an hour on 2× volume (with a $250k liquidity gate).
Runs free on GitHub Actions. No server, no Zapier.

---

## Step 1 — Make your Telegram bot (3 min)
1. In Telegram, open a chat with **@BotFather**.
2. Send `/newbot`, follow prompts, pick a name + username.
3. BotFather replies with a **bot token** like `8123456789:AAH...`. Copy it.
4. Open a chat with your new bot and send it any message (e.g. "hi").
   (A bot can't message you until you message it first.)

## Step 2 — Get your chat ID (1 min)
1. In Telegram, open a chat with **@userinfobot**.
2. It replies with your numeric **Id** (e.g. `645301122`). Copy it.

## Step 3 — Put the code on GitHub (5 min)
1. Create a free account at github.com if you don't have one.
2. Click **New repository** → name it `coinbase-alert` → **Private** → Create.
3. Click **uploading an existing file** and drag in all 3 files from this folder,
   keeping the `.github/workflows/` folder structure intact. Commit.

## Step 4 — Add your secrets (2 min)
In the repo: **Settings → Secrets and variables → Actions → New repository secret.**
Add two:
- Name `TELEGRAM_BOT_TOKEN`  → value = the token from Step 1
- Name `TELEGRAM_CHAT_ID`    → value = the id from Step 2

## Step 5 — Turn it on & test
1. Go to the **Actions** tab → enable workflows if prompted.
2. Click **coinbase-1h-alert** → **Run workflow** to fire it once manually.
3. If any coin currently qualifies you'll get a Telegram ping. If not, that's
   normal — it'll fire automatically at the top of each hour when something hits.

---

## Tuning (edit the top of crypto_alert.py)
- `PCT_THRESHOLD = 7.0`   → minimum 1h gain
- `VOL_MULTIPLE  = 2.0`   → volume spike vs trailing hourly average
- `USD_VOL_FLOOR = 250000`→ liquidity gate; raise to cut more noise

## Notes
- Times are UTC. "Top of the hour" runs may be delayed a few minutes when
  GitHub is busy — fine for this use.
- GitHub disables scheduled workflows after 60 days of zero repo activity;
  just push any small commit to keep it alive.
- A handful of Coinbase products may not be tradable on a Canadian retail
  account. If you ever get a coin you can't trade in-app, ignore it (or add
  it to a skip-list). This is an alert, not trading advice.
