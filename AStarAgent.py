import operator

from Agent import *
from heapq import *
from copy import *

from US_STATE import *

class AStarAgent(Agent):

    def __init__(self, type, color):
        super().__init__(type, color)
        self.cost = 0

    def takeTurn(self, countries):
        self.attack(countries)
        self.cost += 2

    def attack(self, countries):
        opponent = None
        mp = {}
        for c in countries:
            mp[c.id] = c
            if c.owner == self:
                c.ownerboolean = True
            else:
                c.ownerboolean = False
                opponent = c.owner

        pq = []
        heapify(pq)
        curState = deepcopy(countries)
        x = int(self.cost + self.heuristic(curState))
        heappush(pq, (x, curState))
        (curCost, curState) = heappop(pq)
        children = self.generateChildren(curState)
        for child in children:
            x = int(self.cost+1 + self.heuristic(child))
            #heappush(pq, (x, deepcopy(child)))
            pq.append((x,deepcopy(child)))
        #heapify(pq)
        sorted(pq, key=operator.itemgetter(0))
        (bestCost, newCountries) = pq[0]

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


    def generateChildren(self, state) -> [[Country]]:
        retStates = []
        amount = self.calcBonusTroops()
        for c in state:
            if c.ownerboolean:
                c.addTroops(amount)
                for neighbor in c.neighbors:
                    if not neighbor.ownerboolean and c.numOfTroops - 1 > neighbor.numOfTroops:
                        #do
                        attackerTroops = c.numOfTroops
                        defenderTroops = neighbor.numOfTroops
                        defenderOwner = neighbor.owner
                        defenderOwner.removeCountry(neighbor)
                        self.countries.append(neighbor)
                        neighbor.owner = self
                        neighbor.numOfTroops = attackerTroops - 1
                        c.numOfTroops = 1
                        neighbor.ownerboolean = True

                        retStates.append(deepcopy(state))
                        #undo
                        c.numOfTroops = attackerTroops
                        neighbor.numOfTroops = defenderTroops
                        neighbor.owner = defenderOwner
                        neighbor.ownerboolean = False
                        self.removeCountry(neighbor)
                        defenderOwner.countries.append(neighbor)
                c.numOfTroops -= amount
        return retStates

    def chooseCountryToAddTroops(self) -> Country:
        pass

    def heuristic(self, state) -> int:
        enemyCountries = 0
        enemyTroops = 0
        for c in state:
            if c.ownerboolean == False:
                enemyCountries += 1
                enemyTroops += c.numOfTroops
        return enemyCountries + enemyTroops
