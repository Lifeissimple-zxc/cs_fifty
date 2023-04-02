#include <stdio.h>
#include <stdlib.h>

// Define our node struct for linked list creation
typedef struct node
{
    int number;
    struct node *next;
}
node;

int main(int argc, char *argv[])
{
    node *list = NULL; // Start of the list
    // Iterate over our argv params
    for (int i = 1; i < argc; i++)
    {
        int number = atoi(argv[i]);

        node *n = malloc(sizeof(node)); // allocate memory for a temp node
        // Error check & exit if applicable
        if (n == NULL)
        {
            // Here we have a bug, we need to free memory that we might allocate if we fail on 2+ iteration
            return 1;
        }
        // Put number from args to the node
        n -> number = number;
        // Set linker of the node to NULL because it is last at this point
        n -> next = NULL;
        // Update linker
        n -> next = list;
        list = n;
    }
    // Iterate over our list and show contents of the list
    node *ptr = list; // points at the first node of the list
    while (ptr != NULL)
    {
        printf("%i\n", ptr->number);
        ptr = ptr -> next; // Update where pointer points
        // On the last iteration we expect to get to NULL
    }
    // Freeing memory
    ptr = list;
    while (ptr != NULL)
    {
        node *next = ptr -> next;
        free(ptr);
        ptr = next;
    }

}