import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

client = openai.Client()

def chama_api(messages):
    completion = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        messages=messages,
        temperature=1
    )
    resposta_assistente = completion.choices[0].message.model_dump(exclude_none=True)
    messages.append(resposta_assistente)
    return resposta_assistente

def chama_api_stream(messages):
    resposta = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        messages=messages,
        temperature=1,
        stream=True
    )

    for resposta_stream in resposta:
        texto = resposta_stream.choices[0].delta.content
        if texto:
            print(texto, end='')

messages = [{'role': 'user', 'content': 'Crie uma história de ficção.'}]


#print(chama_api(messages=messages))
print(chama_api_stream(messages=messages))
