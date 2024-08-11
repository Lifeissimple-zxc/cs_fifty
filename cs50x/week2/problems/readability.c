#include <cs50.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include <math.h>
//https://cs50.harvard.edu/x/2022/psets/2/readability/
int count_letters(string text, int textLen);
int countWords(string text, int letterCount, int textLen);
int countSentences(string text, int textLen);
int getIndex(int letterCount, int wordCount, int sentenceCount);
void assignGrade(int index);

int main(void)
{
    //Ask user for input
    string textToGrade = get_string("Text: ");
    int textLen = strlen(textToGrade); //get len of text to see how many iterations to do
    int letterCount = count_letters(textToGrade, textLen);
    int wordCount = countWords(textToGrade, letterCount, textLen);
    int sentenceCount = countSentences(textToGrade, textLen);
    int index = getIndex(letterCount, wordCount, sentenceCount);
    assignGrade(index);
}

//Helper funcs are written here
int count_letters(string text, int textLen)
{
    //Since string is an array of characters, we iterate through it and count alpa chars

    int letterCount = 0; //init counter var
    for (int i = 0; i < textLen; i++)
    {
        char curChar = text[i];
        if (isalpha(tolower(curChar)))
        {
            letterCount++;
        }
    }
    return letterCount;
}

int countWords(string text, int letterCount, int textLen)
{
    int wordCount = 0;
    if (letterCount == 0)
    {
        printf("Sentence has zero letters thus cannot have words! Check input!\n");
    }
    else
    {
        for (int i = 0; i < textLen; i++)
        {
            if (text[i] == ' ' && text[i + 1] != ' ' && i != 0)
            {
                wordCount++;
            }
        }
    }
    return wordCount + 1; //adding 1 because there will always be count of spaces + 1 words in a sentence
}

int countSentences(string text, int textLen)
{
    int sentenceCount = 0;
    for (int i = 0; i < textLen; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            if (isalpha(text[i - 1]) && (text[i + 1] == ' ' || text[i + 1] == '\0'))
            {
                sentenceCount++;
            }
        }
    }
    return sentenceCount;
}

int getIndex(int letterCount, int wordCount, int sentenceCount)
{
    double index;
    float L = (float) letterCount / (float) wordCount * 100; //letters per 100 words
    float S = (float) sentenceCount / (float) wordCount * 100; //sentences per 100 words

    index = round(0.0588 * L - 0.296 * S - 15.8);
    int indexInt = (int) index;
    return indexInt;
}

void assignGrade(int index)
{
    string result;
    if (index > 16)
    {
        printf("Grade 16+\n");
    }
    else if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade %i\n", index);
    }
}