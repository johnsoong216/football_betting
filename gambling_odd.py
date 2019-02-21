"""
Algorithm Interface
"""

class Game:
    """
    Initialize a game
    """    
    def __init__(self) -> None:
        
        
        #Enter Needed Info
        self.hometeam = input("Enter the name of your home team: ")
        self.awayteam = input("Enter the name of your away team: ")
        self.home = float(input("Enter the odds(in decimal) of home team winning: "))
        self.draw = float(input("Enter the odds(in decimal) of a draw: "))
        self.away = float(input("Enter the odds(in decimal) of away team winning: "))
        
        total = (input("How much do you want to bet in total? " ))
        hchance = input("What is the likelihood of home team victory(In your opinion)? Use percentage within the range 0-1: ")
        dchance = input("What is the likelihood of a draw(In your opinion)? Use percentage within the range 0-1: ")
        achance = input("What is the likelihood of away team victory(In your opinion? Use percentage within the range 0-1: ")
        acceptance = input("How much can you afford to lose? " )

        self.player = [float(hchance), float(dchance), float(achance), float(total), float(acceptance)]        

        #Return_Rate
        self.return_rate = 1/(1/self.home + 1/self.draw + 1/self.away)
        
    
    def __str__(self) -> str:
        return None
    def hedge_bet(self) -> list:

        away = 1/(1 + self.away/self.home + self.away/self.draw - self.away)
        draw = self.away/self.draw * away
        home = self.away/self.home * away
        return [round(home + draw + away ,2), round(home, 2), round(draw, 2), round(away, 2)]
    
    def optimization(self) -> list:
        
        #Betting company odds
        bhome = 1/ (self.home/self.return_rate) 
        bdraw = 1/ (self.draw/self.return_rate) 
        baway = 1/ (self.away/self.return_rate) 
        
        #Judgement
        pwin = self.player[3] * (self.player[0] * self.home)
        pdraw = self.player[3] * (self.player[1] * self.draw)
        ploss = self.player[3] * (self.player[2] * self.away) 
        #Actual Bet
        xwin = self.player[3] * self.player[0]
        xdraw = self.player[3] * self.player[1]
        xloss = self.player[3] * self.player[2]
        
        #No need for modification
        if 1 - self.return_rate >= self.player[4]/self.player[3]:
            return [0.0, 0.0, 0.0]
        elif (pwin <= self.player[3] and ploss <= self.player[3] and pdraw <=self.player[3]):
            return [0.0, 0.0, 0.0]
        elif pwin >= self.player[3]- self.player[4] and pdraw >= self.player[3] - self.player[4] and ploss >= self.player[3] - self.player[4]:
            return [xwin, xdraw, xloss]
        #Needs modification
        else:
            if bhome <=self.player[0]:
                if bdraw <= self.player[1]:
                    xwin = self.player[0] * self.player[3] /(self.player[0] + self.player[1])
                    xdraw = self.player[1] * self.player[3] /(self.player[0] + self.player[1])
                    xloss = 0 
                    while xloss * self.away <= self.player[3] - self.player[4]:
                        xloss += 0.01
                        xwin -= 0.01 * (self.home - self.player[0])/(self.home + self.draw - self.player[0] - self.player[1])
                        xdraw -= 0.01 * (self.draw - self.player[1])/(self.home + self.draw - self.player[0] - self.player[1])
                else:
                    if baway <= self.player[2]:
                        xwin = self.player[0] * self.player[3] /(self.player[0] + self.player[2])
                        xdraw = 0
                        xloss = self.player[2] * self.player[3] /(self.player[0] + self.player[2])
                        while xdraw * self.draw <= self.player[3] - self.player[4]:
                            xdraw += 0.01
                            xwin -= 0.01 * (self.home - self.player[0])/(self.home + self.away- self.player[0] - self.player[2])
                            xloss -= 0.01 * (self.away - self.player[2])/(self.home + self.away - self.player[0] - self.player[2])
                    else:
                        xwin = self.player[3]
                        xdraw = 0
                        xloss = 0                    
                        while (self.draw * xdraw < self.player[3] -self.player[4]) or (self.away * xloss < self.player[3] - self.player[4]) :
                            xwin -= 0.01
                            xdraw += 0.01 * (self.draw - self.player[1])/(self.draw + self.away- self.player[1] - self.player[2])
                            xloss += 0.01 * (self.away - self.player[2])/(self.draw + self.away - self.player[1] - self.player[2])                            
            elif bdraw <= self.player[1]:
                if baway <= self.player[2]:
                    xloss = self.player[2] * self.player[3] /(self.player[2] + self.player[1])
                    xdraw = self.player[1] * self.player[3] /(self.player[2] + self.player[1])
                    xwin = 0
                    while xwin * self.home <= self.player[3] - self.player[4]:
                        xwin += 0.01
                        xdraw -= 0.01 * (self.draw - self.player[1])/(self.draw + self.away- self.player[1] - self.player[2])
                        xloss -= 0.01 * (self.away - self.player[2])/(self.draw + self.away - self.player[1] - self.player[2])                       
                else:
                    xwin = 0
                    xdraw = self.player[3]
                    xloss = 0                        
                    while (xwin * self.home  < self.player[3] -self.player[4]) or (xaway * self.away < self.player[3] - self.player[4]):
                        xdraw -= 0.01
                        xwin += 0.01 * (self.home - self.player[0])/(self.home + self.away- self.player[0] - self.player[2])
                        xloss += 0.01 * (self.away - self.player[2])/(self.home + self.away - self.player[0] - self.player[2])                      
            else:
                xwin = 0
                xdraw = 0
                xloss = self.player[3]
                while (xwin * self.home  < self.player[3] -self.player[4]) or (xdraw * self.draw < self.player[3] - self.player[4]):
                    xloss -= 0.01
                    xdraw += 0.01 * (self.draw - self.player[1])/(self.home + self.draw- self.player[1] - self.player[0])
                    xwin += 0.01 * (self.home - self.player[0])/(self.draw + self.home - self.player[1] - self.player[0])
            if (xwin * self.home < self.player[3] - self.player[4]) or (xdraw * self.draw < self.player[3] - self.player[4]) or (xloss * self.away <self.player[3] - self.player[4]):
                xwin = xdraw = xloss = 0
            return [round(xwin, 2), round(xdraw, 2), round(xloss, 2)]

if __name__ == "__main__":
    for x in range(0,100):
        a = Game()
        if a.return_rate > 1 or a.return_rate < 0.75:
            print("Invalid Odds")
        elif a.optimization()[0] == a.optimization()[1] == a.optimization()[2] == 0:
            print("Don't bet on this game.")
        else:
            print("{}: {} Draw: {} {}: {}".format(a.hometeam, a.optimization()[0], a.optimization()[1], a.awayteam, a.optimization()[2]))
            print("Outcome &  W/L")
            print("Home Victory: {}, Draw: {}, Away Victory: {}".format(round(a.optimization()[0] * a.home - a.player[3], 2), round(a.optimization()[1] * a.draw - a.player[3], 2), round(a.optimization()[2] * a.away - a.player[3],2)))
          
            
            
        
            
        
        
