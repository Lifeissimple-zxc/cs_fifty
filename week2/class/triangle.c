#include <cs50.h>
#include <stdio.h>

bool valid_triangle(double a, double b, double c);

// main goes here
int main(void)
{
    bool check = valid_triangle(7, 10, 5);
    printf("%s\n", check?"true":"false");
}

bool valid_triangle(double a, double b, double c)
{
    // check that all sides are positive
    if ((a <= 0) || (b <= 0) || (c <= 0))
    {
        return false;
    }

    // check sum sides
    if ( ((a + b) < c) || ((a + c) < b) || ((b + c) < a) )
    {
        return false;
    }
    
    return true;
}