#include <string.h>
#include <cs50.h>
#include <ctype.h>
#include <stdio.h>

int main(void) //void == "I do not take CLI args"s
{
    string s = get_string("Before: ");
    printf("After:  ");
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        //if upper --> make lower: this can be shortened to just
        printf("%c", toupper(s[i]));
        // char curr_c = s[i];
        // if (islower(s[i])) // use of a ready func
        // {
        //     printf("%c", toupper(curr_c));
        // }
        // else
        // {
        //     printf("%c", curr_c);
        // }
    }
    printf("\n");
}