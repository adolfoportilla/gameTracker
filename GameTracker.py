#ADOLFO PORTILLA
import fileinput
import sys


#Class where all the functions are
class gameTracker(object):
    
    def __init__(self):
        
        '''
        This is how the data base will look

        self.gameTracker = {'Games': {'Names': ['Name', 'ID'], 'Victories': ['victoryID', 'gameID', 'name', 'Points'] }, 
        'Players': {'Names': ['Name', 'ID'], 'Plays': ['playID', 'gameID', 'IGN'], 'Friends': ['Player1', 'Player2'], 'Victories': ['playerID','gameID', 'victoryID']}}
        '''

        '''The GamesPlayed Dictionary is a helper function just containing the player id and the games played by him'''
        self.gameTracker = {'Games': {'Names': {} , 'Victories': {}, 'NumberOfVictories':{}, 'IndividualVictories':{} }, 
        'Players': {'Names': {}, 'Plays': {},'GamesPlayed':{}, 'Friends': {}, 'Victories': {} }}
        


    '''HELPER FUNCTIONS'''

    #Helper function to return the total victories a player has in a specific game
    def TotalVictories(self, playerID, gameID):

        totalVictories = self.gameTracker['Games']['NumberOfVictories'][gameID]
        victoriesP1 = self.gameTracker['Players']['Victories'][playerID]
        victories = 0

        for NoV in self.gameTracker['Players']['Victories'][playerID]:
            if NoV[0] == gameID:
                victories += 1

        victories = str(victories) + "/" + str(totalVictories)
        return victories

    #Returns the total points scored in a specific game by a player
    def TotalPointsGame(self, playerID, gameID):
        victories = self.gameTracker['Players']['Victories'][playerID]
        points = 0

        for gameid, victoryID in victories:
            if gameID == gameid:
                points += int(self.gameTracker['Games']['Victories'][victoryID][2])

        return points

    #Returns the total points of a player in all games
    def TotalPoints(self, playerID):

        points = 0

        if playerID not in self.gameTracker['Players']['Victories']:
            return 0
    
        for xxx, victoryID in self.gameTracker['Players']['Victories'][playerID]:
            points += int(self.gameTracker['Games']['Victories'][victoryID][2])

        return points

    #reads the input and decides what to do next
    def parseLines(self):
        
        for line in sys.stdin:    
            self.num = line.split()

            if len(self.num) < 2 :
                pass

            elif self.num[0] == "AddPlayer":

                if len(self.num) == 4:
                    self.AddPlayer(self.num[1],self.num[2],self.num[3])
                elif len(self.num) == 3:
                    self.AddPlayer(self.num[1],self.num[2],"NoLastname")
                else:
                    "Something is wrong"

            elif self.num[0]  == "AddGame":
                self.gameName=''

                for x in self.num[2:]:
                    self.gameName += x + ' '
                
                self.AddGame(self.num[1],self.gameName)

            elif self.num[0] == "AddVictory":

                self.victoryName = ''
                '''If and else statements to separate the one word name victory and the other ones'''
                if len(self.num) == 5:
                    self.victoryName = self.num[3][1:-1]
                else:
                    for x in self.num[3:]:
                        if x[0] == '"':                    
                            self.victoryName += x[1:] + ' '
                        elif x[-1] == '"':
                            self.victoryName += x[:-1]
                            break
                        else:
                            self.victoryName += x + ' '                    

                self.AddVictory(self.num[1], self.num[2], self.victoryName, self.num[-1])

            elif self.num[0] == "Plays":

                self.Plays(self.num[1],self.num[2],self.num[3][1:-1])

            elif self.num[0] == "AddFriends":

                self.AddFriends(self.num[1],self.num[2])

            elif self.num[0] == "WinVictory":

                self.WinVictory(self.num[1],self.num[2],self.num[3])

            elif self.num[0] == "SummarizePlayer":
                self.SummarizePlayer(self.num[1])
            
            elif self.num[0] == "FriendsWhoPlay":
                self.FriendsWhoPlay(self.num[1],self.num[2])

            elif self.num[0] == "ComparePlayers":
                self.ComparePlayers(self.num[1],self.num[2],self.num[3])

            elif self.num[0] == "SummarizeGame":
                self.SummarizeGame(self.num[1])

            elif self.num[0] == "SummarizeVictory":
                self.SummarizeVictory(self.num[1],self.num[2])

            elif self.num[0] == "VictoryRanking":
                self.VictoryRanking()


            else:
                pass

    #prints the data structure (dictionary) to see how the data is organized
    def printDictionary(self):
        print self.gameTracker


    '''FUNCTIONS NEEDED'''
    #Each function is self explanatory    
    def AddPlayer(self, id, name,lastname):
        self.playersName = name + ' ' + lastname
        self.playersName = self.playersName.strip('\"')
        self.gameTracker['Players']['Names'][id] = self.playersName

    def AddGame(self,id,gameName):
        self.gameTracker['Games']['Names'][id] = gameName

    def AddVictory(self,gameID, victoryID, name, points):

        if victoryID in self.gameTracker['Games']['Victories']:
            self.gameTracker['Games']['Victories'][victoryID] += [gameID,name,points]
        else:
            self.gameTracker['Games']['Victories'][victoryID] = [gameID,name,points]
        #To add the number of victories of a specific game
        if gameID in self.gameTracker['Games']['NumberOfVictories']:
            self.gameTracker['Games']['NumberOfVictories'][gameID] += 1
        else:
            self.gameTracker['Games']['NumberOfVictories'][gameID] = 1

    def Plays(self,playerID, gameID, IGN):

        if playerID in self.gameTracker['Players']['Plays'] :
            self.gameTracker['Players']['Plays'][playerID] += [[gameID, IGN]]
        else:
            self.gameTracker['Players']['Plays'][playerID] = [[gameID, IGN]]

        #Helper dictionary to be easy to keep track of which games a player has played
        if playerID in self.gameTracker['Players']['GamesPlayed'] :
            self.gameTracker['Players']['GamesPlayed'][playerID] += [gameID]
        else:
            self.gameTracker['Players']['GamesPlayed'][playerID] = [gameID]

    def AddFriends(self,player1, player2):

        if player1 not in self.gameTracker['Players']['Friends']:
            self.gameTracker['Players']['Friends'][player1] = [player2]
        elif player1 in self.gameTracker['Players']['Friends']:
            self.gameTracker['Players']['Friends'][player1] += [player2]
        else:
            pass 
        if player2 not in self.gameTracker['Players']['Friends']:
            self.gameTracker['Players']['Friends'][player2] = [player1]
        elif player2 in self.gameTracker['Players']['Friends']:
            self.gameTracker['Players']['Friends'][player2] += [player1]
        else:
            pass

    def WinVictory(self,playerID, gameID, victoryID):

        if playerID in self.gameTracker['Players']['Victories']:
            self.gameTracker['Players']['Victories'][playerID] += [[gameID, victoryID]]
        else:
            self.gameTracker['Players']['Victories'][playerID] = [[gameID, victoryID]]

        if victoryID in self.gameTracker['Games']['IndividualVictories']:
            self.gameTracker['Games']['IndividualVictories'][victoryID] += 1
        else:
            self.gameTracker['Games']['IndividualVictories'][victoryID] = 1

    def FriendsWhoPlay(self, playerID, gameID):
        
        friendsPlayerID = self.gameTracker['Players']['Friends'][playerID]
        friendsWhoPlay = []

        for player in friendsPlayerID:
            if player in self.gameTracker['Players']['GamesPlayed']:
                gamesSinglePlayer = self.gameTracker['Players']['GamesPlayed'][player]
                if gameID in gamesSinglePlayer:
                    friendsWhoPlay += [player]

        
        friendsWhoPlayName = []

        '''To change from ID to Name'''
        for i in friendsWhoPlay:
            friendsWhoPlayName += [self.gameTracker['Players']['Names'][i]]
        
        print friendsWhoPlayName
    
    def ComparePlayers(self,player1ID, player2ID, gameID):
        
        player1 = self.gameTracker['Players']['Names'][player1ID]
        player2 = self.gameTracker['Players']['Names'][player2ID]
        victoriesP1 = self.gameTracker['Players']['Victories'][player1ID]
        victoriesP2 = self.gameTracker['Players']['Victories'][player2ID]
        victoryPointsP1 = 0
        victoryPointsP2 = 0 
        pointsP1 = 0
        pointsP2 = 0

        print
        print
        print "---------- Report Comparing ", player1, "and", player2 , "----------"
        print
        print "         ------------ Game ", self.gameTracker['Games']['Names'][gameID], "------------"
        print
        print

        for NoV in self.gameTracker['Players']['Victories'][player1ID]:
            if NoV[0] == gameID:
                victoryPointsP1 += 1
        for NoV in self.gameTracker['Players']['Victories'][player2ID]:
            if NoV[0] == gameID:
                victoryPointsP2 += 1

        
        for gameid, victoryID in victoriesP1:
            if gameID == gameid:
                pointsP1 += int(self.gameTracker['Games']['Victories'][victoryID][2])

        for gameid, victoryID in victoriesP2:
            if gameID == gameid:
                pointsP2 += int(self.gameTracker['Games']['Victories'][victoryID][2])

        print "Player", player1, "scored", pointsP1, "In a total of", self.TotalVictories(player1ID, gameID), "victories"
        print "Player", player2, "scored", pointsP2, "In a total of", self.TotalVictories(player2ID, gameID), "victories"

        print
        print
        print

    def SummarizePlayer(self,playerID):
        
        print "Player:", self.gameTracker['Players']['Names'][playerID] 
        print "Total Gamescore: ", self.TotalPoints(playerID)
        print
        print "Game", "\t\t\t", "Victories", "\t", "Gamescore", "\t\t", "IGN"
        print 10*"---------"
        
        counter = 1
        gameName = self.gameTracker['Games']['Names']
        games = []

        for game in self.gameTracker['Players']['GamesPlayed'][playerID]:
            games += [[self.TotalPointsGame(playerID, game),game]]
        
        for score,game in sorted(games,reverse=1):
            
            output = str(counter) + '.'
            output += gameName[game][1:-2][0: 24-len(output)]
            output += (24-len(output))*' ' + str(self.TotalVictories(playerID, game))
            output += (40-len(output))*' ' + str(score)
            output += (64-len(output))*' ' + str(self.gameTracker['Players']['Plays'][playerID][counter-1][1])

            counter += 1
            print output
            
        print
        print "Friends", "\t\t", "Gamescore" 
        print 5*"---------"
        
        counter = 1
        friends = []

        for friend in self.gameTracker['Players']['Friends'][playerID]:
            friends += [[self.TotalPoints(friend), self.gameTracker['Players']['Names'][friend]]]

        for score, name in  sorted(friends, reverse= 1):

            output = str(counter)+". "
            output += name[0: 24-len(output)] 
            output +=  (24-len(output))*" " + str(score)
            counter += 1
            print output
        print
        print

    def SummarizeGame(self,gameID):
        print self.gameTracker['Games']['Names'][gameID][1:-2], "Game Summary"
        print
        print "Victory ID","\t","Name", "\t\t\t","# of times accomplished"
        print 8*"---------"

        for victories in sorted(list(self.gameTracker['Games']['Victories'])):
            if victories not in self.gameTracker['Games']['IndividualVictories']:
                pass
            else:
                if self.gameTracker['Games']['Victories'][victories][0] == gameID:
                    output = str(victories)
                    output += "\t\t"
                    output += self.gameTracker['Games']['Victories'][victories][1]
                    output += (30-len(output))*" " + str(self.gameTracker['Games']['IndividualVictories'][victories])
                    print output

        print
        print "Players"
        print 2*"---------"

        for player in list(self.gameTracker['Players']['GamesPlayed']):
            if gameID in self.gameTracker['Players']['GamesPlayed'][player]:
                print self.gameTracker['Players']['Names'][player]

    def SummarizeVictory(self,gameID, victoryID):
        
        players = []
        playersVictory = []
        for player in self.gameTracker['Players']['GamesPlayed']:
            if gameID in self.gameTracker['Players']['GamesPlayed'][player]:
                players += [player]

        for player in self.gameTracker['Players']['Victories']:
            if player in players:
                for game, victoryid in  self.gameTracker['Players']['Victories'][player]:
                    if victoryid == victoryID:
                        playersVictory += [player]
        
        

        print "Summarize Victory of", victoryID,"---->" , self.gameTracker['Games']['Victories'][victoryID][1]
        print
        print "Players who have won the victory"
        print 4*"---------"
        for player in playersVictory:
            print self.gameTracker['Players']['Names'][player]
        print
        print "Percentage of players who play that game who have the Victory"
        print 7*"---------"
        output = str(len(playersVictory)*100 / float(len(players)))
        output += "%"
        print output

    def VictoryRanking(self):
        
        print "Victory Ranking"
        print
        print "Player", "\t\t\t", "Gamescore"
        print 5*"---------"
        
        players = []
        counter = 1

        for player in list(self.gameTracker['Players']['Names']):
            players += [[self.TotalPoints(player), player]]

        for score,name in sorted(players, reverse = 1):
            output = str(counter)+". "
            output += self.gameTracker['Players']['Names'][name][0: 24-len(output)]
            output +=  (24-len(output))*" " + str(score)
            counter += 1
            print output
        
        print
        print
    

    
def main():
    
    Game1 = gameTracker()
    Game1.parseLines()

    
    
main()