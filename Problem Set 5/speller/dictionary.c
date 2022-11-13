// Implements a dictionary's functionality

#include <ctype.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>
#include <strings.h>
#include <stdlib.h>

#include "dictionary.h"

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 100000;
int total_words = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *word)
{
    // TODO
    // define all needed variables
    int value = hash(word);
    node *check = table[value];

    // while chech has a value
    while (check != NULL)
    {
        // if the word is in the node check->word return true
        if (strcasecmp(word, check->word) == 0)
        {
            return true;
        }
        // get the next word to repeat again
        check = check->next;
    };
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    // set the hash score variable
    int score = 0;
    for (int i = 0; i < strlen(word); i++)
    {
        // if the index of the word is a letter, get the score of it by making it a capital letter and minusing the ASCII by 'A'
        if ((word[i] >= 'A' && word[i] <= 'Z') || (word[i] >= 'a' && word[i] <= 'z'))
        {
            score = toupper(word[i]) - 'A';
        }
    }
    // return the score
    return score;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(const char *dictionary)
{
    // TODO
    // Open files and determine scaling factor
    FILE *input = fopen(dictionary, "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return false;
    }

    // intialize all vairables
    int count = 0;
    char next_word[LENGTH + 1];


    // load in dictionary
    while (fscanf(input, "%s", next_word) != EOF)
    {
        // create a new node in the while loop to copy each word
        node *output = malloc(sizeof(node));
        if (output == NULL)
        {
            free(output);
            return false;
        }

        // copy each word to the output node
        strcpy(output->word, next_word);

        // get the hash of the next word
        int value = hash(next_word);

        // put this hash value into the output node
        output->next = table[value];

        // put the whole of output into the hash table
        table[value] = output;

        // increase count by one to keep track of words
        count++;
    };
    // make the global variable total words equal to count
    total_words = count;

    // close the input file
    fclose(input);
    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void)
{
    // return the global variable total words
    return total_words;

}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    // TODO

    for (int i = 0; i < N; i++)
    {
        // make a new node unload to be equal to each word (location) inside of the table
        node *unload = table[i];
        // while the table is still a word
        while (unload != NULL)
        {
            // make a temp node set it equal to unload
            node *tmp = unload;
            // get the next word in unload
            unload = unload->next;
            // free the temp word
            free(tmp);
        };

        // if at the end of the table return true
        if (unload == NULL && i == N - 1)
        {
            return true;
        }
    }

    return false;
}
