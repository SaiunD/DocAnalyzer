from dotenv import load_dotenv
import os
import openai
from libs.tokens import TokenCounter

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("-x-> OpenAI API key is not set. Please check your .env file.")

openai.api_key = api_key


def query_openai(system_prompt, user_prompt, token_counter: TokenCounter):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        if 'choices' not in response or not response['choices']:
            raise ValueError("-x-> No choices found in response.")

        result = response['choices'][0].get('message', {}).get('content', '')

        if not result:
            raise ValueError("-x-> Received empty content from OpenAI.")

        token_counter.add_tokens(response.usage.total_tokens)
        return result

    except openai.error.OpenAIError as e:
        print(f"-x-> OpenAI error: {e}")
        raise
    except Exception as e:
        print(f"-x-> Error during OpenAI query: {e}")
        raise
