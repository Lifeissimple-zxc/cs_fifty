#include <cs50.h>
#include <stdio.h>

int main(int argc, string argv[]) //that's how we give command line args
{
    if (argc != 2)
    {
        printf("Missing CLI argument");
        return 1; //1 means problematic status
    }
    printf("hello, %s\n", argv[1]);
    return 0; //0 means ok, w/o explicit return statement main() always returns 0r
}