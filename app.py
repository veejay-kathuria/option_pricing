from flask import Flask, render_template, render_template_string, jsonify, request
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
from threading import Thread
import json


app = Flask(__name__)

# # Stock Tickers
stock = open('static/stocks.json')
stocks = json.load(open('static/stocks.json'))
# # print (stocks)


def black_scholes(S, K, T, r, sigma, option_type="call"):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put option 
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
        
    return price


def binomial_tree_complete(S, K, T, r, sigma, steps, option_type="call"):
    # Function to price an option using the Binomial Tree model.
    # Also returns the stock price tree and option price tree for visualization.

    dt = T / steps
    u = np.exp(sigma * np.sqrt(dt))
    d = 1 / u
    p = (np.exp(r * dt) - d) / (u - d)
    
    stock_tree = np.zeros((steps + 1, steps + 1))
    option_tree = np.zeros((steps + 1, steps + 1))
    
    for i in range(steps + 1):
        j=0
        while j<=i:
            stock_tree[j, i] = S * (u**(i-j)) * (d**j)
            j = j+1
  
    for i in range(steps + 1):
        if option_type == "call":
            option_tree[i, steps] = max(0, stock_tree[i, steps] - K)
        elif option_type == "put":
            option_tree[i, steps] = max(0, K - stock_tree[i, steps])
    
    for j in range(steps - 1, -1, -1):
        for i in range(j + 1):
            option_tree[i, j] = np.exp(-r * dt) * (p * option_tree[i, j + 1] + (1 - p) * option_tree[i + 1, j + 1])
    
    return option_tree[0, 0], stock_tree, option_tree, p, u, d




# Route for main data
@app.route('/', methods=['GET', 'POST'])
def index():
    bt_price = None
    stock_tree = None
    option_tree = None
    p = None
    u = None
    d = None
    
    if request.method == 'POST':
        try:
            ticker = request.form['stock_name'].upper()
            expiry = request.form['expiry']
            strike_price = float(request.form['strike_price'])
            steps = int(request.form['steps'])
            option_type = request.form['option_type'].lower()
            print ([ticker,expiry,strike_price,steps,option_type])

            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")

            options_chain = stock.option_chain(expiry)
            # Get the call and put options data
            if option_type == 'call':
                calls = options_chain.calls
                option_price = calls[calls['strike'] == strike_price].iloc[-1].lastPrice
                print (option_price)
            else:
                puts = options_chain.puts
                option_price = puts[puts['strike'] == strike_price].iloc[-1].lastPrice
                print (option_price)  

            S = data['Close'].iloc[0]
            r = 0.05  # risk-free rate
            
            expiry_date = pd.to_datetime(expiry).date()
            current_date = pd.to_datetime(data.index[0]).date()
            
            T = (expiry_date - current_date).days / 365.0
            sigma = stock.history(period="1y")['Close'].pct_change().std() * np.sqrt(252)
            
            bs_price = black_scholes(S, strike_price, T, r, sigma, option_type=option_type)
            bt_price, stock_tree, option_tree, p, u, d = binomial_tree_complete(S, strike_price, T, r, sigma, steps, option_type=option_type)
            

        except Exception as e:
            print ("ERROR in index: %s" %e)
            return render_template('index.html', error=str(e))


        return render_template('index.html', bs_price = bs_price, bt_price=bt_price, stock_tree=stock_tree, option_tree=option_tree, ticker=request.form.get('stock_name'), S=S, strike_price=strike_price, T=T, r=r, sigma=sigma, steps=steps, u=u, d=d, p=p, option_price = option_price)

    return render_template('index.html')


# Route to provide stock suggestions
@app.route('/stock_suggestions', methods=['GET'])
def stock_suggestions():
    query = request.args.get('query', '').lower()
    
    if not query:
        return jsonify([]) 
    suggestions = [stock for stock in stocks if query in stock['name'].lower()]
    
    return jsonify(suggestions)


#Fetch Stock Price

def get_current_price(ticker_symbol):
    try:
        ticker = yf.Ticker(str(ticker_symbol)).history()
        current_price = round(ticker['Close'].iloc[-1],2)
        return current_price
    except Exception as e:
        return None
    
@app.route('/fetch_stock_price', methods=['GET'])
def fetch_stock_price():
    ticker = request.args.get('ticker', '').upper()
    
    if not ticker:
        return jsonify({'error': 'No ticker provided'}), 400
    
    price = get_current_price(ticker)
    
    
    if price is None:
        return jsonify({'error': 'Could not fetch the current price'}), 500
    
    return jsonify({'ticker': ticker, 'price': price})


# Fetch option data
@app.route('/fetch_expiry_strike', methods=['GET'])
def fetch_expiry_strike():
    ticker = request.args.get('ticker', '').upper()

    if ticker:
        try:
            stock = yf.Ticker(ticker)
            # print (stock)   
            # Get the available expiry dates
            expiry_dates = stock.options

            # Get the first expiry date to fetch the option chain
            first_expiry = expiry_dates[0]

            # Fetch the options chain for the first expiry date
            options_chain = stock.option_chain(first_expiry)

            # Extract the strike prices from the call options (can use puts too)
            strike_prices = list(options_chain.calls['strike'])

            # Return the expiry dates and strike prices
            return jsonify({'expiries': expiry_dates, 'strikes': strike_prices})

        except Exception as e:
            return jsonify({'error': str(e)})

    return jsonify({'error': 'Invalid Ticker'})



if __name__ == '__main__':
    app.run(debug=True)