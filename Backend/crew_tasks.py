# crew_tasks.py

# Each tool is a callable class with a .run() method, compatible with CrewAI structure

from Backend.forecasting import load_and_prepare_data, compute_analytics, forecast_with_mlp, forecast_january_with_mlp
from Backend.llm import generate_recommendation


# Tool 1 – Data Collector
class CollectStockDataTool:
    name = "Data Collector"
    description = "Loads and cleans stock data from a CSV file"

    def run(self):
        file_path = "World-Stock-Prices-Dataset.csv"
        df = load_and_prepare_data(file_path)
        analytics = compute_analytics(df)
        return analytics

# Tool 2 – Data Processor
class ProcessStockDataTool:
    name = "Data Processor"
    description = "Processes stock data, forecasts prices, and computes analytics"

    def run(self, selected_ticker):
        file_path = "World-Stock-Prices-Dataset.csv"
        df = load_and_prepare_data(file_path)
        analytics = compute_analytics(df)

        ticker = selected_ticker
        forecast_df, mse, rmse = forecast_january_with_mlp(df, ticker)

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

    def run(self,ticker, company, forecast_price, growth, rmse, sector):
        
        return generate_recommendation(ticker, company, forecast_price, growth, rmse, sector)
