from abc import ABC, abstractmethod
from typing import AsyncGenerator

class Actor(ABC):
    """
    Abstract base class for Actor entities in a system.

    This class defines the interface for actors, where actors are entities capable of sending messages.
    It uses Python's Abstract Base Class (ABC) module to ensure that all subclasses implement
    the specified abstract methods.
    """

    def __init__(self) -> None:
        """
        Initializes an Actor instance.

        Currently, this constructor does not perform any initialization and serves as a placeholder.
        It can be overridden in subclasses to add common initialization logic for all Actor types.
        """
        pass

    @abstractmethod
    async def send_message_gen(self, message: str) -> AsyncGenerator[str, None]:
        """
        Abstract asynchronous generator method for sending a message.

        Subclasses must implement this method to define how an Actor sends a message.
        This method is expected to handle message sending asynchronously, potentially involving
        multiple steps or waiting for external events.

        Args:
            message: A string representing the message to be sent.

        Yields:
            str: Parts of the message or status updates as the message is being sent.

        Note:
            This method is designed to be used with 'async for' in calling code.
        """
        pass
