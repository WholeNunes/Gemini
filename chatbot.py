import google.generativeai as genai

class GeniAIException(Exception):
    """GenAI Exception base class"""
    
class ChatBot:
    CHATBOT_NAME = 'Whole AI'
    
    def __init__(self, api_key):
        self.genai = genai
        self.genai.configure(api_key=api_key)
        self.model = self.genai.GenerativeModel('gemini-1.5-pro-latest')
        self.conversation = None
        self._conversation_history = []
        
        self.preload_conversation()
       
    def send_prompt(self, prompt, temperature=0.1):
        if temperature < 0 or temperature > 1:
            raise GeniAIException('Temperature must be between 0 and 1')
        
        if not prompt:
            raise GeniAIException('Prompt cannot be empty') 
        
        try:
            response = self.conversation.send_message(
                content=prompt,
                generation_config=self._generation_config(temperature),
            )
            response.resolve()
            return f'{response.text}\n' + '---' * 20
        except Exception as e:
            raise GeniAIException(e.message)
    
    @property
    def history(self):
        conversation_history = [
            {'role': message.role, 'text': message.parts[0].text} for message in self.conversation.history
        ]
        return conversation_history
    
    def clear_conversation(self,):
        self.conversation = self.model.start_chat(history=[])
        
    def start_conversation(self):
        self.conversation = self.model.start_chat(history=self._conversation_history)
       
    def _generation_config(self, temperature, candidate_count=1, max_output_tokens = 1028):
        return genai.types.GenerationConfig(
            temperature=temperature,
            candidate_count=candidate_count,
            max_output_tokens=max_output_tokens,
        )
        
    def _contruct_message(self, text, role='user'):
         return {
            'role': role,
            'parts': [text]
         }
         
    def preload_conversation(self, conversation_history=None):
        if isinstance(conversation_history, list):
            self._conversation_history = conversation_history
        else:
            self._conversation_history = [
                self._contruct_message('From now on, return the output as a JSON object that can be loaded in python with the key as \'text\'. For exemple, {"text": "<output goes here>"}'),
                self._contruct_message('{"text": "Sure, I can return the output as a regular JSON object with the key as `text`. Here is an example: {"text": "Your Output"}.', 'model'),
                self._contruct_message('Responda todas as perguntas que eu te fazer sempre em Português(PT)'),
                self._contruct_message('{"text": "Sem problemas, irei responder todas as suas perguntas em Português PT-BR.', 'model')
            ]