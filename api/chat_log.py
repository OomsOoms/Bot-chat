import asyncio
from langchain.llms import Ollama

from utils.logger import CustomLogger
import random
import requests
import json

logger = CustomLogger(__name__)


class Model:

    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def __call__(self, message_list: list = []):

        # Create a copy of the list
        formatted_list = [message.copy() for message in message_list]

        # Change the role of the messages in the copied list
        formatted_list = [
            {"role": "assistant" if message["role"] == self.model else "user", "content": message["content"]}
            for message in formatted_list
        ]

        payload = {
            "model": self.model,
            "messages": formatted_list,
        }

        response = requests.post(
            f"{self.base_url}/api/chat", json=payload, stream=True)

        content = ""
        for line in response.iter_lines():
            if line:
                response_json = json.loads(line)
                if "message" in response_json:
                    content += response_json["message"]["content"]

        return content


class ChatLog:

    models = [
        #Model(base_url="http://localhost:11434", model="llama2-rude-2"),
        Model(base_url="http://localhost:11434", model="llama2-horny"),
       # Model(base_url="http://localhost:11434", model="copilot-edit"),
    ]

    def __init__(self):
        # Select a random model to start with
        self.current_model = random.choice(self.models)

        self.log = [{"role": "user", "content": "im about to cum"}]

    async def start(self):
        logger.info("Starting chat log")
        # generate a message to start the chat
        self.log.append({"role": "user", "content": self.current_model(self.log)})
        
        while True:

                logger.info(f"{self.log[-1]['role']}: {self.log[-1]['content']}")

                # Select a random model to use for the next message, ensuring it's different from the current model
                other_models = [model for model in self.models if model.model != self.current_model.model]
                #self.current_model = random.choice(other_models)

                message = self.current_model(self.log).split("###")[0].strip()
                self.log.append({"role": "user", "content": message})



if __name__ == "__main__":
    chat_log = ChatLog()
    asyncio.run(chat_log.start())
