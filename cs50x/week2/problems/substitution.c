#include <cs50.h>
#include <stdio.h>
#include <ctype.h>

//https://cs50.harvard.edu/x/2022/psets/2/substitution/

int get_key_len(string key);
int is_alpha_key(string key, int key_len);
void string_to_lower(string str, int str_len, char lower_container[]);
int has_no_duplicates(string key, int key_len);

int main(int argc, string argv[])
{
    // Check user arguments
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1;
    }
    // At this point we know that we have received the key so saving to a variable is ok
    string key_raw = argv[1];
    // We also need key array len to perform checks
    int key_len = get_key_len(key_raw);
    // Check key len
    if (key_len != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    // Check that we only have alpha chars
    if (is_alpha_key(key_raw, key_len) == 0)
    {
        printf("Key has non-alphabetic characters, cannot procced :(\n");
        return 1;
    }
    // Convert key to lower
    // First we create a container for lowered key
    char key_lower[key_len];
    string_to_lower(key_raw, key_len, key_lower);

    // Check for duplicates
    if (has_no_duplicates(key_lower, key_len) == 0)
    {
        printf("Key has duplicate characters, cannot procced :(\n");
        return 1;
    }
    // Get user input
    string user_str = get_string("plaintext: ");

    // Transform input to all lower by creating a lowered copy
    int user_input_len = get_key_len(user_str);
    char user_str_lower[user_input_len];
    string_to_lower(user_str, user_input_len, user_str_lower);

    // Creating a variable to store our ciphered text
    char cipher_text[user_input_len];

    for (int i = 0; i < user_input_len; i++)
    {
        // Get current character, a separate variable for lower key to preserve case
        char curr_char = user_str[i];
        // We don't change non-alpha characters
        cipher_text[i] = curr_char;
        // Handling of alpha chars
        if (isalpha(curr_char))
        {
            char curr_char_lower = user_str_lower[i];
            // Convert character to a position within default string abcdefghijklmnopqrstuvwxyz
            int char_pos = curr_char_lower - 97;
            // Get mapped character by indexing the key with the position of the character
            char mapped_char = key_lower[char_pos];
            // Check of user input case, we only check for upper case because we always get lower chars from key_lower
            if (isupper(curr_char))
            {
                // Rewrite our mapped char to upper
                mapped_char = toupper(mapped_char);
            }
            // Store to string
            cipher_text[i] = mapped_char;
        }
    }

    // Final output
    printf("ciphertext: ");
    for (int i = 0; i < user_input_len; i++)
    {
        printf("%c", cipher_text[i]);
    }
    printf("\n");

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
    }
    while (key[len] != '\0');

    return len;
}
// Not a validation per se, but needed
void string_to_lower(string str, int str_len, char lower_container[])
{
    // Expects an array-container for lower string to be saved within
    for (int i = 0; i < str_len; i++)
    {
        char curr_char = str[i];
        lower_container[i] = curr_char;
        // Check if lower & override
        if (isupper(curr_char))
        {
            lower_container[i] = tolower(curr_char);
        }
    }
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
