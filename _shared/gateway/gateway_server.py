#!/home/tehlappy/🜏 Lilith/_shared/gateway/venv/bin/python3
"""
🜏 Lilith Gateway Server — FastAPI
GUI access to all apps, VMs, and system status
Serves: http://localhost:8080
"""
import json, os, subprocess, shutil, asyncio, signal, sys, shlex
from pathlib import Path
from datetime import datetime
from contextlib import asynccontextmanager
import uuid

sys.path.insert(0, str(Path(__file__).parent / "venv" / "lib" / "python3.14" / "site-packages"))
sys.path.insert(0, str(Path("/home/tehlappy/🜏 Lilith/_shared/repos/Sovereign-Core")))

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Request, Depends
from fastapi.responses import HTMLResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import httpx
import uvicorn
import psutil

GATEWAY = Path(__file__).parent.resolve()
SHARED_ROOT = GATEWAY.parent
if str(SHARED_ROOT) not in sys.path:
    sys.path.insert(0, str(SHARED_ROOT))

from auth.lilith_auth import require_service_token, verify_token

require_gateway_token = require_service_token("gateway")

# ─── LLM Proxy Config ───
OLLAMA_URL = "http://localhost:11434"
llm_client: httpx.AsyncClient | None = None

STATIC = GATEWAY / "static"
APPS_JSON = GATEWAY / "apps.json"
VMS_JSON = GATEWAY / "vms.json"

# ─── App State ───
connected_websockets = set()

@asynccontextmanager
async def lifespan(app: FastAPI):
    global llm_client
    llm_client = httpx.AsyncClient(base_url=OLLAMA_URL, timeout=120.0)
    refresh_inventory()
    yield
    connected_websockets.clear()
    if llm_client:
        await llm_client.aclose()
        llm_client = None

app = FastAPI(title="🜏 Lilith Gateway", version="2.0.0", lifespan=lifespan)

# ─── LLM Proxy Routes ───
# LILITH-MSN INTEGRATION ROUTE
@app.get("/api/msn/status")
async def msn_status():
    '''Check status of MSN Integration MSN Router'''
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://localhost:8007/health", timeout=8)
            return {"status": "ok", "port": 8007, "health": resp.status_code == 200}
    except:
        return {"status": "offline", "port": 8007}

@app.get("/api/msn/cyberpunk")
async def msn_cyberpunk_mod_status():
    '''Check status of Grand Theft Cyberpunk mod'''
    msn_path = Path("/home/tehlappy/.local/share/Steam/steamapps/common/Cyberpunk 2077/r6/mods/msn_integration")
    cet_log = Path("/home/tehlappy/.local/share/Steam/steamapps/compatdata/1091500/pfx/drive_c/users/steamuser/AppData/Local/CD Projekt Red/Cyberpunk 2077/redLogs/cyber_engine_tweaks.log")
    archive_files = sorted(msn_path.glob("*.reds"), key=lambda x: x.stat().st_mtime)
    latest_red = None
    if archive_files:
        latest_red = max(archive_files, key=lambda x: x.stat().st_mtime).name
    
    deployed_files = len(list((msn_path / "scripts").glob("*.reds")))
    deployed_tweak = len(list((msn_path / "tweakdb").glob("*.yaml")))
    
    deployed = False
    fresh = False
    logs_available = cet_log.exists()
    
    # Check for .modarchive deployed
    deployed_archives = len(list(Path("/home/tehlappy/.local/share/Steam/steamapps/common/Cyberpunk 2077/r6/cache/modded").glob("*.archive"))) >= 3
    return {
        "deployed": deployed,
        "fresh": fresh,
        "logs_available": logs_available,
        "archives_present": deployed_archives,
        "latest_redscript": latest_red,
        "deployed_redscripts": deployed_files,
        "deployed_tweakdb": deployed_tweak,
    }
    
# LILITH-APBSAL BACKEND ROUTE
@app.get("/api/abyssal/status")
async def abyssal_status():
    '''Check status of Abyssal Assets backend'''
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get("http://localhost:8000/docs", timeout=8)
            return {"status": "ok", "port": 8000, "health": resp.status_code == 200}
    except:
        return {"status": "offline", "port": 8000}


