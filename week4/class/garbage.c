#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    int scores[1024]; // We declare, but not assign any values
    // As a result, we get an array of random garbage values :( )
    for (int i = 0; i < 1024; i++)
    {
        printf("%i\n", scores[i]);
    }
}