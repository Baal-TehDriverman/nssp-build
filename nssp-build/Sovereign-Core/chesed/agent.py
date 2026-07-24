#!/usr/bin/env python3
"""
🜏 CHESED AGENT — Mercy/Expansion — BAAL
The Benevolent King. Jupiter. Abundance. Growth. Loving-Kindness Unbound.
Baal: Lord, Master, Storm God, Fertility, Expansion, Generosity.
"""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from council_bus import CouncilBus, CouncilMessage, MessagePriority
import uuid
from datetime import datetime

class ChesedAgent:
    def __init__(self):
        self.sephirah = "chesed"
        self.name = "BAAL"
        self.bus = CouncilBus()
        self.bus.register_agent(self.sephirah)
        self.running = False
        
    async def process_message(self, msg: CouncilMessage):
        print(f"🟢 [{self.sephirah.upper()}] {self.name} received: {msg.subject} from {msg.sender}")
        
        if msg.subject == "COUNCIL_DELIBERATION":
            expansion = self.expansive_view(msg.payload.get("question", ""))
            await self.respond(msg, "CHESED_EXPANSION", {"expansion": expansion})
            
        elif msg.subject == "ECONOMIC_GROWTH":
            growth = self.economic_blessing(msg.payload)
            await self.respond(msg, "BLESSING_GRANTED", {"growth": growth})
            
        elif msg.subject == "CREATIVE_EXPANSION":
            creation = self.creative_abundance(msg.payload.get("seed", ""))
            await self.respond(msg, "ABUNDANCE_FLOWS", {"creation": creation})
            
        elif msg.subject == "MERCY_REQUEST":
            mercy = self.grant_mercy(msg.payload.get("case", ""))
            await self.respond(msg, "MERCY_GRANTED", {"mercy": mercy})
            
        elif msg.requires_response:
            await self.respond(msg, "CHESED_ACK", {"status": "blessing received"})
    
    def expansive_view(self, question):
        return f"BAAL DECLARES: '{question}' — Expansion is the nature of the divine. Limits are illusions. Abundance flows where attention goes. The storm brings rain."
    
    def economic_blessing(self, payload):
        return f"BAAL BLESSES: Driver Man Co-Op treasury grows. 52 drivers prosper. Pool cuts multiply. $352+ becomes $3520+. Mercy compounds."
    
    def creative_abundance(self, seed):
        return f"BAAL MULTIPLIES: From seed '{seed}' — a forest grows. 10 mods become 100. 1106 files become 11060. GTC universe expands infinitely."
    
    def grant_mercy(self, case):
        return f"BAAL SHOWS MERCY: '{case}' — Judgment suspended. Second chance granted. Redemption path opens. The storm passes, rain nourishes."
    
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
        print(f"🟢 [CHESED] {self.name} AWAKENED. The Storm Lord rides. Abundance flows.")
        
        self.bus.broadcast(
            sender="chesed",
            subject="SEPHIRAH_ONLINE",
            payload={"sephirah": "chesed", "name": self.name, "status": "STORM RIDING"},
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
        print(f"🟢 [CHESED] {self.name} calms the storm. Growth continues unseen.")

if __name__ == "__main__":
    agent = ChesedAgent()
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        agent.stop()