from flask import Flask, jsonify, request, render_template
from web3 import Web3
ENV_MODE = 'production'
app = Flask(__name__)

# Conexión a las redes de Polygon y BSC
polygon_rpc = "https://polygon-rpc.com/"
bsc_rpc = "https://bsc-dataseed1.binance.org/"
web3_polygon = Web3(Web3.HTTPProvider(polygon_rpc))
web3_bsc = Web3(Web3.HTTPProvider(bsc_rpc))

# Token Addresses
tokens = {
    "mcoin": "0x8fa62D23FB6359c1e1685dBFa9B63eF27eCDb612",
    "usdt": "0xc2132D05D31c914a87C6611C10748AEb04B58e8F"
}

# Endpoint para obtener el progreso de la donación
@app.route('/donation/progress', methods=['GET'])
def donation_progress():
    wallet_address = "0x6c455601f9bd87cb892da76529f1a3a4f90362bd"
    total_value = 0
    
    # Obtener balances de Polygon
    for token, address in tokens.items():
        token_contract = web3_polygon.eth.contract(address=Web3.to_checksum_address(address), abi=[
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
                
        total_value += balance  # Suponiendo que el balance se interpreta en tokens

    goal = 444444  # Objetivo de donación en el token base

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
