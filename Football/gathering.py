import sqlite3

from tabulate import tabulate

conn = sqlite3.connect('data.db')

cursor = conn.execute("SELECT id,Country,League from Competitions")
competitions = {}
for competition_id, country, league in cursor:
    if country in competitions:
        competitions[country].append([competition_id, league])
    else:
        competitions[country] = [[competition_id, league]]

print(tabulate(tabular_data=map(lambda a: [a], competitions.keys()), showindex=True, headers=['ID', 'County'],
               tablefmt="fancy_grid"))

while True:
    country = input("Select a county: ")
    if str.isdigit(country):
        country = int(country)
        if 0 <= int(country) < len(competitions):
            country = list(competitions.keys())[country]
            break
print(tabulate(tabular_data=map(lambda a: [a[1]], competitions[country]), showindex=True, headers=['ID', 'County'],
               tablefmt="fancy_grid"))

while True:
    league = input("Select a League: ")
    if str.isdigit(league):
        league = int(league)
        if 0 <= int(league) < len(competitions[country]):
            competition_id = competitions[country][league][0]
            league = competitions[country][league][1]
            print("Fetching data for {0}, {1}".format(country, league))
            break

filename = input("Filename: ")

cursor = conn.execute("SELECT team1,team2,score1,score2 from Matches where competition=?", (competition_id,))
with open(filename, 'w') as f:
    # Ομάδα1-Ομάδα2:Σκορ1-Σκορ2
    f.writelines(map(lambda record: "{}-{}:{}-{}\n".format(*record), cursor))

conn.close()
