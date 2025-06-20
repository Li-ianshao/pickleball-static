import xml.etree.ElementTree as ET
import urllib.request

# 從 GitHub 上讀取 XML
url = 'https://raw.githubusercontent.com/Li-ianshao/pickleball-static/main/static/schedule.xml'
with urllib.request.urlopen(url) as response:
    xml_data = response.read()
    root = ET.fromstring(xml_data)

# 預設排序 match（需先轉數字 round）
def sorted_matches(court):
    return sorted(
        court.findall('match'),
        key=lambda m: int(m.get('round') or 9999)
    )

html = """
<!DOCTYPE html>
<html lang='zh'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>比賽賽程總覽</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    .match-box {
      border-radius: 0.75rem;
      border: 1px solid #d1d5db;
      box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
      padding: 0.75rem;
      position: relative;
      background-color: white;
    }
    .match-box.finished { background-color: #f3f4f6; }
    .match-box.running-beginner { background-color: #dbeafe; }
    .match-box.running-advanced { background-color: #fef9c3; }
    .round-tab {
      position: absolute;
      top: -1rem;
      left: 1rem;
      padding: 0.25rem 0.75rem;
      border-radius: 0.375rem 0.375rem 0 0;
      font-size: 0.875rem;
      font-weight: 600;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
      background-color: white;
      border: 1px solid #e5e7eb;
    }
    .match-container {
      display: flex;
      justify-content: space-between;
      font-size: 1rem;
      font-weight: 500;
      margin-top: 0.5rem;
    }
    .player-col { width: 33%; }
    .score-col { width: 33%; text-align: center; font-weight: bold; }
  </style>
</head>
<body class="bg-gray-100 min-h-screen p-4">
  <h1 class="text-2xl font-bold text-center mb-6">比賽賽程總覽</h1>
  <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
"""

# 場地排序依序 A → B → C → D
for court in ['Court A', 'Court B', 'Court C', 'Court D']:
    court_elem = root.find(f".//court[@name='{court}']")

    title = f"{court} ({'Beginner - Intermediate' if court in ['Court A', 'Court B'] else 'Advanced' if court == 'Court D' else 'Practice'})"
    html += f"<div class='bg-white rounded-lg shadow p-4'><h2 class='text-lg font-semibold mb-4'>{title}</h2>"

    if court_elem is None:
        html += "<p class='text-gray-500'>本球場作為練習用途，暫無比賽安排。</p></div>"
        continue

    matches = sorted_matches(court_elem)
    prev_status = None

    for idx, match in enumerate(matches):
        tL1 = match.get('teamLPlayer1')
        tL2 = match.get('teamLPlayer2')
        tR1 = match.get('teamRPlayer1')
        tR2 = match.get('teamRPlayer2')
        sL = match.get('teamLScore')
        sR = match.get('teamRScore')
        round_num = match.get('round') or f"{idx+1}"
        beginner = match.get('isBeginner') == 'true'

        if sL and sR:
            status = 'finished'
        else:
            if prev_status == 'finished':
                status = 'running-beginner' if beginner else 'running-advanced'
            else:
                status = ''
        prev_status = status if status.startswith('finished') else prev_status

        html += f"""
        <div class='match-box {status}'>
          <div class='round-tab'>Round {round_num}</div>
          <div class='match-container'>
            <div class='player-col text-left'>{tL1}<br>{tL2}</div>
            <div class='score-col'>{(f"{sL} : {sR}" if sL and sR else "V.S")}</div>
            <div class='player-col text-right'>{tR1}<br>{tR2}</div>
          </div>
        </div>
        """

    html += "</div>"

html += """
  </div>
  <script>
    setInterval(() => location.reload(), 30000);
  </script>
</body>
</html>
"""

with open('schedule.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("✅ schedule.html 已從 GitHub XML 生成完畢")
