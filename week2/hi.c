#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Lines below do HI! using chars / chars casted as ints
    // char c1 = 'H';
    // char c2 = 'I';
    // char c3 = '!';

    // printf("%i %i %i\n", (int) c1, (int) c2, (int) c3); // () is type casting, explicit conversion of char to int

    //The following lines utilize string type
    string s = "HI!";
    printf("%i %i %i\n", s[0], s[1], s[2]);
}