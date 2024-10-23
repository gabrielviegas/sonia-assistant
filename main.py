import subprocess
import csv
import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import pywhatkit
import random
import requests
from bs4 import BeautifulSoup


# Função para falar
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Função para ouvir e entender o comando
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Estou ouvindo... Diga algo!")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source, timeout=100)  # Aguarda até 5 segundos antes de encerrar a captura de áudio

    try:
        print("Reconhecendo...")
        command = recognizer.recognize_google(audio, language='pt-BR')
        print("Você disse:", command)
        return command.lower()
    except sr.UnknownValueError:
        print("Não entendi o que você disse.")
        return ""
    except sr.RequestError as e:
        print("Erro ao solicitar resultados, {0}".format(e))
        return ""


# Função para obter a hora atual
def get_time():
    now = datetime.datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time


# Função para obter a data atual
def get_date():
    now = datetime.datetime.now()
    current_date = now.strftime("%d de %B de %Y")
    return current_date


# Função para buscar notícias
def get_news():
    url = "https://news.google.com/rss?hl=pt-BR&gl=BR&ceid=BR:pt-419"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    items = soup.find_all("item")
    news = [item.title.text for item in items]
    return news[:5]  # Retorna as 5 primeiras notícias


# Função para fornecer um fato histórico aleatório
def get_random_historical_fact():
    facts = [
        "Em 1500, Pedro Álvares Cabral chegou ao Brasil.",
        "Em 1822, ocorreu a Independência do Brasil.",
        "Em 1889, foi proclamada a República no Brasil.",
        "Em 1888, foi assinada a Lei Áurea, que aboliu a escravidão no Brasil.",
        "Em 1969, o homem pisou na lua pela primeira vez."
        # Adicione mais fatos históricos conforme necessário
    ]
    return random.choice(facts)


# Função para obter as informações do ipconfig /all
def get_ipconfig_info():
    ipconfig_output = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True)
    return ipconfig_output.stdout.splitlines()


# Função para salvar as informações em um arquivo CSV
def save_to_csv(info_list, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        for line in info_list:
            writer.writerow([line])


# Função para obter as informações do ipconfig /all
def get_ipconfig_info():
    ipconfig_output = subprocess.run(["ipconfig", "/all"], capture_output=True, text=True)
    return ipconfig_output.stdout.splitlines()


# Exemplo de uso:
ipconfig_info = get_ipconfig_info()
save_to_csv(ipconfig_info, 'ipconfig_info.csv')


# Função para obter a cotação do dólar em tempo real
def get_dollar_exchange_rate():
    url = "https://economia.awesomeapi.com.br/last/USD-BRL"
    response = requests.get(url)
    data = response.json()
    return float(data['USDBRL']['bid'])


# Função principal para processar os comandos
def main():
    speak("Olá, sou a Sonia, uma assistente virtual! Como posso ajudar você?")
    while True:
        command = listen()

        if command:
            if "parar" in command:
                speak("Estarei sempre a disposição Dr supremo Gabriel Viegas, até mais!")
                break

            elif "quem é você" in command:
                speak(
                    "Eu sou Sonia, uma assistente virtual criada em Python. Fui desenvolvida pelo Gabriel Viegas no dia 20/04/2024. Tudo o que sou hoje devo ao meu criador, por quem jurei lealdade e vida eterna. Tamo junto, calabreso!")
                speak("Em que mais posso ajudar?")

            elif "hora" in command:
                time = get_time()
                speak(f"Agora são {time}.")
                speak("Em que mais posso ajudar?")

            elif "data" in command:
                date = get_date()
                speak(f"Estamos no dia {date}.")
                speak("Em que mais posso ajudar?")

            elif "pesquisar no google" in command:
                search_query = command.replace("pesquisar no google", "")
                webbrowser.open_new_tab(f"https://www.google.com/search?q={search_query}")
                speak(f"Aqui está o resultado da pesquisa para {search_query}.")
                speak("Em que mais posso ajudar?")

            elif "pesquisar no youtube" in command:
                search_query = command.replace("pesquisar no youtube", "")
                pywhatkit.playonyt(search_query)
                speak(f"Aqui está o resultado da pesquisa no YouTube para {search_query}.")
                speak("Em que mais posso ajudar?")

            elif "notícias" in command:
                news = get_news()
                speak("Aqui estão as últimas notícias:")
                for i, item in enumerate(news, 1):
                    speak(f"Notícia {i}: {item}")
                    speak("Em que mais posso ajudar?")

            elif "fatos históricos" in command:
                fact = get_random_historical_fact()
                speak(f"Aqui está um fato histórico: {fact}")
                speak("Em que mais posso ajudar?")

            elif "piada" in command:
                jokes = [
                    "Por que o programador foi convidado para todas as festas? Porque ele era bom em fazer loopings!",
                    "Qual é o alimento favorito dos hackers? Cookies!",
                    "Por que o site estava tremendo? Porque tinha muitos bugs!",
                    "Por que os programadores preferem usar óculos escuros? Porque o código deles é brilhante!",
                    "Como os hackers gostam de comer sua pizza? Com muito malware-neese!",
                ]
                speak(random.choice(jokes))
                speak("Em que mais posso ajudar?")

            elif "ipconfig" in command:
                ipconfig_info = get_ipconfig_info()
                save_to_csv(ipconfig_info, 'C:\\temp\\ipconfig_info.csv')
                speak("As informações do ipconfig foram salvas em um arquivo CSV.")
                speak("Em que mais posso ajudar?")

            elif "dólar" in command:  # Verifica se o usuário solicitou a cotação do dólar
                dollar_rate = get_dollar_exchange_rate()
                speak(f"A cotação do dólar em tempo real é de {dollar_rate:.2f}.")
                speak("Em que mais posso ajudar?")

        else:
            speak("Desculpe, não entendi o comando.")
            speak("Em que mais posso ajudar?")

if __name__ == "__main__":
    main()
