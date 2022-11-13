# TODO
from cs50 import get_int
from cs50 import get_string
import re

non_multi = 0
multi = 0

credit_card = get_int("Number: ")

# to check the
check = credit_card

length = 0

# get the length of the card
for i in range(len(str(credit_card))):
    length += 1

# chcek if the lenght of the credit card is valid
if (length != 13 and length != 15 and length != 16):
    print("INVALID")

# while loop to look at each number
while True:
    # if the credit card number is 0 break out of the loop
    if credit_card == 0:
        break
    # add the first and then every other number to non mutltiply int
    non_multi += int(credit_card % 10)

    # divide the credit card by 10 to look at the next number
    credit_card = int(credit_card/10)

    # add the second and then every other number to times 2 int
    times2 = int((credit_card % 10) * 2)

    # divide the credit card by 10 to look at the next number
    credit_card = int(credit_card/10)

    # get the individual number of the numbers that after they have been multiplied by 2
    tmp = int(times2 % 10)
    tmp1 = int(times2 / 10)
    multi = int(multi) + tmp + tmp1

# if mutli and non_multi added up with remainder 10 = 0 print which card the credit card number belongs to
if (multi + non_multi) % 10 == 0:
    if int(str(check)[:1]) == 4:
        print("VISA")
    elif int(str(check)[:1]) == 5 and (int(str(check)[1:2]) >= 0 and int(str(check)[1:2]) <= 5):
        print("MASTERCARD")
    elif int(str(check)[:1]) == 3 and (int(str(check)[1:2]) == 4 or int(str(check)[1:2]) == 7):
        print("AMEX")
    else:
        print("INVALID")
else:
    print("INVALID")