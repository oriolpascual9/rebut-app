import PySimpleGUI as sg
from DataHandler import DataHandler
from OutputPDF import OutputPDF
from OutputExcel import OutputExcel

sg.theme('DarkAmber')

# Define the layout for your window
layout = [
    [sg.Text('Tria data'), sg.Input(key='data', size=(20,1)), sg.CalendarButton('Calendar', target='data', close_when_date_chosen=True,  format='%d-%m-%Y')],
    [sg.Text('Total Import'), sg.InputText(key='import')],
    [sg.Text('Total Berenars'), sg.InputText(key='berenar')],
    [sg.Text('Total Pica-piques'), sg.InputText(key='pica-pica')],
    [sg.Text('Total Xuxes'), sg.InputText(key='xuxes')],
    [sg.Button('Submit'), sg.Button('Cancel')]
]

# Create the Window
window = sg.Window('Window Title', layout)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (None, 'Cancel'):   # If user closes window or clicks cancel
        break
    if event == 'Submit':
        # You can use the values dictionary to access the input data
        # and do something with it here
        dh = DataHandler(values)
        rebuts = dh.generateRebuts()
        importes = dh.generateImportes()

        i = 0
        for rebut in rebuts:
            OutputPDF(rebut, i).generatePDF()
            i+=1

        OutputExcel(rebuts, importes).generateExcel()

        break

window.close()