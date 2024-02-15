from FileHandler import FileHandler
from distribution import generate_split

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
        self.importe = values['import']
        self.nberenars = int(values['berenar'])
        self.npicapica = int(values['pica-pica'])
        self.nxuxes = int(values['xuxes'])
        self.day = datetime.strptime(values['data'], "%d-%m-%Y")

    def generateRebuts(self):
        rebuts = []
        if self.day.strftime("%A") == "Friday":
            rebuts = DataHandler.generateRebutsDiv(self)
        elif self.day.strftime("%A") == "Saturday":
            rebuts = DataHandler.generateRebutsDiss(self)
        elif self.day.strftime("%A") == "Sunday":
            rebuts = DataHandler.generateRebutsDium(self)
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
        
        return rebuts
    
    def generateImportes(self):
        importes = []
        if self.day.strftime("%A") == "Friday":
            importes = DataHandler.generateImportesDiv(self)
        else:
            importes = [self.importe]
        return importes
    
    def generateRebutsDiv(self):
        rebuts = []
        div_percent = int(random.uniform(40,50)) / 100
        dij_percent = int(random.uniform(25,32)) / 100
        set_percent = 1 - div_percent - dij_percent
        dim_percent = set_percent * (int(random.uniform(30,40)) / 100)
        dm_percent = set_percent * (int(random.uniform(25,40)) / 100)
        dll_percent = set_percent - dim_percent - dm_percent
       
        # festes dll
        rebuts += DataHandler.generateFestes(self, dll_percent, self.day - timedelta(days=4), setmana)
        
        # quan nberenars es baix,
        
        # festes dm
        rebuts += DataHandler.generateFestes(self, dm_percent, self.day - timedelta(days=3), setmana)
        # festes dim
        rebuts += DataHandler.generateFestes(self, dim_percent, self.day - timedelta(days=2), setmana)
        # festes dij
        rebuts += DataHandler.generateFestes(self, dij_percent, self.day - timedelta(days=1), setmana)
        # festes div
        rebuts += DataHandler.generateFestes(self, div_percent, self.day, div)

        return rebuts

    def generateImportesDiv(self):
        div_percent = int(random.uniform(40,50)) / 100
        dij_percent = int(random.uniform(25,32)) / 100
        set_percent = 1 - div_percent - dij_percent
        dim_percent = set_percent * (int(random.uniform(30,40)) / 100)
        dm_percent = set_percent * (int(random.uniform(25,40)) / 100)
        dll_percent = set_percent - dim_percent - dm_percent

        return [self.importe*dll_percent, self.importe*dm_percent, 
                self.importe*dim_percent, self.importe*dij_percent,
                self.importe*div_percent]

    def generateRebutsDiss(self):
        rebuts = []
        mati_percent = int(random.uniform(40,55)) / 100
        tarda_percent = 1 - mati_percent
        
        # festes diss mati
        rebuts += DataHandler.generateFestes(self, mati_percent, self.day, diss_mt)

        # festes diss tarda
        rebuts += DataHandler.generateFestes(self, tarda_percent, self.day, diss_td)

        return rebuts
    
    def generateRebutsDium(self):
        rebuts = []
        dium_percent = 1
        
        # festes diss mati
        rebuts += DataHandler.generateFestes(self, dium_percent, self.day, dium)
        
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
        if parts_berenars[0] <= 10:
            return

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
            "nom" : "joan",
            "nberenars" : nberenars,
            "data" : date.strftime("%d/%m/%y"),
            "xuxes": nxuxes,
            "picapica": npicapica,
            "import": 0, # l'import es calcula despres de corregir els errors de rounding
            "preu_berenar": preu,
            "preu_xuxes": xuxes,
            "preu_picapica": picapica,
            "fiança": fianca,
            "rebut_num": nrebut
        }
        return festa
    
    def checkAndCorrect(self, rebuts):
        real_berenars = sum(rebut['nberenars'] for rebut in rebuts)
        real_xuxes = sum(rebut['xuxes'] for rebut in rebuts)
        real_picapica = sum(rebut['picapica'] for rebut in rebuts)

        if real_berenars != self.nberenars:
            rebuts = DataHandler.correct(self, 'nberenars', rebuts, real_berenars, self.nberenars)

        if real_xuxes != self.nxuxes:
            rebuts = DataHandler.correct(self, 'xuxes', rebuts, real_xuxes, self.nxuxes)

        if real_picapica != self.npicapica:
            rebuts = DataHandler.correct(self, 'picapica', rebuts, real_picapica, self.npicapica)
        
        return rebuts
    
    def correct(self, key, rebuts, real, original):
        # generate as many random selected parties as elements missing
        nrebuts = list(range(len(rebuts)))

        festes = Counter(random.choices(nrebuts, k = original - real))

        # assign the missing berenars to the randomly selected parties
        for i, valor in festes.items():
            rebuts[i][key] += valor
    
        return rebuts
    
    def handleFiança(self, rebuts):
        # generate 3 or 4 random parties to take out fiança
        nrebuts = [index for index,festa in enumerate(rebuts) if festa['nberenars'] <= 14]
        max_festes = max(len(rebuts) - 1, 4)
        nfestes = random.randint(1,max_festes)
        festes = random.choices(nrebuts, k = nfestes)
        for i in festes:
            rebuts[i]['fiança'] = 0

        return rebuts
    
    def computeImport(self, rebut):
        rebut['import'] += rebut['nberenars'] * rebut['preu_berenar']
        rebut['import'] += rebut['xuxes'] * xuxes
        rebut['import'] += rebut['picapica'] * picapica

        return rebut      
