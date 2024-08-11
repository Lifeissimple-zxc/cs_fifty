#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h> // For bool types
#include "wav.h"
//https://cs50.harvard.edu/x/2023/psets/4/reverse/

int check_format(WAVHEADER header);
int get_block_size(WAVHEADER header);

int main(int argc, char *argv[])
{
    // Ensure proper usage
    // First we check that we have 2 args
    if (!((argc - 1) == 2))
    {
        printf("Wrong number of arguments passed, 2 are needed!\n");
        return 1;
    }
    // Then we check validity of the inputs
    for (int pos = 1; pos < 3; pos++)
    {
        if (strstr(argv[1], ".wav") == NULL) // could be done better, TBD if needed
        {
            printf("Expected a .wav file!\n");
            return 1;
        }
    }
    // Remember our filenames
    char *infile = argv[1];
    char *outfile = argv[2];

    // Open input file for reading
    FILE *inputwav = fopen(infile, "r");
    // Check that we actually have managed to open the file
    if (inputwav == NULL)
    {
        printf("Could not open %s.\n", infile);
        return 1;
    }

    // Read header into an array
    WAVHEADER wavhdr;
    fread(&wavhdr, sizeof(WAVHEADER), 1, inputwav);
    // Use check_format to ensure WAV format
    if (!check_format(wavhdr))
    {
        printf("File header is not a WAV header.\n");
        return 1;
    }

    // Open output file for writing
    FILE *outwav = fopen(outfile, "w");
    // Check that we actually have managed to open the file
    if (outwav == NULL)
    {
        printf("Could not open %s.\n", outfile);
        return 1;
    }

    // Write header to file
    fwrite(&wavhdr, sizeof(WAVHEADER), 1, outwav);

    // Use get_block_size to calculate size of block
    int block_size = get_block_size(wavhdr); // this is 4, but wav samples are usually 2, not sure why we need this at all

    // Write reversed audio to file
    // Place cursor to the end of our input file
    fseek(inputwav, 0, SEEK_END); // Place cursor at the end of the file
    // Store header size to a variable
    int hdr_size = (int) sizeof(WAVHEADER);
    BYTE buffer[block_size]; // Create array for storing bytes of the block size we calculated
    // Iteratively move block by block while also writing to outoput file
    // We iterate till we are above header size, exclusive!
    while ((ftell(inputwav)) > hdr_size)
    {

        // Because we start at the end of the file, we firstly do an extra step back of 1 block
        fseek(inputwav, -block_size, SEEK_CUR);
        // Read file one block, now we are where we started on this iteration
        fread(&buffer, block_size, 1, inputwav);
        // Write to output (our input position does not change)
        fwrite(&buffer, block_size, 1, outwav);
        // Step two blocks back to work
        fseek(inputwav, -block_size, SEEK_CUR);
    }
    // Close files
    fclose(inputwav);
    fclose(outwav);
}

int check_format(WAVHEADER header)
{
    // TODO #4
    if (header.format[0] == 'W' && header.format[1] == 'A' && header.format[2] == 'V' && header.format[3] == 'E')
    {
        return true;
    }
    return false;
}

int get_block_size(WAVHEADER header)
{
    // number of channels * bytes per sample
    return (int) header.numChannels * header.bitsPerSample / 8; // Dividing by 8 to convert bits to bytes
}