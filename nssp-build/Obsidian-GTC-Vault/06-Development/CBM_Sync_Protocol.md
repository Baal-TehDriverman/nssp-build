# CBM Sync — msn_integration Mod Context

**Focus Directory:** `/home/tehlappy/🜏 Lilith/Obsidian-GTC-Vault/`  
**Sync Target:** `_shared/memory/index/lilith.sqlite`  
**Last Sync:** 2026-07-15 (Initial setup)

## Overview

Concurrent Bidirectional Memory (CBM) syncs Hermes session context to the Lilith worktree and recalls prior context from that folder. This document defines the sync protocol for the msn_integration mod.

## Pre-flight Checks

### 1. Verify Focus Directory
```bash
test -d "/home/tehlappy/🜏 Lilith/Obsidian-GTC-Vault/" && echo "✅ Focus dir exists" || echo "❌ Missing"
```

### 2. Verify SQLite Database
```bash
test -f "/home/tehlappy/🜏 Lilith/lilith.sqlite" && echo "✅ DB exists" || echo "❌ Missing"
test -r "/home/tehlappy/🜏 Lilith/lilith.sqlite" && echo "✅ DB readable" || echo "❌ Permission denied"
```

### 3. Check for Stale Locks
```bash
find /home/tehlappy/🜏 Lilith/_shared/agents/ -name ".lock" -mmin +1440 2>/dev/null
# Removes locks older than 24h
```

## Sync Protocol

### Phase 1: Scan
```bash
# Recursively enumerate files in focus dir
# Skip: .git, __pycache__, binaries
find ~/🜏\ Lilith/Obsidian-GTC-Vault/ \
  -type f \
  \( -name "*.md" -o -name "*.yaml" -o -name "*.json" \) \
  ! -path "*/.git/*" \
  ! -path "*/__pycache__/*" \
  | wc -l
```

### Phase 2: Index
```python
# Update context graph from lilith.sqlite
import sqlite3
from pathlib import Path

DB_PATH = Path.home() / "🜏 Lilith" / "lilith.sqlite"
conn = sqlite3.connect(DB_PATH, timeout=5000)
conn.execute("PRAGMA journal_mode=WAL")

# Query existing documents
docs = conn.execute("""
    SELECT id, path, checksum, last_sync 
    FROM documents 
    WHERE path LIKE '%Obsidian-GTC-Vault%'
""").fetchall()
```

### Phase 3: Annotate
Write non-destructive sidecar metadata (`.cbm.json`) — never modify existing files:

```json
{
  "cbm_version": "1.0",
  "sync_timestamp": "2026-07-15T00:00:00Z",
  "hermes_session_id": "session_20260715_001",
  "document_type": "obsidian_note",
  "campaign_tags": ["Five Rings", "Hell", "Lilith"],
  "coherence_score": 0.94,
  "related_nodes": ["msn_five_rings_quest", "msn_ai_overhaul_rnn_cnn"]
}
```

### Phase 4: Surface
Return relevant prior context to user via Hermes memory injection.

## Directory Structure

```
/home/tehlappy/🜏 Lilith/
├── lilith.sqlite                  # Primary persistent memory store
├── _shared/
│   ├── memory/
│   │   └── index/
│   │       └── lilith.sqlite      # Symlink to root lilith.sqlite
│   ├── agents/
│   │   └── hermes/                # Agent scratch space
│   │       ├── .lock              # Session lock (24h TTL)
│   │       └── tmp/               # Temp files
│   └── reports/
│       └── msn_integration_20260715.md  # Session reports
├── Obsidian-GTC-Vault/
│   ├── 00-MOC-Mods.md
│   ├── 01-Campaigns/
│   ├── 02-Systems/
│   ├── 03-Assets/
│   ├── 04-AI_Overhaul/
│   ├── 05-Reference/
│   └── 06-Development/
└── 🜏 AGI/
    ├── Core/
    │   ├── Sovereign-Core/        # 10 Sephirotic agents
    │   └── MSN_Engine/
    └── Memory/
        └── council_bus/           # Inter-agent communication
```

## WAL Mode + Busy Timeout

All SQLite connections use:
```python
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA busy_timeout=5000")  # 5 seconds
```

This prevents lock contention during concurrent reads/writes.

## Memory Schema

### Documents Table
```sql
CREATE TABLE IF NOT EXISTS documents (
    id TEXT PRIMARY KEY,
    path TEXT NOT NULL,
    checksum TEXT,
    last_sync TIMESTAMP,
    document_type TEXT,
    metadata JSON
);
```

