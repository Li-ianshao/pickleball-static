import random
import os

# 隨機姓名生成器
first_names = ["Alex", "Jamie", "Taylor", "Jordan", "Morgan", "Casey", "Drew", "Skyler"]
last_names = ["Smith", "Lee", "Brown", "Clark", "Lopez", "Wang", "Khan", "Patel"]

def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# 實際使用時請貼上實際選手資料
players = {
    "Day-Beginner-Intermediate": [generate_name() for _ in range(8)],
    "Night-Beginner-Intermediate": [generate_name() for _ in range(8)],
    "Day-Advanced": [generate_name() for _ in range(8)],
    "Night-Advanced": [generate_name() for _ in range(8)]
}

# 場地與隊伍設定
courts = {
    "Court A (Beginner - Intermediate)": ["Team 1", "Team 2", "Team 3", "Team 4"],
    "Court B (Beginner - Intermediate)": ["Team 5", "Team 6", "Team 7", "Team 8"],
    "Court C (Advanced)": ["Team 9", "Team 10", "Team 11", "Team 12"],
    "Court D (Advanced)": ["Team 13", "Team 14", "Team 15", "Team 16"]
}

# HTML 開頭
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset=\"UTF-8\">
    <title>Pickleball 分組管理</title>
    <style>
        * { box-sizing: border-box; }
        body { font-family: Arial, sans-serif; padding: 1rem; display: flex; flex-direction: column; gap: 2rem; }

        .players-panel {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 1rem;
        }
        .column-title {
            font-weight: bold;
            margin-bottom: 0.25rem;
        }
        .group {
            padding: 0.5rem;
            border: 1px solid #ccc;
            border-radius: 0.5rem;
            background-color: #f8fafc;
        }
        .player {
            display: inline-block;
            background: #dbeafe;
            color: #1e3a8a;
            padding: 0.3rem 0.6rem;
            margin: 0.2rem;
            border-radius: 9999px;
            font-size: 0.875rem;
            border: 1px solid #60a5fa;
            cursor: grab;
        }

        .court-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            grid-template-rows: 1fr 1fr;
            gap: 2rem;
        }
        .court {
            padding: 1rem;
            background-color: #f0fdf4;
            border: 2px solid #4ade80;
            border-radius: 1rem;
        }
        .team {
            border: 2px dashed #94a3b8;
            min-height: 3rem;
            padding: 0.5rem;
            margin-bottom: 0.5rem;
            background: #f8fafc;
            border-radius: 0.375rem;
            transition: background-color 0.2s;
        }
        .team.over {
            background-color: #bbf7d0;
        }
    </style>
</head>
<body>
    <h1 class="text-xl font-bold mb-4">選手分組管理介面</h1>
    <div class="players-panel">
"""

# 產生左側選手欄位
for group, names in players.items():
    html += f"<div class='group'><div class='column-title'>{group}</div>"
    for name in names:
        html += f"<div class='player' draggable='true'>{name}</div>"
    html += "</div>"

html += "</div><div class='court-grid'>"

# 產生右側球場與隊伍空格（按照四宮格排版）
for court, teams in courts.items():
    html += f"<div class='court'><strong>{court}</strong>"
    for team in teams:
        html += f"<div class='team' ondragover='allowDrop(event)' ondragleave='leave(event)' ondrop='drop(event)'></div>"
    html += "</div>"

# HTML 結尾加上 JS
html += """
    </div>
<script>
    let dragged;

    document.querySelectorAll('.player').forEach(el => {
        el.addEventListener('dragstart', e => {
            dragged = e.target;
            e.dataTransfer.setData('text/plain', e.target.innerText);
            e.dataTransfer.setDragImage(e.target, 0, 0);
        });
    });

    function allowDrop(e) {
        e.preventDefault();
        e.currentTarget.classList.add('over');
    }

    function leave(e) {
        e.currentTarget.classList.remove('over');
    }

    function drop(e) {
        e.preventDefault();
        e.currentTarget.classList.remove('over');
        if (dragged) e.currentTarget.appendChild(dragged);
    }
</script>
</body>
</html>
"""

# 寫入 output
os.makedirs("output", exist_ok=True)
with open("output/grouping.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ grouping.html 已產生於 output/ 資料夾中")
