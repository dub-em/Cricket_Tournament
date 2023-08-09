import random

class umpire():
    
    def __init__(self):
        pass
    
    def coinflip(self, teams):
        '''Selects which team start as batting team and which start as bowling.'''
        teams = teams
        team_roles = ['batting','fielding']
        first_rolepick = random.choices(team_roles, k=1)
        first_rolepick = first_rolepick[0]
        teams[0].role = first_rolepick
        index = team_roles.index(first_rolepick)
        pop_mssg = team_roles.pop(index)
        teams[1].role = team_roles[0]
        
    def teamrole_flip(self, teams):
        '''After the first half (120 overs or batting team total retired hurt),
        the umpire changes the roles of the teams.'''
        teams = teams
        oldstatus_1 = teams[0].role
        oldstatus_2 = teams[1].role
        teams[0].role = oldstatus_2
        teams[1].role = oldstatus_1
      