from Agent import *
import ctypes
import time
import threading


class GreedyAgent(Agent):
    c=None
    num=0

    def func(self):
        #country.numOfTroops=num
        self.c.numOfTroops=self.num
    def takeTurn(self):

        # time.sleep(5)
        troopsAddedToCountry=self.addBonusTroops()
        print(troopsAddedToCountry.id)
        self.attackHelper(troopsAddedToCountry)
        return True

    def addBonusTroops(self):
        myCountries = self.countries

        # heuristic to put bonus troops : for every country of mine will get num of enemy troops surrouned by
        #                                and the bonus troops will add to country with
        #                                max num of surrouned troops - amount of troops in this country
        bonustroops = self.calcBonusTroops()
        surroundedwith = []

        for mycountry in myCountries:
            counter = 0
            for c in mycountry.neighbors:
                if (c.owner == self):
                    counter -= c.numOfTroops
                else:
                    counter += c.numOfTroops
            surroundedwith.append(counter - mycountry.numOfTroops)
        flag = True
        while flag:
            indexToPutTroops = surroundedwith.index(max(surroundedwith))
            if myCountries[indexToPutTroops].owner == self:

                myCountries[indexToPutTroops].numOfTroops += bonustroops
                return myCountries[indexToPutTroops]


            else:
                del surroundedwith[indexToPutTroops]

    def attackHelper(self ,troopsAddedToCountry):
        global countryAttackto
        myCountries = self.countries
        surroundedwith = []

        for mycountry in myCountries:
            counter = 0
            for c in mycountry.neighbors:
                if (c.owner == self):
                    counter -= c.numOfTroops
                else:
                    counter += c.numOfTroops
            surroundedwith.append(counter - mycountry.numOfTroops)
        flag = True
        while flag:

            surroundedwith.sort()
            i=0
            for s in surroundedwith  :
                 if (myCountries[i].owner == self):
                     countryAttackFrom = myCountries[i]
                     countryAttackFrom.neighbors.sort(key=lambda x: x.numOfTroops)
                     for c in countryAttackFrom.neighbors:
                          countryAttackto=c
                          if countryAttackto.numOfTroops < countryAttackFrom.numOfTroops-1  and countryAttackto.owner != self:
                              # do the attack
                              numOfTroopsAttackwith = countryAttackto.numOfTroops+1
                              use_timer=True
                              if use_timer:
                                temp_num_to=numOfTroopsAttackwith
                                temp_num_from=countryAttackFrom.numOfTroops
                                t=threading.Timer(3,self.setTroops,args=(countryAttackto,countryAttackFrom,temp_num_to,temp_num_from,troopsAddedToCountry,troopsAddedToCountry.numOfTroops))
                                t.start()
                                troopsAddedToCountry.numOfTroops= str(troopsAddedToCountry.numOfTroops)+' B'
                                countryAttackFrom.numOfTroops=str(countryAttackFrom.numOfTroops)+'A'
                                countryAttackto.numOfTroops = str(countryAttackto.numOfTroops)+"D"
                              else:
                                  countryAttackFrom.numOfTroops -= numOfTroopsAttackwith
                                  countryAttackto.owner.removeCountry(countryAttackto)
                                  countryAttackto.owner = self
                                  countryAttackto.owner.countries.append(countryAttackto)


                              flag = False
                              return
                 i+=1
            print("NO possible attacks")
#            ctypes.windll.user32.MessageBoxW(0, "NO POSSIBLE ATTACKS", "ALERT", 1)
            return
    def setTroops(self,country_to,country_from,num_to,num_from,troopsAddedToCountry,num_bonus):
        country_to.numOfTroops=num_to
        country_from.numOfTroops=num_from
        country_from.numOfTroops -= num_to
        country_to.owner.removeCountry(country_to)
        country_to.owner = self
        country_to.owner.countries.append(country_to)
        troopsAddedToCountry.numOfTroops=num_bonus
    def setTroopsBonus(self,country,old_num,amount):
        country.numOfTroops=old_num+amount