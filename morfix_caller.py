import requests
import bs4
from pandas import read_clipboard
import time
import sys
import tty
import termios
import csv
import platform
import os

dictionary = {}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

csv_file = {}

def get_csv_file():
    global csv_file
    with open(os.getcwd() + '/Words.csv', 'r', encoding = 'utf-8-sig') as file:
        reader = csv.reader(file)
        for row in reader:
            csv_file[row[0]] = row[1]

def show_messagebox(title, message):
    print(title, message)
    # if platform.system() == "Windows":
    #     MessageBox(message, title)
    # else:
    #     alert(text=message, title=title)


def get_clipboard():
    try:
        text = read_clipboard(sep='\\v', header=None).iloc[0, 0]
    except:
        text = ''
    return text

def check_in_csv(english_word):
    global csv_file
    if english_word in csv_file.keys():
        return csv_file[english_word]
    
    return None

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    ch = ""
    try:
        tty.setraw(fd)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    return ch

def main_job():
    get_csv_file()
    print("The app is up and running...")
    print("Press q and enter at any time to stop the program.")
    english_word = get_clipboard()
    print(english_word)

    while True:
        time.sleep(1.5)
        if english_word != get_clipboard():
            english_word = get_clipboard()
            print(english_word)
        else:
            continue
        translated_word = check_in_csv(english_word)
        if not translated_word:
            try:
                r = requests.get(f"https://www.morfix.co.il/{english_word}", headers=HEADERS)
            except ConnectionError:
                print("Be aware that you arent connected to the network...")
                show_messagebox("Error", "Be aware that you arent connected to the network...")
                continue
            soup = bs4.BeautifulSoup(r.content,'html.parser')
            try: 
                translated_word = soup.find('div', {'class': 'normal_translation_div'}).text.strip()[::-1]
                dictionary[english_word] = translated_word
            except:
                print("Couldnt find the word you are looking for")
                show_messagebox("Error", "Couldnt find the word you are looking for")
                continue

        print(translated_word)
        show_messagebox(english_word,translated_word[::-1])

    with open("Words.csv", 'a', newline='', encoding = 'utf-8-sig') as file:
        writer = csv.writer(file)
        for key, value in dictionary.items():
            print(key + " -> " + value)
            writer.writerow([key,value])


def main():
    main_job()

if __name__ == "__main__":
    main()
