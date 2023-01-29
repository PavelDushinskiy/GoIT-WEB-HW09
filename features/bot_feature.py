from typing import List, Callable


class BotFeature():
    """
    A base class that handles commands for the features.
    """

    def __init__(self, command_handlers: dict[str, Callable]):
        self.command_handlers = command_handlers

    def name(self):
        pass

    def handle_command(self, command: str, *args: List[str]):
        handler = self.command_handlers.get(command, None)
        if handler:
            return handler(*args)
        else:
            raise ValueError("Unexpected command")
