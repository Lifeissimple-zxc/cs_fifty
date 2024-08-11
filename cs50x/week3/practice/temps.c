// Practice working with structs
// Practice applying sorting algorithms

// https://cs50.harvard.edu/x/2023/problems/3/temps/

#include <cs50.h>
#include <stdio.h>

#define NUM_CITIES 10 // defines a const, no ';' at the end is needed
// Define a data struct containing a city and its temperature
typedef struct
{
    string city;
    int temp;
}
avg_temp;

avg_temp temps[NUM_CITIES];

void sort_cities(avg_temp avg_temps_array[]);

int main(void)
{
    temps[0].city = "Austin";
    temps[0].temp = 97;

    temps[1].city = "Boston";
    temps[1].temp = 82;

    temps[2].city = "Chicago";
    temps[2].temp = 85;

    temps[3].city = "Denver";
    temps[3].temp = 90;

    temps[4].city = "Las Vegas";
    temps[4].temp = 105;

    temps[5].city = "Los Angeles";
    temps[5].temp = 82;

    temps[6].city = "Miami";
    temps[6].temp = 97;

    temps[7].city = "New York";
    temps[7].temp = 85;

    temps[8].city = "Phoenix";
    temps[8].temp = 107;

    temps[9].city = "San Francisco";
    temps[9].temp = 66;

    sort_cities(temps);

    printf("\nAverage July Temperatures by City\n\n");

    for (int i = 0; i < NUM_CITIES; i++)
    {
        printf("%s: %i\n", temps[i].city, temps[i].temp);
    }
}

// TODO: Sort cities by temperature in descending order
void sort_cities(avg_temp avg_temps_array[]) // this is correct (almost)
{
    // Selection sort
    // Itereate over items of an array
    // Since we are going for DESC order, we go from left to right
    for (int i = NUM_CITIES - 1; i > 0; i--)
    {
        for (int j = i - 1; j > -1; j--)
        {
            if (avg_temps_array[j].temp < avg_temps_array[i].temp)
            {
                avg_temp temp = avg_temps_array[i]; // Create a helper variable to perform swap
                // Swap items of the array
                avg_temps_array[i] = avg_temps_array[j];
                avg_temps_array[j] = temp;
            }
        }
    }
}

// void sort_cities(avg_temp avg_temps_array[]) // this is correct (almost)
// {
//     // Selection sort
//     // Itereate over items of an array
//     for (int i = 0; i < NUM_CITIES - 1; i++)
//     {
//         // Find max value in the array because we need it in descending order, not ascending
//         for (int j = i + 1; j < NUM_CITIES; j++)
//         {
//             if (avg_temps_array[j].temp > avg_temps_array[i].temp)
//             {
//                 avg_temp temp = avg_temps_array[i]; // Create a helper variable to perform swap
//                 // Swap items of the array
//                 avg_temps_array[i] = avg_temps_array[j];
//                 avg_temps_array[j] = temp;
//             }
//         }
//     }
// }