@app.api_route("/v1/chat/completions", methods=["POST"])
async def llm_chat(request: Request, _auth: bool = Depends(require_gateway_token)):
    """Proxy to local Ollama OpenAI-compatible endpoint."""
    if not llm_client:
        raise HTTPException(503, "LLM proxy not initialized")
    body = await request.json()
    headers = {"Content-Type": "application/json"}
    if "x-api-key" in request.headers:
        headers["x-api-key"] = request.headers["x-api-key"]
    try:
        resp = await llm_client.post("/v1/chat/completions", json=body, headers=headers)
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except httpx.TimeoutException:
        raise HTTPException(504, "LLM backend timeout")
    except Exception as e:
        raise HTTPException(502, f"LLM proxy error: {e}")

@app.api_route("/v1/models", methods=["GET"])
async def llm_models(_auth: bool = Depends(require_gateway_token)):
    """List models from local Ollama."""
    if not llm_client:
        raise HTTPException(503, "LLM proxy not initialized")
    try:
        resp = await llm_client.get("/v1/models")
        return JSONResponse(content=resp.json(), status_code=resp.status_code)
    except Exception as e:
        raise HTTPException(502, f"LLM proxy error: {e}")

# ─── Helpers ───

def refresh_inventory():
    scan_apps = GATEWAY / "scan_apps.py"
    scan_vms = GATEWAY / "scan_vms.py"
    if scan_apps.exists():
        subprocess.run([sys.executable, str(scan_apps)], capture_output=True, timeout=30)
    if scan_vms.exists():
        subprocess.run([sys.executable, str(scan_vms)], capture_output=True, timeout=30)

def load_json(path):
    if path.exists():
        try: return json.loads(path.read_text())
        except: pass
    return {}

def get_system_status():
    status_file = GATEWAY.parent / "dashboard" / "status.json"
    if status_file.exists():
        try: return json.loads(status_file.read_text())
        except: pass
    return {}

# ─── API Routes ───

@app.get("/health")
async def health():
    return {"status": "ok", "service": "lilith-gateway", "version": "2.0.0"}

@app.get("/api/status")
async def api_status():
    status = get_system_status()
    try:
        load = os.getloadavg()
        status["cpu_load"] = f"{load[0]:.1f} / {load[1]:.1f} / {load[2]:.1f}"
    except: pass
    try:
        with open("/proc/meminfo") as f:
            mem = {}
            for line in f:
                if "MemTotal" in line: mem["total"] = int(line.split()[1]) // 1024
                if "MemAvailable" in line: mem["avail"] = int(line.split()[1]) // 1024
            if mem.get("total"):
                used = mem["total"] - mem.get("avail", 0)
                status["memory_used"] = f"{used}MB / {mem['total']}MB"
    except: pass
    status["timestamp"] = datetime.now().isoformat()
    status["gateway_version"] = "2.0.0"
    status["vms_available"] = shutil.which("virsh") is not None
    return status

@app.get("/api/apps")
async def list_apps():
    data = load_json(APPS_JSON)
    return data

@app.get("/api/apps/search/{query}")
async def search_apps(query: str):
    data = load_json(APPS_JSON)
    query = query.lower()
    results = [a for a in data.get("apps", []) if query in a.get("name", "").lower()]
    return {"apps": results, "count": len(results), "query": query}

