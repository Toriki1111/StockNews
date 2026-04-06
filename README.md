# 📈 Global Multi-Sector Market Tracker

![Python](https://img.shields.io/badge/Python-3.10-blue)
![Automation](https://img.shields.io/badge/Automation-GitHub_Actions-green)
![Trigger](https://img.shields.io/badge/External_Trigger-Cron--job.org-orange)

An automated tool designed to track "The Big Three" market leaders across major global sectors. This project monitors market trends and maintains consistent GitHub contribution activity through automated logging.

## 🚀 Key Features
- **Reliable Automation:** Triggered via `repository_dispatch` using **cron-job.org** to ensure 100% uptime and daily commits.
- **Multi-Sector Monitoring:** Tracks top 3 entities in Defense, Energy, Tech, Finance, and Precious Metals.
- **Real-time Data:** Fetches live market metrics and price fluctuations via the `yfinance` API.
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
- **Infrastructure:** GitHub Actions (CI/CD)
- **External Scheduler:** Cron-job.org (via REST API)

## 📝 Workflow Logic
1. **External Trigger:** Cron-job.org sends a POST request to the GitHub API every morning.
2. **Action Initiation:** The `repository_dispatch` event triggers the `daily_commit.yml` workflow.
3. **Data Fetching:** The Python script queries live market data for all sectors in the watchlist.
4. **Processing:** Data is formatted into Markdown tables with status indicators (🟢/🔴).
5. **Auto-Commit:** The system stages, commits, and pushes the updated log to maintain the repository's activity streak.

---
*Automated Market Intelligence Tool*
