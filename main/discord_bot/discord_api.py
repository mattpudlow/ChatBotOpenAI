from typing import Tuple

from dotenv import load_dotenv
from discord import Intents, Client
import os
from main.chatgpt_ai.openai import chatgpt_response

load_dotenv()

discord_token = os.getenv('DISCORD_TOKEN')
intents = Intents.default()
intents.message_content = True


def check_privacy(user_message: str) -> Tuple[bool, str]:
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    return is_private, user_message


class MyClient(Client):

    async def on_ready(self) -> None:
        print('Successfully logged in as: ', self.user)

    async def on_message(self, message):
        print(message.content)
        if message.author == self.user:
            return
        command, user_message = None, None

        for text in ['/ai', '/bot', '/chatgpt']:
            if message.content.startswith(text):
                command = message.content.split(' ')[0]
                user_message = message.content.replace(text, '')
                print(command, user_message)

        if command == '/ai' or command == '/bot' or command == '/chatgpt':
            if check_privacy(user_message)[0]:
                response = chatgpt_response(prompt=check_privacy(user_message)[1])
                await message.author.send(response)
            else:
                bot_response = chatgpt_response(prompt=user_message)
                await message.channel.send(f'Answer: {bot_response}')


client = MyClient(intents=intents)
