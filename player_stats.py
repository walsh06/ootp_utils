import re

def get_stat(player, headers, stat):
    return float(player[headers.index(stat)])

def append_avg(player, headers):
    ab = float(player[headers.index('ab')])
    if ab > 0:
        avg = float(player[headers.index('h')])/float(player[headers.index('ab')])
    else:
        avg = 0
    player.insert(-1, avg)

def append_era(player, headers):
    ip = get_stat(player, headers, "ip")

    if ip > 0:
        era = (get_stat(player, headers, "er") / ip) * 9
    else:
        era = 0
    player.insert(-1, era)


def append_whip(player, headers):
    ip = get_stat(player, headers, "ip")

    if ip > 0:
        whip = (get_stat(player, headers, "ha")+  get_stat(player, headers, "w"))/ ip
    else:
        whip = 0
    player.insert(-1, whip)


def get_teams_ids(teams_string_list, id_first=True):
    teams_dict = {}
    for team in teams_string_list:
        team_string = team.split(',')[0]
        items = re.match("//(.*?) => (.*?) \(Baseball Federation => 100\)", team_string).groups()
        if items:
            if id_first:
                teams_dict[items[0]] = items[1]
            else:
                teams_dict[items[1]] = items[0]

    return teams_dict

def combine_batting_stats():
    with open("Player Tracking - player_batting_stats.csv") as f:
        contents = f.readlines()

    teams = get_teams_ids(contents[1:33])

    headers = contents[67][2:].split(',')

    combined_stats = {}

    for player_line in contents[69:]:
        player = player_line.split(',')
        if player[headers.index('league_level_id')] != '2':
            player_id = player[0]
            if player_id in combined_stats:
                for x in range(5,27):
                    combined_stats[player_id][x + 2] = float(combined_stats[player_id][x + 2]) + float(player[x])
            else:
                if player[4] in teams:
                    player.insert(5, teams[player[4]])
                player.insert(1, "{} {}".format(player[2], player[1]))
                combined_stats[player_id] = player

    with open("combined_batting_stats.csv", "w") as f:
        headers.insert(1, "Name")
        headers.insert(6, "Team Name")
        headers.insert(-1, "avg")

        f.write(",".join(headers))
        for player in combined_stats:
            append_avg(combined_stats[player], headers)
            f.write(",".join([str(x) for x in combined_stats[player]]))

def combine_pitching_stats():
    with open("Player Tracking - player_pitching_stats.csv") as f:
        contents = f.readlines()

    teams = get_teams_ids(contents[1:33], id_first=False)
    headers = contents[67][2:].split(',')

    combined_stats = {}

    for player_line in contents[69:]:
        player = player_line.split(',')
        if player[headers.index('league_level_id')] != '2':
            player_id = player[0]
            if player_id in combined_stats:
                for x in range(5,headers.index('league_level_id')):
                    combined_stats[player_id][x + 2] = float(combined_stats[player_id][x + 2]) + float(player[x])
            else:
                if player[4] in teams:
                    player.insert(5, teams[player[4]])
                player.insert(1, "{} {}".format(player[2], player[1]))
                combined_stats[player_id] = player

    headers.insert(1, "Name")
    headers.insert(6, "Team Name")
    headers.insert(-1, "ERA")
    headers.insert(-1, "WHIP")

    for player in combined_stats:
        append_era(combined_stats[player], headers)
        append_whip(combined_stats[player], headers)

    with open("combined_pitching_stats.csv", "w") as f:
        f.write(",".join(headers))
        for player in combined_stats:
            f.write(",".join([str(x) for x in combined_stats[player]]))

combine_pitching_stats()
