from Agent import *
from Node import *
from US_STATE import *
class RealTimaAStarAgent(Agent):

    def takeTurn(self, countries):
        #initialize state
        #intitialState = Node(US_STATE.countries, self)

        self.attack(countries)



    def attack(self, state):
        opponent = None
        mp = {}
        for c in state:
            mp[c.id] = c
            if c.owner == self:
                c.ownerboolean = True
            else:
                c.ownerboolean = False
                opponent = c.owner

        newCountries = self.decision(state)

        self.countries.clear()
        opponent.countries.clear()
        for c in newCountries:
            if c.ownerboolean is True:
                mp[c.id].owner = self
                self.countries.append(c)
            else:
                mp[c.id].owner = opponent
                opponent.countries.append(mp[c.id])
            mp[c.id].numOfTroops = c.numOfTroops

    def decision(self, state) -> [Country]:
        (child, x) = self.maximize(state, 0, -1e9)
        return child

    def heuristic(self, state: [Country]):
        attacking = 0
        defending = 0

        for c in state:
            if c.owner == self:
                for n in c.neighbors:
                    if n.owner != self and c.numOfTroops - 1 > n.numOfTroops:
                        attacking += 1
            else:
                for n in c.neighbors:
                    if n.owner == self and c.numOfTroops - 1 <= n.numOfTroops:
                        defending += 1

        return attacking+defending



    def chooseCountryToAddTroops(self) -> Country:
        pass