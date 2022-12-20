#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

//https://cs50.harvard.edu/x/2022/psets/2/substitution/

int get_key_len(string key);
int is_alpha_key(string key, int key_len);
string key_to_lower(string key, int key_len);
int has_no_duplicates(string key, int key_len);
void get_mapping(string key, int mapper[]);

int main(int argc, string argv[])
{
    // Check user arguments
    if (argc != 2){
        printf("Usage: ./substitution key\n");
        return 1;
    }
    // At this point we know that we have received the key so saving to a variable is ok
    string key_raw = argv[1];
    // char key_arrayed[] = "ke";
    // We also need key array len to perform checks
    int key_len = get_key_len(key_raw);
    // Check key len
    if (key_len != 26)
    {
        printf("Got wrong key len: %i! Expected 26.\n", key_len);
        return 1;
    }
    // Check that we only have alpha chars
    if (is_alpha_key(key_raw, key_len) == 0)
    {
        printf("Key has non-alphabetic characters, cannot procced :(\n");
        return 1;
    }
    // Convert key to lower
    string key_lower = key_to_lower(key_raw, key_len);
    // Check for duplicates
    if (has_no_duplicates(key_lower, key_len) == 0)
    {
        printf("Key has duplicate characters, cannot procced :(\n");
        return 1;
    }
    // printf("All good with the key!\n");
    // return 0;
    int mapper[26];
    get_mapping(key_lower, mapper);
    return 0;

}


// Helper functions start here
int get_key_len(string key)
{
    // String is an array of so we can iterate over it
    // All strings in c end with "\0" so we can do a while loop to count len
    // Tried with sizeof, did not work :(
    // We are not handling edge cases because we will separately validate our argv contens
    int len = 0;
    do
    {
        len++;
    } while(key[len] != '\0');
    return len;
}
// Not a validation per se, but needed
string key_to_lower(string key, int key_len)
{
    for (int i = 0; i < key_len; i++)
    {
        char curr_char = key[i];
        // Check if lower
        if (!islower(curr_char))
        {
            key[i] = tolower(curr_char);
        }
    }
    return key;
}
// Validation functions are below
int is_alpha_key(string key, int key_len)
{
    // Checks if key is alpha by iterating over its chars and checking each of them
    for (int i = 0; i < key_len; i++)
    {
        // Check for each charater, return first 0 we encounter
        if (!isalpha(key[i])) //return 0; if we want it one-lined
        {
            return 0;
        }
    }
    // Finally return 1 if we do not return during the loop
    return 1;
}

int has_no_duplicates(string key, int key_len)
{
    // Brute force: we compare each element of array with all other elements, stop at the first matching pair
    // We ignore the last element to avoid extra operations in the inner loop
    for (int i = 0; i < key_len - 1; i++)
    {
        for (int j = i + 1; j < key_len; j++)
        {
            if (key[i] == key[j])
            {
                // We return from the func as soon as we get to the first duplicate
                return 0;
            }
        }
    }
    // In case we checked all elements and located 0 duplicates, we return 1
    return 1;
}
// Mapping functions are below
// C does not encourage returning arrays so we do not do it and just modify a pre-created one
void get_mapping(string key, int mapper[])
{
    // Here we expect key to be lower so we default string is lower too
    string default_string = "abcdefghijklmnopqrstuvwxyz";
    //Map differences with Eng Alphabet
    for (int i = 0; i < 26; i++)
    {
        // Store within the provided mapper array
        mapper[i] = key[i] - default_string[i];
    }
}

string perform_cipher(string plain_text, int mapper[])
{
    int i = 0;
    do
    {
        char curr_char = plain_text[i];
        
        i++;
    } while (plain_text[i] != '\0');
}

