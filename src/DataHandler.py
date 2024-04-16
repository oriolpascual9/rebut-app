from src.FileHandler import FileHandler
from src.distribution import generate_split

from datetime import datetime, timedelta
import random
from collections import Counter
import math

# import variables about price
# nrebut will be updated once rebuts are finished being generated
fileHandler = FileHandler()
setmana, div, diss_mt, diss_td, dium, \
xuxes, picapica, nrebut, fianca = fileHandler.readVariables()

class DataHandler:
    def __init__(self, values):
        self.importe = float(values['import'])
        self.nberenars = int(values['berenar'])
        self.npicapica = int(values['pica-pica'])
        self.nxuxes = int(values['xuxes'])
        self.day = datetime.strptime(values['data'], "%d-%m-%Y")

        # Gestionar festius si n'hi ha
        dia_dict = {
            "Dilluns": 4,
            "Dimarts": 3,
            "Dimecres": 2,
            "Dijous": 1,
            "Divendres": 0
        }
        self.festius = [dia_dict[dia] for dia in values['festa_list']]

    def generateRebuts(self, unhandeled = False):
        rebuts = []
        no_festa_days = []

        if unhandeled:
            if self.day.strftime("%A") == "Saturday":
                rebuts = DataHandler.generateRebutsDiss(self)
            else:
                rebuts = DataHandler.generateRebutsDium(self, unhandeled)

        else: 
            if self.day.strftime("%A") == "Friday":
                rebuts, no_festa_days = DataHandler.generateRebutsDiv(self)
            elif self.day.strftime("%A") == "Saturday":
                rebuts = DataHandler.generateRebutsDiss(self)
            elif self.day.strftime("%A") == "Sunday":
                rebuts = DataHandler.generateRebutsDium(self, False)
            else:
                raise Exception("Data no correspon a div, diss o dium")
        
        # rounding error will make sum not equaling totals for berenars, picapica o xuxes
        rebuts = DataHandler.checkAndCorrect(self,rebuts)
        rebuts = DataHandler.handleFiança(self,rebuts)
        rebuts = [DataHandler.computeImport(self, rebut) for rebut in rebuts]

        print("Correct nberenars: ", self.nberenars == sum(rebut['nberenars'] for rebut in rebuts))
        print("Correct nxuxes: ", self.nxuxes == sum(rebut['xuxes'] for rebut in rebuts))
        print("Correct npicapica: ", self.npicapica == sum(rebut['picapica'] for rebut in rebuts))
        
        # update last number of rebut used
        fileHandler.writeRebutAndClose(nrebut)
        
        return rebuts, no_festa_days
    
    def generateImportes(self, no_festa_days):
        importes = []
        if self.day.strftime("%A") == "Friday":
            importes = DataHandler.generateImportesDiv(self, no_festa_days)
        else:
            importes = {self.day : self.importe}
        return importes
    
    def generateRebutsDiv(self):
        global nrebut
        parcial_nrebut = nrebut

        rebuts = []
        div_percent = int(random.uniform(40,50)) / 100
        dij_percent = int(random.uniform(25,32)) / 100
        set_percent = 1 - div_percent - dij_percent
        dim_percent = set_percent * (int(random.uniform(30,40)) / 100)
        dm_percent = set_percent * (int(random.uniform(25,40)) / 100)
        dll_percent = set_percent - dim_percent - dm_percent

        percents = {
            4: dll_percent,
            3: dm_percent,
            2: dim_percent,
            1: dij_percent,
            0: div_percent
        }
        
        # Inicialitzem dies que no hi ha festa amb dies festius
        days_not_assigned = self.festius
        no_festa_days = []          
        while True:
            for key, percent in percents.items():
                day_offset = key # div - 4 = dll
                rebuts_before = rebuts.copy()
                # festes dll, dm, dim, dj
                if day_offset > 0:
                    rebuts += DataHandler.generateFestes(self, percent, self.day - timedelta(days=day_offset), setmana)
                else: # div canvia el preu
                    rebuts += DataHandler.generateFestes(self, percent, self.day, div)
                
                # no hi ha suficients berenars per generar una festa (nberenars<=10)
                if rebuts_before == rebuts:
                    days_not_assigned.append(day_offset)
                
                day_offset -= 1
            
            # all days have been assigned we may proceed
            if len(days_not_assigned) == 0:
                break
                
            # there is not enough berenars for all days, prepare redistribution
            else:
                nrebut = parcial_nrebut
                rebuts = []

                percents, dia_no_assignat = DataHandler.redistribucioFesta(self, percents, days_not_assigned)
                days_not_assigned = []
                no_festa_days.append(dia_no_assignat)

        return rebuts, no_festa_days

    def generateImportesDiv(self, no_festa_days):
        div_percent = int(random.uniform(40,50)) / 100
        dij_percent = int(random.uniform(25,32)) / 100
        set_percent = 1 - div_percent - dij_percent
        dim_percent = set_percent * (int(random.uniform(30,40)) / 100)
        dm_percent = set_percent * (int(random.uniform(25,40)) / 100)
        dll_percent = set_percent - dim_percent - dm_percent

        importes = {
            4 : self.importe*dll_percent, 
            3 : self.importe*dm_percent, 
            2 : self.importe*dim_percent,
            1 : self.importe*dij_percent,
            0 : self.importe*div_percent
        }

        for dia_festiu in self.festius:
            if dia_festiu != None:
                # first we take 40% to be redistributed between the other days
                distr = importes[dia_festiu] / (len(importes) - 1)

                importes = {key: (0 if key == dia_festiu else value + distr) for key, value in importes.items()}


        for no_festa_dia in no_festa_days:
            if no_festa_dia != None:
                # first we take 40% to be redistributed between the other days
                distr = 0.4*importes[no_festa_dia] / (len(importes) - 1)
                # then reduce the day with no party to 60%
                importes[no_festa_dia] = 0.6*importes[no_festa_dia]
        
                importes = {key: (value if key == no_festa_dia else value + distr) for key, value in importes.items()}

        # translacio de numero a format calendari pels imports
        importes = {self.day - timedelta(days=key): value for key, value in importes.items()}

        return importes

    def generateRebutsDiss(self):
        rebuts = []
        rebuts2 = []
        mati_percent = int(random.uniform(40,55)) / 100
        tarda_percent = 1 - mati_percent
        
        # festes diss mati
        while len(rebuts) == 0:
            rebuts = DataHandler.generateFestes(self, mati_percent, self.day, diss_mt)

        # festes diss tarda
        while len(rebuts2) == 0:
            rebuts2 = DataHandler.generateFestes(self, tarda_percent, self.day, diss_td)

        return rebuts + rebuts2
    
    def generateRebutsDium(self, unhandeled):
        rebuts = []
        dium_percent = 1
        preu = dium

        if unhandeled:
            if self.day.strftime("%A") == "Friday":
                preu = div
            elif self.day.strftime("%A") == "Sunday":
                preu = dium
            else:
                preu = setmana
        
        # festes diss mati
        while len(rebuts) == 0:
            rebuts += DataHandler.generateFestes(self, dium_percent, self.day, preu)
        
        return rebuts

    def generateFestes(self, percent, date, preu):
        rebuts = []
        berenars_day = percent * float(self.nberenars)
        picapica_day = percent * float(self.npicapica)
        xuxes_day = percent * float(self.nxuxes)

        parts_berenars = generate_split(berenars_day)

        nfestes = list(range(len(parts_berenars)))
        picapicafesta = Counter(random.choices(nfestes, k = math.floor(picapica_day)))
        xuxes_festa = Counter(random.choices(nfestes, k = math.floor(xuxes_day)))

        # less than 10 participants per party, cancel and redistribute
        if parts_berenars[0] < 10:
            return []

        for i in range(len(parts_berenars)):
            npicapica = picapicafesta[i] if i in picapicafesta else 0
            nxuxes = xuxes_festa[i] if i in xuxes_festa else 0
            rebuts.append(DataHandler.generateFesta(self, parts_berenars[i], nxuxes, npicapica, date, preu))

        return rebuts
    
    def generateFesta(self, nberenars, nxuxes, npicapica, date, preu):
        # update the nrebut
        global nrebut
        nrebut += 1

        festa =  {
            "nom" : DataHandler.findName(),
            "nberenars" : nberenars,
            "data" : date.strftime("%d/%m/%y"),
            "xuxes": 0,
            "picapica": npicapica,
            "import": 0, # l'import es calcula despres de corregir els errors de rounding
            "preu_berenar": preu,
            "preu_xuxes": xuxes,
            "preu_picapica": picapica,
            "fiança": fianca,
            "rebut_num": nrebut
        }
        return festa
    
    def findName():
        noms = FileHandler().readNameList()
        return random.choice(noms)
    
    def find_closest_sum(numbers, target):
        # Initialize a list to keep track of the best sums achievable with subsets
        dp = [None] * (target + 1)
        dp[0] = []  # Base case: no number needed to reach sum 0
        for number in numbers:
            for potential_sum in range(target, number - 1, -1):
                if dp[potential_sum - number] is not None:
                    new_combination = dp[potential_sum - number] + [number]
                    if dp[potential_sum] is None or sum(new_combination) > sum(dp[potential_sum]):
                        dp[potential_sum] = new_combination

        # Find the non-None value closest to the target (without exceeding it)
        for i in range(target, -1, -1):
            if dp[i] is not None:
                return i, dp[i]

    
    def generateXuxes(self, rebuts):
        berenars_list = [rebut['nberenars'] for rebut in rebuts]
        final_sum, comb = DataHandler.find_closest_sum(berenars_list, self.nxuxes)
        for rebut in rebuts:
            for nxuxes in comb:
                if rebut['nberenars'] == nxuxes:
                    rebut['xuxes'] = nxuxes
                    comb.remove(nxuxes)
                    break

        return rebuts
       
    def checkAndCorrect(self, rebuts):
        real_berenars = sum(rebut['nberenars'] for rebut in rebuts)
        real_picapica = sum(rebut['picapica'] for rebut in rebuts)

        rebuts = DataHandler.generateXuxes(self, rebuts)
        real_xuxes = sum(rebut['xuxes'] for rebut in rebuts)
        rebuts = DataHandler.correct(self, 'xuxes', rebuts, real_xuxes, self.nxuxes)

        if real_berenars != self.nberenars:
            rebuts = DataHandler.correct(self, 'nberenars', rebuts, real_berenars, self.nberenars)

        if real_picapica != self.npicapica:
            rebuts = DataHandler.correct(self, 'picapica', rebuts, real_picapica, self.npicapica)
        
        return rebuts
    
    def correct(self, key, rebuts, real, original):
        #if key == 'xuxes':
        #    nrebuts = [idx for idx in list(range(len(rebuts))) if rebuts[idx][key] > 0]
        #else:
        # generate as many random selected parties as elements missing
        nrebuts = list(range(len(rebuts)))

        festes = Counter(random.choices(nrebuts, k = original - real))

        # assign the missing berenars to the randomly selected parties
        for i, valor in festes.items():
            rebuts[i][key] += valor
    
        return rebuts
    
    def handleFiança(self, rebuts):
        num_fiança = int(round(len(rebuts) * 0.2,0))
        nrebuts = [index for index,festa in enumerate(rebuts) if festa['nberenars'] <= 14]

        # nomes amb fiança 0 per festa de menys de 14
        # sino hi ha doncs saltem pas
        if len(nrebuts) != 0 and num_fiança > 0:
            festes = random.choices(nrebuts, k = num_fiança)
            for i in festes:
                rebuts[i]['fiança'] = 0

        return rebuts
    
    def computeImport(self, rebut):
        rebut['import'] += rebut['nberenars'] * rebut['preu_berenar']
        rebut['import'] += rebut['xuxes'] * xuxes
        rebut['import'] += rebut['picapica'] * picapica

        return rebut
    
    def redistribucioFesta(self, percents, days_not_assigned):
        # aquesta funcio agafa els dies que no han sigut assignats per insuficiencia de berenars(<10)
        # si hi ha més d'un dia no assignat els combina per provar si s'arriba al minim de dinars
        # si només n'hi ha un reparteix el percentatge entre els dies assignats

        # create dictionary with not assigned percents
        percents_not_assigned = {key: percents[key] for key in percents if key in days_not_assigned}

        # Create a list of keys, weighted by their magnitude (higher keys have more chance to be selected)
        keys = []
        for key in percents_not_assigned.keys():
            keys.extend([key] * key)  # Multiply the occurrence of each key by its value

        # per algun motiu de vegades divendres(0) no l'assigna
        # si nomes es divendres la llista de keys estara buida
        key_to_remove = None
        if len(keys) > 0:
            # Select a random key to remove
            key_to_remove = random.choice(keys)

            # if there is just one day not assigned the value needs to be shared to all the other percents
            # you cannot try to share
            if len(days_not_assigned) == 1:
                percents_not_assigned = percents

            # Calculate the value to distribute among other keys
            value_to_distribute = percents_not_assigned[key_to_remove] / (len(percents_not_assigned) - 1)

            # Remove the selected key
            del percents_not_assigned[key_to_remove]
            if key_to_remove in percents: del percents[key_to_remove]

            # Distribute the value of the removed key evenly among the remaining keys
            for key in percents_not_assigned:
                percents_not_assigned[key] += value_to_distribute

        # retorna un merge dels dictionaris, si concideixen agafa els valors de percents_not_assigned
        result = {**percents, **percents_not_assigned}

        return {**percents, **percents_not_assigned}, key_to_remove

