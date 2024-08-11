#include <cs50.h>
#include <stdio.h>

void build_pyramid(int size);

int main(void)
{
    int size; // Declare size variable
    //Check input for validity
    do
    {
        size = get_int("Size: "); // Get user input
    }
    while (size < 1 || size > 8);
    build_pyramid(size);
}

void build_pyramid(int size)
{
    //Loop for rows
    for (int row = 0; row < size; row++)
    {
        //Loop for columns
        for (int col = 0; col < (size * 2) + 1; col++)
        {
            //If in middle -> print a double space
            if (col == size)
            {
                printf("  ");
            }
            //Otherwise -> Print a brick
            else
            {
                if (col < size - row - 1)
                {
                    printf(" ");
                }
                else
                {
                    // Pyramind form - right side
                    if (!(col > size + row + 1))
                    {
                        printf("#");
                    }
                }
            }
        }
        //Change row
        printf("\n");
    }
}