#include <cs50.h>
#include <stdio.h>

int main(void)
{
    const int MINE = 2; //const prevents a variable to be changed, CAPITALISAION is a reminder that is is a constant
    int points = get_int("How many points did you lose? ");

    if (points < MINE)
    {
        printf("You lost fewer points than me.\n");
    }
    else if (points > MINE)
    {
        printf("You lost more points than me.\n");
    }
    else
    {
        printf("You lost the same number of points as me.\n")
    }
}