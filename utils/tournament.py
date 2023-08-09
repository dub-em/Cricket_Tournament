from .team import team

class tournament():
    
    def __init__(self, name, number_of_teams):
        self.name = name
        self.number_of_teams = number_of_teams
        self.start_teams = {}
        self.winning_teams = {}
        self.start_groups = {}
        self.updated_groups = {}
        
    def populate_teams(self):
        '''Fills all teams into a dictionary.'''
        for i in range(self.number_of_teams):
            name = 'Team'+str(i)
            self.start_teams[str(i)] = team(name)
            
    def team_grouping(self):
        '''Group all the teams so they can play against each other'''
        number_of_groups = self.number_of_teams/2
        for i in range(int(number_of_groups)):
            self.start_groups[str(i)] = []
            self.updated_groups[str(i)] = []
        for i in self.start_teams.keys():
            group = int(i)//2
            self.start_groups[str(group)].append(self.start_teams[i])
            self.updated_groups[str(group)].append(self.start_teams[i])
                
    def winninteam_update(self, team, group):
        '''After a team wins her match, this function adds it to the
        winning team list to be regrouped'''
        team = team
        group = group
        self.winning_teams[str(group)] = team
        
    def update_groups(self):
        '''Takes in the winning teams and regroups then for the 
        next stage of matches'''
        self.updated_groups = {}
        number_of_groups = len(self.winning_teams.keys())/2
        if number_of_groups >= 1: #This determines if the number of remaining teams is enough for a group
            for i in range(int(number_of_groups)):
                self.updated_groups[str(i)] = []
            for i in self.winning_teams.keys():
                group = int(i)//2
                self.updated_groups[str(group)].append(self.winning_teams[i])
            return "Tournament Ongoing" #If team are enough then tournament continues
        else:
            return "Tournament Completed" #Else, tournament is concluded.
          