# TODO
from cs50 import get_int
from cs50 import get_string
import re


def main():
    # get the input text from the user
    while True:
        answer = get_string("Text: ")
        if str(answer):
            break
    # call the grade level function to get the grade level of the text
    grade_level(answer)


def grade_level(text):
    # set all needed variables, set words to 1 to get last word in a sentence
    letter, words, sentences, i = 0, 1, 0, 0
    # look at each letter in the length of the text
    while i < len(text):
        # see if i matches to a letter, if so add 1 to letter
        if (text[i].lower() >= 'a' and text[i].lower() <= 'z'):
            letter += 1
        # see if i mathces to a space, if so add 1 to words
        elif text[i] == ' ':
            words += 1
        # see if i mathces to a '.', '!' or '?', if so add 1 to sentences
        elif text[i] == '.' or text[i] == '!' or text[i] == '?':
            sentences += 1
        # go to the next letter
        i += 1

    # get L for the Coleman-Liau index
    L = (letter/words)*100
    # get S for the Coleman-Liau index
    S = (sentences/words)*100

    # calculate the grade level and round to the nearest int
    grade_level = round(0.0588 * L - 0.296 * S - 15.8)

    # print the grade level with specific text if before grade 1
    if (grade_level < 1):
        print("Before Grade 1")
    # print the grade level with specific text if after grade 15
    elif grade_level > 15:
        print("Grade 16+")
    # else print the grade level
    else:
        print(f"Grade {grade_level}")


# call main
main()