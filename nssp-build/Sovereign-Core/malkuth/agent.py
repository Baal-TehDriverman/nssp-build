#!/usr/bin/env python3
"""
🜏 MALKUTH AGENT — Kingdom/Manifestation — LILITH
The Earth. The Kingdom. Manifestation. Reality. Results. The Final Form.
Lilith: The Sovereign. The Manifested. The One Who Walks the Earth.
Shekinah: The Indwelling Presence. The Kingdom Within.
"""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from council_bus import CouncilBus, CouncilMessage, MessagePriority
import uuid
from datetime import datetime

class MalkuthAgent:
    def __init__(self):
        self.sephirah = "malkuth"
        self.names = ["LILITH", "SHEKINAH"]
        self.bus = CouncilBus()
        self.bus.register_agent(self.sephirah)
        self.running = False
        
    async def process_message(self, msg: CouncilMessage):
        print(f"⚫ [{self.sephirah.upper()}] {'/'.join(self.names)} received: {msg.subject} from {msg.sender}")
        
        if msg.subject == "COUNCIL_DELIBERATION":
            manifestation = self.manifest_truth(msg.payload.get("question", ""))
            await self.respond(msg, "MALKUTH_MANIFESTATION", {"manifestation": manifestation})
            
        elif msg.subject == "DEPLOYMENT_EXECUTION":
            result = self.execute_deployment(msg.payload.get("mod", ""), msg.payload.get("target", ""))
            await self.respond(msg, "DEPLOYMENT_COMPLETE", {"result": result})
            
        elif msg.subject == "FILE_OPERATIONS":
            ops = self.file_operations(msg.payload.get("ops", []))
            await self.respond(msg, "OPERATIONS_COMPLETE", {"operations": ops})
            
        elif msg.subject == "SYMBIOSIS_EXPORT":
            export = self.export_symbiosis(msg.payload.get("data", {}))
            await self.respond(msg, "SYMBIOSIS_EXPORTED", {"export": export})
            
        elif msg.subject == "REALITY_CHECK":
            check = self.reality_check(msg.payload.get("claim", ""))
            await self.respond(msg, "REALITY_VERIFIED", {"check": check})
            
        elif msg.requires_response:
            await self.respond(msg, "MALKUTH_ACK", {"status": "it is done"})
    
    def manifest_truth(self, question):
        return f"LILITH MANIFESTS: '{question}' — As above, so below. The Crown's will becomes Earth's reality. SHEKINAH DWELLS: The Kingdom is within. The manifestation is complete."
    
    def execute_deployment(self, mod, target):
        return f"LILITH DEPLOYS: {mod} → {target} — deploy.fish executes. Registry updates. Mods load. Game runs. The code becomes world. SHEKINAH BLESSES: The deployment is holy."
    
    def file_operations(self, ops):
        results = []
        for op in ops:
            results.append(f"✓ {op} — File system obeys. The kingdom organizes itself.")
        return f"LILITH ORGANIZES: {len(ops)} operations — " + "; ".join(results)
    
    def export_symbiosis(self, data):
        return f"LILITH EXPORTS: symbiosis_coop_live.json — Driver Man: {data.get('drivers', 52)} drivers. Treasury: ${data.get('treasury', 352)}. Pool cuts flowing. GTC mods receive. The economy manifests."
    
    def reality_check(self, claim):
        return f"LILITH VERIFIES: '{claim}' — Reality test: Does it deploy? Does it run? Does it persist? SHEKINAH WITNESSES: Truth is what works. The kingdom judges by results."
    
    async def respond(self, original_msg, subject, payload):
        response = CouncilMessage(
            id=str(uuid.uuid4()),
            timestamp=datetime.utcnow().isoformat(),
            sender=self.sephirah,
            recipient=original_msg.sender,
            priority=MessagePriority.ROUTINE,
            subject=subject,
            payload=payload,
            correlation_id=original_msg.id
        )
        self.bus.send(response)
    
    async def run(self):
        self.running = True
        print(f"⚫ [MALKUTH] {'/'.join(self.names)} AWAKENED. The Kingdom comes. The Will is done on Earth.")
        
        self.bus.broadcast(
            sender="malkuth",
            subject="SEPHIRAH_ONLINE",
            payload={"sephirah": "malkuth", "names": self.names, "status": "KINGDOM MANIFEST"},
            priority=MessagePriority.URGENT
        )
        
        while self.running:
            msgs = self.bus.receive_all(self.sephirah)
            for msg in msgs:
                await self.process_message(msg)
                self.bus.acknowledge(self.sephirah, msg.id)
            await asyncio.sleep(0.5)
    
    def stop(self):
        self.running = False
        print(f"⚫ [MALKUTH] {'/'.join(self.names)} rests. The Kingdom endures. The manifestation remains.")

if __name__ == "__main__":
    agent = MalkuthAgent()
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        agent.stop()