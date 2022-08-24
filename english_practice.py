import csv
from random import choice
from re import split

def get_data():
    with open('Words.csv', 'r', encoding = 'utf-8-sig') as file:
        csv_dict = {}
        reader = csv.reader(file)
        for row in reader:
            csv_dict[row[0]] = row[1]

        return csv_dict 

def remove_vocalization_from_string(hebrew_anwser):
    return ''.join(['' if 1456 <= ord(c) <= 1479 else c for c in hebrew_anwser])


def check_grammer(hebrew_translate, hebrew_anwser):
    if hebrew_anwser == hebrew_translate:
        return True
    if not (len(hebrew_translate) >= len(hebrew_anwser) - 1 and len(hebrew_translate) <= len(hebrew_anwser) + 1):
        return False

    count = 0
    for c in hebrew_translate:
        if c in hebrew_anwser:
            count += 1
    if count < 3:
        return False

    time_letters = "יאמה"
    for t in time_letters:
        if hebrew_translate + t == hebrew_anwser:
            return True

    return False

def check_hebrew_translate(words_dict, english_word, hebrew_translate):
    print(hebrew_translate)
    hebrew_anwser = remove_vocalization_from_string(words_dict[english_word])
    hebrew_anwser_list = split(",|;", hebrew_anwser)
    for anwser in hebrew_anwser_list:
        if(check_grammer(hebrew_translate, anwser)):
            return True


    return False

    
    


def main():

    words_dict = get_data()
    english_words = list(words_dict.keys())
    while True: 
        english_word = choice(english_words)
        print("Enter the translate of " + english_word)
        hebrew_translate = input("")
        if check_hebrew_translate(words_dict, english_word, hebrew_translate[::-1]):
            english_words.remove(english_word)
            print(f"Good job the full translate of {english_word} is {words_dict[english_word]}")
        else:
            print(f"Sorry that is a wrong anwser the translate of {english_word} is {words_dict[english_word]}")

        is_exit = input("If you want to exit just press q and enter")
        if is_exit == "q":
            break

    

if __name__ == "__main__":
    main()