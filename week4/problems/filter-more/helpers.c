#include "helpers.h"
#include "math.h" // We need this to round our colors' values
#include "stdio.h" // For printf debugging :)
#include "stdlib.h" // For malloc
//https://cs50.harvard.edu/x/2023/psets/4/filter/more/
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Prepare a variable for average computation
    BYTE avg_color;
    // Iterate over rows
    for (int row = 0; row < height; row++)
    {
        // Iterate over cols
        for (int col = 0; col < width; col++)
        {
            // Compute average: important to divide by float or we lose precision!
            avg_color = (BYTE) round((image[row][col].rgbtBlue + image[row][col].rgbtGreen + image[row][col].rgbtRed) / 3.0);
            //printf("%i\n", avg_col);
            // Update colors in our pixel
            image[row][col].rgbtBlue = avg_color;
            image[row][col].rgbtGreen = avg_color;
            image[row][col].rgbtRed = avg_color;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Allocate memory for a temp storage, 1 byte
    RGBTRIPLE tmp;
    // Iterating over all rows of our image
    for (int row = 0; row < height; row++)
    {
        // Odd width scenario
        if (width % 2 != 0)
        {
            // Get middle of our row, this is also how many steps we need
            int steps = floor(width / 2);
            for (int s = steps; s > 0; s--)
            {
                // Store right
                tmp = image[row][steps + s];
                // Update rightmost
                image[row][steps + s] = image[row][steps - s];
                // Update leftmost
                image[row][steps - s] = tmp;
            }
        }
        // Even width scenario
        else
        {
            int steps = width / 2;
            for (int s = 0; s < steps; s++)
            {
                // Store rightmost data to temp variable
                tmp = image[row][0 + s];
                // Update righmost data
                image[row][0 + s] = image[row][width - 1 - s];
                // Update leftmost data
                image[row][width - 1 - s] = tmp;
            }
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Because of the nature of this operation, we need a copy of image that we can reference when editing pixels
    RGBTRIPLE img_copy[height][width];
    // Populate copy with data
    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col++)
        {
            img_copy[row][col] = image[row][col];
        }
    }
    // Filter application logic
    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col++)
        {
            // Decide on the divisor for computing average
            int divisor = 0; // Default value
            // Compute our color sums
            double red_sum = 0, green_sum = 0, blue_sum = 0; // tried BYTE but it results in overflow acc to a search on Google
            // Then we need to handle what other pixels to account for as well
            // Instead of writing a very bulk series of if statements, we can try a loop
            // We can iterate from -1 to 1 and see what pixels surrounding the one we need are valid
            for (int i = -1; i < 2; i++)
            {
                for (int j = -1; j < 2; j++)
                {
                    // We can't allow the marker to go outside col & row limits
                    if (((row + i >= 0) && (row + i < height)) && ((col + j >= 0) && (col + j < width)))
                    {
                        red_sum += img_copy[row + i][col + j].rgbtRed;
                        green_sum += img_copy[row + i][col + j].rgbtGreen;
                        blue_sum += img_copy[row + i][col + j].rgbtBlue;
                        // Increment divisor
                        divisor++;
                    }
                }
            }
            // At this point we have divisor and our sums so we can update our pixel
            image[row][col].rgbtRed = round(red_sum / (float) divisor);
            image[row][col].rgbtGreen = round(green_sum / (float) divisor * 1.0);
            image[row][col].rgbtBlue = round(blue_sum / (float) divisor * 1.0);
        }
    }
    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // Similar to blur, we firstly create a copy of the original image
    RGBTRIPLE img_dump[height][width];
    // This is again needed not to base calculation on the pixels we edit
    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col ++)
        {
            img_dump[row][col] = image[row][col];
        }
    }
    // Define our matrices for calculations
    int g_x[3][3] =
    {
        {-1, 0, 1},
        {-2, 0, 2},
        {-1, 0, 1}
    };
    int g_y[3][3] =
    {
        {-1, -2, -1},
        {0, 0, 0},
        {1, 2, 1}
    };
    // Iterate over image's pixels
    for (int row = 0; row < height; row++)
    {
        for (int col = 0; col < width; col++)
        {
            // One more loop to handle all three colors that we have
            for (int c_count = 0; c_count < 3; c_count++)
            {
                // Declare variable to store our color sums
                int gx = 0;
                int gy = 0;
                // Reuse our approach with iterating over 9 surrounding pixels
                for (int r = -1; r < 2; r++)
                {
                    for (int c = -1; c < 2; c++)
                    {
                        // Check we are not bordering
                        if (((row + r >= 0) && (row + r < height)) && ((col + c >= 0) && (col + c < width)))
                        {
                            if (c_count == 0)
                            {
                                gx += (g_x[r + 1][c + 1] * img_dump[row + r][col + c].rgbtRed);
                                gy += (g_y[r + 1][c + 1] * img_dump[row + r][col + c].rgbtRed);
                            }
                            else if (c_count == 1)
                            {
                                gx += (g_x[r + 1][c + 1] * img_dump[row + r][col + c].rgbtGreen);
                                gy += (g_y[r + 1][c + 1] * img_dump[row + r][col + c].rgbtGreen);
                            }
                            else
                            {
                                gx += (g_x[r + 1][c + 1] * img_dump[row + r][col + c].rgbtBlue);
                                gy += (g_y[r + 1][c + 1] * img_dump[row + r][col + c].rgbtBlue);
                            }

                        }
                        // Add 0 to our sum if yes
                        else
                        {
                            gx += 0;
                            gy += 0;
                        }
                    }
                }
                // At this point we are ready to compute our values for the pixel
                int color_val = round(sqrt(pow(gx, 2) + pow(gy, 2)));
                // Cap because RGB is [0, 255] using reassignment
                if (color_val > 255)
                {
                    color_val = 255;
                }
                // Assing our value to the needed color of the pixel
                if (c_count == 0)
                {
                    image[row][col].rgbtRed = color_val;
                }
                else if (c_count == 1)
                {
                    image[row][col].rgbtGreen = color_val;
                }
                else
                {
                    image[row][col].rgbtBlue = color_val;
                }
            }
        }
    }
    return;
}
