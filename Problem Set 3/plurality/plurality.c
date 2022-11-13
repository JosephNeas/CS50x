#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // iterate through each candidate in the candidate array
    for (int i = 0; i < candidate_count; i++)
    {
        // look at their user inputs name compared to names in the candidate array and add 1 to their votes
        if (strcmp(candidates[i].name, name) == 0)
        {
            candidates[i].votes += 1;
            // printf("%s - %d \n", candidates[i].name, candidates[i].votes);
            return true;
        }
    }
    // if name doesn't match any name in the candidates array return false
    return false;
}

// Print the winner (or winners) of the election
void print_winner(void)
{
    // initialize the vairable for the winners vote count
    int winner_votes = 0;

    // loop through each canidates vote and compare to the winners votes
    for (int i = 0; i < candidate_count; i++)
    {
        // if the winners votes is lower than the current candidates update the winners votes
        if (candidates[i].votes > winner_votes)
        {
            winner_votes = candidates[i].votes;
        }
    }

    // loop through each candidates votes
    for (int i = 0; i < candidate_count; i++)
    {
        // If the candidates votes match the winners votes print their name
        if (candidates[i].votes == winner_votes)
        {
            printf("%s\n", candidates[i].name);
        }
    }
    return;
}