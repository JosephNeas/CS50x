#include "helpers.h"
#include <math.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float pixel = 0.0;
    // go to each pixel in a column
    for (int i = 0; i < height; i++)
    {
        // go to each pixel in a row
        for (int j = 0; j < width; j++)
        {
            // get the total rgb of each pixel
            pixel = image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed;
            // divide by 3.0 to get the average rgb
            pixel = pixel / 3.0;
            pixel = round(pixel);

            // make each pixel's rgb the same as the average pixel rbg
            image[i][j].rgbtBlue = pixel;
            image[i][j].rgbtGreen = pixel;
            image[i][j].rgbtRed = pixel;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float original_red, original_blue, original_green;
    float sepiaRed = 0, sepiaBlue = 0, sepiaGreen = 0;

    // go to each pixel in a column
    for (int i = 0; i < height; i++)
    {
        // go to each pixel in a row
        for (int j = 0; j < width; j++)
        {
            // get the total rgb of each pixel
            original_red = image[i][j].rgbtRed;
            original_blue = image[i][j].rgbtBlue;
            original_green = image[i][j].rgbtGreen;

            // get the sepia rgb for each pixel
            sepiaRed = .393 * original_red + .769 * original_green + .189 * original_blue;
            sepiaBlue = .272 * original_red + .534 * original_green + .131 * original_blue;
            sepiaGreen = .349 * original_red + .686 * original_green + .168 * original_blue;

            // make sure each sepiaRGB is capped at 255
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            // apply the sepia filter
            image[i][j].rgbtRed = round(sepiaRed);
            image[i][j].rgbtBlue = round(sepiaBlue);
            image[i][j].rgbtGreen = round(sepiaGreen);
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    int temp[3];
    // go to each pixel in a column
    for (int i = 0; i < height; i++)
    {
        // want a reverse variabel that is the width minus 1 to stay in the bounds of the width - j
        int reverse = width - 1;
        // go to each pixel in a row less than the width divided by 2 as the code will fail if going over half the width
        for (int j = 0; j < width / 2; j++)
        {
            // put the first half of the image in a temp variable to add to reverse image
            temp[0] = image[i][j].rgbtRed;
            temp[1] = image[i][j].rgbtGreen;
            temp[2] = image[i][j].rgbtBlue;

            // put the reverse image in the image starting from the left
            image[i][j].rgbtRed = image[i][reverse - j].rgbtRed;
            image[i][j].rgbtGreen = image[i][reverse - j].rgbtGreen;
            image[i][j].rgbtBlue = image[i][reverse - j].rgbtBlue;

            // put the left half of the image in the right starting from the right
            image[i][reverse - j].rgbtRed = temp[0];
            image[i][reverse - j].rgbtGreen = temp[1];
            image[i][reverse - j].rgbtBlue = temp[2];
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE temp[height][width];

    // go to each pixel in a column
    for (int i = 0; i < height; i++)
    {
        // go to each pixel in a row less than the width divided by 2 as the code will fail if going over half the width
        for (int j = 0; j < width; j++)
        {
            // intialize variables to get the averages of the rgb colors in order to average out the neighbors
            int red = 0, blue = 0, green = 0;
            // to divide rgb by the amount of neighbors used
            float count = 0;

            // look at the height to see if near corners as well as get the 3 different heights near the intial pixel
            for (int k = i - 1; k < (i + 2); k++)
            {
                // look at the width to see if near corners as well as get the 3 different widths at each height near the intial pixel
                for (int l = j - 1; l < (j + 2); l++)
                {
                    // if the image is near a corner skip over values that don't exist
                    if (k < 0 || k > (height - 1) || l < 0 || l > (width - 1))
                    {
                        continue;
                    }

                    // add up all the rgb color values
                    red += image[k][l].rgbtRed;
                    green += image[k][l].rgbtGreen;
                    blue += image[k][l].rgbtBlue;

                    // add 1 to count as this means we got the values of a pixel
                    count++;
                }
                // put the average color of rgb in the temp image
                temp[i][j].rgbtRed = round(red / count);
                temp[i][j].rgbtGreen = round(green / count);
                temp[i][j].rgbtBlue = round(blue / count);
            }
        }
    }

    // go to each pixel in a column
    for (int i = 0; i < height; i++)
    {
        int six_pixel = 0;
        // go to each pixel in a row less than the width divided by 2 as the code will fail if going over half the width
        for (int j = 0; j < width; j++)
        {
            // pu the blurred image value into each pixel
            image[i][j].rgbtRed = temp[i][j].rgbtRed;
            image[i][j].rgbtGreen = temp[i][j].rgbtGreen;
            image[i][j].rgbtBlue = temp[i][j].rgbtBlue;
        }
    }
    return;
}
