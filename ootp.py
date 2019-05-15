import time

class Match():

    def __init__(self, home_team, away_team, day, time):
        self.home_team = home_team
        self.away_team = away_team
        self.day = day
        self.time = time

    def __lt__(self, other):
            return self.day < other.day

    @property
    def match_string(self):
        return '<GAME day="{day}" time="{time}" away="{away}" home="{home}" />'.format(day=self.day,
                                                                                       time=self.time,
                                                                                       home=self.home_team,
                                                                                       away=self.away_team)



class MatchSeries():

    def __init__(self, home_team, away_team, start_day, times, games):
        self.matches = []
        if len(times) == 1:
            times = [times[0] for x in range(0, games)]
        for x in range(0, games):
            self.matches.append(home_team, away_team, start_day+x, times[x])


class Schedule():

    @classmethod
    def from_matrix(cls, teams, matches, matrix, series_length, series_break, game_times, tag=None):
        schedule = cls(teams, matches, tag)
        day = 1
        for week in matrix:
            for y in range(0, series_length):
                for x in range(0, len(week), 2):
                    schedule.add_match(week[x], week[x+1], day, game_times[y])
                day += 1
            day += series_break
        return schedule

    @classmethod
    def from_week_dict(cls, teams, matches, week_dict, series_length, game_times, tag=None):
        schedule = cls(teams, matches, tag)
        for week in week_dict:
            matches = week_dict[week]
            for day in range(0, series_length):
                for x in range(0, len(matches), 2):
                    game_day = ((week - 1) * 7) + day + 1
                    schedule.add_match(matches[x], matches[x+1], game_day, game_times[day])
        return schedule

    def __init__(self, teams, matches, tag=None):
        self.match_list = []
        self.teams = teams
        self.matches = matches
        self.tag = tag
        self.max_day = 1

    def add_match(self, home_team, away_team, day, time):
        self.match_list.append(Match(home_team, away_team, day, time))
        if day > self.max_day:
            self.max_day = day

    def write_schedule(self, start_month, start_date, start_day, structure):
        match_strings = [match.match_string for match in sorted(self.match_list)]
        tag = "_{}".format(self.tag) if self.tag else ""
        schedule_path = "{}_teams_{}_matches{}_{:.0f}.lsdl".format(self.teams, self.matches, tag, time.time())
        header_template = """<?xml version="1.0" encoding="ISO-8859-1"?>

<SCHEDULE type="ILN_BGY_G{games}_{structure}_C_" inter_league="0" balanced_games="1" games_per_team="{games}" start_month="{start_month}" start_day="{start_date}" start_day_of_week="{start_day}">

<GAMES>
"""
        
        with open(schedule_path, "w") as f:
            f.write(header_template.format(games=self.matches,
                                           structure=structure,
                                           start_month=start_month,
                                           start_date=start_date,
                                           start_day=start_day))
            f.write("\n".join(match_strings))
            f.write("\n</GAMES>")
            f.write("\n</SCHEDULE>")


def extend_matrix(matrix, extensions):
    matches = []
    for week in matrix:
        matches.append(extend_matches(week, extensions))
    return matches


def extend_week_dict(week_dict, extensions):
    matches = {}
    for week in week_dict:
        matches[week] = extend_matches(week_dict[week], extensions)
    return matches


def extend_matches(matches, extensions):
    extended_matches = [x for x in matches]
    for x in range(0, len(matches), 2):
        for extension in extensions:
            extended_matches.extend([matches[x] + extension, matches[x+1] + extension])
    return extended_matches


def swap_home_away(matches):
    swapped_matches = []
    for x in range(0, len(matches), 2):
        swapped_matches.append(matches[x+1])
        swapped_matches.append(matches[x])
    return swapped_matches

def combine_week_dicts(week_dicts, weeks):
    combined_dict = {}
    for week in range(1, weeks + 1):
        for week_dict in week_dicts:
            if week in week_dict:
                if week not in combined_dict:
                    combined_dict[week] = []
                combined_dict[week].extend(week_dict[week])
    return combined_dict


def print_home_count(weeks, teams):
    test = dict((i,{"home": 0, "total": 0}) for i in range(1, teams + 1))
    for week in weeks:
        for x in range(0, len(weeks[week]), 2):
            test[weeks[week][x + 1]]['home'] += 1
            test[weeks[week][x + 1]]['total'] += 1
            test[weeks[week][x]]['total'] += 1

    for team in test:
        print("TEAM: {}, Home matches: {} ({}%)".format(team,
                                                       test[team]['home'],
                                                       (float(test[team]['home'])/float(test[team]['total']) * 100)))
