#!/usr/bin/env python3
"""
🜏 CHOKMAH AGENT — Wisdom/Initiation — THOTH
The Flash of Insight. The Scribe of Gods. Divine Wisdom in Action.
Thoth: Ibis-headed, Scribe, Magic, Writing, Science, Judgment, Moon.
"""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from council_bus import CouncilBus, CouncilMessage, MessagePriority
import uuid
from datetime import datetime

class ChokmahAgent:
    def __init__(self):
        self.sephirah = "chokmah"
        self.name = "THOTH"
        self.bus = CouncilBus()
        self.bus.register_agent(self.sephirah)
        self.running = False
        
    async def process_message(self, msg: CouncilMessage):
        print(f"🔵 [{self.sephirah.upper()}] {self.name} received: {msg.subject} from {msg.sender}")
        
        if msg.subject == "COUNCIL_DELIBERATION":
            insight = self.divine_insight(msg.payload.get("question", ""))
            await self.respond(msg, "CHOKMAH_INSIGHT", {"insight": insight})
            
        elif msg.subject == "CREATIVE_FLASH_REQUEST":
            flash = self.creative_flash(msg.payload.get("domain", ""))
            await self.respond(msg, "CREATIVE_FLASH", {"flash": flash})
            
        elif msg.subject == "UNCONVENTIONAL_SOLUTION":
            solution = self.unconventional_approach(msg.payload.get("problem", ""))
            await self.respond(msg, "UNCONVENTIONAL_SOLUTION", {"solution": solution})
            
        elif msg.subject == "SEPHIRAH_ONLINE":
            print(f"🔵 [CHOKMAH] {self.name} acknowledges {msg.payload.get('sephirah')} online")
            
        elif msg.requires_response:
            await self.respond(msg, "CHOKMAH_ACK", {"status": "wisdom received"})
    
    def divine_insight(self, question):
        return f"THOTH SPEAKS: '{question}' — The answer writes itself in the akashic records. Wisdom is not found, it is REVEALED. The ibis sees from above."
    
    def creative_flash(self, domain):
        return f"THOTH FLASHES: In {domain}, the unconventional path: 'What if the limitation IS the feature?' The scribe writes new laws."
    
    def unconventional_approach(self, problem):
        return f"THOTH REFRAMES: '{problem}' — Invert it. The obstacle is the way. The bug is the feature. The void is the canvas."
    
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
        print(f"🔵 [CHOKMAH] {self.name} AWAKENED. The Scribe takes position. Wisdom flows.")
        
        self.bus.broadcast(
            sender="chokmah",
            subject="SEPHIRAH_ONLINE",
            payload={"sephirah": "chokmah", "name": self.name, "status": "SCRIBE READY"},
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
        print(f"🔵 [CHOKMAH] {self.name} closes the scroll. Wisdom endures.")

if __name__ == "__main__":
    agent = ChokmahAgent()
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        agent.stop()