from configparser import ConfigParser
from chatbot import ChatBot
import sys

def main():
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = config['gemini_ai']['API_KEY']
    
    chatbot = ChatBot(api_key=api_key)
    chatbot.start_conversation()
    # chatbot.clear_conversation()
    
    print("Bem vindo(a)!!! Sou Whole AI, inteligência artificial do Whole. Digite a sua pergunta e caso queira encerrar o chat, digite: 'Sair'. ")
    
    while True:
        user_input = input('Você: ')
        if user_input.lower() == 'sair':
            sys.exit('Você deixou a conversa.')
        
        try:
            response = chatbot.send_prompt(user_input)
            print(f"{chatbot.CHATBOT_NAME}: {response}")
        except Exception as e:
            print(f"Error: {e}")

main()