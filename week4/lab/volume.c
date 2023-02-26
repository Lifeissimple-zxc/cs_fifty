// Modifies the volume of an audio file
// https://cs50.harvard.edu/x/2023/labs/4/volume/

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h> // needed for reading / writing data from .wav file

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n"); // temp line
        return 1;
    }

    // Convert string input to float
    float factor = atof(argv[3]);

    // Copy header from input file to output file
    // Create pointer for header info (we do it on stack so no free() to be called later)
    uint8_t header_p[HEADER_SIZE];
    // Read header from input to our pointer
    fread(header_p, sizeof(uint8_t) * HEADER_SIZE, 1, input);
    // Write from pointer to new file
    fwrite(header_p, sizeof(uint8_t) * HEADER_SIZE, 1, output);

    // Read samples from input file and write updated data to output file
    // Move cursor within sfiles to pass header
    fseek(input, (long int) HEADER_SIZE, SEEK_SET);
    fseek(output, (long int) HEADER_SIZE, SEEK_SET);
    int16_t tmp; // temp variable for storing sample data
    //while (feof(input) == 0) // Does not work because feof returns 0 later then we need it
    while (fread(&tmp, sizeof(int16_t), 1, input)) // Read till we can
    {
        // Scale our sample
        tmp *= factor;
        // Write to output file
        fwrite(&tmp, sizeof(int16_t), 1, output);
    }
    // Close files
    fclose(input);
    fclose(output);
}