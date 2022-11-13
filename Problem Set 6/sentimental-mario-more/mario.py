# TODO
from cs50 import get_int

while True:
    answer = get_int("Height: ")
    if answer > 0 and answer < 9:
        break

j = 1

for i in range(answer):
    # print the spaces before the first block
    print(" "*(answer-j),  end="")
    # print the left side of the pyramid
    print("#"*j,  end="")
    # print the space between the bricks
    print("  ", end="")
    # print the right side of the pyramid
    print("#"*j,  end="")
    # get new line
    print()
    # add 1 to j to 1 more brick
    j += 1
