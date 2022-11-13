#include <cs50.h>
#include <stdio.h>

void check_valid(long credit_card);
int extract_numbers(long number);


int main(void)
{
    long credit_card  = get_long("Number: ");
    check_valid(credit_card);
}

void check_valid(long credit_card)
{
    long for_length = credit_card;
    long card_check = credit_card;
    int times_2 = 0;
    int non_times = 0;
    int i = 0;
    int total = 0;
    int multi = 0;
    int j, remainder, remainder_multi, times_2_last, times_2_last_number;

    // get the length of the credit card
    while(for_length > 0)
    {
        for_length = for_length / 10;
        i++;
    }

     // check to see if the card is invalid
    if (i != 13 && i != 15 && i != 16)
    {
        printf("INVALID\n");
        return;
    }
    do
    {
            // get the last remainder of last number in the credit card
            remainder = credit_card % 10;

            // store each non_multiply number into the array
            non_times += remainder;

            // go to next number in credit card
            credit_card /= 10;

            // get the next remainder of next number in the credit card
            remainder_multi = credit_card % 10;
            times_2 = remainder_multi;

            credit_card /= 10;

            // times these number by 2
            times_2 = times_2 * 2;

            // get the individual number of the numbers that after they have been multiplied by 2
            times_2_last = times_2 % 10;
            times_2_last_number = times_2 / 10;
            multi = multi + times_2_last + times_2_last_number;
    }
    while (credit_card != 0);

    total = multi + non_times;
    // printf("%d \n", total);

    // Check if the total can be divided by 10 evenly
    if (total % 10 == 0)
    {
        // get the first two numbers of the credit card
        do
        {
            card_check /= 10;
        }
        while (card_check > 100);

        // check if the card is a Visa
        if (card_check / 10 == 4)
        {
            printf("VISA\n");
        }

        // check if the card is a Amex
        else if (card_check / 10 == 3 && (card_check % 10 == 4 || card_check % 10 == 7))
        {
            printf("AMEX\n");
        }
        // Check if the card is a Mastercard
        else if (card_check / 10 == 5 && (card_check % 10 > 0 && card_check % 10 < 6))
        {
            printf("MASTERCARD\n");
        }
        else
        {
            printf("INVALID\n");
        }
    }
    // if nothing matches then it must be an invalid card
    else
    {
        printf("INVALID\n");
    }
}

