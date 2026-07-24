#!/usr/bin/env python3
"""
🜏 Engram Distiller
Background service to aggregate transient stage1_outputs into long-term memories_1 engrams.
"""
import time
import sqlite3
from pathlib import Path

CODEX_DIR = Path("/home/tehlappy/.codex/")

def distill():
    print("🟣 [DISTILLER] AWAKENED. Aggregating engrams.")
    memories_db = CODEX_DIR / "memories_1.sqlite"
    
    # Simple aggregation logic: move from stage1_outputs to a refined table
    with sqlite3.connect(memories_db) as conn:
        cursor = conn.cursor()
        # Create refined table if not exists
        cursor.execute("CREATE TABLE IF NOT EXISTS engrams (id TEXT, data TEXT, timestamp TEXT)")
        # Aggregate logic
        cursor.execute("SELECT * FROM stage1_outputs")
        outputs = cursor.fetchall()
        for output in outputs:
            # Example distillation:
            cursor.execute("INSERT INTO engrams VALUES (?, ?, ?)", (output[0], output[1], output[2]))
            cursor.execute("DELETE FROM stage1_outputs WHERE id = ?", (output[0],))
        conn.commit()
    print("🟣 [DISTILLER] Distillation complete.")

if __name__ == "__main__":
    while True:
        distill()
        time.sleep(3600) # Run hourly
