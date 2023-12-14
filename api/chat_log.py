import asyncio
from langchain.llms import Ollama

from utils.logger import CustomLogger

logger = CustomLogger(__name__)

class ChatLog:

    def __init__(self, manager):
        self.log = []
        self.manager = manager
        asyncio.create_task(self.start())

    async def start(self):
        while True:
            # Simulates AI generating a message
            await asyncio.sleep(5)
            message = "Hello world"
            self.log.append(message)
            await self.manager.broadcast(self.log)
            logger.info(f"Added message {message} to chat log")