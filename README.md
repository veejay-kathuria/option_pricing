# Option Pricing Calculator

This project provides a pricing calculator for financial derivatives (options) on selected stocks using two well-known methods: **Black-Scholes** and the **Binomial Tree** method. It allows users to select a stock and an option, calculate the option price using both models, and compare the derived values with the present market price. The project fetches live data from the Yahoo Finance API and uses Python and Flask to display the results on an interactive web interface.

## Features
- **Real-time data**: Fetches live stock and option data from Yahoo Finance API.
- **Option pricing models**:
  - **Black-Scholes Model** for European-style options.
  
  - **Binomial Tree Model** for both European and American options.
- **Comparison**: Compares the prices derived from both models with the actual market price of the option.
- **User Input**: 
  - Stock ticker symbol.
  - Option type (Call/Put).
  - Strike price.
  - Expiry date.
  - Number of steps in the Binomial Tree method.
- **Visual representation**: Displays the Binomial Tree as a visual diagram, showing both stock and option price paths.

## Workflow
1. **Input**: The user provides the stock ticker, option type (Call/Put), strike price, expiry date, and the number of steps for the Binomial Tree method via a web form.
2. **Live Data Fetch**: The app uses Yahoo Finance to fetch the current stock price, option chain data (strike price, expiry dates), and other market parameters like the US 10-year Treasury yield for the risk-free rate.
3. **Calculations**:
   - **Black-Scholes Model**: Computes the option price based on user inputs and market data for European options.
   - **Binomial Tree Method**: Generates a price tree for the stock and calculates option values using backward induction.
4. **Comparison**: The app compares the results from both models and displays them alongside the current market price.
5. **Visualization**: A visual Binomial Tree representation is provided, showing stock prices and option values at each step.
6. **Output**: Results are displayed on the web interface, including the input parameters, calculated option prices (from both models), and the live option price from the market.

## Libraries Used
- **Flask**: Web framework to build the application and present the results on an HTML page.
- **Yahoo Finance** (`yfinance`): To fetch real-time stock and option data.
- **NumPy**: For numerical computations, including matrix operations in the Binomial Tree method.
- **Matplotlib**: For plotting and visualizing the option pricing trees.
- **Bootstrap**: To style the HTML form and results page, providing a clean and responsive design.
- **Pandas**: For managing and manipulating data fetched from the Yahoo Finance API.

## Results
The application provides:
- **Option Prices**: Both Black-Scholes and Binomial Tree model prices for the selected option.
- **Comparison**: A side-by-side comparison of the two model prices with the actual market price.
- **Visualization**: A detailed and interactive Binomial Tree that demonstrates stock price movements and option price calculations at each step.

Example results for a call option:
- **Black-Scholes Price**: $10.50
- **Binomial Tree Price**: $10.45
- **Market Price**: $10.60

This comparison highlights how closely both models track the actual market price and allows users to understand the differences between them.

## Possible References
- Black, F., & Scholes, M. (1973). "The Pricing of Options and Corporate Liabilities." *Journal of Political Economy*, 81(3), 637-654.
- Cox, J. C., Ross, S. A., & Rubinstein, M. (1979). "Option Pricing: A Simplified Approach." *Journal of Financial Economics*, 7(3), 229-263.
- Hull, J. C. (2009). *Options, Futures, and Other Derivatives*. Prentice Hall.
- Yahoo Finance API Documentation: [https://pypi.org/project/yfinance/](https://pypi.org/project/yfinance/)

## Installation
1. Clone this repository:
   ```bash
   git clone https://github.com/username/option-pricing-calculator.git
2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
3. Run the Flask application:
    ```bash
    python app.py
4. Open your browser and navigate to http://127.0.0.1:5000/ to interact with the application.