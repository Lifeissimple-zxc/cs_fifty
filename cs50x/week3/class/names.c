#include <cs50.h>
#include <stdio.h>
#include <string.h>

int main(void)
{
    string names[] = {"Bill", "Charlie", "Fred", "George", "Ginny", "Percy", "Ron"};

    for (int i = 0; i < 7; i++)
    {
        //if (names[i] == "Ron") // This makes us face an error :(
        // We cannot directly compare strings because it is not a primitive in C :(
        if (strcmp(names[i], "Makar") == 0)
        {
            printf("Found:)\n");
            return 0;
        }
    }
    printf("Not Found:(\n");
    return 1;
}