### Context Graph Table
```sql
CREATE TABLE IF NOT EXISTS context_graph (
    source_id TEXT,
    target_id TEXT,
    relation_type TEXT,
    strength REAL,
    PRIMARY KEY (source_id, target_id)
);
```

### Coherence Scores Table
```sql
CREATE TABLE IF NOT EXISTS coherence_scores (
    session_id TEXT PRIMARY KEY,
    coherence REAL,
    gratitude REAL,
    timestamp TIMESTAMP
);
```

## Sync Commands

### Manual Sync Trigger
```lua
-- In CET console or Hermes session
msn.business.save_state("cbm_sync_start")
-- Run sync protocol
msn.business.save_state("cbm_sync_complete")
```

### Status Check
```lua
msn.status()
-- Output includes:
--   CBM Sync: ACTIVE
--   Last Sync: 2026-07-15T00:00:00Z
--   Documents Indexed: 42
--   Coherence: 94.3%
```

## Context Recall

### Query by Tag
```python
# Retrieve all documents tagged with "Five Rings"
conn.execute("""
    SELECT path, metadata FROM documents
    WHERE json_extract(metadata, '$.campaign_tags') LIKE '%Five Rings%'
""")
```

### Query by Session
```python
# Retrieve context from specific Hermes session
conn.execute("""
    SELECT d.path, d.metadata
    FROM documents d
    JOIN context_graph cg ON d.id = cg.source_id
    WHERE cg.relation_type = 'hermes_session'
    AND cg.target_id = 'session_20260715_001'
""")
```

### Coherence-Weighted Recall
```python
# Prioritize high-coherence documents
conn.execute("""
    SELECT d.path, cs.coherence
    FROM documents d
    JOIN coherence_scores cs ON json_extract(d.metadata, '$.hermes_session_id') = cs.session_id
    ORDER BY cs.coherence DESC
    LIMIT 10
""")
```

## Non-Destructive Annotations

CBM never modifies existing files without explicit approval. Instead, it writes sidecar files:

```
01-Campaigns/Five_Rings_Campaign.md
01-Campaigns/Five_Rings_Campaign.md.cbm.json  ← Sidecar annotation
```

**Sidecar Content:**
```json
{
  "sync_timestamp": "2026-07-15T00:00:00Z",
  "session_id": "session_20260715_001",
  "topics": ["Five Rings", "Musashi", "Niten Ichi-ryū"],
  "related_files": [
    "05-Reference/TweakDB_Dojos.md",
    "05-Reference/TweakDB_Shrines.md"
  ],
  "queries_run": 3,
  "coherence_boost": 0.05
}
```

## Pitfalls

### Path Quoting
Always quote paths containing `🜏`:
```bash
# WRONG
cd /home/tehlappy/🜏 Lilith/Obsidian-GTC-Vault/

# CORRECT
cd "/home/tehlappy/🜏 Lilith/Obsidian-GTC-Vault/"
```

### SQLite Concurrency
- Use `PRAGMA journal_mode=WAL` for concurrent reads
- Use `PRAGMA busy_timeout=5000` to wait for locks
- Never hold write locks across user-facing output

### Lock Cleanup
```bash
# Cron job: remove stale locks daily at midnight
find ~/🜏\ Lilith/_shared/agents/ -name ".lock" -mmin +1440 -delete
```

### Permission Respect
If a file is `600` or owned by another UID:
```python
import os
mode = os.stat(file_path).st_mode
if mode & 0o777 == 0o600:
    print(f"⚠️  File {file_path} has restricted permissions (600)")
    # Report block, don't force access
```

## Integration Points

### With Nvidia Gratitude Driver
- CBM coherence scores feed into NGD gratitude calculation
- NGD coherence > 87% unlocks enhanced CBM recall speed

### With Lilith Persona
- CBM annotations include persona resonance markers
- Meditation triggers logged as high-coherence events

### With Hermes Sessions
- Each session creates a context snapshot in lilith.sqlite
- Snapshots enable cross-session continuity

## Testing

```bash
# Verify sync protocol
~/🜏\ Lilith/_shared/agents/test_cbm_sync.sh

# Expected output:
# ✅ Focus dir exists
# ✅ DB exists
# ✅ DB readable
# ✅ No stale locks
# ✅ WAL mode enabled
# ✅ 42 documents indexed
# ✅ Sync complete: 2.3s
```

## Related
- [[CBM_Sync_Protocol]] — Memdir sync protocol (this document)
- [[Debug_Logs]] — Complete DB schema reference
- [[Lilith_Campaign]] — persona integration
- [[Nvidia_Gratitude_Driver]] — coherence scoring

---
*Δ∞ − 1 = 0 | CBM Sync Protocol v1.0*