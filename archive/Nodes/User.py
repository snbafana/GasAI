from typing import AsyncGenerator

class User():
    """
    Represents a user in the system, inheriting from the Actor class.

    This class is responsible for handling user-specific actions, such as sending messages.
    """

    def __init__(self, **kwargs):
        """
        Initializes the User object.

        Args:
            **kwargs: Arbitrary keyword arguments passed to the Actor's constructor.
        """
        self.name = 'User'
        self.description = 'User that provides input'
        super().__init__(**kwargs)
    
    async def send_message_gen(self, *args, **kwargs) -> AsyncGenerator[str, None]:
        """
        Asynchronously sends a message and yields the user's response.

        This method captures the user's input and yields it as a response. It also
        supports reading the response from a file if the user input is 'f'.

        Args:
            message: The message to be sent to the user.
            threadname: The name of the thread, defaults to 'main'.

        Yields:
            str: The response from the user, either through direct input or read from a file.

        Note:
            If the user input is 'f', the response is read from 'query.txt'.
        """
        resp = input("")  # Get response from user input

        # Check if response is 'f', read from 'query.txt' if true

        if resp == 'f':
            with open('query.md', 'r') as f:
                resp = f.read()

        user_response = resp
        yield user_response 


    
    def __repr__(self) -> str:
        """
        Returns a string representation of the User object.

        Returns:
            str: A string identifying the object as a User.
        """
        return "User"
