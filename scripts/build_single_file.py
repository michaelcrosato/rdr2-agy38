#!/usr/bin/env python3
import os
import re

def build():
    # 1. Read engine
    with open('my-3d2dge-agent.js', 'r', encoding='utf-8') as f:
        engine_code = f.read()
    # In HTML, any '</script>' inside a script block closes the tag immediately
    engine_code = engine_code.replace('</script>', '<\\/script>')

    # 2. Read data files (strip export statements)
    with open('src/data/missions.js', 'r', encoding='utf-8') as f:
        missions_code = f.read()
    missions_code = re.sub(r'export\s+const\s+MISSIONS\s*=', 'const MISSIONS =', missions_code)

    with open('src/data/compendium.js', 'r', encoding='utf-8') as f:
        compendium_code = f.read()
    compendium_code = re.sub(r'export\s+const\s+', 'const ', compendium_code)

    # 3. Read systems (strip export / import statements)
    systems = ['audio.js', 'deadeye.js', 'horse.js', 'combat.js', 'world.js', 'law.js', 'hunting.js', 'camp.js', 'minigames.js', 'journal.js', 'mission-runner.js']
    systems_code = ""
    for sys in systems:
        path = os.path.join('src/systems', sys)
        with open(path, 'r', encoding='utf-8') as f:
            code = f.read()
        # strip imports and exports
        code = re.sub(r'import\s+[^;]+;\n?', '', code)
        code = re.sub(r'export\s+(class|const|function)', r'\1', code)
        systems_code += f"\n// === SYSTEM: {sys} ===\n" + code + "\n"

    # 4. Read game.js (strip imports)
    with open('src/game.js', 'r', encoding='utf-8') as f:
        game_code = f.read()
    game_code = re.sub(r'import\s+[^;]+;\n?', '', game_code)

    # 5. Read index.html to extract styles and HTML shell
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Extract CSS from <style>...</style>
    style_match = re.search(r'<style>(.*?)</style>', html, re.DOTALL)
    css = style_match.group(1) if style_match else ""

    # Extract body content (excluding <script> tags)
    body_match = re.search(r'<body>(.*?)<script', html, re.DOTALL)
    body_content = body_match.group(1).strip() if body_match else ""

    # Assemble complete single-file HTML
    single_html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no, viewport-fit=cover">
  <title>DEAD HORIZON: 1899 — An Outlaw's Redemption</title>
  <style>
{css}
  </style>
</head>
<body>
{body_content}

  <script>
// ============================================================================
// 1. ENGINE FOUNDATION (my-3D2dge AGENT EDITION + WESTERN RIG EXTENSIONS)
// ============================================================================
{engine_code}

// ============================================================================
// 2. DATA (COMPENDIUM & ALL 153 CANONICAL MISSIONS)
// ============================================================================
{compendium_code}

{missions_code}

// ============================================================================
// 3. WESTERN GAMEPLAY SYSTEMS
// ============================================================================
{systems_code}

// ============================================================================
// 4. MASTER GAME LOOP & CONTROLLER
// ============================================================================
{game_code}

// UI Bridge Functions
function triggerShoot() {{ if (window.RDR2Game) window.RDR2Game.shoot(); }}
function triggerDeadeye() {{ if (window.RDR2Game) window.RDR2Game.deadeye(); }}
function triggerMount() {{ if (window.RDR2Game) window.RDR2Game.mount(); }}
function triggerWhistle() {{ if (window.RDR2Game) window.RDR2Game.whistle(); }}
function triggerReload() {{ if (window.RDR2Game) window.RDR2Game.reload(); }}
function openJournal() {{ if (window.RDR2Game) window.RDR2Game.journal(); }}
function openMissions() {{ if (window.RDR2Game) window.RDR2Game.missions(); }}
function triggerPoker() {{ if (window.RDR2Game) window.RDR2Game.poker(); }}

const views = ['threequarter', 'iso', 'topdown', 'brawler'];
let vIdx = 0;
function cycleView() {{
  vIdx = (vIdx + 1) % views.length;
  if (window.RDR2Game && window.RDR2Game.game) {{
    window.RDR2Game.game.setView(views[vIdx]);
  }}
  document.getElementById('btn-view').textContent = 'VIEW: ' + views[vIdx].toUpperCase();
}}

let crtOn = true;
function toggleCRT() {{
  crtOn = !crtOn;
  document.getElementById('viewport').className = (crtOn ? 'crt-effect' : '');
  document.getElementById('btn-crt').textContent = 'CRT: ' + (crtOn ? 'ON' : 'OFF');
}}
  </script>
</body>
</html>
"""

    # Target 1: Windows desktop temp folder
    win_dir = "/mnt/c/Users/micha/OneDrive/Desktop/Deskop/temp"
    os.makedirs(win_dir, exist_ok=True)
    win_target = os.path.join(win_dir, "dead-horizon-1899.html")
    with open(win_target, 'w', encoding='utf-8') as f:
        f.write(single_html)
    print(f"Written single self-contained HTML to: {win_target} (Size: {len(single_html)} bytes)")

    # Target 2: Workspace local file
    local_target = "dead-horizon-1899.html"
    with open(local_target, 'w', encoding='utf-8') as f:
        f.write(single_html)
    print(f"Written local single self-contained HTML to: {local_target} (Size: {len(single_html)} bytes)")

if __name__ == '__main__':
    build()
