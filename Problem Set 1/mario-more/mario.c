#include <cs50.h>
#include <stdio.h>

void print_brick(int bricks, int spaces);

int main(void)
{
    int height;
    do
    {
        height = get_int("Please enter a height between 1-8: ");
    }
    while (height < 1 || height > 8);

    // main function to print bricks
    for (int i = 1; i <= height; i++)
    {
        print_brick(i, height);
        printf("\n");
    }
}


void print_brick(int bricks, int spaces)
{
    // Print the spaces before the bricks
    for (int k = spaces - bricks; k >= 1; k--)
    {
        printf(" ");
    }
    // Print the first column(s) of bricks
    for (int i = 0; i < bricks; i++)
    {
        printf("#");
    }

    // print the space in between the bricks
    printf("  ");

    // print the second column(s) of bricks
    for (int j = 0; j < bricks; j++)
    {
        printf("#");
    }
}


