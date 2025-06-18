import os
import random

first_names = ["Alex", "Jamie", "Casey", "Jordan", "Taylor", "Morgan", "Bailey", "Riley", "Quinn", "Skyler"]
last_names = ["Lee", "Chen", "Kim", "Patel", "Smith", "Brown", "Nguyen", "Garcia", "Martinez", "Walker"]
suits = ["\u2660", "\u2663", "J\u2663", "Q\u2663", "K\u2663", "A\u2663", "\u2665", "\u2666", "J\u2665", "Q\u2665", "K\u2665", "A\u2665"]

players = [f"{random.choice(last_names)}{random.choice(first_names)}" for _ in range(32)]
random.shuffle(players)

categories = {
    "Day-Beginner": ['華啟梅','陶家樂','胡小蓮','孟愛貞','林 臻','莊家玲','邱如玉','施蓉蓉','謝元興'],
    "Day-Advanced": ['羅天文','李彤庭'],
    "Night-Beginner": ['華啟梅','徐慶如','Alexander Nguyen','Joy Liu','吳尚真','李倩','溫孟璇','Joseph Richardson'],
    "Night-Advanced": ['張立揚','William Hou','湯士昀']
}

html = """
<!DOCTYPE html>
<html lang='en'>
<head>
  <meta charset='UTF-8'>
  <meta name='viewport' content='width=device-width, initial-scale=1.0'>
  <title>分組管理</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <style>
    .player-tag {
      box-shadow: inset 0 1px 2px rgba(0,0,0,0.15);
      border: 2px solid #60a5fa;
    }
    .group-slot .symbol {
      cursor: pointer;
    }
    .symbol-picker {
      position: absolute;
      display: none;
      z-index: 50;
    }
    .symbol-picker button {
      width: 3.0rem;
      height: 2.5rem;
      margin: 0.25rem;
      font-size: 1.25rem;
      font-family: revert;
      border: 1px solid #ccc;
      border-radius: 0.375rem;
      background-color: #f9fafb;
    }
  </style>
</head>
<body class="bg-gray-100 min-h-screen p-6">
  <h1 class="text-2xl font-bold mb-4 text-center">🏓 分組管理</h1>
  <div class='grid grid-cols-2 gap-6 bg-white p-6 rounded shadow-lg mb-6 relative'>
    <div id="symbol-picker" class="symbol-picker bg-white border rounded shadow p-2 flex flex-wrap w-64 hidden"></div>
"""

html += "<div class='col-span-2 grid grid-cols-2 md:grid-cols-4 gap-4'>\n"
for label, names in categories.items():
    html += f"<div><h2 class='font-semibold text-lg mb-2'>{label}</h2><div class='flex flex-wrap gap-2'>"
    for name in names:
        html += f"<div class='player-tag px-3 py-1 bg-blue-100 text-blue-900 rounded-full cursor-move' draggable='true'>{name}</div>"
    html += "</div></div>"
html += "</div>"

for section in ["Beginner", "Advanced"]:
    html += f"""
    <div class="bg-slate-50 shadow-inner p-4 rounded border">
      <h2 class="text-lg font-semibold mb-4">{section}</h2>
      <div class="space-y-3 group-type" id="{section.lower()}-groups" data-type="{section.lower()}">
    """
    for _ in range(3):
        html += f"""
        <div class="group-slot flex items-center p-2 bg-white border-2 border-gray-300 rounded shadow">
          <button onclick="openSymbolPicker(this)" class="symbol mr-4 w-16 h-10 flex items-center justify-center border border-gray-500 rounded text-xl">?</button>
          <div class="flex flex-wrap gap-2"></div>
        </div>
        """
    html += f"""
      </div>
      <button onclick="addGroup('{section.lower()}-groups')" class="mt-3 px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600">新增空間</button>
    </div>
    """

html += "</div>"

