'''
Leaderboard for minesweeper game
'''
class Leaderboard:
    '''
    creates a new instance of object with empty leaderboard

    @param self(Leaderboard): this object
    '''
    def __init__(self):
        self.leaderboard = {} #name --> LeaderBoardEntry

    '''
    adds a json with game data to existing leaderboard entry or creates new entry

    @param self(Leaderboard): this object
    @param json(dict): json with game data to add
    '''
    def add(self, json):
        name = json.get("name")
        entry = self.leaderboard.get(name)

        if entry != None:
            entry.add_json(json)
        else:
            entry = LeaderboardEntry(name)
            entry.add_json(json)
            self.leaderboard[name] = entry

    '''
    return an ordered array of jsons for each player, best to worst rankings

    @param self(Leaderboard): this object

    @return (list): list of jsons ordered from highest to lowest ranking attribute
    '''
    def to_array(self):
        jsons = [x.to_json() for x in self.leaderboard.values()]

        ranks = sorted([x.ranking() for x in self.leaderboard.values()], reverse=True)

        rtn = []

        for rank in ranks:
            for json in jsons:
                if json.get("ranking") == rank:
                    rtn.append(json)
                    jsons.remove(json)
        
        return rtn

'''
A single player's data (i.e. collection of game data) on minesweeper
'''
class LeaderboardEntry:
    '''
    creates a new instance of object with empty list of game data

    @param self(LeaderboardEntry): this object
    @param name(string): unique identifier for this player
    '''
    def __init__(self, name):
        self.name = name
        self.jsons = [] #array of jsons where name = self.name

    '''
    adds a new game data json to list of games under this player

    @param self(LeaderboardEntry): this object
    @param json(dict): new game data json
    '''
    def add_json(self, json):
        if json.get("name") == self.name:
            self.jsons.append(json)
    
    '''
    returns the average time (rounded) on all games played for this player

    @param self(LeaderboardEntry): this object

    @return (float): average time rounded to 2 decimal places
    '''
    def avg_time(self):
        if len(self.jsons) == 0:
            return 0
        
        sum = 0
        total = 0
        for i in self.jsons:
            sum += i.get("time")
            total += 1

        return round(sum / total, 2)

    '''
    returns the average score (rounded) on all games played for this player

    @param self(LeaderboardEntry): this object

    @return (float): average score rounded to 2 decimal places
    '''
    def avg_score(self):
        if len(self.jsons) == 0:
            return 0
        
        sum = 0
        total = 0
        for i in self.jsons:
            sum += i.get("score")
            total += 1

        return round(sum / total, 2)
    
    '''
    returns the amount of wins on all games played for this player

    @param self(LeaderboardEntry): this object

    @return (int): number of wins
    '''
    def wins(self):
        total = 0
        for i in self.jsons:
            if i.get("win"):
                total += 1
            
        return total

    '''
    returns the amount of losses on all games played for this player

    @param self(LeaderboardEntry): this object

    @return (int): number of losses
    '''
    def losses(self):
        total = 0
        for i in self.jsons:
            if not(i.get("win")):
                total += 1

        return total
    
    '''
    returns the calculated ranking (rounded) for this player
    (wins) / (wins + losses) * average time * average score

    @param self(LeaderboardEntry): this object

    @return (float): calculated ranking rounded to 2 decimal places
    '''
    def ranking(self): # (wins) / (wins + loses) * average time * average score
        wins = self.wins()
        losses = self.losses()
        avg_time = self.avg_time()
        avg_score = self.avg_score()

        return round((wins) / (wins + losses) * avg_time * avg_score, 2)
    
    '''
    returns json representing this player with relevant statistics
    (in order) ranking, name, wins, losses, average time, average score 

    @param self(LeaderboardEntry): this object

    @return (dict): json of this player with relevant statistics (see above)
    '''
    def to_json(self):
        return {
            "ranking": self.ranking(),
            "name": self.name,
            "wins": self.wins(),
            "losses": self.losses(),
            "avg_time": self.avg_time(),
            "avg_score": self.avg_score()
        }

    