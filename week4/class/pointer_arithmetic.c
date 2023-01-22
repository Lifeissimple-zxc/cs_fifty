#include <stdio.h>

int main(void)
{
    char *s = "HI!"; // This works
    // Pointer arithmetic
    // printf("%c\n", *s);
    // printf("%c\n", *(s+1)); // addition on pointer, we move 1 byte
    // printf("%c\n", *(s+2)); // one more addition, we move 1 more byte
    // printf("%c\n", *(s+50000)); // one more addition, we move many more bytes, SEGMENTATION FAULT!
    // //////////////////////////////////////////////
    printf("%s\n", s);
    printf("%s\n", s+1); // print string from the second character
    printf("%s\n", s+2); // print string from the third character
}