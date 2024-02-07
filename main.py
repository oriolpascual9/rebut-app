from DataHandler import DataHandler
from Output import Output

values = {
    "import" : 100,
    "berenar": 203,
    "pica-pica": 10,
    "xuxes": 125,
    "data": "02-02-2024"
}

dh = DataHandler(values)
rebuts = dh.generateRebuts()

i = 0
for rebut in rebuts:
    Output(rebut, i).generatePDF()
    i+=1