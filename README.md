📊 Market Eye – AI-Powered Stock Analysis System

Market Eye is an intelligent web-based stock analysis system that provides:

🔍 Data-driven financial forecasting

🧠 Investment recommendations using Gemini LLM

📄 PDF reports for decision-making

👥 Secure login/logout with activity logging

⚙️ Task orchestration powered by CrewAI

🗂️ Project Structure


📁 Backend Core Modules

File	Description
crew_tasks.py	

Contains the main task functions for CrewAI agents: data collection, forecasting, and recommendation.

forecasting.py	

Time-series forecasting using MLPRegressor and performance metrics (MSE, RMSE).


llm.py	

Gemini-based recommendation generator using structured input.


pdf_generator.py	

Exports analysis results and recommendations as professional PDFs.


auth.py	

Handles user registration, password hashing, login, and activity logging.


📁 App & UI

File	Description
app.py	
Streamlit front-end for login, ticker selection, forecast visualization, LLM output, and PDF export.
db_setup.py	One-time setup script to initialize users.db with tables users and activity_logs.


📁 Data & Storage

File	Description
users.db	SQLite database storing user credentials and action logs.
World-Stock-Prices-Dataset.csv	Real-time stock data for multiple global tickers.


✅ Features

🔐 User Authentication
Register/Login using hashed passwords. Activity logs maintained for every user event.

📈 Stock Forecasting Engine
Forecasts future stock prices using machine learning (MLP). Shows actual vs. predicted prices.

🧠 Gemini LLM Recommendations
Generates personalized investment suggestions (Buy / Hold / Sell) based on analytical metrics.

📄 PDF Report Generation
Includes stock analysis, forecast summary, and AI recommendation.

🧠 CrewAI Integration
Modular task orchestration with agent-based flow: Data → Analytics → AI Advice.

🚀 How to Run
1. Clone the repository

git clone https://github.com/your-username/market-eye.git
cd market-eye
2. Set up Python environment

python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
3. Set up database

python db_setup.py
4. Run the app

streamlit run app.py
5. Run agent-based CLI (optional)

python crew_runner.py
📦 Requirements
All dependencies are included in requirements.txt, including:

streamlit
fpdf
scikit-learn
pandas
google-generativeai
crewai
langchain
sqlite3
📌 Notes
You must add your Google Gemini API Key in llm.py:
