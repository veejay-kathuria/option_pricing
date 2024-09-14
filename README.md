Option Pricing Calculator
This project provides a pricing calculator for financial derivatives (options) on selected stocks using two well-known methods: Black-Scholes and the Binomial Tree method. It allows users to select a stock and an option, calculate the option price using both methods, and compare the derived values with the current market price.

Features
Real-time data: Fetches live stock and option data from Yahoo Finance API.
Option pricing models: Implements two key option pricing methods:
Black-Scholes Model for European-style options.
Binomial Tree Model for both European and American options.
Comparison: Compares the prices derived from both models with the actual market price of the option.
User Input:
Stock ticker symbol.
Option type (Call/Put).
Strike price.
Expiry date.
Number of steps in the Binomial Tree method.
Installation
1. Clone the Repository
bash
Copy code
git clone https://github.com/your-username/option-pricing-calculator.git
cd option-pricing-calculator
2. Set Up a Virtual Environment
bash
Copy code
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3. Install Required Packages
bash
Copy code
pip install -r requirements.txt
Make sure requirements.txt includes the following:

Flask
yfinance
numpy
scipy
matplotlib
bootstrap-flask (optional for frontend UI styling)
4. Running the Application
bash
Copy code
flask run
The app will be accessible at http://127.0.0.1:5000/.

Usage
Step 1: Select a Stock
Enter the stock ticker symbol (e.g., AAPL for Apple) in the search bar.
The app will fetch available expiry dates and strike prices for options on that stock.
Step 2: Select an Option
Choose the desired expiry date and strike price from the dropdown menus.
Select whether you want to calculate the price for a Call or Put option.
Step 3: Calculate Option Prices
The app calculates the price of the option using both the Black-Scholes and Binomial Tree models.
For the Binomial Tree method, you can specify the number of steps in the tree.
Step 4: View the Results
The app presents the following:
Black-Scholes Price
Binomial Tree Price
Live Market Price fetched in real-time.
A comparison of these three prices with graphical representation.
Option Pricing Models
1. Black-Scholes Model
A closed-form model primarily used for pricing European call and put options. The formula considers factors like volatility, the risk-free rate, and time to expiry.

2. Binomial Tree Model
A numerical method for pricing American and European options by discretizing the time to expiry into multiple steps, simulating possible price movements at each step.

Example
Suppose you select a Call option on AAPL stock with a strike price of $150 and an expiry date of 2024-12-31. The app will:

Fetch real-time data for the stock and the option.
Calculate the option's theoretical price using the Black-Scholes and Binomial Tree models.
Display a comparison of these calculated values against the current market price.
Contributing
If you’d like to contribute, please fork the repository and use a feature branch. Pull requests are welcome.

License
This project is licensed under the MIT License.
