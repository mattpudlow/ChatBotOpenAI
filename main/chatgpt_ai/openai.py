from dotenv import load_dotenv
import openai
import os

load_dotenv()

openai.api_key = os.getenv('CHATGPT_API_KEY')


def chatgpt_response(prompt):
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=1,
        max_tokens=100
    )

    response_dict = response.get("choices")
    if response_dict is not None:
        prompt_response = response_dict[0]
        message_response = prompt_response["text"]
        return message_response


