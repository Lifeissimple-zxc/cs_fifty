#include <cs50.h>
#include <stdio.h>

int compute_years(int current_pop, int end_pop);

int main(void)
{
    // TODO: Prompt for start size
    int start_size;
    // Keep on prompting till we get a proper input
    do
    {
        start_size = get_int("Start size: ");
    }
    while (start_size < 9);
    // TODO: Prompt for end size
    int end_size;
    do
    {
        end_size = get_int("End size: ");
    }
    while (end_size < start_size);
    // TODO: Calculate number of years until we reach threshold
    int years_needed = compute_years(start_size, end_size);
    // TODO: Print number of years
    printf("Years: %i\n", years_needed);
}
// Helpers
int compute_years(int current_pop, int end_pop)
{
    int years_needed = 0;
    if (current_pop == end_pop)
    {
        return years_needed;
    }
    int population_by_year = current_pop;
    do
    {
        // Compute how many we lose / gain
        int lamas_lost = population_by_year / 4;
        int lamas_gained = population_by_year / 3;
        // Compute Population by EOY
        population_by_year = population_by_year + lamas_gained - lamas_lost;
        // Increment year variable
        years_needed++;
    }
    while (population_by_year < end_pop);

    return years_needed;
}
/////////////////////////////////Functions based approach I considered but decided not to use :(
// int validate_start_input(int lamas_count)
// {
//     while (lamas_count < 9)
//     {
//         lamas_count = get_int("Start size: ");
//     }
// }

// int validate_end_input(int start_size, int end_size)
// {
//     while (end_size <= start_size)
//     {
//         end_size = get_int("End size: ")
//     }
// }