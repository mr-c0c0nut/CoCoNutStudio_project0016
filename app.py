from flask import Flask, render_template

app = Flask(__name__)

# 8 Modes Icon Mapping
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

# Raw Player Data
RAW_PLAYERS = [
    {
        "username": "anh5me27051",
        "modes": [
            {"mode": "UHC", "tier": "HT4", "points": 25},
            {"mode": "Axe", "tier": "LT4", "points": 20},
            {"mode": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Vandekynang22",
        "modes": [
            {"mode": "UHC", "tier": "HT4", "points": 25},
            {"mode": "Axe", "tier": "HT5", "points": 15},
            {"mode": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "LikedasMC",
        "modes": [
            {"mode": "Sword", "tier": "HT5", "points": 15},
            {"mode": "Axe", "tier": "HT5", "points": 15},
            {"mode": "UHC", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "CatRista",
        "modes": [
            {"mode": "UHC", "tier": "LT4", "points": 20},
            {"mode": "Axe", "tier": "LT4", "points": 20}
        ]
    },
    {
        "username": "Chuyenn",
        "modes": [
            {"mode": "Sword", "tier": "LT4", "points": 20},
            {"mode": "UHC", "tier": "HT5", "points": 15}
        ]
    },
    {
        "username": "rautrang3245",
        "modes": [
            {"mode": "Sword", "tier": "LT3", "points": 30}
        ]
    },
    {
        "username": "Uchiha_nho",
        "modes": [
            {"mode": "Sword", "tier": "HT4", "points": 25}
        ]
    },
    {
        "username": "gbaoz21",
        "modes": [
            {"mode": "Sword", "tier": "HT4", "points": 25}
        ]
    },
    {
        "username": "AGL_Mipp",
        "modes": [
            {"mode": "Sword", "tier": "LT5", "points": 10},
            {"mode": "SMP", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Wai_VN",
        "modes": [
            {"mode": "Sword", "tier": "LT4", "points": 20}
        ]
    },
    {
        "username": "TD4T_",
        "modes": [
            {"mode": "UHC", "tier": "LT4", "points": 20}
        ]
    },
    {
        "username": "Lovuongdaide",
        "modes": [
            {"mode": "UHC", "tier": "HT5", "points": 15}
        ]
    },
    {
        "username": "Ag_qkhang",
        "modes": [
            {"mode": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "MeoBeo_",
        "modes": [
            {"mode": "UHC", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "longskibidop_51321",
        "modes": [
            {"mode": "UHC", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Khang",
        "modes": [
            {"mode": "Vanilla", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "mr.c0c0nut._91571",
        "modes": [
            {"mode": "Sword", "tier": "LT5", "points": 10}
        ]
    },
    {
        "username": "Lovundaide",
        "modes": [
            {"mode": "UHC", "tier": "LT5", "points": 10}
        ]
    }
]

def calculate_rankings(players):
    # Calculate total points
    for p in players:
        p["total_points"] = sum(m["points"] for m in p["modes"])
    
    # Sort descending by total points
    players_sorted = sorted(players, key=lambda x: x["total_points"], reverse=True)
    
    # Apply Standard Competition Ranking (1224 ranking)
    rankings = []
    current_rank = 1
    for i, p in enumerate(players_sorted):
        if i > 0 and p["total_points"] < players_sorted[i - 1]["total_points"]:
            current_rank = i + 1
        p_copy = dict(p)
        p_copy["rank"] = current_rank
        rankings.append(p_copy)
        
    return rankings

@app.route("/")
def home():
    rankings = calculate_rankings(RAW_PLAYERS)
    return render_template("index.html", rankings=rankings, mode_icons=MODE_ICONS)

if __name__ == "__main__":
    app.run(debug=True)
