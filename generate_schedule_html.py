import xml.etree.ElementTree as ET
import os

# 讀取 XML
xml_path = 'static/schedule.xml'
tree = ET.parse(xml_path)
root = tree.getroot()

# 產生 HTML
html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>比賽賽程</title>
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            border: 1px solid #ccc;
            padding: 8px;
            text-align: center;
        }
        th {
            background-color: #f0f0f0;
        }
    </style>
</head>
<body>
    <h2>比賽賽程總覽</h2>
"""

# 遍歷每個球場及比賽
for court in root.findall('court'):
    court_name = court.get('name')
    html += f"<h3>{court_name}</h3>"
    html += """
    <table>
        <tr>
            <th>Round</th>
            <th>Team L</th>
            <th>Team L Player 1</th>
            <th>Team L Player 2</th>
            <th>Score</th>
            <th>Team R</th>
            <th>Team R Player 1</th>
            <th>Team R Player 2</th>
        </tr>
    """
    for match in court.findall('match'):
        round_num = match.get('round', '')
        teamL = match.get('teamL', '')
        teamR = match.get('teamR', '')
        teamLPlayer1 = match.get('teamLPlayer1', '')
        teamLPlayer2 = match.get('teamLPlayer2', '')
        teamRPlayer1 = match.get('teamRPlayer1', '')
        teamRPlayer2 = match.get('teamRPlayer2', '')
        teamLScore = match.get('teamLScore', '')
        teamRScore = match.get('teamRScore', '')

        html += f"""
        <tr>
            <td>{round_num}</td>
            <td>{teamL}</td>
            <td>{teamLPlayer1}</td>
            <td>{teamLPlayer2}</td>
            <td>{teamLScore} : {teamRScore}</td>
            <td>{teamR}</td>
            <td>{teamRPlayer1}</td>
            <td>{teamRPlayer2}</td>
        </tr>
        """

    html += "</table><br>"

html += """
</body>
</html>
"""

# 寫入 output
os.makedirs("output", exist_ok=True)
with open("output/schedule.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ 已產生 schedule.html")