#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    // TODO: Print the winner
    if (score1 > score2)
    {
        printf("Player 1 wins!\n");
    }
    else if (score2 > score1)
    {
        printf("Player 2 wins!\n");
    }
    else
    {
        printf("Tie!\n");
    }
}

int compute_score(string word)
{
    // TODO: Compute and return score for string
    // set up needed variables
    int i = 0;
    int index = 0;
    int total = 0;
    int n = strlen(word);

    // convert all the leters of the string to upper case
    do
    {
        if (word[i] >= 'a' && word[i] <= 'z')
        {
            word[i] = word[i] - 32;
        }
        else
        {
            word[i] = word[i];
        }
        i++;
    }
    while (i < n);

    // printf("%s", word);
    // printf("\n");

    // Get the points of each letter by interating through each letter in the now lower case word
    for (i = 0, n = strlen(word); i < n; i++)
    {
        // only want to look at letters of the word; nothing else in the ASCII table
        if (word[i] >= 'A' && word[i] <= 'Z')
        {
            index = word[i] - 65;
            // printf("%d \n", POINTS[index]);
            total += POINTS[index];
        }
    }
    // printf("%d \n", total);
    return total;
}
