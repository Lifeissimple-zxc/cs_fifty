#include <stdio.h>
#include <cs50.h>

int main(void)
{
    int user_input = get_int("Enter a number: ");
    if (user_input % 2 == 0)
    {
        printf("%i is an even number", user_input);
    }
    else
    {
        printf("%i is an odd number", user_input);
    }
}