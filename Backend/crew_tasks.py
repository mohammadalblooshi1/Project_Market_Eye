# crew_tasks.py

# Each tool is a callable class with a .run() method, compatible with CrewAI structure

from forecasting import load_and_prepare_data, compute_analytics, forecast_with_mlp
from llm import generate_recommendation


# Tool 1 – Data Collector
class CollectStockDataTool:
    name = "Data Collector"
    description = "Loads and cleans stock data from a CSV file"

    def run(self):
        file_path = "World-Stock-Prices-Dataset.csv"
        df = load_and_prepare_data(file_path)
        return df


# Tool 2 – Data Processor
class ProcessStockDataTool:
    name = "Data Processor"
    description = "Processes stock data, forecasts prices, and computes analytics"

    def run(self):
        file_path = "World-Stock-Prices-Dataset.csv"
        df = load_and_prepare_data(file_path)
        analytics = compute_analytics(df)

        ticker = df['Ticker'].unique()[0]
        forecast_df, mse, rmse = forecast_with_mlp(df, ticker)

        return {
            "ticker": ticker,
            "analytics": analytics,
            "forecast_df": forecast_df,
            "mse": mse,
            "rmse": rmse
        }


# Tool 3 – LLM Recommendation Generator
class LLMRecommendationTool:
    name = "LLM Recommendation Generator"
    description = "Generates Buy/Hold/Sell advice using Gemini LLM"

    def run(self):
        # Example input; ideally should come from user or Agent 2
        ticker = "AAPL"
        company = "Apple Inc."
        forecast_price = 187.20
        growth = 34.75
        rmse = 3.41
        sector = "Technology"

        return generate_recommendation(ticker, company, forecast_price, growth, rmse, sector)