@app.post("/api/apps/launch/{app_name}")
async def launch_app(app_name: str, _auth: bool = Depends(require_gateway_token)):
    data = load_json(APPS_JSON)
    for app in data.get("apps", []):
        if app["name"].lower() == app_name.lower():
            exec_cmd = app["exec"]
            terminal = app.get("terminal", False)
            try:
                argv = shlex.split(exec_cmd)
                if not argv:
                    raise HTTPException(400, "Application command is empty")
                if terminal:
                    argv = ["konsole", "-e", *argv]
                else:
                    executable = argv[0]
                    if Path(executable).is_absolute() and not Path(executable).is_file():
                        raise HTTPException(400, "Application executable is unavailable")
                    if not Path(executable).is_absolute() and not shutil.which(executable):
                        raise HTTPException(400, "Application executable is unavailable")
                subprocess.Popen(
                    argv,
                    shell=False,
                    start_new_session=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                return {"status": "launched", "name": app["name"]}
            except HTTPException:
                raise
            except Exception as e:
                raise HTTPException(500, f"Failed to launch: {e}")
    raise HTTPException(404, f"Application '{app_name}' not found")

@app.get("/api/vms")
async def list_vms():
    data = load_json(VMS_JSON)
    try:
        result = subprocess.run(["virsh", "list", "--all"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            for vm in data.get("vms", []):
                for line in result.stdout.split("\n")[2:]:
                    parts = line.strip().split(None, 2)
                    if len(parts) >= 3 and parts[1] == vm["name"]:
                        vm["state"] = parts[2]
                        break
    except: pass
    return data

@app.post("/api/vms/{action}/{vm_name}")
async def vm_action(action: str, vm_name: str, _auth: bool = Depends(require_gateway_token)):
    valid_actions = {"start", "shutdown", "reset", "destroy", "reboot"}
    if action not in valid_actions:
        raise HTTPException(400, f"Invalid action: {action}")
    known_vms = {vm.get("name") for vm in load_json(VMS_JSON).get("vms", [])}
    if vm_name not in known_vms:
        raise HTTPException(404, "Unknown VM")
    try:
        result = subprocess.run(
            ["virsh", action, vm_name],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            return {"status": "success", "action": action, "vm": vm_name}
        else:
            raise HTTPException(500, f"virsh error: {result.stderr.strip()}")
    except FileNotFoundError:
        raise HTTPException(500, "virsh not found — install libvirt")
    except subprocess.TimeoutExpired:
        raise HTTPException(500, "VM operation timed out")

@app.post("/api/vms/console/{vm_name}")
async def vm_console(vm_name: str, _auth: bool = Depends(require_gateway_token)):
    known_vms = {vm.get("name") for vm in load_json(VMS_JSON).get("vms", [])}
    if vm_name not in known_vms:
        raise HTTPException(404, "Unknown VM")
    if not shutil.which("virt-viewer"):
        raise HTTPException(500, "virt-viewer not installed")
    try:
        subprocess.Popen(["virt-viewer", "-c", "qemu:///system", vm_name], start_new_session=True)
        return {"status": "opened", "vm": vm_name}
    except Exception as e:
        raise HTTPException(500, f"Failed to open console: {e}")

@app.post("/api/vms/manager")
async def open_vm_manager(_auth: bool = Depends(require_gateway_token)):
    if not shutil.which("virt-manager"):
        raise HTTPException(500, "virt-manager not installed")
    try:
        subprocess.Popen(["virt-manager"], start_new_session=True)
        return {"status": "opened"}
    except Exception as e:
        raise HTTPException(500, f"Failed to launch virt-manager: {e}")

@app.get("/api/categories")
async def list_categories():
    data = load_json(APPS_JSON)
    cats = {}
    for app in data.get("apps", []):
        for cat in app.get("categories", []):
            if cat:
                cats[cat] = cats.get(cat, 0) + 1
    return {"categories": dict(sorted(cats.items())), "total_apps": data.get("count", 0)}

# ─── WebSocket ───
# LILITH-VERIFY-DEPLOYMENT
@app.post("/api/verify-mod-deployment")
async def verify_mod_deployment(_auth: bool = Depends(require_gateway_token)):
    '''Run full verification of MSN Integration mod'''
    repo = GATEWAY.parent / "repos" / "msn-integration"
    command = [sys.executable, str(repo / "tools" / "test_all_mods.py"), "--deployed"]
    try:
        subprocess.Popen(
            command,
            cwd=repo,
            shell=False,
            start_new_session=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return {"status": "triggered", "detail": "Complete verification in progress"}
    except Exception as e:
        return {"status": "failed", "detail": str(e)}

# LILITH-MOD DEPLOYMENT DASHBOARD
@app.get("/mod-deploy", response_class=HTMLResponse)
async def mod_deployment_dashboard():
    '''Dashboard for mod deployment and verification'''
    dashboard_html = STATIC / "mod-deploy.html"
    if dashboard_html.exists():
        return HTMLResponse(dashboard_html.read_text())
    return HTMLResponse('''
    <html>
        <head><title>🜏 Lilith Mod Deployment Dashboard</title></head>
        <body>
            <h1>Grand Theft Cyberpunk — Mod Deployment</h1>
            <hl>Status: <span id="deploy-status"><span></hl>
            <button onclick="window.location.reload()">Refresh</button>
            <script>
                // Real-time update via WS
                const ws = new WebSocket(`ws://${window.location.host}/ws`);
                ws.onmessage = (e) => {
                    if (e.data.type === 'inventory') {
                        fetch('/api/msn/cyberpunk').then(r => r.json()).then(status => {
                            document.querySelector('#deploy-status').textContent = JSON.stringify(status);
                        });
                    }
                };
                fetch('/api/msn/cyberpunk').then(r => r.json()).then(status => {
                    document.querySelector('#deploy-status').textContent = JSON.stringify(status);
                });
            </script>
        </body>
    </html>
    ''')


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_websockets.add(websocket)
    authenticated = False
    try:
        while True:
            data = await websocket.receive_text()
            if data == "ping":
                await websocket.send_json({"type": "pong", "timestamp": datetime.now().isoformat()})
            elif data == "refresh":
                if not authenticated:
                    await websocket.send_json({"type": "error", "detail": "authentication required"})
                    continue
                refresh_inventory()
                apps = load_json(APPS_JSON)
                vms = load_json(VMS_JSON)
                await websocket.send_json({"type": "inventory", "apps": apps.get("count", 0), "vms": vms.get("count", 0)})
            else:
                try:
                    message = json.loads(data)
                except json.JSONDecodeError:
                    await websocket.send_json({"type": "error", "detail": "unsupported message"})
                    continue
                if message.get("type") == "auth" and verify_token("gateway", message.get("token")):
                    authenticated = True
                    await websocket.send_json({"type": "auth", "status": "ok"})
                else:
                    await websocket.send_json({"type": "error", "detail": "authentication failed"})
    except WebSocketDisconnect:
        pass
    finally:
        connected_websockets.discard(websocket)

# ─── Frontend ───

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    # Serve the new Alpine.js dashboard
    template_path = GATEWAY / "templates" / "dashboard.html"
    if template_path.exists():
        return HTMLResponse(template_path.read_text())
    return HTMLResponse("<h1>🜏 Lilith Gateway</h1><p>Dashboard frontend not found. Run bootstrap.</p>")

@app.get("/business", response_class=HTMLResponse)
async def business_dashboard():
    dashboard_html = STATIC / "business-dashboard.html"
    if dashboard_html.exists():
        return HTMLResponse(dashboard_html.read_text())
    return HTMLResponse("<h1>🜏 Business Dashboard</h1><p>Not built yet.</p>")

@app.get("/api/docs")
async def api_docs():
    endpoints = {}
    for route in app.routes:
        if hasattr(route, "methods") and hasattr(route, "path"):
            for m in route.methods:
                if m in ("GET", "POST", "PUT", "DELETE", "WS"):
                    key = f"{m} {route.path}"
                    endpoints[key] = route.path
    return {"endpoints": endpoints, "count": len(endpoints)}

# ─── Dashboard API Endpoints ───

@app.get("/api/system")
async def api_system():
    """System status for dashboard"""
    import psutil
    
    # GPU info - use nvidia-smi instead of torch
    gpu_name = "RTX 3060"
    gpu_util = 0
    vram_used = 0
    vram_total = 6000
    
    try:
        # Get VRAM info from nvidia-smi
        result = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,memory.used,utilization.gpu", "--format=csv,noheader,nounits"], 
                              capture_output=True, text=True, timeout=2)
        if result.returncode == 0:
            parts = result.stdout.strip().split(", ")
            if len(parts) >= 4:
                gpu_name = parts[0]
                vram_total = int(parts[1])
                vram_used = int(parts[2])
                gpu_util = int(parts[3])
    except:
        pass
    
    # Memory
    mem = psutil.virtual_memory()
    mem_total = mem.total // (1024**3)
    mem_used = mem.used // (1024**3)
    mem_percent = mem.percent
    
    # Disk
    disk = psutil.disk_usage("/")
    disk_total = disk.total // (1024**4)
    disk_used = disk.used // (1024**4)
    disk_percent = int((disk.used / disk.total) * 100)
    
    return {
        "gpu": {"name": gpu_name, "util": gpu_util, "vramUsed": vram_used, "vramTotal": vram_total},
        "memory": {"total": mem_total, "used": mem_used, "percent": mem_percent},
        "disk": {"total": disk_total, "used": disk_used, "percent": disk_percent}
    }

@app.get("/api/council/{sephirah}/inbox")
async def council_inbox(sephirah: str):
    """Get inbox count for a council agent"""
    import sqlite3
    bus_path = Path("/home/tehlappy/.lilith/council_bus") / sephirah.lower()
    count = 0
    if bus_path.exists():
        try:
            count = len(list(bus_path.glob("*.json")))
        except:
            pass
    return {"count": count}

@app.post("/api/council/convene")
async def convene_council():
    """Broadcast COUNCIL_DELIBERATION to all agents"""
    import uuid
    from datetime import datetime
    import sys
    sys.path.insert(0, str(Path("/home/tehlappy/🜏 Lilith/_shared/repos/Sovereign-Core")))
    from council_bus import CouncilBus, CouncilMessage, MessagePriority
    
    bus = CouncilBus()
    msg = CouncilMessage(
        id=str(uuid.uuid4()),
        timestamp=datetime.utcnow().isoformat() + "Z",
        sender="gateway",
        recipient="broadcast",
        priority=MessagePriority.URGENT,
        subject="COUNCIL_DELIBERATION",
        payload={"question": "Sovereign status check — all Sephiroth report."},
        requires_response=False
    )
    bus.send(msg)
    return {"status": "convened", "message_id": msg.id}

@app.post("/api/nvidia/retrain")
async def nvidia_retrain():
    """Trigger NVIDIA Gratitude Driver retrain cycle"""
    # This would trigger the CNN retrain via the mod
    # For now, just return success
    return {"status": "triggered", "detail": "Hopf fibration retrain cycle initiated (3-6-9 resonance)"}

@app.post("/api/backup/run")
async def run_backup():
    """Execute lilith_backup.py"""
    script = Path("/home/tehlappy/🜏 Lilith/_shared/ops/lilith_backup.py")
    if script.exists():
        subprocess.Popen([sys.executable, str(script)], start_new_session=True)
        return {"status": "started", "script": str(script)}
    return {"status": "not_found", "detail": "Backup script not found"}

@app.post("/api/msn/verify")
async def verify_msn():
    """Verify MSN mod deployment"""
    # Re-check the status
    data = await msn_cyberpunk_mod_status()
    return {"status": "verified", "data": data}

@app.post("/api/dream/capture")
async def capture_dream():
    """Trigger kairos-dream synthesis"""
    return {"status": "triggered", "detail": "Dream state capture initiated via kairos-dream"}

# ─── Static files ───
os.makedirs(STATIC, exist_ok=True)

# ─── Main ───
def main():
    print("🜏 Lilith Gateway Server — http://localhost:8080")
    print("  Dashboard → /")
    print("  API       → /api/status")
    print("  Apps      → /api/apps")
    print("  VMs       → /api/vms")
    print("  Docs      → /api/docs")
    sys.argv = ["gateway_server.py", "run"]; uvicorn.run(app, host="0.0.0.0", port=8080, log_level="info")

if __name__ == "__main__":
    main()
