import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")

    # TODO: Read database file into a variable
    persons = []
    # read in the first CSV file
    with open(sys.argv[1], "r") as database:
        reader = csv.DictReader(database)
        # get the header of the file
        DB_header = reader.fieldnames
        # file the persons list with the people
        for row in reader:
            persons.append(row)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as DNA:
        DNA_data = DNA.read()

    # Find longest match of each STR in DNA sequence

    # intialize STR Name variable
    STR_name = []
    # look at each value in the DB_header
    for STR in (DB_header):
        # only want the STR sequences and append them to the
        if STR != "name":
            STR_name.append(STR)

    # make an empty dictionary with all the STR sequences and set thier value to 0
    STRS = dict.fromkeys(STR_name, 0)
    for x in STR_name:
        # set the STR sequences to the longest match
        STRS[x] = longest_match(DNA_data, x)

    # TODO: Check database for matching profiles

    # look at each person in the persons list
    for person in persons:
        # intialize sequence variable to see if person matches all STR sequences
        sequences = 0
        for str in STRS:
            # See if the str of the person matches the longest STR recoreded and add plus one to the sequences
            if int(person[str]) != STRS[str]:
                continue
            sequences += 1

        # if the sequences variables is the same lenght as the STR dicitonary, found match and print their name
        if (sequences == len(STRS)):
            print(person['name'])
            return

    # else return no match
    print("No Match")
    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
