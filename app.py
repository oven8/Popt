from flask import Flask, render_template, request, jsonify
from optimizer import calculate_optimal_weights, ticker_to_name, current_bond_yield

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', CBR=round(current_bond_yield()*100,4))

@app.route('/optimize', methods=['POST'])
def optimize():
    tickers = request.json.get('tickers', None)
    bond_yield = request.json.get('bond_yield') or round(current_bond_yield()*100,4)
    print(bond_yield)
    weights = calculate_optimal_weights(bond_yield/100,tickers=tickers)
    names = ticker_to_name(tickers=tickers)
    
    results = [{"ticker": ticker, "weight": weight, "name": name} 
               for ticker, weight, name in zip(weights.keys(), weights.values(), names)]
    
    return jsonify({"results": results,"bond_yield": bond_yield})

if __name__ == '__main__':
    app.run(debug=True)
