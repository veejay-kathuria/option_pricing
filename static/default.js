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

    // Clear the suggestions
    document.getElementById('autocomplete-list').innerHTML = '';
}