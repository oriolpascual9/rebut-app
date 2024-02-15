from DataHandler import DataHandler
from OutputPDF import OutputPDF
from OutputExcel import OutputExcel

values = {
    "import" : 1500,
    "berenar": 98,
    "pica-pica": 5,
    "xuxes": 71,
    "data": "02-02-2024"
}

dh = DataHandler(values)
rebuts = dh.generateRebuts()
importes = dh.generateImportes()

i = 0
for rebut in rebuts:
    OutputPDF(rebut, i).generatePDF()
    i+=1

OutputExcel(rebuts,importes).generateExcel()