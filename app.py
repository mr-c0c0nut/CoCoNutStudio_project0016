import os
from flask import Flask, render_template, jsonify

# Thiết lập đường dẫn thư mục templates tuyệt đối để tránh lỗi TemplateNotFound trên Render
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

app = Flask(__name__, template_folder=template_dir)

# Mapping Icon URL cho các chế độ chơi
MODE_ICONS = {
    "Mace": "https://i.ibb.co/cXcHtW5c/1533764190723113050.webp",
    "Axe": "https://i.ibb.co/zW8WcJKh/1533764227607560233.webp",
    "Sword": "https://i.ibb.co/yFmTKyXC/1533764260486844488.webp",
    "SMP": "https://i.ibb.co/C3RjZR8v/1533764288055873638.webp",
    "NethOP": "https://i.ibb.co/G349PxWx/1533764316262826025.webp",
    "Pot": "https://i.ibb.co/ynR4j8kp/1533764426941993140.webp",
    "UHC": "https://i.ibb.co/nMSsgPcv/1533764468876771448.webp",
    "Vanilla": "https://i.ibb.co/5hPZXd0S/1533764503161012344.webp"
}

# Điểm số quy đổi theo danh hiệu (LT5 -> HT1)
TIER_POINTS = {
    "HT1": 60, "HT2": 50, "HT3": 40, "HT4": 30, "HT5": 20,
    "LT1": 15, "LT2": 10, "LT3": 8,  "LT4": 5,  "LT5": 2,
    "NONE": 0, "": 0
}

# Dữ liệu gốc 18 Players
RAW_PLAYERS = [
    {"username": "Player_01", "modes": {"Mace": "HT1", "Axe": "HT2", "Sword": "HT3", "SMP": "LT1", "NethOP": "LT2", "Pot": "LT3", "UHC": "LT4", "Vanilla": "LT5"}},
    {"username": "Player_02", "modes": {"Mace": "HT2", "Axe": "HT1", "Sword": "HT2", "SMP": "HT3", "NethOP": "LT1", "Pot": "LT2", "UHC": "LT3", "Vanilla": "LT4"}},
    {"username": "Player_03", "modes": {"Mace": "HT3", "Axe": "HT3", "Sword": "HT1", "SMP": "HT2", "NethOP": "HT3", "Pot": "LT1", "UHC": "LT2", "Vanilla": "LT3"}},
    {"username": "Player_04", "modes": {"Mace": "LT1", "Axe": "HT4", "Sword": "HT4", "SMP": "HT1", "NethOP": "HT2", "Pot": "HT3", "UHC": "LT1", "Vanilla": "LT2"}},
    {"username": "Player_05", "modes": {"Mace": "LT2", "Axe": "LT1", "Sword": "HT5", "SMP": "HT4", "NethOP": "HT1", "Pot": "HT4", "UHC": "LT2", "Vanilla": "LT1"}},
    {"username": "Player_06", "modes": {"Mace": "LT3", "Axe": "LT2", "Sword": "LT1", "SMP": "HT5", "NethOP": "HT4", "Pot": "HT1", "UHC": "LT3", "Vanilla": "LT2"}},
    {"username": "Player_07", "modes": {"Mace": "LT4", "Axe": "LT3", "Sword": "LT2", "SMP": "LT1", "NethOP": "HT5", "Pot": "HT2", "UHC": "HT1", "Vanilla": "LT3"}},
    {"username": "Player_08", "modes": {"Mace": "LT5", "Axe": "LT4", "Sword": "LT3", "SMP": "LT2", "NethOP": "LT1", "Pot": "HT5", "UHC": "HT2", "Vanilla": "HT1"}},
    {"username": "Player_09", "modes": {"Mace": "HT4", "Axe": "LT5", "Sword": "LT4", "SMP": "LT3", "NethOP": "LT2", "Pot": "LT1", "UHC": "HT3", "Vanilla": "HT2"}},
    {"username": "Player_10", "modes": {"Mace": "HT5", "Axe": "HT5", "Sword": "LT5", "SMP": "LT4", "NethOP": "LT3", "Pot": "LT2", "UHC": "LT1", "Vanilla": "HT3"}},
    {"username": "Player_11", "modes": {"Mace": "LT1", "Axe": "LT1", "Sword": "HT1", "SMP": "LT5", "NethOP": "LT4", "Pot": "LT3", "UHC": "LT2", "Vanilla": "LT1"}},
    {"username": "Player_12", "modes": {"Mace": "LT2", "Axe": "LT2", "Sword": "HT2", "SMP": "HT1", "NethOP": "LT5", "Pot": "LT4", "UHC": "LT3", "Vanilla": "LT2"}},
    {"username": "Player_13", "modes": {"Mace": "LT3", "Axe": "LT3", "Sword": "HT3", "SMP": "HT2", "NethOP": "HT1", "Pot": "LT5", "UHC": "LT4", "Vanilla": "LT3"}},
    {"username": "Player_14", "modes": {"Mace": "LT4", "Axe": "LT4", "Sword": "HT4", "SMP": "HT3", "NethOP": "HT2", "Pot": "HT1", "UHC": "LT5", "Vanilla": "LT4"}},
    {"username": "Player_15", "modes": {"Mace": "LT5", "Axe": "LT5", "Sword": "HT5", "SMP": "HT4", "NethOP": "HT3", "Pot": "HT2", "UHC": "HT1", "Vanilla": "LT5"}},
    {"username": "Player_16", "modes": {"Mace": "HT1", "Axe": "HT1", "Sword": "LT1", "SMP": "HT5", "NethOP": "HT4", "Pot": "HT3", "UHC": "HT2", "Vanilla": "HT1"}},
    {"username": "Player_17", "modes": {"Mace": "HT2", "Axe": "HT2", "Sword": "LT2", "SMP": "LT1", "NethOP": "HT5", "Pot": "HT4", "UHC": "HT3", "Vanilla": "HT2"}},
    {"username": "Player_18", "modes": {"Mace": "HT3", "Axe": "HT3", "Sword": "LT3", "SMP": "LT2", "NethOP": "LT1", "Pot": "HT5", "UHC": "HT4", "Vanilla": "HT3"}}
]

def build_leaderboard():
    processed = []
    
    # 1. Tính tổng điểm và cấu trúc lại mode cho từng player
    for p in RAW_PLAYERS:
        total_points = 0
        formatted_modes = []
        
        for mode_name, tier in p["modes"].items():
            pts = TIER_POINTS.get(tier, 0)
            total_points += pts
            formatted_modes.append({
                "name": mode_name,
                "tier": tier,
                "points": pts,
                "icon": MODE_ICONS.get(mode_name, "")
            })
            
        processed.append({
            "username": p["username"],
            "total_points": total_points,
            "modes": formatted_modes
        })
        
    # 2. Sắp xếp giảm dần theo tổng điểm
    processed.sort(key=lambda x: x["total_points"], reverse=True)
    
    # 3. Tính rank theo Competition Ranking Standard
    current_rank = 1
    for i in range(len(processed)):
        if i > 0 and processed[i]["total_points"] < processed[i - 1]["total_points"]:
            current_rank = i + 1
        processed[i]["rank"] = current_rank
        
    return processed

@app.route("/")
def index():
    leaderboard_data = build_leaderboard()
    return render_template(
        "index.html", 
        players=leaderboard_data, 
        leaderboard=leaderboard_data, 
        data=leaderboard_data
    )

@app.route("/api/leaderboard", methods=["GET"])
def get_leaderboard():
    leaderboard_data = build_leaderboard()
    return jsonify(leaderboard_data), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
