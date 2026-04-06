# 📈 Automatic US Market Stock

![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automation-2088FF?logo=github-actions&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.10-3776AB?logo=python&logoColor=white)
![Market Data](https://img.shields.io/badge/Data-Yahoo_Finance-7B0099?logo=yahoo&logoColor=white)
![Status](https://img.shields.io/badge/Status-Cloud_Native-success)
![Cron-Job.org](https://img.shields.io/badge/Cron--Job.org-Trigger-orange?logo=clockify&logoColor=white)

**Automatic US Market Stock** is a professional-grade automated data pipeline. It monitors, processes, and archives global financial indicators (US Equities, Energy, and Precious Metals) 24/7 without requiring a dedicated server.

---

## 🚀 Key Features

* **Autonomous Operation:** Fully managed via GitHub Actions and triggered by Cron-job.org for 100% uptime.
* **Data Archiving & Logging:** Automatically maintains `autocommit.txt`, a self-rotating ledger of the last 1,000 market updates.
* **ICT Timezone (GMT+7):** Synchronized with Vietnam Standard Time for accurate local reporting.
* **GitHub Activity Boost:** Generates daily automated commits ("Green Grass") to showcase active repository maintenance.

---

## 💡 Flexible Output Options

This system is designed to be versatile. Users can choose how they want to receive or store their data:

1.  **Logging Mode (Default):** The system fetches data and saves it directly to `autocommit.txt` in the repository. Perfect for building a historical dataset.
2.  **Notification Mode (Optional):** Integrate with **Discord Webhooks** to receive real-time visual reports on your server. 
    * *Note: If you don't want Discord notifications, simply do not add the `DISCORD_WEBHOOK_URL` secret, and the system will continue to log data silently.*

---

## 📊 Monitored Assets

The pipeline tracks strategic tickers for a global market overview:
* **Tech:** AAPL, MSFT, GOOGL.
* **Energy:** XOM, CVX, COP.
* **Defense:** LMT, RTX, NOC.
* **Finance:** JPM, BAC, GS.
* **Safe Havens(Gold,Silver,...):** Gold (GC=F), Silver (SI=F).
(U can modify code of this part if want to add somthing )
---

## 🛠️ Technical Architecture

| Layer | Technology |
| :--- | :--- |
| **Language** | Python 3.10 |
| **API** | Yahoo Finance (`yfinance`) |
| **Orchestration** | GitHub Actions (CI/CD) |
| **Trigger** | Repository Dispatch (via Cron-job.org) |
| **Storage** | Flat-file Logging (`autocommit.txt`) |

---

## ⚙️ Quick Setup

1.  **Fork** this repository.
2.  **Enable Actions**: Go to the **Actions** tab and enable workflows.
3.  **Permissions**: Go to **Settings > Actions > General** and select **"Read and write permissions"**.
4.  **(Optional) Discord**: Add your webhook URL to GitHub Secrets as `DISCORD_WEBHOOK_URL`.
5.  **Trigger**: Link your repository dispatch endpoint with Cron-job.org.

---

## 🛡️ License
Distributed under the MIT License:
MIT License

Copyright (c) 2026 Phu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
