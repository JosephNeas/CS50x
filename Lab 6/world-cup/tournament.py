# Simulate a sports tournament

import csv
import sys
import random

# Number of simluations to run
N = 1000


def main():

    # Ensure correct usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python tournament.py FILENAME")

    teams = []
    # TODO: Read teams into memory from file
    # Open the file
    with open(sys.argv[1]) as file:
        # Read in the file
        reader = csv.DictReader(file)
        # Look at each row in the rile
        for row in reader:
            # Put each team into a dictionary with its name and rating
            team_dic = {"team": row["team"], "rating": int(row["rating"])}
            # Append to the teams list
            teams.append(team_dic)
        # print(teams)

    counts = {}
    # TODO: Simulate N tournaments and keep track of win counts
    for i in range(N):
        # get the winner of the tournament
        winner = simulate_tournament(teams)
        # if the winner is not in the counts dictionary add the winner and set thier value to 1
        if winner not in counts:
            counts[winner] = 1
        # if they alreay were added, add 1 to thier value
        else:
            counts[winner] += 1

    # Print each team's chances of winning, according to simulation
    for team in sorted(counts, key=lambda team: counts[team], reverse=True):
        print(f"{team}: {counts[team] * 100 / N:.1f}% chance of winning")


def simulate_game(team1, team2):
    """Simulate a game. Return True if team1 wins, False otherwise."""
    rating1 = team1["rating"]
    rating2 = team2["rating"]
    probability = 1 / (1 + 10 ** ((rating2 - rating1) / 600))
    return random.random() < probability


def simulate_round(teams):
    """Simulate a round. Return a list of winning teams."""
    winners = []

    # Simulate games for all pairs of teams
    for i in range(0, len(teams), 2):
        if simulate_game(teams[i], teams[i + 1]):
            winners.append(teams[i])
        else:
            winners.append(teams[i + 1])

    return winners


def simulate_tournament(teams):
    """Simulate a tournament. Return name of winning team."""
    # TODO
    # Simulate games for all pairs of teams

    # Get the first round of teams to aquire the first round of winners
    winners = simulate_round(teams)

    # look at all matches from the new winners list
    for i in range(len(winners)):
        # if the len of the winners list is 1, know we have a winner
        if len(winners) == 1:
            return winners[0]["team"]
        # else keep simulating rounds with the new winners list 
        else:
            winners = simulate_round(winners)


if __name__ == "__main__":
    main()
