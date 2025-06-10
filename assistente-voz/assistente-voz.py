import openai

from io import BytesIO
import speech_recognition as sr ##Reconhecimento do áudio pelo microfone
from playsound import playsound ##Lib responsável por dar play no áudio
from dotenv import load_dotenv, find_dotenv

from pathlib import Path

_ = load_dotenv(find_dotenv())
client = openai.Client()

recognizer = sr.Recognizer()

ARQUIVO_AUDIO = 'resposta_assistant.mp3'

def grava_audio():
    with sr.Microphone() as source:
        print("Ouvindo...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)
    return audio

def transcricao_audio(audio_arquivo):
    wav_data = BytesIO(audio_arquivo.get_wav_data())
    wav_data.name = 'audio.wav'
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=wav_data
    )
    return transcript.text

def completa_texto(mensagens):
    return client.chat.completions.create(
        model='gpt-3.5-turbo',
        max_tokens=1000,
        temperature=0,
        messages=mensagens
    )

def cria_audio(texto):
    if Path(ARQUIVO_AUDIO).exists():
        Path(ARQUIVO_AUDIO).unlink()
    resposta = client.audio.speech.create(
        input=texto,
        model='tts-1',
        voice='shimmer'
    )
    resposta.write_to_file(ARQUIVO_AUDIO)

def roda_audio():
    playsound(ARQUIVO_AUDIO)

if __name__ == "__main__":

    mensagens = []
    while True:
        audio = grava_audio()
        transcricao = transcricao_audio(audio)

        print(f"Usuário: {transcricao}")

        mensagens.append({"role": "user", "content": transcricao})
        resposta = completa_texto(mensagens)
        resposta_assistant = resposta.choices[0].message.content
        mensagens.append({"role": "assistant", "content": resposta_assistant})


        print(f"Assistant: {resposta_assistant}")
        cria_audio(resposta_assistant)
        roda_audio()






