import random
import math

class player():
    
    def __init__(self, name, team):
        self.name = name
        self.team = team
        self.bowling = random.uniform(0.4,1.0)
        self.batting = random.uniform(0.4,1.0)
        self.fielding = random.uniform(0.4,1.0)
        self.running = random.uniform(0.4,1.0)
        self.overs_left = 4
        self.field_angularpos = 0
        self.field_radialdist = 0
        self.field_xpos = 0
        self.field_ypos = 0
        self.field_role = ''
        self.batting_status = ''
        self.batting_position = ''
        self.bat_angularpos = 0
        self.bat_radialdist = 0
        self.bat_xpos = 0
        self.bat_ypos = 0
        
        self.rev_bowling = 0
        self.rev_batting = 0
        self.rev_fielding = 0
        self.rev_running = 0
        
    def __str__(self):
        diction = {'name':self.name,
                'team':self.team,
                'BBFR skills rating':[self.bowling, self.batting, self.fielding, self.running],
                'overs left':self.overs_left,
                'field_xpos':self.field_xpos,
                'field_ypos':self.field_ypos,
                'field_role':self.field_role
                }
        for i in diction.keys():
            if i != 'team':
                print(i,':',diction[i])
        return 'team: {}'.format(diction['team'])
    
    def original_val(self):
        '''Takes record of the original value at the point of creation of a player'''
        self.rev_bowling = self.bowling
        self.rev_batting = self.batting
        self.rev_fielding = self.fielding
        self.rev_running = self.running
        
    def bowling_fatigue(self):
        '''Physical fatigue after each play'''
        self.bowling -= 0.0210 
        
    def fielding_fatigue(self):
        '''Physical fatigue after each play'''
        self.fielding -= 0.0167
        
    def batting_fatigue(self):
        '''Physical fatigue after each play'''
        self.batting -= 0.0185
        
    def running_fatigue(self):
        '''Physical fatigue after each play'''
        self.running -= 0.0200
        
    def over_deplete(self):
        '''Number of overs left for each player after each over'''
        self.overs_left -= 1
        
    def calc_coordinate(self):
        '''Calculated the x and y position using the angular position
        and radial distance'''
        tetha = self.field_angularpos
        hyp = self.field_radialdist
        self.field_xpos = math.sin(math.radians(tetha))*hyp
        self.field_ypos = math.cos(math.radians(tetha))*hyp
        
    def value_refresh(self):
        '''Reverts all the values and skill of a player to its original value
        at the end of a match, so the same set of players can be maintained 
        through the tournament.'''
        self.bowling = self.rev_bowling
        self.batting = self.rev_batting
        self.fielding = self.rev_fielding
        self.running = self.rev_running
        self.overs_left = 4
        self.field_angularpos = 0
        self.field_radialdist = 0
        self.field_xpos = 0
        self.field_ypos = 0
        self.field_role = ''
        self.batting_status = ''
        self.batting_position = ''
        self.bat_angularpos = 0
        self.bat_radialdist = 0
        self.bat_xpos = 0
        self.bat_ypos = 0