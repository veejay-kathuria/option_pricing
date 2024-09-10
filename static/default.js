// JavaScript function to fetch stock suggestions
async function fetchStockSuggestions() {
    const query = document.getElementById('stock_name').value;
    const suggestionsDiv = document.getElementById('autocomplete-list');

    if (query.length > 2) {  // Only make a request if more than 2 characters are typed
        // Make an AJAX call to the backend to fetch stock suggestions
        const response = await fetch(`/stock_suggestions?query=${query}`);
        const suggestions = await response.json();

        // Clear any existing suggestions
        suggestionsDiv.innerHTML = '';

        // Add the new suggestions
        suggestions.forEach(suggestion => {
            const div = document.createElement('div');
            div.classList.add('autocomplete-suggestion');
            div.textContent = `${suggestion.name} (${suggestion.symbol})`;
            div.onclick = () => selectStock(suggestion.symbol);
            suggestionsDiv.appendChild(div);
        });
    } else {
        // Clear the suggestions if the query is too short
        suggestionsDiv.innerHTML = '';
    }
}


function selectStock(symbol) {
    // Set the selected stock symbol in the input field
    document.getElementById('stock_name').value = symbol;
    fetchExpiryAndStrikes()
    
    

    // Clear the suggestions
    document.getElementById('autocomplete-list').innerHTML = '';
}

async function fetchStockPrice(ticker){
    // const ticker = document.getElementById('stock_name').value;
    try {
        const response = await fetch(`/fetch_stock_price?ticker=${ticker}`);
        const data = await response.json();
        
        if (data.error) {
            console.log("Error Occured: " +data.error);
        } else {
            document.getElementById('current_stock_price').innerHTML = `Last traded Price: $${data.price}`;
            // alert(`The current price of ${data.ticker} is $${data.price}`);
        }
    } catch (error) {
        console.error('Error fetching price:'+ error);
    }
}


async function fetchExpiryAndStrikes() {
    const ticker = document.getElementById('stock_name').value;
    fetchStockPrice(ticker)
    const expiryDropdown = document.getElementById('expiry');
    const strikeDropdown = document.getElementById('strike_price');

    // Reset dropdowns
    expiryDropdown.innerHTML = '<option value="">Select Expiry Date</option>';
    strikeDropdown.innerHTML = '<option value="">Select Strike Price</option>';

    if (ticker.length > 2) {
        try {
            // Fetch the available expiry dates and strike prices from the backend
            const response = await fetch(`/fetch_expiry_strike?ticker=${ticker}`);
            const data = await response.json();

            // Populate the expiry date dropdown
            data.expiries.forEach(expiry => {
                const option = document.createElement('option');
                option.value = expiry;
                option.textContent = expiry;
                expiryDropdown.appendChild(option);
            });

            // Populate the strike price dropdown
            data.strikes.forEach(strike => {
                const option = document.createElement('option');
                option.value = strike;
                option.textContent = strike;
                strikeDropdown.appendChild(option);
            });
        } catch (error) {
            console.error('Error fetching expiry and strike prices:', error);
        }
    }
}

    