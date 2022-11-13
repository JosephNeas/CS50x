#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>


typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Check for invalid usage
    if (argc != 2)
    {
        printf("Usage: recover IMAGE\n");
        return 1;
    }

    // open image file
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    // define the output file
    FILE *output = NULL;

    // get the number for each jpg
    int n = 0;

    // intialize a char for each file made
    char file[8] = {0};

    // want to look at each byte of a jpg, 152 bytes
    BYTE buffer[512];

    // while input is open
    while (fread(&buffer, sizeof(buffer), 1, input) == 1)
    {
        // check to see if the first three bytes match to that of a jpg
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            // if it is not the first time through then close the previous output
            if (n != 0)
            {
                fclose(output);
            }

            // format the file to the next jpg found
            sprintf(file, "%03i.jpg", n);
            // write this specific jpg file to the output file
            output = fopen(file, "w");
            // increase n by one as have added another jpg
            n++;
        }

        // if not first time through
        if (n != 0)
        {
            // write the entire file to output 
            fwrite(&buffer, sizeof(buffer), 1, output);
        }
    };

    fclose(input);
    fclose(output);
}