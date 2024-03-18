from src.DataHandler import DataHandler
from src.OutputPDF import OutputPDF
from src.OutputExcel import OutputExcel

values = {
    "import" : 1500,
    "berenar": 98,
    "pica-pica": 5,
    "xuxes": 71,
    "data": "09-02-2024"
}

dh = DataHandler(values)
rebuts, no_festa_days = dh.generateRebuts()
importes = dh.generateImportes(no_festa_days)

i = 0
for rebut in rebuts:
    OutputPDF(rebut, i).generatePDF()
    i+=1

OutputExcel(rebuts,importes).generateExcel()