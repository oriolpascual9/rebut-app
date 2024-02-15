import pandas as pd

class OutputExcel:
    def __init__(self,rebuts, importes):
        df = pd.DataFrame(rebuts)
        columns = ["nberenars","picapica"]
        # groupby data per tenir els totals de berenars i picapiques al dia
        self.df_total = df.groupby("data").sum()[columns]
        
        # ordenar per data per poder fer match amb l'import
        self.df_total.index = pd.to_datetime(self.df_total.index, format = "%d/%m/%y")
        self.df_total.sort_index(inplace=True)
        self.df_total["import"] = importes
        
        # generem la base restant el 10% del import total
        self.df_total["base"] = self.df_total["import"].apply(lambda x: x/1.1)
        self.df_total["iva"] = self.df_total["base"].apply(lambda x: x * 0.1)

    def generateExcel(self):
        self.df_total['date'] = list(map(lambda data: data.strftime("%d/%m/%y"),self.df_total.index))

        # groupby your key and freq
        g = self.df_total.groupby(pd.Grouper(freq='M'))
        # groups to a list of dataframes with list comprehension
        dfs = [group for _,group in g]

        for df in dfs:
            filename = "./facturacio/" + df.index[0].strftime("%m-%y") + ".xlsx"
            
            columns = ["date","base","iva","import","nberenars","picapica"]
            headers = ["Data","BI","IVA","Import","Berenars","Pica-pica"]
            
            df.to_excel(filename, index=False, columns=columns, header=headers)