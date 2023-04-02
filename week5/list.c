#include <stdio.h>
#include <stdlib.h>

int main(void)
{
    // How can we allocate more memory to extend our array?
    int *list = malloc(3 * sizeof(int));

    if (list == NULL)
    {
        return 1; // This means stuff went bad :()
    }
    list[0] = 1; // we can also do *list = 1;
    list[1] = 2; // *(list + 1);
    list[2] = 3;

    // Some stuff (code) here...

    // Allocate more memory
    int *tmp = realloc(list, 4 * sizeof(int)); // this is how we reallocate memory to extend our array
    // The above allows us not to manually copy values from 1 array to another
    // We store it to a temp variable not to introduce memory leak chance
    if (tmp == NULL) // malloc or realloc returns NULL if device is out of memory
    {
        free(list); // free what we asked for earlier
        return 1;
    }
    // Add new value to the array
    list[3] = 4;

    for (int i = 0; i < 4; i++)
    {
        printf("%i\n", list[i]);
    }
    // Free our allocated memory
    free(list); //free(tmp); also works

    //OLD WAY OF DOING STUFF DOWN
    // int list[3];

    // list[0] = 1;
    // list[1] = 2;
    // list[2] = 3;

    // for (int i = 0; i < 3; i++)
    // {
    //     printf("%i\n", list[i]);
    // }

}