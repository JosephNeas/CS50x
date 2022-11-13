#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <math.h>

int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
int get_gradelevel(float letters, float words, float sentences);

int main(void)
{
    // define variables
    int letters = 0;
    int words = 0;
    int sentences = 0;
    int score = 0;

    // get user inputed string
    string text = get_string("Text: ");

    // Get all the letters words and sentences from the user inputed text
    letters = count_letters(text);
    words = count_words(text);
    sentences = count_sentences(text);

    // Get the gradelevel of the text
    score = get_gradelevel(letters, words, sentences);

    // if grade level is less than 1 print specific string
    if (score < 1)
    {
        printf("Before Grade 1\n");
    }
    // if grade level is more than 16 print specific string
    else if (score >= 16)
    {
        printf("Grade 16+\n");
    }
    else
    {
        printf("Grade %d\n", score);
    }
}

int count_letters(string text)
{
    int count = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        // look at each character in the text to determine if it is a letter, if so add 1 to count
        if ((text[i] >= 'a' && text[i] <= 'z') || (text[i] >= 'A' && text[i] <= 'Z'))
        {
            count += 1;
        }
    }
    return count;
}


int count_words(string text)
{
    int count = 0;
    // look at each space in the text to determine if it is the end of a word, if so add 1 to count
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 32)
        {
            count += 1;
        }
    }
    return count + 1;
}

int count_sentences(string text)
{
    int count = 0;
    // look at each character in the text to determine if it is an ending punctuation, if so add 1 to count
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == 33 || text [i] == 46 || text[i] == 63)
        {
            count += 1;
        }
    }
    return count;
}

int get_gradelevel(float letters, float words, float sentences)
{
    float score = 0;
    // printf("%d, %d, %d\n", letters, words, sentences);
    float lw = 0;
    float sw = 0;

    // get the float of letters divided by words times 100 as per the Coleman-Liau index
    lw = ((letters / words) * 100);

    // get the float of sentences divided by words times 100
    sw = ((sentences / words) * 100);

    // Perform the Coleman-Liau index
    score = (0.0588 * lw - 0.296 * sw - 15.8);
    // printf("%f\n", score);

    // round to get the nearest int
    score = round(score);

    // printf("%f\n", score);
    return score;
}
