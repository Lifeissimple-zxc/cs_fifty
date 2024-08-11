#include <cs50.h>
#include <stdio.h>
#include <cs50.h>
#include <stdio.h>

void draw_recursive(int n);

int main(void)
{
    int height = get_int("Height: ");
    draw_recursive(height);
}

//
void draw_recursive(int n)
{
    // We implement a save check to exit the execution if we are out of pyramid blocks to draw
    if (n <= 0)
    {
        return;
    }

    draw_recursive(n - 1); // This is our recursive function call

    for (int i = 0; i < n; i++)
    {
        printf("#");
    }
    printf("\n");
}