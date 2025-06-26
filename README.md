# Autonomous Portfolio Pilot

A lightweight, containerized proof-of-concept that:

1. Loads a user portfolio from `portfolio.json`
2. Fetches live and historical prices via Yahoo Finance (`yfinance`)
3. Runs a mean–variance portfolio rebalance
4. Generates a dry-run list of BUY/SELL trades
5. Calls OpenAI to explain the rebalance in two sentences

This project demonstrates an end-to-end agentic AI loop (Perceive → Reason → Act) in a portable Docker environment.

---

## 🚀 Features

- **Data Ingestion**: Reads holdings from `portfolio.json` and price data with `yfinance`.
- **Optimization**: Mean–variance solver (SciPy) to compute target allocations under a risk coefficient.
- **Action Planning**: Prints BUY/SELL trades for a dry run (no real orders executed).
- **LLM Explanation**: Uses OpenAI’s Chat API to generate a concise rationale for the rebalance.
- **Containerization**: Fully self-contained in Docker for reproducible demos.
- **Run Script**: A convenience PowerShell script (`run.ps1`) automates build and run steps.

---

## 🛠️ Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop) (Linux-container mode)
- PowerShell (Windows) or a Unix shell (macOS/Linux)
- An OpenAI API key (for LLM explanations)

---

## ⚙️ Project Setup

1. **Clone the repository**:

   ```bash
   git clone https://github.com/<your-username>/robo-advisor-mvp.git
   cd robo-advisor-mvp
   ```

2. **Create your environment file**:
   
   In the project root, create a file named `.env` and add:

   ```dotenv
   OPENAI_API_KEY=sk-your-openai-key
   ```

   Have already provided a .env file for you to edit.

3. **Customize your portfolio**:

   Edit `portfolio.json` to list your tickers and share counts. Example:

   ```json
   {
     "AAPL": 20,
     "MSFT": 15,
     "GOOGL": 10,
     "AMZN": 5,
     "TSLA": 8,
     "NVDA": 12,
     "JPM": 25,
     "V": 18,
     "JNJ": 14,
     "DIS": 10
   }
   ```

---

## 📦 Installation & Dependencies

All code runs inside a Docker container; no local Python installation is required. Key dependencies:

- **Python libraries**: `pandas`, `numpy`, `scipy`, `yfinance`, `python-dotenv`, `openai`
- **Docker tools**: Docker Engine and CLI

---

## 🚀 Usage

### A. Quick Start (PowerShell run script)

Run the provided `run.ps1` to build the image, mount your local files, and execute the script:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\\run.ps1
```

This will:

- Rebuild the Docker image (picks up any portfolio changes)
- Run the container with your OpenAI key
- Display price fetch logs, proposed trades, and the LLM explanation

### B. Manual Docker Commands

1. **Build the Docker image**:

   ```bash
   docker build -t robo-advisor-mvp .
   ```

2. **Run the container**:

   ```bash
   # Option 1: use your .env file
   docker run --rm --env-file .env -v "${PWD}:/app" -w /app robo-advisor-mvp

   # Option 2: inject the key directly (PowerShell)
   docker run --rm -e "OPENAI_API_KEY=$Env:OPENAI_API_KEY" -v "${PWD}:/app" -w /app robo-advisor-mvp
   ```

Mounting the current directory (`-v "${PWD}:/app"`) ensures your updated `portfolio.json` is used without rebuilding.

---

## 📈 How It Works

1. **Perceive**: Load `portfolio.json` and fetch price data (live + 30-day history).
2. **Reason**: Compute expected returns and covariance; solve mean–variance optimization.
3. **Plan & Act**: Print a dry-run list of trades and call OpenAI for a natural-language explanation.
4. **Containerization**: All steps run inside a Docker container for consistency.

---

## 🛣️ Next Steps

- Integrate with a sandbox broker API (e.g., Alpaca) for real dry-runs
- Expose the logic as a REST API (FastAPI) and build a React dashboard
- Publish the Docker image to Docker Hub for easy sharing

---

## 📄 License

This project is released under the MIT License. See `LICENSE` for details.

---

*Feel free to fork, open issues, and submit pull requests!*

