#include <stdio.h>
#include <cs50.h>
#include <string.h>
//Main
int main(void)
{
    string name = get_string("Name is: ");
    int lenght = strlen(name);
    printf("Name length is %i\n", lenght);
}