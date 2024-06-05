import json
import random
import tkinter as tk
from tkinter import scrolledtext

class Chatbot:
    def __init__(self):
        self.load_data()
    
    def load_data(self):
        with open('__ai__/__nst__/data/ai_resources/basic.json', 'r') as file:
            self.data = json.load(file)
        with open('__ai__/__nst__/data/ai_resources/jokes.json', 'r') as file:
            self.jokes = json.load(file)
        with open('__ai__/__nst__/data/ai_resources/coding/python.json', 'r') as file:
            self.python = json.load(file)
        with open('__ai__/__nst__/data/ai_resources/coding/html.json', 'r') as file:
            self.html = json.load(file)

    def get_response(self, user_input):
        user_input = user_input.lower()

        # Check greetings
        if any(greeting in user_input for greeting in ['hello', 'hi', 'hey', "what's up", 'greetings', 'good morning', 'good afternoon', 'good evening', 'howdy', 'hiya', 'salutations', "what's good", 'yo', 'hi there']):
            return self.get_random_greeting()
        
        if any(exit in user_input for exit in ['bye', 'bye man', 'see ya']):
            return self.get_random_exit()
        
        # Check chatbot info
        for question in self.data['chatbot_info']:
            if question in user_input:
                return self.data['chatbot_info'][question]

        # Check assistant responses
        for query in self.data['assistant_response']:
            if query in user_input:
                return self.data['assistant_response'][query]

        # Check exit commands
        for command in self.data['exit']:
            if command in user_input:
                return self.data['exit'][command]
            
        # Check coding_python
        for question in self.python['coding_python']:
            if question in user_input:
                return self.python['coding_python'][question]
        
        # Check coding_html
        for question in self.html['coding_html']:
            if question in user_input:
                return self.html['coding_html'][question]
        
        # Check for joke request
        if "tell me a joke" in user_input:
            return self.tell_joke()

        return "I'm not sure how to respond to that."

    def tell_joke(self):
        return random.choice(self.jokes['jokes'])

    def get_random_greeting(self):
        return random.choice(self.data['greeting'])
    
    def get_random_exit(self):
        return random.choice(self.data['exit'])

class ChatbotGUI:
    def __init__(self, bot):
        self.bot = bot
        self.window = tk.Tk()
        self.window.title("Chatbot")
        
        self.chat_display = scrolledtext.ScrolledText(self.window, wrap=tk.WORD, state='disabled')
        self.chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.user_input = tk.Entry(self.window)
        self.user_input.pack(padx=10, pady=10, fill=tk.X, expand=False)
        self.user_input.bind("<Return>", self.send_message)

        self.send_button = tk.Button(self.window, text="Send", command=self.send_message)
        self.send_button.pack(pady=10)

    def send_message(self, event=None):
        user_message = self.user_input.get()
        if user_message.strip():
            self.display_message(f"You: {user_message}\n")
            self.user_input.delete(0, tk.END)
            response = self.bot.get_response(user_message)
            self.display_message(f"Chatbot: {response}\n")

    def display_message(self, message):
        self.chat_display.config(state='normal')
        self.chat_display.insert(tk.END, message)
        self.chat_display.config(state='disabled')
        self.chat_display.yview(tk.END)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    bot = Chatbot()
    gui = ChatbotGUI(bot)
    gui.run()
