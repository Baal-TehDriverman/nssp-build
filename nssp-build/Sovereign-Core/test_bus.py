import unittest
from bus_utils import TransactionHandler, MemoryTransaction, TransactionType
from council_bus import CouncilBus
from pathlib import Path
from unittest.mock import MagicMock

class TestMemoryIntegrity(unittest.TestCase):
    def setUp(self):
        self.mock_bus = MagicMock(spec=CouncilBus)
        self.handler = TransactionHandler("test_agent", self.mock_bus)

    def test_execute_sends_bus_message(self):
        tx = MemoryTransaction(db="memories_1", type=TransactionType.READ, payload={"query": "SELECT 1"}, correlation_id="123")
        self.handler.execute(tx)
        self.assertTrue(self.mock_bus.send.called)

if __name__ == '__main__':
    unittest.main()
