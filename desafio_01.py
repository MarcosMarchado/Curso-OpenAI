import openai
import sys
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = openai.Client()


def chatbot_stream(temperature=1, model='gpt-3.5-turbo-0125', mensagens=None):
    response_stream = client.chat.completions.create(
        temperature=temperature,
        model=model,
        stream=True,
        messages=mensagens
    )

    texto_completo = ''
    print("Assistant: ")
    for texto in response_stream:
        texto_stream = texto.choices[0].delta.content
        if texto_stream:
            texto_completo += texto_stream
            print(texto_stream, end='')
    print()
    mensagem_assistant = {'role': 'assistant', 'content': texto_completo}
    mensagens.append(mensagem_assistant)
    return mensagens


while True:
    mensagens_conversa = []
    print("Bem vindo ao Chatbot da Dorinha!")
    print("Aperte ENTER para continuar ou CTRL + D para sair...")

    try:
        tecla = sys.stdin.read(1)  # Lê um único caractere
    except EOFError:
        print("\nSaindo do chatbot...")
        break

    if tecla == "\n":
        chat_rodando = True
        while chat_rodando:
            texto_user = input("User: ")
            mensagem = {'role': 'user', 'content': texto_user}

            if texto_user.strip().upper() == "#SAIR":
                chat_rodando = False
                mensagens_conversa = []
                break  # Sai do loop do chat

            else:
                mensagens_conversa.append(mensagem)
                chatbot_stream(mensagens=mensagens_conversa)

    elif tecla == '\x04':  # Captura CTRL + D (EOF)
        print("\nSaindo do chatbot...")
        break

