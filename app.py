import random
import math, time
import streamlit as st
from PIL import Image
from streamlit_extras.add_vertical_space import add_vertical_space
from utils.player import player 
from utils.pitch_dim import pitch_dim
from utils.team import team
from utils.tournament import tournament
from utils.umpire import umpire
from utils import extra
 
#Imports image for the sidebar
tournament_header = Image.open('./images/Tournament_Header.jpg')
tournament_header = tournament_header.resize((300, 150))

#Sidebar contents
with st.sidebar: 
    st.sidebar.image(tournament_header)
    st.title('Cricket Tournament Simulator')
    st.markdown('''
    ## About
    This app simply simulates a Cricket tournament between a specified number of teams.
    - [Streamlit](https://streamlit.io/)
 
    The current tournament comprises of 8 teams, who play amongst each other.
    The winners play amongst each other until one team emerges the champion.
    ''')
    add_vertical_space(5)
    
def main():
    '''Function which simulates the entire tournament.'''
    #Setting the tournament

    st.header("Cricket World Tournament")

    #Imports pictures which will be used later to add context/sentiment to the match updates.
    tournament_winner = Image.open('./images/Tournament_Winners.jpg')
    tournament_winner = tournament_winner.resize((400, 200))
    match_winners_1 = Image.open('./images/Match_Winners_1.jpg')
    match_winners_1 = match_winners_1.resize((400, 200))
    match_winners_2 = Image.open('./images/Match_Winners_2.jpg')
    match_winners_2 = match_winners_2.resize((400, 200))
    match_winners_3 = Image.open('./images/Match_Winners_3.jpg')
    match_winners_3 = match_winners_3.resize((400, 200))
    match_winners_4 = Image.open('./images/Match_Winners_4.jpg')
    match_winners_4 = match_winners_4.resize((400, 200))
    list_of_images = [match_winners_1,match_winners_2,match_winners_3,match_winners_4]

    #Define a new tournament
    new_tournament = tournament('World Tournament', 8)

    #Create new pitch
    new_pitch = pitch_dim()

    #Assign an umpire
    referee = umpire()
    
    #Using specified number of teams, create new teams for the tournament
    new_tournament.populate_teams()
    
    #The players are created for each team
    for n in new_tournament.start_teams.keys():
        new_tournament.start_teams[n].player_descr()
        
    #Group team using grouping function
    new_tournament.team_grouping()

    #Initiates the state of the Tournament
    tournament_status = "Tournament Ongoing"
    level = 1

    #While loop keeps running until there are no more groups matches to be had.
    while tournament_status == "Tournament Ongoing":
        for group_number in new_tournament.updated_groups.keys():
            current_group = new_tournament.updated_groups[group_number]
            #A group's match

            #Referee decide which teams occupy which role to start the game.
            referee.coinflip(current_group)
            for teams in current_group:
                if teams.role == 'batting':
                    batting_team = teams
                else:
                    fielding_team = teams

            #Match begins
            #The two halves of the match is iterated through
            for i in range(2):
                #Match Preambles and Preparations

                orig_playtype = 'power_play' #Fielding teams starts with a power play formation
                playtype_overcount = 0 #Determing the number of overs before the field team play formation is changed.
                player_overcount = 0 #Determing the number of overs before a pitcher is changed
                batting_team_score = 0 #Batting team's score is initiated

                #Batting team fill their bench with all players for a start
                batting_team.bat_fillbench()

                #Batting team decides which player
                batting_team.bat_playerselect('game_start', new_pitch)

                #Records the overs balance of each player in the fielding team
                fielding_team.overs_status()

                #Distributes the player in the fielding team according to the type of play.
                fielding_team.team_fielddistribution(new_pitch, orig_playtype)

                #Current Pitcher is identitfied
                pitcher = extra.find_pitcher(fielding_team)

                #Wicket Keeper is extracted
                wicketkeeper =  extra.wicket_keeper(fielding_team)

                #Current Batter is identitfied
                batter = extra.find_batter(batting_team)

                for j in range(120):
                    #One half of a match contains 20 overs, which amounts to 120 balls at 6 balls per over.

                    #Ball is thrown
                    ball_thrown = random.uniform((pitcher.bowling-0.1),1.0)
                    pitcher.bowling_fatigue()

                    #Probability of hitting the ball is decided
                    batter_hits_prob = random.uniform((batter.batting+0.1),1.0)
                    batter.batting_fatigue()

                    #A hit or no hit is confirmed 
                    if batter_hits_prob >= ball_thrown:
                        #If the ball is hit what happens

                        #Position of every fielder is determined for later use
                        field_players = [fielding_team.players[i] for i in fielding_team.players.keys()]
                        balltoplayer_dist = []
                        ball_angle = random.uniform(0.0, 360.0) #ball angle is randomly generated

                        #ball distance across the pitch is a function of the batter and pitchers skills
                        ball_dist_perc = ((ball_thrown+batter_hits_prob)/2)+random.uniform(0.0,0.3)

                        if ball_dist_perc >= 1.0:
                            #Ball goes out of boudnary without bounce
                            points = 6
                            batting_team_score += points

                        elif (ball_dist_perc >= 0.9) & (ball_dist_perc < 1.0):
                            #Ball goes out of boundary with bounce/roll
                            points = 4
                            batting_team_score += points

                        elif (ball_dist_perc >= 0.5) & (ball_dist_perc < 0.9):
                            #Ball is hit to a certain part of the field
                            ball_raddist = ball_dist_perc * new_pitch.outer_radius
                            ball_xpos = math.sin(math.radians(ball_angle))*ball_raddist
                            ball_ypos = math.cos(math.radians(ball_angle))*ball_raddist

                            #Closest player to the ball landing position is calculated
                            balltoplayer_dist = [math.sqrt((ball_xpos - players.field_xpos)**2 + (ball_ypos - players.field_ypos)**2) 
                                                 for players in field_players]
                            min_dist = min(balltoplayer_dist)
                            index = balltoplayer_dist.index(min_dist)

                            #The closest player to the ball is the deciding player
                            deciding_player = field_players[index]

                            #Probability of player catching ball is calculated using the deciding player
                            catch_prob = random.uniform(deciding_player.fielding+0.15,1.0)

                            if catch_prob >= batter_hits_prob:
                                #Deciding player catches the ball, then...
                                #Probability of catch out is calculated
                                deciding_player.fielding_fatigue() #Fatigue function which reduces players skill per activity on the field

                                catchout_prob = random.uniform(deciding_player.fielding, 1.0)

                                if catchout_prob >= batter_hits_prob:
                                    #Player catches ball without bounce

                                    #Batting player has been caught out and will be substituted by a next down
                                    for players in batting_team.bat_active_players:
                                        if players.batting_position == "batter":
                                            batting_team.bat_retiredhurt(players)

                                    #Points updated
                                    points = 0
                                    batting_team_score += points

                                    #If the list of next down players is empty then the current half is concluded.
                                    if len(batting_team.bat_next_down) == 0:
                                        if (i+1) == 1:
                                            commentator = 'First half of Match {}, Group Level {} is concluded!'.format(group_number, str(level))
                                            st.write(f'{commentator}')
                                        else:
                                            commentator = 'Second half of Match {}, Group Level {} is concluded!'.format(group_number, str(level))
                                            st.write(f'{commentator}')
                                        time.sleep(1)
                                        break

                                    #If the next down list is still populated, caught out player is substituted
                                    batting_team.bat_playerselect('game_ongoing', new_pitch)

                                else:
                                    #If there is no catch out...
                                    #fielder (deciding player) throws the ball back to the wickets
                                    balltowicket_dist = []

                                    #Distance ball needs to travel to both wickets are calculated
                                    ballto_northwicket = math.sqrt((ball_xpos - new_pitch.northwicket_xpos)**2 + (ball_ypos - new_pitch.northwicket_ypos)**2)
                                    balltowicket_dist.append(ballto_northwicket)
                                    ballto_southwicket = math.sqrt((ball_xpos - new_pitch.southwicket_xpos)**2 + (ball_ypos - new_pitch.southwicket_ypos)**2)
                                    balltowicket_dist.append(ballto_southwicket)

                                    #Closest wicket is calculated
                                    targetwicket_dist = min(balltowicket_dist)

                                    #Distance to the closest wicket is used to compute number of runs achieved by the batter and runner
                                    numberofruns_achieved = targetwicket_dist//new_pitch.pitch_length #distance of ball to wicket divided by pitch distance

                                    #Both batter and runner experience running fatigue due to running activity
                                    for players in batting_team.bat_active_players:
                                        players.running_fatigue()

                                    #Distance away from crease is calculated to decided on whether it is a runout or not when ball reaches the wicket.
                                    dist_fromcrease = math.modf(targetwicket_dist/new_pitch.pitch_length)[0]

                                    if dist_fromcrease <= 0.30:
                                        #Batting players' distance away from crease is insignificant, so no runout.
                                        points = numberofruns_achieved
                                        batting_team_score += points
                                    else:
                                        #Batting players are significantly away from crease so  there is a runout.
                                        if (numberofruns_achieved%2) != 0:
                                            #Number of runs are odd, hence the batter and runner have a role change.
                                            batting_team.bat_positionflip(new_pitch)

                                        #The player closest to the wicket being target is calculated.
                                        balltobatteam_dist = [math.sqrt((ball_xpos - players.bat_xpos)**2 + (ball_ypos - players.bat_xpos)**2) 
                                                              for players in batting_team.bat_active_players]
                                        targetplayer_dist = min(balltobatteam_dist)
                                        index = balltobatteam_dist.index(targetplayer_dist)

                                        #The player whose wicket is targeted is affected by the runout
                                        players = batting_team.bat_active_players[index]
                                        batting_team.bat_retiredhurt(players) #Player is then removed from pitch
                                        points = numberofruns_achieved
                                        batting_team_score += points #Batting team scores are updated

                                        #If the list of next down players is empty then the current half is concluded.
                                        if len(batting_team.bat_next_down) == 0:
                                            if (i+1) == 1:
                                                commentator = 'First half of Match {}, Group Level {} is concluded!'.format(group_number, str(level))
                                                st.write(f'{commentator}')
                                            else:
                                                commentator = 'Second half of Match {}, Group Level {} is concluded!'.format(group_number, str(level))
                                                st.write(f'{commentator}')
                                            time.sleep(1)
                                            break
                                        batting_team.bat_playerselect('game_ongoing', new_pitch)
                            else:
                                #If deciding player doesn't catch the ball at the given speed, then the ball rolls out of boundary
                                points = 4
                                batting_team_score += points #Batting teams score is updated.
                        else:
                            #If ball force is low, then batter and runner decide not to run which means no run out, however...
                            #there can still be a catch-out which is calculated for.
                            ball_raddist = ball_dist_perc * new_pitch.outer_radius
                            ball_xpos = math.sin(math.radians(ball_angle))*ball_raddist
                            ball_ypos = math.cos(math.radians(ball_angle))*ball_raddist

                            #Closest player to ball landing position is calculated
                            balltoplayer_dist = [math.sqrt((ball_xpos - players.field_xpos)**2 + (ball_ypos - players.field_ypos)**2) 
                                                 for players in field_players]
                            min_dist = min(balltoplayer_dist)
                            index = balltoplayer_dist.index(min_dist)

                            #catch out probability is calculated based on closest player (deciding player) to the ball
                            deciding_player = field_players[index]
                            deciding_player.fielding_fatigue()

                            catchout_prob = random.uniform(deciding_player.fielding, 1.0)

                            if catchout_prob >= batter_hits_prob:
                                #The is a catch out, and current batter is removed
                                for players in batting_team.bat_active_players:
                                        if players.batting_position == "batter":
                                            batting_team.bat_retiredhurt(players)

                                #Batting team points are updated
                                points = 0
                                batting_team_score += points

                                #If the list of next down players is empty then the current half is concluded.
                                if len(batting_team.bat_next_down) == 0:
                                    if (i+1) == 1:
                                        commentator = 'First half of Match {}, Group Level {} is concluded!'.format(group_number, str(level))
                                        st.write(f'{commentator}')
                                    else:
                                        commentator = 'Second half of Match {}, Group Level {} is concluded!'.format(group_number, str(level))
                                        st.write(f'{commentator}')
                                    time.sleep(1)
                                    break
                                
                                #If the next down list is still populated then the removed player is substituted.
                                batting_team.bat_playerselect('game_ongoing', new_pitch)
                            else:
                                #If no catch out then dot ball.
                                points = 0
                                batting_team_score += points #Batting team score is updated.   
                    else:
                        #If the ball isn't hit, what happens

                        #Wicket Keeper attempts to catch the ball
                        ball_caught = random.uniform((wicketkeeper.fielding+0.2),1.0)
                        if ball_caught >= ball_thrown:
                            #If wicket keeper catches the ball without contact with batter, then dot ball
                            wicketkeeper.fielding_fatigue()
                            points = 0
                            batting_team_score += points #Batting team points are updated accordingly
                        else:
                            #If wicket keeper missed the ball as well, then batter and runner can decide to run
                            #runout process above is repeated
                            field_players = [fielding_team.players[i] for i in fielding_team.players.keys()]
                            balltoplayer_dist = []
                            ball_angle = 0.0
                            ball_dist_perc = (ball_thrown/2)+random.uniform(0.0,0.5) #ball speed/distance across the field is calculated
                            if (ball_dist_perc >= 0.9) & (ball_dist_perc <= 1.0):
                                #Ball goes out of boundary
                                points = 4
                                batting_team_score += points
                            elif (ball_dist_perc >= 0.5) & (ball_dist_perc < 0.9):
                                #Ball rolls to a certain part of the field
                                ball_raddist = ball_dist_perc * new_pitch.outer_radius
                                ball_xpos = math.sin(math.radians(ball_angle))*ball_raddist
                                ball_ypos = math.cos(math.radians(ball_angle))*ball_raddist

                                #Closest player to the ball landing position is calculated
                                balltoplayer_dist = [math.sqrt((ball_xpos - players.field_xpos)**2 + (ball_ypos - players.field_ypos)**2) 
                                                     for players in field_players]
                                min_dist = min(balltoplayer_dist)
                                index = balltoplayer_dist.index(min_dist)

                                deciding_player = field_players[index] #Closes player to the ball
                                #Probability of player catching ball is calculated using the closest player (deciding player)
                                catch_prob = random.uniform(deciding_player.fielding+0.15,1.0)

                                if catch_prob >= ball_thrown:
                                    #fielder catches and throws the ball back to the wickets
                                    balltowicket_dist = []

                                    #Distance ball needs to travel to both wickets are calculated
                                    ballto_northwicket = math.sqrt((ball_xpos - new_pitch.northwicket_xpos)**2 + (ball_ypos - new_pitch.northwicket_ypos)**2)
                                    balltowicket_dist.append(ballto_northwicket)
                                    ballto_southwicket = math.sqrt((ball_xpos - new_pitch.southwicket_xpos)**2 + (ball_ypos - new_pitch.southwicket_ypos)**2)
                                    balltowicket_dist.append(ballto_southwicket)

                                    #Closest wicket is calculated
                                    targetwicket_dist = min(balltowicket_dist)

                                    #Distance to the closest wicket is used to compute number of runs achieved by the batter and runner
                                    numberofruns_achieved = targetwicket_dist//new_pitch.pitch_length

                                    #Deciding player (fielder) and the runners both experience fatigue from field activity
                                    deciding_player.fielding_fatigue()
                                    for players in batting_team.bat_active_players:
                                        players.running_fatigue()

                                    #Distance away from crease is calculated to decided on whether it is a runout or not.
                                    dist_fromcrease = math.modf(targetwicket_dist/new_pitch.pitch_length)[0]

                                    if dist_fromcrease <= 0.30:
                                        #Batting players' distance away from crease is insignificant, so no runout.
                                        runout = 'false'
                                        points = numberofruns_achieved
                                        batting_team_score += points
                                    else:
                                        #Batting players are significantly away from crease so  there is a runout.
                                        if (numberofruns_achieved%2) != 0:
                                            #Number of runs are odd, hence the batter and runner have a role change.
                                            batting_team.bat_positionflip(new_pitch)

                                        balltobatteam_dist = [math.sqrt((ball_xpos - players.bat_xpos)**2 + (ball_ypos - players.bat_xpos)**2) 
                                                              for players in batting_team.bat_active_players]
                                        targetplayer_dist = min(balltobatteam_dist)
                                        index = balltobatteam_dist.index(targetplayer_dist)

                                        #The player whose wicket is targeted is affected by the runout
                                        players = batting_team.bat_active_players[index]
                                        batting_team.bat_retiredhurt(players) #Player is removed from the field to eb substituted
                                        points = numberofruns_achieved
                                        batting_team_score += points

                                        #If the list of next down players is empty then the current half is concluded.
                                        if len(batting_team.bat_next_down) == 0:
                                            if (i+1) == 1:
                                                commentator = 'First half of Match {}, Group Level {} is concluded!'.format(group_number, str(level))
                                                st.write(f'{commentator}')
                                            else:
                                                commentator = 'Second half of Match {}, Group Level {} is concluded!'.format(group_number, str(level))
                                                st.write(f'{commentator}')
                                            time.sleep(1)
                                            break
                                        
                                        #If there are more player on the next down list, then a substitution is made for the removed player
                                        batting_team.bat_playerselect('game_ongoing', new_pitch)
                                else:
                                    #If player doesn't catch the ball at the current speed then the ball rolls out of boundary
                                    ball_caught = 'false'
                                    points = 4
                                    batting_team_score += points
                            else:
                                #If ball force is low, then batter and runner decide not to run and the ball is a dot ball
                                points = 0
                                batting_team_score += points #Batting team points are updated accordingly

                    #This determine the current player formation of the fielding team and if a redistribution is needed
                    playtype_overcount += 1
                    if playtype_overcount <= 36: #6 overs at the beginning of the half
                        playtype = 'power_play'
                    elif (playtype_overcount > 36) & (playtype_overcount <=96): #10 overs in between
                        playtype = 'normal_play'
                    else: #The remaining 4 overs at the end of the half
                        playtype = 'power_play'

                    if orig_playtype != playtype: #If playtype changes the fielding team redistribution is carried out.
                        fielding_team.team_fielddistribution(new_pitch, playtype)
                        orig_playtype = playtype

                        #Current Pitcher is identitfied after redistriution
                        pitcher = extra.find_pitcher(fielding_team)

                        #Wicket Keeper is extracted
                        wicketkeeper =  extra.wicket_keeper(fielding_team)

                    #This determines if the bowler will be changed after one over 1 is exhausted, and subsequently causes a team redistribution
                    player_overcount += 1
                    if player_overcount == 6: #One over is exhausted and the bowler has to be changed
                        pitcher.over_deplete()
                        fielding_team.overs_status() #Selects players only from player with total remaining overs not exhausted
                        fielding_team.team_fielddistribution(new_pitch, playtype, pitcher)
                        player_overcount = 0

                        #Current Pitcher is identitfied after redistriution
                        pitcher = extra.find_pitcher(fielding_team)

                        #Wicket Keeper is identified after redistribution as well
                        wicketkeeper =  extra.wicket_keeper(fielding_team)

                #Batting teams final score is updated after the end of a half
                batting_team.final_matchscore = batting_team_score

                #At the end of first half of 120balls or next down list exhaustion, the team roles are flipped by the umpire
                referee.teamrole_flip(current_group)
                for teams in current_group:
                    if teams.role == 'batting':
                        batting_team = teams
                    else:
                        fielding_team = teams

            #Obtains the winning team from the final match scores
            scores = [] 
            team_names = []
            for teams in current_group:
                scores.append(teams.final_matchscore)
                team_names.append(teams.name)
                max_score = max(scores)
                index = scores.index(max_score)

            #Comments on the winner of the match and the score of both teams.
            commentator = 'Final Result for Match {} of Group Level {}!'.format(group_number, str(level))
            st.write(f'{commentator}')
            commentator = 'With both teams {}, having a final score of {},'.format(team_names, scores)
            st.write(f'{commentator}')
            commentator = '{} wins the match with a final score of {}.'.format(team_names[index], scores[index])
            st.write(f'{commentator}')
            current_image = random.choice(list_of_images)
            st.image(current_image, caption=commentator)
            commentator = '\n'
            st.write(f'{commentator}')
            time.sleep(2)

            #Refreshes the values of the teams and the players in preparation for the next match in the next level
            for teams in current_group:
                teams.value_refresh()
                for i in teams.players.keys():
                    teams.players[i].value_refresh()

            #Adds the winning teams to the winning teams list, which will be used to form the next group matches
            winningteam = current_group[index]
            new_tournament.winninteam_update(winningteam, group_number)

        #Forms the next group matches using only the winning teams
        tournament_status = new_tournament.update_groups()
        new_tournament.winning_teams = {}

        #Update the current group level
        level += 1

    #Comments on the winner of the tournament.
    commentator = 'Final Result for the Tournament!'
    st.write(f'{commentator}')
    commentator = '{} wins the tournament with an outstanding performance!.'.format(winningteam.name)
    st.write(f'{commentator}')
    st.image(tournament_winner, caption=commentator)

 
if __name__ == '__main__':
    main()