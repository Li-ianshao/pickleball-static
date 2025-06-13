import random
import os
import xml.etree.ElementTree as ET

# 隨機姓名生成器
first_names = ["Alex", "Jamie", "Taylor", "Jordan", "Morgan", "Casey", "Drew", "Skyler"]
last_names = ["Smith", "Lee", "Brown", "Clark", "Lopez", "Wang", "Khan", "Patel"]

def generate_name():
    return f"{random.choice(first_names)} {random.choice(last_names)}"

# 實際使用時請貼上實際選手資料
players = {
    "Day-Beginner-Intermediate": ['華啟梅', '陶家樂', '胡小蓮', '孟愛貞', '林臻', '莊家玲', '邱如玉', 'TBA'],
    "Night-Beginner-Intermediate": ['華啟梅','徐慶如','Alexander Nguyen','Joy Liu','吳尚真','李倩','溫孟璇','TBA'],
    "Day-Advanced":['羅天文','李彤庭','TBA','TBA','TBA','TBA','TBA','TBA'],
    "Night-Advanced":['張立揚','William Hou','TBA','TBA','TBA','TBA','TBA','TBA'],


    # "Day-Beginner-Intermediate": [generate_name() for _ in range(8)],
    # "Night-Beginner-Intermediate": [generate_name() for _ in range(8)],
    #"Day-Advanced": [generate_name() for _ in range(8)],
    #"Night-Advanced": [generate_name() for _ in range(8)]
}

# 場地與隊伍設定
courts = {
    "Court A (Beginner - Intermediate)": ["Team 1", "Team 2", "Team 3", "Team 4"],
    "Court B (Beginner - Intermediate)": ["Team 5", "Team 6", "Team 7", "Team 8"],
    "Court C (Advanced)": ["Team 9", "Team 10", "Team 11", "Team 12"],
    "Court D (Advanced)": ["Team 13", "Team 14", "Team 15", "Team 16"]
}

court_suits = {
    "Court A (Beginner - Intermediate)": "♥️",
    "Court B (Beginner - Intermediate)": "♦️",
    "Court C (Advanced)": "♠️",
    "Court D (Advanced)": "♣️"
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
            user-select: none;
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
            position: relative;
        }

        .court-suit { 
            position: absolute;
            top: -4.5px;
            left: 22.75px;
            font-size: 30px;
            font-weight: bold;
        }

        .court-title {
            margin-left: 3rem;
            font-weight: bold;
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
    <h1 class=\"text-xl font-bold mb-4\">選手分組管理介面</h1>
    <div class=\"players-panel\">
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
    suit = court_suits.get(court, '')
    html += f"<div class='court'><div class='court-suit'>{suit}</div><div class='court-title'>{court}</div>"
    for team in teams:
        html += f"  <div class='team' teamId='{team}'></div>\n"
    html += "</div>"

html += """
    </div>
    <button onclick=\"generateXML()\" style=\"margin-top: 2rem; padding: 0.75rem 1.5rem; background-color: #3b82f6; color: white; border: none; border-radius: 0.375rem; font-weight: bold;\">產生 XML</button>

<script>
    document.addEventListener('DOMContentLoaded', () => {
        let dragged = null;

        document.querySelectorAll('.player').forEach(el => {
            el.addEventListener('dragstart', e => {
                dragged = e.target;
                e.dataTransfer.setData('text/plain', e.target.innerText);
                e.dataTransfer.setDragImage(e.target, 0, 0);
            });
        });

        document.querySelectorAll('.team').forEach(el => {
            el.addEventListener('dragover', allowDrop);
            el.addEventListener('dragleave', leave);
            el.addEventListener('drop', drop);
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
            if (dragged && !e.currentTarget.contains(dragged)) {
                e.currentTarget.appendChild(dragged);
            }
        }
    });

    function generateScheduleXML(courtMatches, teamPlayers) {
        let result = `<?xml version="1.0" encoding="UTF-8"?>\n<schedule>\n`;

        Object.entries(courtMatches).forEach(([courtName, teamList]) => {
            result += `  <court name="${courtName}">\n`;

            for (let i = 0; i < teamList.length; i++) {
            for (let j = i + 1; j < teamList.length; j++) {
                const teamL = teamList[i];
                const teamR = teamList[j];

                const teamLPlayers = teamPlayers[teamL] || ["", ""];
                const teamRPlayers = teamPlayers[teamR] || ["", ""];

                result += `    <match round="" `;
                result += `teamL="${teamL}" teamR="${teamR}" `;
                result += `teamLPlayer1="${teamLPlayers[0]}" teamLPlayer2="${teamLPlayers[1]}" `;
                result += `teamRPlayer1="${teamRPlayers[0]}" teamRPlayer2="${teamRPlayers[1]}" `;
                result += `teamLScore="" teamRScore="" />\n`;
            }
            }

            result += `  </court>\n`;
        });

        result += `</schedule>`;
        console.log("🏓 賽程 XML：", result);
        return result;
    }

    function generateXML() {
        let courts = document.querySelectorAll('.court');
        let result = `<?xml version="1.0" encoding="UTF-8"?>\n<groups>\n`;
        let courtMatches = {};
        let teamPlayers = {};

        courts.forEach(court => {
            let courtName = court.querySelector('.court-title').innerText;
            let teams = court.querySelectorAll('.team');

            result += `  <court name="${courtName}">\n`;
            courtMatches[courtName] = [];

            teams.forEach(teamDiv => {
                const teamId = teamDiv.getAttribute("teamId");
                result += `    <team id="${teamId}">\n`;
                courtMatches[courtName].push(teamId);

                let teamMemberNames = [];
                teamDiv.querySelectorAll('.player').forEach(player => {
                    result += `      <player>${player.innerText}</player>\n`;
                    teamMemberNames.push(player.innerText);
                });

                teamPlayers[teamId] = teamMemberNames;
                result += `    </team>\n`;
            });

            result += `  </court>\n`;
        });

        result += '</groups>';
        console.log("📦 分組 XML:");
        console.log(result);

        generateScheduleXML(courtMatches, teamPlayers);

        alert("✅ 分組與賽程 XML 皆已顯示於 console 中。");
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
