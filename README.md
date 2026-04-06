# 📈 Daily Stock Activity Bot

[![Daily Stock Bot](https://github.com/Toriki1111/autocommit/actions/workflows/daily_commit.yml/badge.svg)](https://github.com/Toriki1111/autocommit/actions/workflows/daily_commit.yml)

## 📖 Overview
This is an automated bot designed to maintain GitHub contribution activity while providing daily logs of specific stock tickers. It leverages **GitHub Actions** to execute a Python script that fetches and records updates every day.

## 🚀 Features
- **Automated Commits:** Keeps the contribution graph active (Green Grass) 365 days a year.
- **Stock Tracking:** Monitors key energy sector stocks in the Vietnamese market, including:
  - **BSR** (Binh Son Refining and Petrochemical)
  - **PVT** (PetroVietnam Transportation)
  - **PVC** (PetroVietnam Chemical and Services)
- **Serverless Execution:** Runs entirely on GitHub Actions infrastructure (no local hosting required).

## 🛠️ Technical Stack
- **Language:** Python 3.x
- **Automation:** GitHub Actions (YAML Workflows)
- **Version Control:** Git

## 📂 Project Structure
- `.github/workflows/daily_commit.yml`: The automation engine that triggers the bot daily.
- `bot_stock.py`: Python script to generate daily stock activity logs.
- `autocommit.txt`: The destination file where daily logs are appended.

## ⚙️ How it Works
1. The workflow is triggered automatically every day at **30:00 UTC** (10:00 AM ICT).
2. The Python script runs and generates a summary for the tracked stock symbols.
3. GitHub Actions commits the changes to the repository using a dedicated `GITHUB_TOKEN`.
4. The contribution activity is updated instantly on the user profile.

---
*Note: This project is part of my exploration into CI/CD workflows and automated data logging.*
