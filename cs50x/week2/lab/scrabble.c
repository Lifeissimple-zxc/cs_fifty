#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};

int compute_score(string word);
string def_winner(int score1, int score2);

int main(void)
{
    // Get input words from both players
    string word1 = get_string("Player 1: ");
    string word2 = get_string("Player 2: ");

    // Score both words
    int score1 = compute_score(word1);
    int score2 = compute_score(word2);

    //Define winner
    string result = def_winner(score1, score2);
    printf("%s\n", result);
}

int compute_score(string word)
{
    int word_score = 0;
    //Parse chars in string as upper
    for (int i = 0, word_len = strlen(word); i < word_len; i++) //double var declaration
    {
        //take all as upper - common ground
        char curr_char = toupper(word[i]);
        //check if char is a letter
        if (isalpha(curr_char))
        {
            //edit score for word
            word_score += POINTS[curr_char - 65];
        }
    }
    return word_score;
}

string def_winner(int score1, int score2)
{
    if (score1 == score2)
    {
        return "Tie!";
    }
    else if (score1 > score2)
    {
        return "Player 1 wins!";
    }
    else
    {
        return "Player 2 wins!";
    }
}
