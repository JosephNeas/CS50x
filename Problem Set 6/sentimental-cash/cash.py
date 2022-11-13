# TODO
from cs50 import get_float

change = 0

while True:
    # get the change from the user
    answer = get_float("Change owed: ")
    if (answer > 0):
        break
    # if the users input is not a positive number ask them again
    else:
        print("Please enter a positive number")

# whuke koop to continue getting change
while True:
    # round the answer to 2 as there was memory problems when minusing .1 give garbage numbers
    answer = round(answer, 2)
    # add one to count each time answer is minused by a coin
    if answer >= .25:
        answer -= .25
        change += 1
    elif (answer < .25 and answer >= .10):
        answer -= .10
        change += 1
    elif (answer < .10 and answer >= .05):
        answer -= .05
        change += 1
    elif (answer < .05 and answer > 0):
        answer -= .01
        change += 1
    elif answer == 0:
        break

# return the total coins given back
print(change)

