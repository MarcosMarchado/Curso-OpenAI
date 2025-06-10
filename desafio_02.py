import openai
import sys
import json
from dotenv import load_dotenv, find_dotenv
import yfinance as yf

import Currency

_ = load_dotenv(find_dotenv())
client = openai.Client()

tools = [{
    "type": "function",
    "function": {
        "name": "obtem_cotacao_atual",
        "description": "Obtem cotação atual de empresas usando como busca o ticker",
        "parameters": {
            "type": "object",
            "properties": {
                "ticker": {
                    "type": "string",
                    "description": "Ticker usado para identificar empresas dentro de corretoras"
                }
            },
            "required": [
                "ticker"
            ],
        }
    }
}]

def obtem_cotacao_atual(ticker=''):
    return json.dumps({'cotacao': chama_api_yfinance(ticker)})


def call_function(name, args):
    if name == "obtem_cotacao_atual":
        return obtem_cotacao_atual(args)

def chama_open_ai(mensagens=[]):
    response_stream = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        stream=True,
        messages=mensagens,
        tool_choice='auto',
        tools=tools
    )

    mensagem_assistant_response = ''
    nome_funcao = ''
    payload_tool_call = ''
    id_call = ''
    houve_tool_call = False

    for response in response_stream:
        delta = response.choices[0].delta

        if hasattr(delta, 'tool_calls') and delta.tool_calls:
            houve_tool_call = True
            tool_call = delta.tool_calls[0]

            if tool_call.type == 'function':
                id_call = tool_call.id
                nome_funcao = tool_call.function.name

            if tool_call.function.arguments:
                payload_tool_call += tool_call.function.arguments

        elif hasattr(delta, 'content') and delta.content:
            # Se não for uma chamada de função, é uma resposta direta
            mensagem_assistant_response += delta.content
            print(delta.content, end='', flush=True)

    print()

    if houve_tool_call and nome_funcao:
        print(payload_tool_call)
        payload_function_json = json.loads(payload_tool_call)
        result_function = call_function(nome_funcao, payload_function_json)

        mensagens.append({
            "role": "assistant",
            "tool_calls": [
                {
                    "id": id_call,
                    "type": "function",
                    "function": {
                        "name": nome_funcao,
                        "arguments": payload_tool_call
                    }
                }
            ]
        })

        mensagens.append({
            "role": "tool",
            "tool_call_id": id_call,
            "content": result_function,
            "name": nome_funcao
        })

        # Segunda chamada com stream para obter a resposta final
        segunda_resposta_stream = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            messages=mensagens,
            stream=True
        )

        resposta_final = ''
        for chunk in segunda_resposta_stream:
            delta = chunk.choices[0].delta
            if hasattr(delta, 'content') and delta.content:
                resposta_final += delta.content
                print(delta.content, end='', flush=True)
        print()
        mensagens.append({'role': 'assistant', 'content': resposta_final})

    elif mensagem_assistant_response:
        mensagens.append({'role': 'assistant', 'content': mensagem_assistant_response})

    return mensagens





def app():
    while True:
        print("Bem vindo ao Chatbot da Dorinha!")
        print("Aperte ENTER para continuar ou CTRL + D para sair...")
        tecla = sys.stdin.read(1)

        if tecla == "\n":
            mensagens_conversa = []
            while True:
                texto_usuario = input("User: ")
                mensagem_usuario_payload = {'role': 'user', 'content': texto_usuario}
                mensagens_conversa.append(mensagem_usuario_payload)

                chama_open_ai(mensagens_conversa)


def chama_api_yfinance(ticker):
    ticker = ticker['ticker'] + '.SA'
    acao = yf.Ticker(ticker)
    info = acao.info

    currency_code = info['currency']
    pais = Currency.Currency[currency_code].value[0]
    moeda = Currency.Currency[currency_code].value[1]

    return f"{moeda} {info['regularMarketPrice']}"

app()