html += """
<div class="mt-6 text-center">
  <button onclick="generateScheduleXMLFromGroups()" class="mt-4 px-4 py-2 bg-green-600 text-white rounded shadow">
  產生賽程 XML
</button>
</div>
<script>
  const suits = ["♠️", "♣️", "J♣️", "Q♣️", "K♣️", "A♣️", "♥️", "♦️", "J♥️", "Q♥️", "K♥️", "A♥️", "J♠️", "Q♠️", "K♠️", "A♠️"];
  let dragged = null;
  let currentSymbolBtn = null;

  document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll('.player-tag').forEach(el => {
      el.addEventListener('dragstart', e => dragged = el);
    });
    document.querySelectorAll('.group-slot').forEach(slot => {
      slot.addEventListener('dragover', e => e.preventDefault());
      slot.addEventListener('drop', e => {
        e.preventDefault();
        if (dragged) slot.querySelector('div.flex').appendChild(dragged);
      });
    });

    const picker = document.getElementById("symbol-picker");
    suits.forEach(s => {
      const btn = document.createElement("button");
      btn.textContent = s;
      btn.onclick = () => {
        if (currentSymbolBtn) currentSymbolBtn.textContent = s;
        picker.classList.add('hidden'); picker.classList.remove('flex');
      };
      picker.appendChild(btn);
    });
  });

  function openSymbolPicker(button) {
    currentSymbolBtn = button;
    const picker = document.getElementById("symbol-picker");
    picker.classList.remove('hidden'); picker.classList.add('flex');
    const rect = button.getBoundingClientRect();
    picker.style.top = (window.scrollY + rect.bottom + 4) + 'px';
    picker.style.left = (window.scrollX + rect.left) + 'px';
  }

  function addGroup(containerId) {
    const container = document.getElementById(containerId);
    
    const div = document.createElement('div');
    div.className = "group-slot flex items-center p-2 bg-white border-2 border-gray-300 rounded shadow mt-2";
    div.innerHTML = `
      <button onclick="openSymbolPicker(this)" class="symbol mr-4 w-16 h-10 flex items-center justify-center border border-gray-500 rounded text-xl">?</button>
      <div class="flex flex-wrap gap-2" ></div>
    `;
    container.appendChild(div);

    div.addEventListener('dragover', e => e.preventDefault());
    div.addEventListener('drop', e => {
      e.preventDefault();
      if (dragged) div.querySelector('div.flex').appendChild(dragged);
    });
  }

  function generateXML() {
  let xml = '<?xml version="1.0" encoding="UTF-8"?>\\n<groups>\\n';
  document.querySelectorAll('.group-slot').forEach(slot => {
    const symbol = slot.querySelector('button.symbol')?.textContent.trim() || '?';
    const players = Array.from(slot.querySelectorAll('.player-tag')).map(p => p.textContent.trim());
    if (players.length > 0) {
      xml += `  <team id="${symbol}">\\n`;
      players.forEach(p => {
        xml += `    <player>${p}</player>\\n`;
      });
      xml += '  </team>\\n';
    }
  });
  xml += '</groups>';
  console.log("📂 分組 XML:");
  console.log(xml);
  alert("✅ XML 已顯示於 console");
}

// 🔽 假設：分組區塊中，每一個 .group-slot 代表一組隊伍
//       每個 .group-slot 裡面有 2 個 .player，並且 data-symbol 屬性代表該隊伍的圖示
// 🔽 假設：分組區塊中，每一個 .group-slot 代表一組隊伍
//       每個 .group-slot 裡面有 2 個 .player，並且 data-symbol 屬性代表該隊伍的圖示

function generateScheduleXMLFromGroups() {
  const beginnerCourts = ['A', 'B'];
  const advancedCourt = 'D';
  const courtMap = { A: [], B: [], D: [] };

  const slots = document.querySelectorAll('.group-slot');
  const beginnerTeams = [];
  const advancedTeams = [];

  slots.forEach(slot => {
    const symbol = slot.querySelector('button.symbol')?.textContent.trim() || '?';
    const players = [...slot.querySelectorAll('.player-tag')].map(p => p.innerText.trim()).filter(x => x);
    const type = slot.closest('.group-type').dataset.type; // beginner / advanced

    const team = {
      symbol,
      players,
    };

    if (type === 'beginner') beginnerTeams.push(team);
    else if (type === 'advanced') advancedTeams.push(team);
  });

  function getMatchups(teams) {
    const result = [];
    const n = teams.length;
    if (n < 4) {
      // 全對全
      for (let i = 0; i < n; i++) {
        for (let j = i + 1; j < n; j++) {
          result.push([teams[i], teams[j]]);
        }
      }
    } else {
      // 每隊與不同對手打3場（簡單隨機挑3個）
      for (let i = 0; i < n; i++) {
        const opponents = [...Array(n).keys()].filter(j => j !== i);
        const selected = opponents.slice(0, 3); // 可加隨機打亂
        selected.forEach(j => {
          if (i < j) result.push([teams[i], teams[j]]);
        });
      }
    }
    return result;
  }

  // 🔄 將 beginnerTeams 分成兩半以對應兩個球場
  const half = Math.ceil(beginnerTeams.length / 2);
  const courtABeginnerTeams = beginnerTeams.slice(0, half);
  const courtBBeginnerTeams = beginnerTeams.slice(half);

  const beginnerMatchesA = getMatchups(courtABeginnerTeams);
  const beginnerMatchesB = getMatchups(courtBBeginnerTeams);
  const advancedMatches = getMatchups(advancedTeams);

  beginnerMatchesA.forEach((pair) => {
    courtMap['A'].push({
      teamL: pair[0],
      teamR: pair[1],
      isBeginner: true,
    });
  });

  beginnerMatchesB.forEach((pair) => {
    courtMap['B'].push({
      teamL: pair[0],
      teamR: pair[1],
      isBeginner: true,
    });
  });

  advancedMatches.forEach(pair => {
    courtMap[advancedCourt].push({
      teamL: pair[0],
      teamR: pair[1],
      isBeginner: false,
    });
  });

  // 🔽 建立 XML 字串
  let xml = `<?xml version="1.0" encoding="UTF-8"?>\n<schedule>\n`;
  Object.entries(courtMap).forEach(([courtId, matches]) => {
    xml += `  <court name="Court ${courtId}">\n`;
    matches.forEach(match => {
      const t1 = match.teamL;
      const t2 = match.teamR;
      xml += `    <match 
      teamL="${t1.symbol}" teamR="${t2.symbol}"
      teamLPlayer1="${t1.players[0] || ''}" teamLPlayer2="${t1.players[1] || ''}"
      teamRPlayer1="${t2.players[0] || ''}" teamRPlayer2="${t2.players[1] || ''}"
      court="${courtId}" teamLScore="" teamRScore=""
      isBeginner="${match.isBeginner}" round=""/>\n`;
    });
    xml += `  </court>\n`;
  });
  xml += '</schedule>';

  console.log('📄 賽程 XML:', xml);
  alert('✅ 已產生賽程 XML，可於 console 複製。');
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
