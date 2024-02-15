from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import landscape, A5
from reportlab.lib.units import cm
from pdf2docx import Converter

class OutputPDF:
    def __init__(self, rebut, num):
        # Create a canvas for A5 paper size
        self.pathfile = "./rebuts/rebut_{:d}".format(rebut['rebut_num'])
        self.c = canvas.Canvas(self.pathfile + ".pdf", pagesize=landscape(A5))

        # draw background greti
        self.c.drawImage('./img/greti.jpg', -8*cm, -5*cm, mask=[0,0,0,0,0,0])
        
        # draw logo
        self.c.drawImage('./img/logo.jpg',x= 0.5*cm,y = 12*cm, width=2*cm, height=2.2*cm)

        # print company's name
        self.c.setFont("Times-Bold", 12)
        self.c.setFillColorRGB(0,0,0) # font colour
        self.c.drawString(x = 8.6*cm, y = 14*cm, text = "MONPIRATA S.L.")
        self.c.setFont("Helvetica", 9)
        self.c.drawString(x = 9.5*cm, y = 13.7*cm, text = "B56200504")        

        # print company's info
        self.c.setStrokeColorRGB(0.1,0.8,0.1)
        self.c.setFillColorRGB(0,0,1) # font colour
        self.c.drawString(x = 0.5*cm, y = 11.5*cm, text = "Aventura Park, Avda. Roma 35")
        self.c.drawString(x = 0.5*cm, y = 11*cm, text = "08029 Barcelona")
        
        # print green line
        self.c.setFillColorRGB(0,0,0) # font colour
        self.c.line(0.5*cm,10.5*cm,20*cm,10.5*cm)

        # print rebut numero
        self.c.setFont("Helvetica", 14)
        self.c.drawString(16.5*cm,12*cm,'Rebut nº ')

        self.c.setFillColorRGB(0,0,1) # font colour
        self.c.setFont("Helvetica", 30)
        self.c.drawString(16.5*cm,11*cm,'REBUT')
        self.c.setFillColorRGB(0,0,0) # font colour

        # print titols dels conceptes
        self.c.setFont("Times-Roman", 22)
        #self.c.drawString(0.5*cm,9*cm,'Productes')
        self.c.drawString(7*cm,9*cm,'Preu')
        self.c.drawString(10*cm,9*cm,'Quantitat')
        self.c.drawString(17*cm,9*cm,'Total')

        # print taula conceptes
        self.c.setStrokeColorCMYK(0,0,0,1) # vertical line colour 
        self.c.line(6.5*cm,9*cm,6.5*cm,2.7*cm)# first vertical line
        self.c.line(9.5*cm,9*cm,9.5*cm,2.7*cm)# second vertical line
        self.c.line(16.5*cm,9*cm,16.5*cm,2.7*cm)# third vertical line
        self.c.line(0.5*cm,2.5*cm,20*cm,2.5*cm)# horizontal line total

        # print down part title
        self.c.drawString(1.2*cm,1.5*cm,'Data:')
        self.c.drawString(7*cm,1.5*cm,'Nom:')
        self.c.setFillColorRGB(0,0,0) # font colour
        self.c.setFont("Times-Roman", 22)
        self.c.drawString(14.5*cm,1.8*cm,'Suma')
        self.c.drawString(14.2*cm,1.1*cm,'Fiança')

        self.c.setFont("Times-Bold", 22)
        self.c.drawString(14.5*cm,0.3*cm,'Total:')

        # print rebut info
        OutputPDF.fillRebutInfo(self, rebut)

    def fillRebutInfo(self, rebut):
        # print data
        self.c.setStrokeColorRGB(0.1,0.8,0.1)
        self.c.setFillColorRGB(0,0,1) # font colour
        self.c.setFont("Helvetica", 18)
        self.c.drawString(x = 1.2*cm, y = 1*cm, text = rebut['data'])

        self.c.setFont("Helvetica", 14)
        self.c.drawString(18.5*cm, 12*cm, str(rebut['rebut_num']))

        productes = ['nberenars','xuxes','picapica']
        cnt = 0
        total_importe = 0
        for producte in productes:
            total_importe += OutputPDF.printProducte(self, rebut, producte, cnt)
            cnt += 1
        
        # print suma
        self.c.drawString(x = 17*cm, y = 1.75*cm, text = "{:.2f} €".format(total_importe))
        # print fiança
        self.c.drawString(x = 17.15*cm, y = 1.0*cm, text = "-{:.2f} €".format(rebut['fiança']))
        # print total
        self.c.drawString(x = 17*cm, y = 0.3*cm, text = "{:.2f} €".format(total_importe - rebut['fiança']))

    # returns importe total del producte
    def printProducte(self, rebut, producte, cnt):
        self.c.setStrokeColorRGB(0.1,0.8,0.1)
        self.c.setFillColorRGB(0,0,1) # font colour
        self.c.setFont("Helvetica", 18)

        name = ''
        preu = ''
        unitats = ''
        if producte == 'nberenars':
            name = 'Berenars'
            preu = round(rebut['preu_berenar'],2)
            unitats = rebut['nberenars']
        elif producte == 'xuxes':
            name = 'Xuxes'
            preu = round(rebut['preu_xuxes'],2)
            unitats = rebut['xuxes']
        elif producte == 'picapica':
            name = 'Pica-pica'
            preu = round(rebut['preu_picapica'],2)
            unitats = rebut['picapica']
        
        y_shift = 8 - cnt
        self.c.drawString(x = 1*cm, y = y_shift*cm, text = name)
        self.c.drawString(x = 7*cm, y = y_shift*cm, text = "{:.2f} €".format(preu))
        self.c.drawString(x = 10*cm, y = y_shift*cm, text = str(unitats))
        self.c.drawString(x = 17*cm, y = y_shift*cm, text = "{:.2f} €".format(unitats*preu))

        return unitats*preu

    def generatePDF(self):
        # Save the PDF
        self.c.save()
        # Create a PDF converter object and convert the PDF
        # cv = Converter(self.pathfile + '.pdf')
        # cv.convert(self.pathfile + '.docx', start=0, end=None)
        # cv.close()
