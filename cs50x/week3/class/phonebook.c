#include <cs50.h>
#include <stdio.h>
#include <string.h>

typedef struct
{
    string name;
    string phone;
}
person;

int main(void)
{
    // string names[] = {"Carter", "David"};
    // string numbers[] = {"+1-617-495-1000", "+1-949-468-2750"};

    // Declare our array of people
    person people[2];
    // Populate people array with data
    people[0].name = "Carter"; // '.' notation allows to access attributes of a struct / class
    people[0].phone = "+1-617-495-1000";

    people[1].name = "David";
    people[1].phone = "+1-949-468-2750";


    for (int i = 0; i < 2; i++)
    {
        if (strcmp(people[i].name, "David") == 0)
        {
            printf("Found %s\n", people[i].phone);
            return 0;
        }
    }
    printf("Not Found\n");
}