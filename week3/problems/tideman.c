#include <cs50.h>
#include <stdio.h>
// Adding some extra header files :)
#include <string.h>

// Max number of candidates
#define MAX 9

// preferences[i][j] is number of voters who prefer i over j
int preferences[MAX][MAX];

// locked[i][j] means i is locked in over j
bool locked[MAX][MAX];

// Each pair has a winner, loser
typedef struct
{
    int winner;
    int loser;
}
pair;

// Array of candidates
string candidates[MAX];
pair pairs[MAX * (MAX - 1) / 2];

int pair_count;
int candidate_count;

// Function prototypes
bool vote(int rank, string name, int ranks[]);
void record_preferences(int ranks[]);
void add_pairs(void);
void sort_pairs(void);
void lock_pairs(void);
void print_winner(void);
bool check_cycle(int winner, int loser);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: tideman [candidate ...]\n");
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
        candidates[i] = argv[i + 1];
    }

    // Clear graph of locked in pairs
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            locked[i][j] = false;
        }
    }

    pair_count = 0;
    int voter_count = get_int("Number of voters: ");

    // Query for votes
    for (int i = 0; i < voter_count; i++)
    {
        // ranks[i] is voter's ith preference
        int ranks[candidate_count];

        // Query for each rank
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i: ", j + 1);

            if (!vote(j, name, ranks))
            {
                printf("Invalid vote.\n");
                return 3;
            }
        }

        record_preferences(ranks);

        printf("\n");
    }

    add_pairs();
    sort_pairs();
    lock_pairs();
    print_winner();
    return 0;
}

// Update ranks given a new vote
bool vote(int rank, string name, int ranks[])
{
    // Check that name is valid using our global variable
    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            // The person was found so we make a record about our rank input
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[]) // revisit
{
    // Nested Loop over ranks and edit preferences[i][j]
    // For every candidate we will have 1 rank so we can use candidate_count for iterations
    // We iterate till pre-last candidate not to go over the limit of the candidates
    for (int i = 0; i < candidate_count - 1; i++)
    {
        // See who lost and update preferences array
        for (int j = i + 1; j < candidate_count; j++)
        {
            // If there is some value - increment
            if (preferences[ranks[i]][ranks[j]])
            {
                preferences[ranks[i]][ranks[j]]++;
            }
            // Otherwise - set to one
            else
            {
                preferences[ranks[i]][ranks[j]] = 1;
            }
        }
    }
    return;
}

// Record pairs of candidates where one is preferred over the other
void add_pairs(void)
{
    // Set pair count to zero as default value
    pair_count = 0;
    // Add pairs of candidates to pairs array of candidate 1 > candidate 2
    // Iterate over preferences array (it's nested)
    for (int i = 0; i < candidate_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            if (preferences[i][j] > preferences[j][i])
            {
                // Update pairs data
                pairs[pair_count].winner = i;
                pairs[pair_count].loser = j;
                // Add stre
                // Account for pair count increase
                pair_count++;
            }
        }
    }
    return;
}

// Sort pairs in decreasing order by strength of victory
void sort_pairs(void)
{
    // Selection sort
    // Itereate over items of an array
    // Since we are going for DESC order, we go from left to right
    for (int i = pair_count - 1; i > 0; i--)
    {
        for (int j = i - 1; j > -1; j--)
        {
            if (preferences[pairs[j].winner][pairs[j].loser] < preferences[pairs[i].winner][pairs[i].loser])
            {
                pair temp = pairs[i]; // Create a helper variable to perform swap
                // Swap items of the array
                pairs[i] = pairs[j];
                pairs[j] = temp;
            }
        }
    }
    return;
}

// Lock pairs into the candidate graph in order, without creating cycles
void lock_pairs(void)
{
    // Iterate over pairs
    for (int i = 0; i < pair_count; i++)
    {
        // Recursion to check if adding a lock creates a cycle
        // We use winner and user several time so storing to a variable
        int winner = pairs[i].winner;
        int loser = pairs[i].loser;
        // Check for cycle
        if (!check_cycle(winner, loser))
        {
            locked[winner][loser] = true;
        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // We need to find a row that has no true values in their row
    // Iterate over locked rows
    for (int col = 0; col < candidate_count; col++)
    {
        // Set true counter per row
        int true_count = 0;
        // Iterate over locked cols
        for (int row = 0; row < candidate_count; row++)
        {
            if (locked[row][col])
            {
                true_count++;
            }
        }
        // Check if our candidate is THE ONE (source)
        if (true_count == 0)
        {
            // Print & return if yes!
            string winner = candidates[col];
            int i = 0;
            do
            {
                printf("%c", winner[i]);
                i++;
            }
            while (winner[i] != '\0');
            // Closing newline print
            printf("\n");
        }

    }
    return;
}
// Makar's helpers
bool check_cycle(int winner, int loser)
{
    // Base case: check if our winner <> loser have a reverted relationship
    if (locked[loser][winner])
    {
        return true;
    }
    // Recursion
    // Check if loser is a winner against any candidate?
    for (int i = 0; i < candidate_count; i++)
    {
        if (locked[loser][i])
        {
            // We found a case where loser won against smbd
            // So we need to check that new winner against the OG winner for a cycle
            if (check_cycle(winner, i))
            {
                return true;
            }
        }
    }
    // Return false as our base case
    return false;

}