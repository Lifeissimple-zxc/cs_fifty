#include <stdio.h>
#include <string.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Check for command line args
    if (argc != 2)
    {
        printf("Usage: ./read infile\n");
        return 1;
    }

    // Create buffer to read into
    char buffer[7]; // It is a char array, so it is actually a pointer

    // Create array to store plate numbers
    char *plates[8];

    FILE *infile = fopen(argv[1], "r");

    int idx = 0;

    while (fread(buffer, 1, 7, infile) == 7)
    {
        // Replace '\n' with '\0'
        buffer[6] = '\0';

        // Save plate number in array
        //plates[idx] = buffer; // here we every time reassign a pointer thus affecting all items of plates array
        // Create storage for our string
        plates[idx] = malloc(strlen(buffer) + 1);
        // Copy
        strcpy(plates[idx], buffer);
        // Increment counter to continue running loop
        idx++;
    }

    for (int i = 0; i < 8; i++)
    {
        printf("%s\n", plates[i]);
    }

    // Free memory, we need to do for reach item in plates, because earlier we allocated it this way
    for (int i = 0; i < 8; i++)
    {
        free(plates[i]);
    }

    // Close our file
    fclose(infile);
}
