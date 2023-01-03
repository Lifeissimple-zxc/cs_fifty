#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>
// https://cs50.harvard.edu/x/2023/problems/3/atoi/

int convert(string input);

int main(void)
{
    string input = get_string("Enter a positive integer: ");

    for (int i = 0, n = strlen(input); i < n; i++)
    {
        if (!isdigit(input[i]))
        {
            printf("Invalid Input!\n");
            return 1;
        }
    }

    // Convert string to int
    printf("%i\n", convert(input));
}

int convert(string input)
{
    // base case for recursion: we stop if null terminator is the first char bc it means we are done!
    if (input[0] == '\0')
    {
        return 0;
    }
    // get last char index
    int index = 0;
    do
    {
        index++;
    }
    while (input[index] != '\0');
    index--;
    // Get last char
    char last_char = input[index];
    // Convert last char to int
    int char_converted = last_char - 48;
    // Update our input string
    input[index] = '\0';
    // recursive function call
    return char_converted + (convert(input) * 10);
}