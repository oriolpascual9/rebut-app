import json

class FileHandler:
    def __init__(self):
        # read info json
        self.filename = './info/info.json'
        self.f = open(self.filename, encoding='utf-8')
        self.data = json.load(self.f)

        self.fn = open('./info/noms.json', encoding='utf-8')
        self.noms = json.load(self.fn)
        self.fn.close()
    
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
    
    def readNameList(self):
        # Create a list of keys, weighted by their magnitude (higher keys have more chance to be selected)
        keys = []
        for key, value in self.noms.items():
            keys.extend([key] * value)  # Multiply the occurrence of each key by its value

        return keys

