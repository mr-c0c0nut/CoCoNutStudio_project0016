from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Dữ liệu người chơi chuẩn từ hệ thống
PLAYERS_DATA = [
    {"username": "anh5me27051", "modes": [{"mode": "UHC", "tier": "HT4", "points": 25}, {"mode": "Axe", "tier": "LT4", "points": 20}, {"mode": "Sword", "tier": "LT5", "points": 10}]},
    {"username": "Vandekynang22", "modes": [{"mode": "UHC", "tier": "HT4", "points": 25}, {"mode": "Axe", "tier": "HT5", "points": 15}, {"mode": "Sword", "tier": "LT5", "points": 10}]},
    {"username": "LikedasMC", "modes": [{"mode": "Sword", "tier": "HT5", "points": 15}, {"mode": "Axe", "tier": "HT5", "points": 15}, {"mode": "UHC", "tier": "LT5", "points": 10}]},
    {"username": "CatRista", "modes": [{"mode": "UHC", "tier": "LT4", "points": 20}, {"mode": "Axe", "tier": "LT4", "points": 20}]},
    {"username": "Chuyenn", "modes": [{"mode": "Sword", "tier": "LT4", "points": 20}, {"mode": "UHC", "tier": "HT5", "points": 15}]},
    {"username": "rautrang3245", "modes": [{"mode": "Sword", "tier": "LT3", "points": 30}]},
    {"username": "Uchiha_nho", "modes": [{"mode": "Sword", "tier": "HT4", "points": 25}]},
    {"username": "gbaoz21", "modes": [{"mode": "Sword", "tier": "HT4", "points": 25}]},
    {"username": "AGL_Mipp", "modes": [{"mode": "Sword", "tier": "LT5", "points": 10}, {"mode": "SMP", "tier": "LT5", "points": 10}]},
    {"username": "Wai_VN", "modes": [{"mode": "Sword", "tier": "LT4", "points": 20}]},
    {"username": "TD4T_", "modes": [{"mode": "UHC", "tier": "LT4", "points": 20}]},
    {"username": "Lovuongdaide", "modes": [{"mode": "UHC", "tier": "HT5", "points": 15}]},
    {"username": "Ag_qkhang", "modes": [{"mode": "Sword", "tier": "LT5", "points": 10}]},
    {"username": "MeoBeo_", "modes": [{"mode": "UHC", "tier": "LT5", "points": 10}]},
    {"username": "longskibidop_51321", "modes": [{"mode": "UHC", "tier": "LT5", "points": 10}]},
    {"username": "Khang", "modes": [{"mode": "Vanilla", "tier": "LT5", "points": 10}]},
    {"username": "mr.c0c0nut._91571", "modes": [{"mode": "Sword", "tier": "LT5", "points": 10}]},
    {"username": "Lovundaide", "modes": [{"mode": "UHC", "tier": "LT5", "points": 10}]}
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ranking')
def ranking():
    return render_template('ranking.html')

@app.route('/api/players', methods=['GET', 'POST'])
def api_players():
    global PLAYERS_DATA
    if request.method == 'POST':
        data = request.get_json()
        if isinstance(data, list):
            PLAYERS_DATA = data
            return jsonify({"status": "success", "message": "Updated successfully"}), 200
        return jsonify({"status": "error", "message": "Invalid data format"}), 400
    
    return jsonify(PLAYERS_DATA)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
