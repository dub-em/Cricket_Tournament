def find_pitcher(fielding_team):
    '''Current Pitcher is identitfied'''
    for i in fielding_team.players.keys():
        if fielding_team.players[i].field_role == "bowler":
            pitcher =  fielding_team.players[i]
            break
    return pitcher

def wicket_keeper(fielding_team):
    '''Current Wicketkeeper is identitfied'''
    for i in fielding_team.players.keys():
        if fielding_team.players[i].field_role == "wicketkeeper":
            wicketkeeper =  fielding_team.players[i]
            break
    return wicketkeeper

def find_batter(batting_team):
    '''Current Batter is identitfied'''
    for players in batting_team.bat_active_players:
        if players.batting_position == "batter":
            batter =  players
            break
    return batter