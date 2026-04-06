# 📈 Daily Stock Auto-Commit Bot

![Market](https://img.shields.io/badge/Market-US_Oil-orange)
![Python](https://img.shields.io/badge/Python-3.10-blue)
![Automation](https://img.shields.io/badge/Automation-GitHub_Actions-green)

An automated tool that tracks major US Oil & Gas stocks and performs daily commits to maintain GitHub contribution activity.

## 🚀 Features
- **Fully Automated:** Powered by GitHub Actions to run every day at 07:00 AM (Vietnam Time).
- **Real-time Data:** Fetches live market indices for **ExxonMobil (XOM)**, **Chevron (CVX)**, and **ConocoPhillips (COP)** via Yahoo Finance.
- **Persistence:** Maintains a historical log of price fluctuations in `autocommit.txt`.

## 🛠️ Tech Stack
- **Language:** Python 3.10
- **Libraries:** `yfinance`, `pandas`, `requests`
- **Automation:** GitHub Actions (Cronjob)

## 📊 Watchlist
| Ticker | Company Name | Exchange |
| :--- | :--- | :--- |
| **XOM** | Exxon Mobil Corporation | NYSE |
| **CVX** | Chevron Corporation | NYSE |
| **COP** | ConocoPhillips | NYSE |

## 📝 How It Works
1. **Trigger:** GitHub Actions starts the workflow based on the defined `cron` schedule.
2. **Fetch:** The `bot_stock.py` script requests data from the Yahoo Finance API.
3. **Log:** Data is processed and appended to `autocommit.txt`.
4. **Commit:** The bot automatically stages, commits, and pushes the changes back to the repository.

---
