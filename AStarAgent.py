import operator

from Agent import *
from heapq import *
from copy import *

from Node import *
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

        newCountries = self.a_star_search(copy.deepcopy(countries))

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

    def a_star_search(self, countries: [Country]) -> [Country]:
        curNode = Node(countries, None)
        frontier = []
        stateToNode = dict()
        heapify(frontier)
        stateToNode[curNode.encodedState] = curNode
        heappush(frontier, (curNode.heuristic, curNode.encodedState))
        explored = set()
        frontier_config = {}
        helper = dict()
        helper[curNode.encodedState] = curNode.heuristic
        frontier_config[curNode.encodedState] = True
        nodes_expanded = 0
        while len(frontier) > 0:
            # if nodes_expanded >= 10000:
            #     x, y = heappop(frontier)
            #     return stateToNode[y].path_to_root().countries
            (cost, encodedState) = heappop(frontier)
            while encodedState in helper and cost > helper[encodedState]:
                cost, encodedState = heappop(frontier)

            explored.add(encodedState)
            helper.pop(encodedState)

            if stateToNode[encodedState].isGoal():
                return stateToNode[encodedState].path_to_root().countries
            nodes_expanded += 1
            for neighborNode in stateToNode[encodedState].generateChildren():
                # Add state to explored states if doesn't already exists.
                if neighborNode.encodedState not in explored and neighborNode.encodedState not in frontier_config:
                    heappush(frontier, (neighborNode.heuristic, neighborNode.encodedState))
                    stateToNode[neighborNode.encodedState] = neighborNode
                    helper[neighborNode.encodedState] = neighborNode.heuristic
                    frontier_config[neighborNode.encodedState] = True
                elif neighborNode.encodedState in helper:
                    if neighborNode.heuristic < helper[neighborNode.encodedState]:
                        heappush(frontier, (neighborNode.heuristic, neighborNode.encodedState))
                        stateToNode[neighborNode.encodedState] = neighborNode
                        helper[neighborNode.encodedState] = neighborNode.heuristic
        return None

    def heuristic(self, state) -> int:
        enemyCountries = 0
        enemyTroops = 0
        for c in state:
            if c.ownerboolean == False:
                enemyCountries += 1
                enemyTroops += c.numOfTroops
        return enemyCountries + enemyTroops
