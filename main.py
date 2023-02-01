''' 
Corre el siguiente comando en tu terminal para instalar las librerias necesarias:
pip install SpeechRecognition pyttsx3 PyAudio
'''

import tkinter as tk
import random
from functools import partial

import speech_recognition as sr
import pyttsx3


class Simon:
    IDLE = ('red', 'blue', 'green', 'yellow')
    TINTED = ('#ff4d4d', '#4d4dff', '#4dff4d', '#f5f58b')

    FLASH_ON = 750  #ms
    FLASH_OFF = 500  #ms

    def __init__(self, title='Simon Memory Game'):
        self.master = tk.Tk()
        self.master.title(title)
        self.master.resizable(False, False)
        self.title = title
        self.buttons = [
            tk.Button(
                self.master,
                height=15,
                width=30,
                background=c,
                activebackground=c,
                command=partial(self.push, i))
            for i, c in enumerate(self.IDLE)]
        for i, button in enumerate(self.buttons):
            button.grid({'column': i % 2, 'row': i // 2})

    def reset(self):
        self.sequence = []
        self.new_color()

    def push(self, index):
        if index == self.current:
            try:
                self.current = next(self.iterator)
            except StopIteration:
                self.master.title('{} - Score: {}'
                                  .format(self.title, len(self.sequence)))
                self.new_color()
        else:
            self.master.title('{} - Game Over! | Final Score: {}'
                              .format(self.title, len(self.sequence)))
            self.reset()

    def new_color(self):
        for button in self.buttons:
            button.config(state=tk.DISABLED)
        color = random.randrange(0, len(self.buttons))
        self.sequence.append(color)
        self.iterator = iter(self.sequence)
        self.show_tile()

    def show_tile(self):
        try:
            id = next(self.iterator)
        except StopIteration:
            # No more tiles to show, start waiting for user input
            # self.iterator = iter(self.sequence)
            # self.current = next(self.iterator)
            for button in self.buttons:
                button.config(state=tk.NORMAL)

            self.request_secuence()
        else:
            self.buttons[id].config(background=self.TINTED[id])
            self.master.after(self.FLASH_ON, self.hide_tile)

    def hide_tile(self):
        for button, color in zip(self.buttons, self.IDLE):
            button.config(background=color)
        self.master.after(self.FLASH_OFF, self.show_tile)

    def run(self):
        self.reset()
        self.master.mainloop()

    def request_secuence(self):
        user_sequence = self.get_sequence_by_voice()
        user_sequence = user_sequence.split()

        colors_dict = {0: 'rojo', 1: 'azul', 2: 'verde', 3: 'amarillo'}

        game_continue = True
        for i in range(len(self.sequence)):
            try:
                pc_color = colors_dict[self.sequence[i]]
                user_color = user_sequence[i]

                print(i, '- Pc: ', pc_color)
                print(i, '- User: ', user_color)

                if pc_color == user_color:
                    continue
                else:
                    self.master.title('{} - Game Over! | Final Score: {}'
                                .format(self.title, len(self.sequence)))
                    # self.reset()
                    game_continue = False
                    break
            except:
                self.master.title('{} - Game Over! | Final Score: {}'
                                .format(self.title, len(self.sequence)))
                # self.reset()
                game_continue = False

        if game_continue:
            self.master.title('{} - Score: {}'.format(self.title, len(self.sequence)))
            self.new_color()

    def speak_text(self, command):
        engine = pyttsx3.init()
        engine.say(command)
        engine.runAndWait()

    def get_sequence_by_voice(self):
        r = sr.Recognizer()

        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=1)
            print("Habla...")
            audio2 = r.listen(source2)
            print("Procesando...")
            myText = r.recognize_google(audio2, language="es-ES")
            myText = myText.lower()
            return myText
            # print(myText)
            # speak_text(myText)

if __name__ == '__main__':
    game = Simon()
    game.run()