#include <cs50.h>
#include <stdio.h>

int main(void)
{
    //We use a do while because we are waiting user to give us an input
    int n;
    do
    {
        n = get_int("Size: ");
    }
    while (n < 1);
    // For each row
    for (i = 0; i < n; i++)
    {
        // For each column
        for (int j = 0; j < n; j++)
        {
            // Print a  brick
            printf("#")
        }
        //Move to the next row
        printf("\n");
    }
}