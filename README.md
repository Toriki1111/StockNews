# 📈 Global Multi-Sector Market Tracker

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Automation](https://img.shields.io/badge/Automation-GitHub_Actions-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)

An automated tool designed to track "The Big Three" market leaders across major global sectors. This project monitors market trends and maintains daily GitHub contribution activity through automated logging.

## 🚀 Key Features
- **Fully Automated:** Powered by GitHub Actions to run on a daily schedule (00:00 UTC).
- **Multi-Sector Monitoring:** Tracks the top 3 entities in Defense, Energy, Tech, Finance, and Precious Metals.
- **Real-time Data:** Fetches live market metrics and price fluctuations via the Yahoo Finance API.
- **Persistence:** Automatically appends detailed reports to `autocommit.txt` with timestamped entries.

## 🏢 Watchlist Overview
| Sector | Market Leaders |
| :--- | :--- |
| **Defense** | Lockheed Martin (LMT), Raytheon (RTX), Northrop Grumman (NOC) |
| **Energy** | ExxonMobil (XOM), Chevron (CVX), ConocoPhillips (COP) |
| **Tech** | Apple (AAPL), Microsoft (MSFT), Alphabet (GOOGL) |
| **Finance** | JPMorgan (JPM), Bank of America (BAC), Goldman Sachs (GS) |
| **Precious Metals** | Gold (GC=F), Silver (SI=F), Barrick Gold (GOLD) |

## 🛠️ Tech Stack
- **Language:** Python 3.10
- **Library:** `yfinance` (Yahoo Finance API), `pandas`
- **Automation:** GitHub Actions (CI/CD)

## 📝 Workflow Logic
1. **Trigger:** GitHub Actions initiates the workflow based on the defined `cron` schedule.
2. **Data Fetching:** The `bot_stock.py` script queries the Yahoo Finance API for current market data.
3. **Processing:** Data is formatted into Markdown tables with visual status indicators (🟢/🔴).
4. **Auto-Commit:** The system stages, commits, and pushes the updated log back to the repository.
