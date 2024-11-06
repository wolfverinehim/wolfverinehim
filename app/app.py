import requests
from flask import Flask, jsonify, request, render_template
from web3 import Web3

ENV_MODE = 'production'
app = Flask(__name__)

# Conexión a las redes de Polygon y BSC
polygon_rpc = "https://polygon-rpc.com/"
bsc_rpc = "https://bsc-dataseed1.binance.org/"
web3_polygon = Web3(Web3.HTTPProvider(polygon_rpc))
web3_bsc = Web3(Web3.HTTPProvider(bsc_rpc))

# Token Addresses y símbolos para CoinGecko
tokens = {
    "mcoin": {
        "address": "0x8fa62D23FB6359c1e1685dBFa9B63eF27eCDb612",
        "symbol": "maricoin"  # Suponiendo que el símbolo en CoinGecko es "mcoin"
    },
    "usdt": {
        "address": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F",
        "symbol": "tether"  # CoinGecko utiliza "tether" para USDT
    }
}

# Obtener el precio en USD de un token usando CoinGecko
def get_token_price(symbol):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    if symbol in data:
        return data[symbol]["usd"]
    return 0  # Si no encuentra el precio, devuelve 0

# Endpoint para obtener el progreso de la donación
@app.route('/donation/progress', methods=['GET'])
def donation_progress():
    wallet_address = "0x5F6bBd4C50ef1a90541a87737C06228F4541cF41"
    total_value = 0
    
    # Obtener balances de Polygon y su valor en USD
    for token, info in tokens.items():
        token_contract = web3_polygon.eth.contract(address=Web3.to_checksum_address(info["address"]), abi=[
                {
                    "constant": True,
                    "inputs": [
                        {"name": "_owner", "type": "address"}
                    ],
                    "name": "balanceOf",
                    "outputs": [{"name": "balance", "type": "uint256"}],
                    "type": "function"
                },
                {
                    "constant": True,
                    "inputs": [],
                    "name": "decimals",
                    "outputs": [{"name": "", "type": "uint8"}],
                    "type": "function"
                }
        ])
        
        # Obtener los decimales del token
        decimals = token_contract.functions.decimals().call()
       
        # Verificar el balance de la wallet
        balance = token_contract.functions.balanceOf(Web3.to_checksum_address(wallet_address)).call()
        
        # Convertir el balance a una representación legible en decimales
        balance = balance / (10 ** decimals)
        
        # Obtener el precio en USD del token desde CoinGecko
        price_usd = get_token_price(info["symbol"])
        
        # Calcular el valor en USD del balance del token
        balance_usd = balance * price_usd

        # Añadir el balance en USD al total
        total_value += balance_usd

    goal = 444444  # Objetivo de donación en USD

    return jsonify({
        "current_donation": total_value,
        "goal": goal
    })

@app.route("/")
def index():
    return render_template("index.html")





# Ejecutar la aplicación según el entorno
if __name__ == '__main__':
    if ENV_MODE == 'development':
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        from waitress import serve
        serve(app, host="0.0.0.0", port=5000) 
