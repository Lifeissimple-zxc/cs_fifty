#include <ctype.h>
#include <cs50.h>
#include <stdio.h>
#include <string.h>

int compute_score(string word);
// Points assigned to each letter of the alphabet
int POINTS[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
int main(void)
{
    string word = "code!";
    int word_score = compute_score(word);
    printf("%s word gives %i score in Scrabble!\n", word, word_score);

}

//Helpers
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