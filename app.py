from flask import Flask, render_template, request
import yfinance as yf
import numpy as np
import pandas as pd
from scipy.stats import norm
from threading import Thread

app = Flask(__name__)


def binomial_tree_complete(S, K, T, r, sigma, steps, option_type="call"):
    # """
    # Function to price an option using the Binomial Tree model.
    # Also returns the stock price tree and option price tree for visualization.
    # """
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
            ticker = request.form['ticker'].upper()
            expiry = request.form['expiry']
            strike_price = float(request.form['strike_price'])
            steps = int(request.form['steps'])
            option_type = request.form['option_type'].lower()
            
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            S = data['Close'][0]
            r = 0.01  # risk-free rate
            
            expiry_date = pd.to_datetime(expiry).date()
            current_date = pd.to_datetime(data.index[0]).date()
            
            T = (expiry_date - current_date).days / 365.0
            sigma = stock.history(period="1y")['Close'].pct_change().std() * np.sqrt(252)
            
            bt_price, stock_tree, option_tree, p, u, d = binomial_tree_complete(S, strike_price, T, r, sigma, steps, option_type=option_type)
        
        except Exception as e:
            print ("ERROR in index")
            return render_template_string('<h1>Error: {{ error }}</h1>', error=str(e))


        return render_template('index.html', bt_price=bt_price, stock_tree=stock_tree, option_tree=option_tree, ticker=request.form.get('ticker'), S=S, strike_price=strike_price, T=T, r=r, sigma=sigma, steps=steps, u=u, d=d, p=p)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)