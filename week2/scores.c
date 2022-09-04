#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int n = get_int("How many scores? ");

    int scores[n];
    //Collect scores
    for (int i = 0; i < n; i++)
    {
        scores[i] = get_int("Score: ");
    }
    //Compute AVG
    int count = 0;
    int sum = 0;
    for (int i = 0; i < n; i++)
    {
        count++;
        sum += i;
    }
    float avgScore = sum / count;
    printf("Average score is: %f\n", avgScore)


}