import json
import os
import sys
import threading

from pynput import keyboard
from termcolor import colored


def on_release(key):
    try:
        if key == keyboard.Key.page_up:
            Aimbot.update_status_aimbot(siema=False)
        if key == keyboard.Key.end:
            Aimbot.clean_up()
        if key == keyboard.Key.insert:
            Aimbot.update_status_aimbot(siema=True)
    except NameError:
        pass


def main():
    global majestic
    majestic = Aimbot(collect_data = "collect_data" in sys.argv)
    majestic.start()

def setup():
    path = "lib/config"
    if not os.path.exists(path):
        os.makedirs(path)

    def prompt(str, is_integer=False):
        valid_input = False
        while not valid_input:
            try:
                if is_integer:
                    number = int(input(str))
                else:
                    number = float(input(str))
                valid_input = True
            except ValueError:
                print("[!] Nieprawidlowe dane wejsciowe. Upewnij sie, że wprowadziles tylko liczbe (e.g. 1920)")
        return number

    # Dodanie wprowadzania wymiarów monitora
    screen_width = prompt("Szerokosc ekranu (e.g. 1920): ", is_integer=True)
    screen_height = prompt("Wysokosc ekranu (e.g. 1080): ", is_integer=True)

    # Zapisanie wymiarów monitora w słowniku
    screen_settings = {
        "screen_width": screen_width,
        "screen_height": screen_height
    }

    # Zapisanie ustawień do pliku config.json
    with open('lib/config/config.json', 'w') as outfile:
        json.dump(screen_settings, outfile)

    print("[INFO] Konfiguracja Zakonczona")

if __name__ == "__main__":
    os.system('cls' if os.name == 'nt' else 'clear')
    os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'

    print(colored('''
__________            .__                         
\____    /____   ____ |  |__ _____ _______  ____  
  /     //  _ \ /    \|  |  \\__  \\_  __ \/  _ \ 
 /     /(  <_> )   |  \   Y  \/ __ \|  | \(  <_> )
/_______ \____/|___|  /___|  (____  /__|   \____/ 
        \/          \/     \/     \/       v0.1.0

(Majestic AimBot Beta)''', "red"))

    path_exists = os.path.exists("lib/config/config.json")
    if not path_exists or ("setup" in sys.argv):
        if not path_exists:
            print("[!] Konfiguracja szerokosci i wysokosci ekranu nie jest ustawiona")
        setup()
    path_exists = os.path.exists("lib/data")
    if "collect_data" in sys.argv and not path_exists:
        os.makedirs("lib/data")
    from lib.aimbot import Aimbot
    listener = keyboard.Listener(on_release=on_release)
    listener.start()
    main()
