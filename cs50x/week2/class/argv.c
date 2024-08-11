#include <cs50.h>
#include <stdio.h>

int main(int argc, string argv[]) //that's how we give command line args
{
    if (argc == 2)
    {
        printf("Hello, %s\n", argv[1]);
    }
    else
    {
        printf("Hello world\n");
    }
}