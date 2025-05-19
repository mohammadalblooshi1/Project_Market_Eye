import streamlit as st
import pandas as pd
from Backend.auth import register_user, login_user, log_activity
from Backend.forecasting import load_and_prepare_data, compute_analytics, forecast_with_mlp, forecast_january_with_mlp
from Backend.llm import generate_recommendation
from Backend.pdf_generator import generate_pdf


# Logout handler
def logout():
    st.session_state.user_id = None
    st.rerun()


# Main app function
def main():
    st.set_page_config(page_title="Market Eye", layout="centered")

    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    if st.session_state.user_id is None:
        st.title("📊 Market Eye: Stock Analysis")
        menu = ["Login", "Register"]
        choice = st.sidebar.selectbox("Menu", menu)

        if choice == "Register":
            st.subheader("Create New Account")
            new_user = st.text_input("Username")
            new_pass = st.text_input("Password", type='password')
            if st.button("Register"):
                if register_user(new_user, new_pass):
                    st.success("Registration successful! Please login.")
                else:
                    st.error("Username already exists.")

        elif choice == "Login":
            st.subheader("Login to Your Account")
            username = st.text_input("Username")
            password = st.text_input("Password", type='password')
            if st.button("Login"):
                user_id = login_user(username, password)
                if user_id:
                    st.session_state.user_id = user_id
                    log_activity(user_id, "login")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    else:
        st.sidebar.success("Logged in ✅")
        if st.sidebar.button("Logout"):
            logout()

        st.subheader("📈 Stock Analytics and Forecasting")

        try:
            df = load_and_prepare_data("World-Stock-Prices-Dataset.csv")
            log_activity(st.session_state.user_id, "data_loaded")

            analytics_df = compute_analytics(df)
            st.markdown("### 🔍 Stock Analytics")
            st.dataframe(analytics_df)

            st.markdown("### 🤖 Forecast and Recommendation")
            selected_ticker = st.selectbox("Select Ticker:", df['Ticker'].unique())

            if selected_ticker:
                forecast_df, mse, rmse = forecast_january_with_mlp(df, selected_ticker)
                st.line_chart(forecast_df.set_index('Date')[['Actual_Close', 'Predicted_Close']])
                st.metric("MSE", f"{mse:.2f}")
                st.metric("RMSE", f"{rmse:.2f}")
                log_activity(st.session_state.user_id, f"forecast_ticker:{selected_ticker}")

                # Extract analytics and company details
                analytics_row = analytics_df[analytics_df['Ticker'] == selected_ticker].iloc[0]
                forecast_price = forecast_df['Predicted_Close'].iloc[-1]
                growth = analytics_row['2020–2025 Growth %']
                sector = df[df['Ticker'] == selected_ticker]['Industry_Tag'].iloc[0]
                company = df[df['Ticker'] == selected_ticker]['Brand_Name'].iloc[0]

                # LLM Recommendation
                recommendation = generate_recommendation(
                    selected_ticker, company, forecast_price, growth, rmse, sector
                )
                st.markdown("### 💡 LLM Recommendation")
                st.info(recommendation)

                # PDF Report
                st.markdown("### 📄 Generate PDF Report")
                if st.button("Download PDF Report"):
                    filename = generate_pdf(
                        ticker=selected_ticker,
                        company=company,
                        analytics_row=analytics_row,
                        forecast_df=forecast_df,
                        mse=mse,
                        rmse=rmse,
                        recommendation=recommendation
                    )
                    with open(filename, "rb") as f:
                        st.download_button(
                            label="📥 Click to Download Report",
                            data=f,
                            file_name=filename,
                            mime="application/pdf"
                        )

        except FileNotFoundError:
            st.warning("CSV file 'World-Stock-Prices-Dataset.csv' not found.")


if __name__ == '__main__':
    main()
