#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    // Manual array instantiation below:
    int *x = malloc(3 * sizeof(int)); // give me a piece of memory that can store 3 ints?
    // Check for null
    if (x == NULL)
    {
        return 1;
    }
    x[0] = 72;
    x[1] = 73;
    x[2] = 33;
    // Free our memory
    free(x);
}
