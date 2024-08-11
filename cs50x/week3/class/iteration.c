#include <cs50.h>
#include <stdio.h>

void draw_classic(int n);

int main(void)
{
    int height = get_int("Height: ");
    draw_classic(height);
}

//
void draw_classic(int n)
{
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < i + 1; j++)
        {
            printf("#");
        }
        printf("\n");
    }
}