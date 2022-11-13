# include <cs50.h>
# include <stdio.h>

int main(void)
{
    // Take in name, string
    string name = get_string("What is your name? ");

    //Print their name 
    printf("Hello, %s\n", name);
}