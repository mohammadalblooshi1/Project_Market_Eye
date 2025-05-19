def generate_recommendation(ticker, company, forecast_price, growth, rmse, sector):
    import google.generativeai as genai
    genai.configure(api_key="AIzaSyCWJn450kzi7rwPzB05YXUDweuEyXwQ-74")  

    prompt = f"""
    Analyze the following stock and suggest whether to Buy, Hold, or Sell. Give me a short recommendation.

    Company: {company} ({ticker})
    Forecasted January 2025 Closing Price: ${forecast_price:.2f}
    Annual Growth since 2020: {growth:.2f}%
    RMSE of prediction model: {rmse:.2f}
    Sector: {sector}

    Please give a professional recommendation with clear reasoning. Be precise. 
    """

    model = genai.GenerativeModel("models/gemini-2.0-flash")
    response = model.generate_content(prompt)


    return response.text.strip()
