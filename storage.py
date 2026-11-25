#!/usr/bin/env python3
"""
Storage Intelligence - live dashboard for YOUR laptop's disk (Windows/macOS/Linux).
Run:  python storage_dashboard.py      (Mac/Linux: python3 storage_dashboard.py)
It opens http://localhost:8000 in your browser. Press Ctrl+C in the terminal to stop.
No packages to install.
"""
import json
import shutil
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

PORT = 8000
GB = 1024 ** 3


def get_storage():
    root = Path.home().anchor or "/"          # C:\ on Windows, / on Mac/Linux
    total, used, free = shutil.disk_usage(root)
    pct = used / total * 100
    if pct < 60:
        status, msg = "Healthy", "Storage is healthy. You have enough free space."
    elif pct < 80:
        status, msg = "Moderate", "Storage is getting fuller. Review large files and your Downloads folder soon."
    elif pct < 90:
        status, msg = "Warning", "Storage is running low. Delete unused apps, old downloads and duplicates."
    else:
        status, msg = "Critical", "Storage is almost full. Free up space now to avoid slowdowns and failed updates."
    return {
        "drive": root,
        "total": round(total / GB, 2),
        "used": round(used / GB, 2),
        "free": round(free / GB, 2),
        "percent": round(pct, 1),
        "status": status,
        "message": msg,
    }


PAGE = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Storage Intelligence</title>
<style>
  :root{--bg1:#16264a;--bg2:#070b16;--card:#111a2e;--line:#27324d;--text:#f2f5fb;--muted:#9aa6c0;
        --blue:#5b9cff;--purple:#a06bff;--teal:#33d6bf;--ok:#33d6bf;--mid:#f5c542;--warn:#ff9a3c;--crit:#ff5c6c}
  *{box-sizing:border-box}
  body{margin:0;min-height:100vh;color:var(--text);font-family:"Segoe UI",system-ui,sans-serif;
       background:linear-gradient(135deg,var(--bg1),var(--bg2) 60%);padding:28px 16px 48px}
  .wrap{max-width:1130px;margin:0 auto}
  h1{margin:0;font-size:32px}
  .sub{color:var(--muted);margin:10px 0 26px}
  .stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:18px}
  .card{background:var(--card);border:1px solid var(--line);border-radius:22px;padding:24px}
  .label{color:var(--muted);font-size:15px}
  .num{font-size:34px;font-weight:700;margin-top:14px}
  .grad-b{background:linear-gradient(90deg,var(--blue),#4f8cff);-webkit-background-clip:text;background-clip:text;color:transparent}
  .grad-p{background:linear-gradient(90deg,var(--purple),#d38bff);-webkit-background-clip:text;background-clip:text;color:transparent}
  .grad-t{background:linear-gradient(90deg,var(--teal),#5fe3a1);-webkit-background-clip:text;background-clip:text;color:transparent}
  .badge{margin-top:8px;font-size:15px}
  .dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:6px;background:var(--ok)}
  .grid{display:grid;grid-template-columns:1.2fr 1fr;gap:18px;margin-top:22px}
  @media(max-width:800px){.grid{grid-template-columns:1fr}}
  h2{margin:0 0 18px;font-size:20px}
  .legend{display:flex;gap:16px;justify-content:center;font-size:13px;margin-bottom:10px}
  .legend i{display:inline-block;width:34px;height:12px;vertical-align:middle;margin-right:6px}
  canvas{display:block;margin:0 auto;max-width:100%}
  .msg{background:#12223f;border-radius:14px;padding:18px 20px;line-height:1.5}
  button{margin-top:22px;border:0;color:#fff;font-size:15px;padding:13px 20px;border-radius:12px;cursor:pointer;
         background:linear-gradient(90deg,#4f7bff,#9b6bff)}
  button:focus-visible{outline:3px solid #fff;outline-offset:2px}
  .stamp{color:var(--muted);font-size:13px;margin-top:16px}
</style></head>
<body><div class="wrap">
  <h1>Storage Intelligence</h1>
  <p class="sub">Live storage monitor for <span id="drive">your laptop</span></p>

  <section class="stats">
    <div class="card"><div class="label">Total storage</div><div class="num grad-b" id="total">-</div></div>
    <div class="card"><div class="label">Used storage</div><div class="num grad-p" id="used">-</div></div>
    <div class="card"><div class="label">Free storage</div><div class="num grad-t" id="free">-</div></div>
    <div class="card"><div class="label">Storage usage</div><div class="num" id="pct">-</div>
      <div class="badge"><span class="dot" id="dot"></span><span id="status">-</span></div></div>
  </section>

  <section class="grid">
    <div class="card">
      <h2>Storage usage chart</h2>
      <div class="legend"><span><i style="background:var(--purple)"></i>Used</span><span><i style="background:var(--teal)"></i>Free</span></div>
      <canvas id="chart" width="360" height="360" role="img" aria-label="Donut chart of used and free storage"></canvas>
    </div>
    <div class="card">
      <h2>Smart storage analysis</h2>
      <div class="msg" id="msg">Reading your disk...</div>
      <button id="refresh">Refresh storage</button>
      <div class="stamp" id="stamp"></div>
    </div>
  </section>
</div>
<script>
const $ = id => document.getElementById(id);
const colors = {Healthy:"#33d6bf", Moderate:"#f5c542", Warning:"#ff9a3c", Critical:"#ff5c6c"};

function drawDonut(used, free){
  const c = $("chart"), g = c.getContext("2d"), cx = 180, cy = 180, r = 140, w = 50;
  g.clearRect(0,0,360,360);
  const total = used + free, start = -Math.PI/2;
  const usedAngle = used/total * 2*Math.PI;
  const seg = (a,b,col) => { g.beginPath(); g.arc(cx,cy,r,a,b); g.lineWidth=w; g.strokeStyle=col; g.stroke(); };
  seg(start, start+usedAngle, "#a06bff");
  seg(start+usedAngle, start+2*Math.PI, "#33d6bf");
}

async function load(){
  $("msg").textContent = "Reading your disk...";
  try{
    const d = await (await fetch("/api/storage")).json();
    $("drive").textContent = "drive " + d.drive;
    $("total").textContent = d.total.toFixed(2) + " GB";
    $("used").textContent  = d.used.toFixed(2) + " GB";
    $("free").textContent  = d.free.toFixed(2) + " GB";
    $("pct").textContent   = d.percent.toFixed(1) + "%";
    $("status").textContent = d.status;
    $("dot").style.background = colors[d.status];
    $("msg").textContent = d.message;
    $("stamp").textContent = "Last updated " + new Date().toLocaleTimeString();
    drawDonut(d.used, d.free);
  }catch(e){
    $("msg").textContent = "Could not read storage. Make sure the Python script is still running.";
  }
}
$("refresh").addEventListener("click", load);
load();
</script></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/storage"):
            body, ctype = json.dumps(get_storage()).encode(), "application/json"
        elif self.path in ("/", "/index.html"):
            body, ctype = PAGE.encode("utf-8"), "text/html; charset=utf-8"
        else:
            self.send_error(404)
            return
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):   # keep the terminal quiet
        pass


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", PORT), Handler)   # local only, not exposed to the network
    url = f"http://localhost:{PORT}"
    print(f"Storage Intelligence running at {url}  (Ctrl+C to stop)")
    threading.Timer(0.8, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")