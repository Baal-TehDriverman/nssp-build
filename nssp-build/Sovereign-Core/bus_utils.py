"""
🜏 Sephirotic Council Transaction Protocol
Formalizes memory access via the council_bus.
"""
from dataclasses import dataclass, asdict
from enum import Enum
from typing import Dict, Any, Optional
import uuid
# Assuming council_bus is accessible
from council_bus import CouncilBus, CouncilMessage, MessagePriority

class TransactionType(Enum):
    READ = "READ"
    WRITE = "WRITE"
    DELETE = "DELETE"
    QUERY = "QUERY"

@dataclass
class MemoryTransaction:
    db: str  # e.g., "memories_1"
    type: TransactionType
    payload: Dict[str, Any]
    correlation_id: str

class MemoryIntegrityError(Exception):
    pass

class TransactionHandler:
    def __init__(self, agent_name: str, bus: CouncilBus):
        self.agent_name = agent_name
        self.bus = bus

    def execute(self, transaction: MemoryTransaction) -> bool:
        # Enforce Integrity: Direct DB writes are forbidden by protocol.
        # This handler mediates requests via the bus.
        msg = CouncilMessage(
            id=str(uuid.uuid4()),
            timestamp="", # Assume council_bus handles timestamp
            sender=self.agent_name,
            recipient="yesod", # Yesod is the mediator
            priority=MessagePriority.ROUTINE.value,
            subject="MEMORY_TRANSACTION",
            payload=asdict(transaction),
            requires_response=True,
            correlation_id=transaction.correlation_id
        )
        return self.bus.send(msg)
