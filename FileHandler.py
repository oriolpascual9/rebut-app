import json

class FileHandler:
    def __init__(self):
        # read info json
        self.filename = './info.json'
        self.f = open(self.filename, encoding='utf-8')
        self.data = json.load(self.f)
    
    def readVariables(self):
        # make info available in variables
        setmana = self.data['setmana']
        div = self.data['div']
        diss_mt = self.data['diss_mt']
        diss_td = self.data['diss_td']
        dium = self.data['dium']
        xuxes = self.data['xuxes']
        picapica = self.data['picapica']
        nrebut = self.data['nrebut']
        fianca = self.data['fianca']

        # close file
        self.f.close()

        return setmana, div, diss_mt, diss_td, dium, xuxes, picapica, nrebut, fianca

    def writeRebutAndClose(self, nrebut):
        # update rebut number
        self.data['nrebut'] = nrebut

        # write file
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f)
