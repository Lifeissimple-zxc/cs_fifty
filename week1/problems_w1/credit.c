#include <cs50.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>

//Include helper funcs
int get_card_len(long card_num);
int add_two_digits(int check_sum, int num);
string validate_card(int check_sum, int card_len, int card_digits[]);

int main(void)
{
    // long card_num = 4003600000000014;
    long card_num = get_long("Enter card number: ");
    int card_len = get_card_len(card_num);
    //Create an array of card digits
    int card_digits[card_len]; //needs to be static due to how C works with arrays
    //Parse Long to array
    long card_num_duplicate = card_num;
    for (int i = card_len - 1; i >= 0 ; i--)
    {
        card_digits[i] = card_num_duplicate % 10;
        card_num_duplicate = card_num_duplicate / 10;
    }
    //Traverse the array from last to first number
    //declare check_sum
    int check_sum = 0; //check if it remained zero later on
    int even_check = card_len % 2;
    //for item in array:
    for (int i = card_len - 1; i >= 0; i--)
    {
        int num = card_digits[i];
        //if len is even:
        if (even_check == 0)
        {
            if (i % 2 == 0) check_sum = add_two_digits(check_sum, num);
            else check_sum += num;
        }
        else
        {
            if (i % 2 == 0) check_sum += num;
            else check_sum = add_two_digits(check_sum, num);
        }

    }
    string check_result = validate_card(check_sum, card_len, card_digits);
    printf("%s\n", check_result);
}
//Helper Funcs Start Here
int get_card_len(long card_num)
{
    //Code to get card_num length
    long len_num = card_num;
    int len_counter = 0;
    do
    {
        len_num = len_num / 10;
        len_counter++;
    } while (len_num != 0);
    return len_counter;
}

int add_two_digits(int check_sum, int num)
{
    if (num * 2 < 10) check_sum += num * 2;
    else check_sum += ((num * 2 % 10) + 1);
    return check_sum;
}

string validate_card(int check_sum, int card_len, int card_digits[])
{
    string result = "INVALID";
    if (check_sum == 0) result = "INVALID";
    if (check_sum % 10 != 0) result = "INVALID";
    else
    {
        //Check for visa
        if (card_digits[0] == 4 && (card_len == 14 || card_len == 16 || card_len == 13)) result = "VISA";
        int first_two = card_digits[0] * 10 + card_digits[1];
        if (card_len == 15 && (first_two == 34 || first_two == 37)) result = "AMEX";
        if (card_len == 16 && (first_two >= 51 && first_two <= 55)) result = "MASTERCARD";
    }
    return result;
}