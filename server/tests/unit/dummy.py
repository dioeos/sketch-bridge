from types import SimpleNamespace


class DummyWebSocket:
    def __init__(self) -> None:
        self.sent: list[str] = []
        self.state = SimpleNamespace()

    async def accept(self) -> None:
        # no-op for unit test
        return

    async def send_text(self, message: str) -> None:
        self.sent.append(message)
