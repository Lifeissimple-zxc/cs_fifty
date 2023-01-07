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
    // // Get count of candidates
    // int candidate_count = sizeof(candidates) / sizeof(candidates[0]);
    // Check that name is valid using our global variable
    for (int i = 0; i < MAX; i++)
    {
        if (strcmp(name, candidates[i]) == 0)
        {
            // We located the candidate so we edit ranks array
            ranks[rank] = i;
            return true;
        }
    }
    return false;
}

// Update preferences given one voter's ranks
void record_preferences(int ranks[])
{
    // Get ranks count
    // int ranks_count = sizeof(ranks) / sizeof(ranks[0]);
    // Nested Loop over ranks and edit preferences[i][j]
    // For every candidate
    for (int i = 0; i < MAX; i++)
    {
        // Stop if we reached last element
        if (i == MAX - 1)
        {
            return;
        }
        // See who lost and update preferences array
        for (int j = i + 1; j < MAX; j++)
        {
            // Check current value
            int current_prefence = preferences[i][j];
            // Increment if it is 1 or higher
            if (current_prefence >= 1)
            {
                preferences[i][j]++;
            }
            // Set to 1 if not
            else
            {
                preferences[i][j] = 1;
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

    // Get how many rows we have in preferences and how many items are in one row
    int preference_rows = sizeof(preferences) / sizeof(preferences[0]);
    int row_items = sizeof(preferences[0]) / sizeof(preferences[0][0]);
    // Iterate over preferences array (it's nested)
    for (int i = 0; i < preference_rows; i++)
    {
        for (int j = 0; j < row_items; j++)
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
            if (preferences[pairs[i].winner][pairs[i].loser] < preferences[pairs[j].winner][pairs[j].loser])
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
    // TODO
    // Populate locked array with true / false flags
    for (int i = 0; i < pair_count; i++)
    {
        int true_count = 0; // might be bullshit
        for (int j = 0; j < MAX; j++)
        {
            // Put false as we don't expect to have self-locked vervices
            if (i == j)
            {
                locked[i][j] = false;
            }
            // Lock vertices
            locked[i][j] = true;


        }
    }
    return;
}

// Print the winner of the election
void print_winner(void)
{
    // TODO
    return;
}