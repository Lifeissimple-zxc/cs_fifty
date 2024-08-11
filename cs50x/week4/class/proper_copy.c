#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h> // this is our header with memory managing  funcs like malloc and free
#include <string.h>

int main(void)
{
    char *s = get_string("s: ");
    if (s == NULL)
    {
        return 1;
    }
    // We don't actually create a new variable, we just reference the address
    //char *t = s; wrong approach

    // Correct copying implementation
    // Allocate memory & create a pointer
    char *t = malloc(strlen(s) + 1);
    // Check for NULL JIC
    if (t == NULL)
    {
        return 1;
    }
    // Actually copy our string
    // Loop implementation
    // for (int i = 0, len = strlen(s) + 1; i < len; i++) //we do +1 because we need our "\0", the terminator
    // {
    //     t[i] = s[i];
    // }
    // Non-loop implementation
    strcpy(t, s);
    // Checks //
    // Check for equality
    // Above we also checked for NULL
    if (strlen(t) > 0)
    {
        t[0] = toupper(t[0]);
    }
    printf("s: %s\n", s);
    printf("t: %s\n", t);

    // Free our memory
    free(t);

    return 0;
}