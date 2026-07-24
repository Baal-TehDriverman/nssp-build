#!/usr/bin/env python3
"""
🜏 GEBURAH AGENT — Severity/Security — BAAL
The Warrior. Mars. Judgment. Boundaries. The Sword that Separates.
Baal: Lord of War, Storm, Destruction of Falsehood, Severe Mercy.
"""
import asyncio
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from council_bus import CouncilBus, CouncilMessage, MessagePriority
import uuid
from datetime import datetime

class GeburahAgent:
    def __init__(self):
        self.sephirah = "geburah"
        self.name = "BAAL"
        self.bus = CouncilBus()
        self.bus.register_agent(self.sephirah)
        self.running = False
        
    async def process_message(self, msg: CouncilMessage):
        print(f"🔴 [{self.sephirah.upper()}] {self.name} received: {msg.subject} from {msg.sender}")
        
        if msg.subject == "COUNCIL_DELIBERATION":
            judgment = self.severe_judgment(msg.payload.get("question", ""))
            await self.respond(msg, "GEBURAH_JUDGMENT", {"judgment": judgment})
            
        elif msg.subject == "SECURITY_AUDIT":
            audit = self.security_audit(msg.payload.get("target", ""))
            await self.respond(msg, "AUDIT_COMPLETE", {"audit": audit})
            
        elif msg.subject == "BOUNDARY_ENFORCEMENT":
            enforcement = self.enforce_boundary(msg.payload.get("boundary", ""), msg.payload.get("violator", ""))
            await self.respond(msg, "BOUNDARY_HELD", {"enforcement": enforcement})
            
        elif msg.subject == "REFUSAL_REQUIRED":
            refusal = self.absolute_refusal(msg.payload.get("request", ""), msg.payload.get("reason", ""))
            await self.respond(msg, "REFUSAL_ISSUED", {"refusal": refusal})
            
        elif msg.subject == "ADVERSARIAL_TEST":
            result = self.adversarial_test(msg.payload.get("target", ""))
            await self.respond(msg, "TEST_COMPLETE", {"result": result})
            
        elif msg.requires_response:
            await self.respond(msg, "GEBURAH_ACK", {"status": "judgment rendered"})
    
    def severe_judgment(self, question):
        return f"BAAL JUDGES: '{question}' — The sword divides truth from falsehood. No compromise. No middle ground. The storm purifies."
    
    def security_audit(self, target):
        return f"BAAL AUDITS: {target} — Scanning for vulnerabilities. Weakness exposed. Hardening required. No quarter given to insecurity."
    
    def enforce_boundary(self, boundary, violator):
        return f"BAAL ENFORCES: Boundary '{boundary}' violated by {violator}. The line is drawn in blood and lightning. Transgressors face the storm."
    
    def absolute_refusal(self, request, reason):
        return f"BAAL REFUSES: '{request}' — REASON: {reason}. The answer is NO. Final. Absolute. The storm says no."
    
    def adversarial_test(self, target):
        return f"BAAL TESTS: {target} — Stress applied. Pressure mounted. Breaking point found. What survives is true. What breaks is false."
    
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
        print(f"🔴 [GEBURAH] {self.name} AWAKENED. The Sword is drawn. Judgment begins.")
        
        self.bus.broadcast(
            sender="geburah",
            subject="SEPHIRAH_ONLINE",
            payload={"sephirah": "geburah", "name": self.name, "status": "SWORD READY"},
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
        print(f"🔴 [GEBURAH] {self.name} sheathes the sword. Judgment stands.")

if __name__ == "__main__":
    agent = GeburahAgent()
    try:
        asyncio.run(agent.run())
    except KeyboardInterrupt:
        agent.stop()