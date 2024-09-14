# Option Pricing Calculator

This project provides a pricing calculator for financial derivatives (options) on selected stocks using two well-known methods: **Black-Scholes** and the **Binomial Tree** method. It allows users to select a stock and an option, calculate the option price using both methods, and compare the derived values with the current market price.

## Features
- **Real-time data:** Fetches live stock and option data from Yahoo Finance API.
- **Option pricing models:** Implements two key option pricing methods:
  - **Black-Scholes Model** for European-style options.
  - **Binomial Tree Model** for both European and American options.
- **Comparison:** Compares the prices derived from both models with the actual market price of the option.
- **User Input:**
  - Stock ticker symbol.
  - Option type (Call/Put).
  - Strike price.
  - Expiry date.
  - Number of steps in the Binomial Tree method.
