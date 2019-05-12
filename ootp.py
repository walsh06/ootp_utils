import time

class Match():

    def __init__(self, home_team, away_team, day, time):
        self.home_team = home_team
        self.away_team = away_team
        self.day = day
        self.time = time

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
        match_strings = [match.match_string for match in self.match_list]
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
    matches = [x[:] for x in matrix]
    for week in matches:
        for x in range(0, len(week), 2):
            for extension in extensions:
                week.extend([week[x] + extension, week[x+1] + extension])
    return matches
