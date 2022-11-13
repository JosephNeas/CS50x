#include <cs50.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

bool only_digits(string s);
string cipher_text(string plain_text, int secret_key);

int main(int argc, string argv[])
{
    int secret_key = 0;
    if (argc == 2 && only_digits(argv[1]) == true)
    {
        secret_key = atoi(argv[1]);
        string plain_text = get_string("plaintext: ");
        string cipered_text = cipher_text(plain_text, secret_key);
        printf("ciphertext: %s\n", cipered_text);

        // printf("%d \n", secret_key);
    }
    else
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

}

bool only_digits(string s)
{
    bool number = false;
    // iterate through each number from the user input to see if the input is a number between 1 and 9
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        // check if each char is a number
        if (s[i] >= '1' && s[i] <= '9')
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

string cipher_text(string plain_text, int secret_key)
{
    int over_Z = 0;
    int letter_over_Z = 0;
    int over_z = 0;
    int letter_over_z = 0;

    for (int i = 0, n = strlen(plain_text); i < n; i++)
    {
        // look at lower case letters
        if ((plain_text[i] >= 'a' && plain_text[i] <= 'z'))
        {
            // look at if the secret key go over z because I then need to restart at a
            if ((plain_text[i] + secret_key >= 'z'))
            {
                // get the amount over z
                over_z = (plain_text[i] + secret_key);

                // get the remainder over z
                over_z = (over_z - 'z') % 26;

                // get the letters exact number
                letter_over_z = plain_text[i];

                // look at case where there should be no change in letter because the key adds up to the same number
                if (over_z == 0)
                {
                    plain_text[i] = plain_text[i];
                }
                // look at the case where the letter need to reset to add the remainder to a
                else
                {
                    // get the total over 96 to be able to make the plain text start over at a
                    letter_over_z = letter_over_z - 96;

                    // reset the plain text at a
                    plain_text[i] = plain_text[i] - letter_over_z;

                    // add the remainder to the plain text
                    plain_text[i] = plain_text[i] + over_z;
                }
            }

            // else just add the letter normally
            else
            {
                plain_text[i] = (plain_text[i] + secret_key);
            }
        }
        else if (plain_text[i] >= 'A' && plain_text[i] <= 'Z')
        {
            if ((plain_text[i] + secret_key >= 'Z'))
            {
                // get the amount over Z
                over_Z = (plain_text[i] + secret_key);

                // get the remainder over Z
                over_Z = (over_Z - 'z') % 26;

                // get the letters exact number
                letter_over_Z = plain_text[i];

                // look at case where there should be no change in letter because the key adds up to the same number
                if (over_Z == 0)
                {
                    plain_text[i] = plain_text[i];
                }
                // look at the case where the letter need to reset to add the remainder to A
                else
                {
                    // get the total over 64 to be able to make the plain text start over at A
                    letter_over_Z = letter_over_Z - 64;

                    // reset the plain text at a
                    plain_text[i] = plain_text[i] - letter_over_Z;

                    // add the remainder to the plain text
                    plain_text[i] = plain_text[i] + over_Z;
                }
            }

            // else just add the letter normally
            else
            {
                plain_text[i] = (plain_text[i] + secret_key);
            }
        }
    }
    return plain_text;
}
