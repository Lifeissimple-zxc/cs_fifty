#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Promopt user for x variable
    int x = get_float("x: "); // long = long interger type, it is neded to compute bigger numbers
    // Prompt user for y variable
    int y = get_float("y: ");
    // Perform division
    float z = float(x) / float(y); // C does Truncation when dividing integers (it only returns the INT part, float is dropped)
    printf("%.50f\n", z);
}