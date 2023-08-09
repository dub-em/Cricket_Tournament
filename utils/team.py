import random
from .player import player

class team():
    
    def __init__(self, name):
        self.name = name
        self.players = {}
        self.role = ''
        self.bat_active_players = []
        self.bat_next_down = []
        self.bat_ret_hurt = []
        self.overs_exhausted = []
        self.overs_notexhausted = []
        self.final_matchscore = 0
        
    def __str__(self):
        print('Team name: {}',format(self.name)) 
        for i in self.players.keys():
            print('Player Details: {}'.format(self.players[i]))
            print('\n')
        return "Description"
    
    def player_descr(self):
        '''Populates the team with players (each player is defined separately)'''
        for i in range(1,12):
            name = "player"+str(i)
            self.players[str(i)] = player(name, self.name)
            self.players[str(i)].original_val()
            
    #def team_postion(self, position):
    #    self.position = position
    
    def overs_status(self):
        '''Demarcate the players by the remaining overs per player.'''
        self.overs_exhausted = []
        self.overs_notexhausted = []
        for i in self.players.keys():
            if self.players[i].overs_left == 0:
                self.overs_exhausted.append(self.players[i])
            else:
                self.overs_notexhausted.append(self.players[i])
        
    def team_fielddistribution(self, pitch, play_type, prev_bowler=None):
        '''Deciding the players positions during a power play or a normal play.
        1 bowler, 6 players in the inner field (including the wicket keeper)
        and 4 players in the outer field for power play.
        1 bowler, 4 players in the inner field (inclduing the wicket keeper)
        and 6 players in the outer field for normal play.'''
        
        pitch = pitch
        play_type = play_type
        prev_bowler = prev_bowler
        
        if play_type == 'power_play':
            inner_players = 6
            outer_players = 4
            inner_maxplayers = 5
        elif play_type == 'normal_play':
            inner_players = 4
            outer_players = 6
            inner_maxplayers = 3
        else:
            raise Exception("Pease enter one of the two plays ('power_play','normal_play')")
            
        incr_innerangle = 360/inner_players
        innerangle = 0       
        incr_outerangle = 360/outer_players
        outerangle = 0
        outerdist = ((pitch.outer_radius - pitch.inner_radius)/2)+pitch.inner_radius
        
        #Selects the bowler from the list of player who haven't exhausted their overs.
        #Also omits the player that just previously bowled to avoid one player playing 2 overs consecutively.
        temp_list_1 = [player for player in self.overs_notexhausted]
        temp_list_2 = [self.players[i] for i in self.players.keys()]
            
        if prev_bowler in temp_list_1:
            index_1 = temp_list_1.index(prev_bowler)
            pop_mssg = temp_list_1.pop(index_1)
            
        weight = [player.bowling for player in temp_list_1]
        
        bowler = random.choices(temp_list_1, weights=weight, k=1)
        bowler = bowler[0]
        
        index_2 = temp_list_2.index(bowler)
        pop_mssg_2 = temp_list_2.pop(index_2)
        
        bowler.field_angularpos = 180
        bowler.field_radialdist = (2/3)*pitch.inner_radius
        bowler.calc_coordinate()
        bowler.field_role = "bowler"
        
        for i in range(len(temp_list_2)):
            if (int(i) <= inner_maxplayers) & (inner_players != 0):
                if int(i) == inner_maxplayers:
                    innerangle += incr_innerangle
                    temp_list_2[i].field_angularpos = innerangle
                    temp_list_2[i].field_radialdist = (2/3)*pitch.inner_radius
                    temp_list_2[i].calc_coordinate()
                    temp_list_2[i].field_role = "wicketkeeper"
                else:
                    innerangle += incr_innerangle
                    temp_list_2[i].field_angularpos = innerangle
                    temp_list_2[i].field_radialdist = (2/3)*pitch.inner_radius
                    temp_list_2[i].calc_coordinate()
                    temp_list_2[i].field_role = "fielder"
                inner_players -= 1
            if (int(i) > inner_maxplayers) & (int(i) <= 10) & (outer_players != 0):
                outerangle += incr_outerangle
                temp_list_2[i].field_angularpos = outerangle
                temp_list_2[i].field_radialdist = outerdist
                temp_list_2[i].calc_coordinate()
                temp_list_2[i].field_role = "fielder"
                outer_players -= 1
                            
    def bat_fillbench(self):
        '''Populates the bench list with the players from which the batter
        and the runner will be selected while other will be left in the next down'''
        for i in self.players.keys():
            self.bat_next_down.append(self.players[i])
            
    def bat_playerselect(self, state, pitch):
        '''Select the batter and the runner from the bench list depending on whether
        it is the beginning of the game or the a player is retired hurt.'''
        state = state
        pitch = pitch
        if state == 'game_start':
            for i in range(2):
                weight = []
                for player in self.bat_next_down:
                    weight.append(player.batting)
                if i == 0:
                    batter = random.choices(self.bat_next_down, weights=weight, k=1)
                    batter = batter[0]
                    index = self.bat_next_down.index(batter)
                    pop_mssg = self.bat_next_down.pop(index)
                    batter.batting_status = 'active'
                    batter.batting_position = 'batter'
                    batter.bat_angularpos = pitch.northwicket_angularpos
                    batter.bat_radialdist = pitch.northwicket_radialdist
                    batter.bat_xpos = pitch.northwicket_xpos
                    batter.bat_ypos = pitch.northwicket_ypos
                    self.bat_active_players.append(batter)
                else:
                    runner = random.choices(self.bat_next_down, weights=weight, k=1)
                    runner = runner[0]
                    index = self.bat_next_down.index(runner)
                    pop_mssg = self.bat_next_down.pop(index)
                    runner.batting_status = 'active'
                    runner.batting_position = 'runner'
                    runner.bat_angularpos = pitch.southwicket_angularpos
                    runner.bat_radialdist = pitch.southwicket_radialdist
                    runner.bat_xpos = pitch.southwicket_xpos
                    runner.bat_ypos = pitch.southwicket_ypos
                    self.bat_active_players.append(runner)
        else:
            weight = []
            category = self.bat_active_players[0].batting_position
            for player in self.bat_next_down:
                weight.append(player.batting)
            sub = random.choices(self.bat_next_down, weights=weight, k=1)
            sub = sub[0]
            index = self.bat_next_down.index(sub)
            pop_mssg = self.bat_next_down.pop(index)
            if category == 'batter':
                sub.batting_status = 'active'
                sub.batting_position = 'runner'
                sub.bat_angularpos = pitch.southwicket_angularpos
                sub.bat_radialdist = pitch.southwicket_radialdist
                sub.bat_xpos = pitch.southwicket_xpos
                sub.bat_ypos = pitch.southwicket_ypos
                self.bat_active_players.append(sub)
            else:
                sub.batting_status = 'active'
                sub.batting_position = 'batter'
                sub.bat_angularpos = pitch.northwicket_angularpos
                sub.bat_radialdist = pitch.northwicket_radialdist
                sub.bat_xpos = pitch.northwicket_xpos
                sub.bat_ypos = pitch.northwicket_ypos
                self.bat_active_players.append(sub)
                
    def bat_positionflip(self, pitch):
        '''In the case the batter and runner choose to run and achieve an odd
        number of runs which causes their positions to flip, this function carries out that
        positio flip'''
        position = [player.batting_position for player in self.bat_active_players]
        self.bat_active_players[0].batting_position = position[1]
        self.bat_active_players[1].batting_position = position[0]
        for player in self.bat_active_players:
            if player.batting_position == 'batter':
                player.bat_angularpos = pitch.northwicket_angularpos
                player.bat_radialdist = pitch.northwicket_radialdist
                player.bat_xpos = pitch.northwicket_xpos
                player.bat_ypos = pitch.northwicket_ypos
            else:
                player.bat_angularpos = pitch.southwicket_angularpos
                player.bat_radialdist = pitch.southwicket_radialdist
                player.bat_xpos = pitch.southwicket_xpos
                player.bat_ypos = pitch.southwicket_ypos
        
                
    def bat_retiredhurt(self, player):
        '''When a player from the batting team is retired hurt, this function
        removes them from the active list and places them in the retired hurt
        list'''
        player = player
        index = self.bat_active_players.index(player)
        self.bat_active_players.pop(index)
        player.batting_status = "inactive"
        self.bat_ret_hurt.append(player)
        
    def value_refresh(self):
        '''Reverts all the values and lists of a team in preparation for another 
        match'''
        self.role = ''
        self.bat_active_players = []
        self.bat_next_down = []
        self.bat_ret_hurt = []
        self.overs_exhausted = []
        self.overs_notexhausted = []
        self.final_matchscore = 0