import openai
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())
client = openai.Client()


# Função para carregar arquivos txt
def carregar_arquivo(caminho):
    with open(caminho, 'r', encoding='utf-8') as f:
        return f.read()

# Carrega os arquivos
comportamento_do_bot = carregar_arquivo("instrucoes_bot.txt")
contexto = carregar_arquivo("contexto.txt")

# Pergunta do usuário
pergunta = input("Quem é a Madalena?")

# Envia a requisição para a API da OpenAI
resposta = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": comportamento_do_bot},
        {"role": "user", "content": f"Considere o seguinte documento como base de conhecimento. Use apenas ele para responder a pergunta, caso não ache nada na base de conhecimento você poderá usar sua própria base da API:\n\n{contexto}"},
        {"role": "user", "content": pergunta}
    ]
)

# Exibe a resposta
resposta_final = resposta.choices[0].message.model_dump(exclude_none=True)
print("\n🔍 Resposta do Assistente:\n")
print(resposta_final)
