#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>
#include <stdio.h>

bool only_letters(string s);
string cipher_text(string plain_text, string letters);

int main(int argc, string argv[])
{
    if (argc == 2 && only_letters(argv[1]) == true && strlen(argv[1]) == 26)
    {
        string plain_text = get_string("plaintext: ");
        string ciphered_text = cipher_text(plain_text, argv[1]);

        printf("ciphertext: %s\n", ciphered_text);
    }
    else if(strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }
}

bool only_letters(string s)
{
    bool number = false;
    // iterate through each number from the user input to see if the input is a number between 1 and 9
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        // check if each char is a number
        if ((s[i] >= 'a' && s[i] <= 'z') || (s[i] >= 'A' && s[i] <= 'Z'))
        {
            number = true;
        }
        // if not return false and stop the for loop
        else
        {
            return false;
        }
    }
    return number;
}

string cipher_text(string plain_text, string letters)
{
    string cipher = NULL;
    int lower_letters = 0;
    int cap_letters = 0;
    for (int i = 0, n = strlen(plain_text); i < n; i++)
    {
        if((plain_text[i] >= 'a' && plain_text[i] <= 'z'))
        {
            lower_letters = plain_text[i] - 96;
            plain_text[i] = tolower(letters[lower_letters]);
        }
        else if ((plain_text[i] >= 'A' && plain_text[i] <= 'Z'))
        {
            cap_letters = plain_text[i] - 64;
            plain_text[i] = toupper(letters[cap_letters]);
        }
    }
    return plain_text;
}