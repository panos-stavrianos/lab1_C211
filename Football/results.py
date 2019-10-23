import operator
import random

from tabulate import tabulate

teams = {}

with open('test.txt') as f:
    def add_to_matches(team, goals_scored, goals_taken):
        if team not in teams.keys():
            teams[team] = {"points": 0, "goals_scored": 0, "goals_taken": 0}

        if goals_scored > goals_taken:
            teams[team]["points"] += 3
        elif goals_scored < goals_taken:
            teams[team]["points"] += 0
        else:
            teams[team]["points"] += 1
        teams[team]["goals_scored"] += goals_scored
        teams[team]["goals_taken"] += goals_taken


    for line in f.readlines():
        a1 = line.replace("\n", "").split(":")
        two_teams = a1[0].split("-")
        two_scores = a1[1].split("-")
        team1 = two_teams[0]
        team2 = two_teams[1]
        score1 = int(two_scores[0])
        score2 = int(two_scores[1])
        add_to_matches(team1, score1, score2)
        add_to_matches(team2, score2, score1)

ranking = []
for i, team in enumerate(teams.keys()):
    ranking.append(
        [team,
         teams[team]['points'],
         "{}-{}".format(teams[team]['goals_scored'], teams[team]['goals_taken'])
         ])
with open("output.txt", "w") as f:
    f.writelines(
        tabulate(tabular_data=ranking, disable_numparse=True,
                 tablefmt="plain"))
random.shuffle(ranking)
with open("output.txt", "w") as f:
    f.writelines(map(lambda record: "{}\t{}\t{}\n".format(*record), ranking))

ranking = sorted(ranking, key=operator.itemgetter(0), reverse=False)  # sort with team name
ranking = sorted(ranking, key=operator.itemgetter(1), reverse=True)  # sort with points
for i, r in enumerate(ranking):
    ranking[i] = ["{}.".format(i)] + r

with open("output_table.txt", "w") as f:
    f.writelines(
        tabulate(tabular_data=ranking, headers=['team', 'points', 'goals'], disable_numparse=True,
                 tablefmt="fancy_grid"))
