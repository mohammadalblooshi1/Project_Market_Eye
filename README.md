# 📊 Market Eye – AI-Powered Stock Analysis System

Market Eye is an intelligent web-based stock analysis system that provides:

- 🔍 Data-driven financial forecasting  
- 🧠 Investment recommendations using Gemini LLM  
- 📄 PDF reports for decision-making  
- 👥 Secure login/logout with activity logging  
- ⚙️ Task orchestration powered by CrewAI  

---

## 🗂️ Project Structure

### 📁 Backend Core Modules

| File             | Description                                                                 |
|------------------|-----------------------------------------------------------------------------|
| `crew_tasks.py`  | Contains the main task functions for CrewAI agents: data collection, forecasting, and recommendation. |
| `forecasting.py` | Time-series forecasting using MLPRegressor and performance metrics (MSE, RMSE). |
| `llm.py`         | Gemini-based recommendation generator using structured input.               |
| `pdf_generator.py` | Exports analysis results and recommendations as professional PDFs.        |
| `auth.py`        | Handles user registration, password hashing, login, and activity logging.   |

### 📁 App & UI

| File          | Description                                                                 |
|---------------|-----------------------------------------------------------------------------|
| `app.py`      | Streamlit front-end for login, ticker selection, forecast visualization, LLM output, and PDF export. |
| `db_setup.py` | One-time setup script to initialize `users.db` with tables `users` and `activity_logs`. |

### 📁 Data & Storage

| File                         | Description                                             |
|------------------------------|---------------------------------------------------------|
| `users.db`                   | SQLite database storing user credentials and action logs. |
| `World-Stock-Prices-Dataset.csv` | Real-time stock data for multiple global tickers.     |

---

## ✅ Features

- 🔐 **User Authentication**  
  Register/Login using hashed passwords. Activity logs maintained for every user event.

- 📈 **Stock Forecasting Engine**  
  Forecasts future stock prices using machine learning (MLP). Shows actual vs. predicted prices.

- 🧠 **Gemini LLM Recommendations**  
  Generates personalized investment suggestions (Buy / Hold / Sell) based on analytical metrics.

- 📄 **PDF Report Generation**  
  Includes stock analysis, forecast summary, and AI recommendation.

- 🧠 **CrewAI Integration**  
  Modular task orchestration with agent-based flow: Data → Analytics → AI Advice.

---

## 🚀 How to Run

### 1. Clone the repository


git clone https://github.com/mohammadalblooshi1/Project_Market_Eye.git

cd market-eye

### 2. Setup Python environment

python3.11 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

### 3. Setup Database

python db_setup.py

### 2. Run the app

streamlit run app.py




