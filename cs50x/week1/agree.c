#include <stdio.h>
#include <cs50.c>

int main(void)
{
    //Prompt user to agree
    char c = get_char("Do you agree? ");
    //Check if the user agreed
    if (c == 'y' || c == 'Y') // || stands for OR in C
    {
        printf("Agreed.\n");
    }
    else if (c == 'n' || c == 'N')
    {
        printf("Disagreed.\n");
    }
    // else
    // {
        
    // }
}