from fpdf import FPDF

# Clean non-Latin-1 characters
def clean(text):
    if isinstance(text, str):
        return (text
                .replace("–", "-")
                .replace("—", "-")
                .replace("’", "'")
                .replace("“", '"')
                .replace("”", '"')
                .replace("•", "-"))
    return str(text)

def generate_pdf(ticker, company, analytics_row, forecast_df, mse, rmse, recommendation, filename="report.pdf"):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, f"Market Eye Report: {clean(company)} ({clean(ticker)})", ln=True, align="C")

    pdf.set_font("Arial", "", 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"High Price: {clean(analytics_row['High'])}", ln=True)
    pdf.cell(200, 10, f"Low Price: {clean(analytics_row['Low'])}", ln=True)
    pdf.cell(200, 10, f"Growth (2020-2025): {clean(round(analytics_row['2020–2025 Growth %'], 2))}%", ln=True)

    pdf.ln(10)
    pdf.cell(200, 10, f"MSE: {clean(round(mse, 2))}", ln=True)
    pdf.cell(200, 10, f"RMSE: {clean(round(rmse, 2))}", ln=True)

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "LLM Recommendation:", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, clean(recommendation))

    pdf.ln(10)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Forecast (Last 5 Days):", ln=True)
    pdf.set_font("Arial", "", 10)
    last5 = forecast_df.tail(5)
    for _, row in last5.iterrows():
        line = f"{row['Date']}: Actual={round(row['Actual_Close'], 2)}, Predicted={round(row['Predicted_Close'], 2)}"
        pdf.cell(200, 8, clean(line), ln=True)

    pdf.output(filename)
    return filename
