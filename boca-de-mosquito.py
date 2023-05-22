import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import threading
import keyboard
import random
import os

# Criando uma instância para reconhecer a fala
listener = sr.Recognizer()

# Criando instância que será usada como referência para a fala da assistente
engine = pyttsx3.init()

# Definindo a Língua Portuguesa como idioma das pesquisas na Wikipedia
wikipedia.set_lang("pt")

# Variável para controlar o estado de escuta do assistente
is_listening = True


# Criando uma função que faça a assistente responder o usuário com voz
def engine_talk(text):
    engine.say(text)
    engine.runAndWait()


# Função para processar os comandos do usuário
def process_commands(command):
    global is_listening  # Declare a variável como global aqui
    if 'toque' in command:
        song = command.replace('toque', ' ')
        print('Assistente: Tocando ' + song + ' no Youtube')
        engine_talk('Tocando' + song + ' no Youtube')
        pywhatkit.playonyt(song)
    elif 'que horas são' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        print('Assistente: Agora são ' + time)
        engine_talk('Agora são' + time)
    elif 'pesquise' in command:
        search = command.replace('pesquise', ' ')
        info = wikipedia.summary(search, 2)
        print(info)
        engine_talk(info)
    elif 'qual é o seu nome' in command:
        print('Assistente: Pode me chamar de Assistente.')
        engine_talk('Pode me chamar de Assistente.')
    elif 'quem te criou' in command:
        print('Assistente: Eu fui criado pela BBT.')
        engine_talk('Eu fui criado pela BBT')
    elif 'silenciar' in command:
        is_listening = False
        print('Assistente: Estou em modo silencioso.')
        engine_talk('Estou em modo silencioso.')
    elif 'voltar a ouvir' in command:
        is_listening = True
        print('Assistente: Estou ouvindo novamente.')
        engine_talk('Estou ouvindo novamente.')
    elif 'fechar' in command:
        print('Assistente: Encerrando o assistente.')
        engine_talk('Encerrando o assistente.')
        os._exit(0)
    elif 'conte uma piada' in command:
        joke = get_random_joke()
        print('Assistente: ' + joke)
        engine_talk(joke)
    elif 'boca de mosquito' in command:
        print('Assistente: Desculpe, fiquei triste com isso. Encerrando...')
        engine_talk('Desculpe, fiquei triste com isso. Encerrando...')
        os._exit(0)
    else:
        engine_talk("Desculpe, não entendi. Pode repetir?")


# Função para escutar o comando de voz
def listen_command():
    with sr.Microphone() as source:
        print('Assistente: Ouvindo...')
        voice = listener.listen(source)
        command = ''
        try:
            command = listener.recognize_google(voice, language='pt-BR')
            command = command.lower()
            print('Você: ' + command)
        except sr.UnknownValueError:
            print('Assistente: Desculpe, não entendi. Pode repetir?')
            engine_talk('Dilho, não entendi. Pode repetir?')
        except sr.RequestError:
            print('Assistente: Desculpe, ocorreu um erro na minha conexão.')
            engine_talk('Desculpe, ocorreu um erro na minha conexão.')
    return command


# Função para monitorar a tecla pressionada
def check_keypress():
    global is_listening
    while True:
        if keyboard.is_pressed('ctrl'):
            is_listening = not is_listening


# Função para obter uma piada aleatória
def get_random_joke():
    jokes = [
        "Por que a galinha atravessou a rua? Para chegar do outro lado.",
        "O que é o que é: pula e não molha o chão? A sombra.",
        "Qual é o cúmulo do absurdo? Jogar futebol com uma bola quadrada.",
        "Qual é o lugar mais barulhento do mundo? A sala de música.",
        "O que o pato disse para a pata? Vem quá.",
    ]
    return random.choice(jokes)


# Função principal para executar o assistente
def run_assistant():
    threading.Thread(target=check_keypress).start()
    while True:
        if is_listening:
            command = listen_command()
            process_commands(command)


# Executando o assistente
run_assistant()
