#include <stdio.h>
#include <cs50.h>
#include <string.h>

int main(void)
{
    string s = get_string("Give input: ");
    printf("Printf output is:\n%s\n", s);
    //How can we do it differently?
    printf("Output char by char:\n");
    for (int i = 0, n = strlen(s); i < n; i++) // declare 2 vars in a for loops
    {
        printf("%c",s[i]);
    }
    printf("\n");


}