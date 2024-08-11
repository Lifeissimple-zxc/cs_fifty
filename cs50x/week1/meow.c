#include <stdio.h>

void meow(int times_to_meow); // propotype of meow(), needed here because of how C is created

int main(void)
{
   meow(3);
}

//Declaration of meow():
void meow(int times_to_meow)
{
   for (int i = 0;, i < times_to_meow; i++)
   {
      printf("meow\n");
   }
}