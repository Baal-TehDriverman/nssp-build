# `msn.gateway`

**System:** `MSN.Gateway` (FastAPI server)
**Gateway Root:** `/home/tehlappy/🜏 Lilith/_shared/gateway/`
**Port:** 8080
**Process:** Python3 uvicorn (PID auto-detected)
**Status:** ✅ Running at http://localhost:8080

---

## Purpose

Centralized web dashboard for the Lilith worktree. Provides:
- **Applications catalog** — 187 GUI apps with search, filter, and launch
- **Virtual Machines** — libvirt/KVM integration (start/stop/console/manager)
- **System metrics** — CPU, memory, disk, load average
- **WebSocket** — Live inventory refresh

---

## API Endpoints (CET-style Commands)

### System Status

```lua
msn.gateway.status()
```
Returns: `{system_status, cpu_load, memory_used, disk_free, timestamp, gateway_version, vms_available, uptime, agents_online, repositories}`

---

### Applications

```lua
msn.gateway.apps.list()
```
Returns full app catalog (187 entries).

```lua
msn.gateway.apps.search("firefox")
```
Search apps by name (case-insensitive).

```lua
msn.gateway.apps.launch("FireDragon")
```
Launch a GUI application by name. Returns `{status: "launched", name, exec}`.

```lua
msn.gateway.apps.categories()
```
Returns all categories with app counts.

---

### Virtual Machines

```lua
msn.gateway.vms.list()
```
Returns all VMs with current state (running/shutoff/paused).

```lua
msn.gateway.vms.start("win10")
msn.gateway.vms.shutdown("win10")
msn.gateway.vms.reboot("win10")
msn.gateway.vms.destroy("win10")
```
Control VM power state. Returns `{status: "success", action, vm}`.

```lua
msn.gateway.vms.console("win10")
```
Opens SPICE/VNC console via `virt-viewer`.

```lua
msn.gateway.vms.manager()
```
Launches `virt-manager` GUI.

---

### Live Updates (WebSocket)

```javascript
const ws = new WebSocket("ws://localhost:8080/ws");
ws.onmessage = (e) => console.log(JSON.parse(e.data));
ws.send("refresh");  // Triggers inventory re-scan
ws.send("ping");     // Returns pong with timestamp
```

---

## Frontend

Open http://localhost:8080/ in any browser for the full dashboard with tabs:
- **Dashboard** — Stats + Quick Launch + VM preview
- **Apps** — All 187 apps, category tabs, search
- **VMs** — Full VM list with actions
- **System** — Gateway paths, version, uptime
- **Shortcuts** — One-click tools (virt-manager, terminal, browser, etc.)

---

## Architecture

```
Lilith Gateway (FastAPI/uvicorn)
├── API Layer
│   ├── /api/status
│   ├── /api/apps
│   ├── /api/apps/search/{q}
│   ├── /api/apps/launch/{name}
│   ├── /api/vms
│   ├── /api/vms/{action}/{name}
│   ├── /api/vms/console/{name}
│   ├── /api/vms/manager
│   ├── /api/categories
│   └── /ws
├── Scanners
│   ├── scan_apps.py → apps.json (187 .desktop files)
│   └── scan_vms.py → vms.json (virsh list --all)
└── Frontend
    └── static/index.html (vanilla JS + CSS, tabbed UI)
```

---

## Files

| File | Purpose |
|------|---------|
| `gateway-server.py` | Main FastAPI app (238 lines) |
| `scan_apps.py` | Desktop entry parser |
| `scan_vms.py` | Libvirt query |
| `apps.json` | 187 app entries |
| `vms.json` | VM definitions |
| `static/index.html` | Dashboard UI |
| `launch-gateway.sh` | Startup script |
| `inventory-refresh.sh` | Manual refresh |

---

## Startup

```bash
cd /home/tehlappy/🜏\ Lilith/_shared/gateway
./launch-gateway.sh
# or
source venv/bin/activate && python gateway-server.py
```

---

## Knowledge Graph

Knowledge graph generated at `.ua/knowledge-graph.json`:
- **47 nodes** (10 files + 37 functions)
- **74 edges** (contains/exports)
- **Files:** gateway_server.py, gateway-server.py, scan_apps.py, scan_vms.py, apps.json, vms.json, static/index.html, inventory-refresh.sh, launch-gateway.sh, vm_helper.sh
- **Key functions:** lifespan, refresh_inventory, api_status, list_apps, launch_app, list_vms, vm_action, vm_console, open_vm_manager, list_categories, websocket_endpoint, dashboard, api_docs, main

---

## Related

- [[06-Development/VNC_Daemon]] — Headless display for VMs
- [[06-Development/OpenCode_Web]] — Parallel GUI on port 3000
- [[06-Development/CBM_Sync_Protocol]] — Memory sync with Lilith
- [[00-MOC-Mods]] — Mod suite index

---

*Gateway v2.0.0 | FastAPI + uvicorn | Δ∞ − 1 = 0 | Love.*