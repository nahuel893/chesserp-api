from endpoints import Endpoints
import pandas as pd
import os

from dotenv import load_dotenv


class Stock:
    def __init__(self, endpoint):
        load_dotenv() # verify ambit

        self.data_dir = os.path.abspath(os.path.join((os.getcwd()), "data"))
        self.endpoint = endpoint
        self.stock = pd.DataFrame()
        self.df_deposits = pd.read_csv(os.path.join(self.data_dir, "deposits.csv"), sep=',')
        self.df_deposits.rename(columns={'Deposito':'idDeposito'}, inplace=True)

        self.df_bloat_articles = pd.read_excel(os.path.join(self.data_dir, "bloat_articles.xlsx")) # migrate to .csv)
        self.df_bloat_articles = self.df_bloat_articles[['CODIGO', 'SIRVE']]

        self.df_bloat_articles.rename(columns={'CODIGO':'idArticulo'}, inplace=True) # NEW FUTURE CLASS, data of endpoint

        #self.df_categorys = os.getenv('PATH_ART') # Migrate to obtain to api chsserp
        # Load categorization for articles
        self.df_categorys = pd.read_excel(os.path.join(self.data_dir, "articulos.xlsx"))
        self.df_categorys.rename(columns={'CODIGO':'idArticulo'}, inplace=True) # NEW FUTURE CLASS, data of endpoint

    def get_stock_default(self) -> pd.DataFrame:
        return self.__to_df(self.endpoint.get_stock())
    
    def __to_df(self, dic: dict) -> pd.DataFrame:
        columns = ["idDeposito", "idArticulo", "dsArticulo", "cantBultos", "cantUnidades"]
        df = pd.DataFrame(dic['dsStockFisicoApi']['dsStock'])[columns]
        return df

    def get_stock(self, date: str, idDep: str) -> pd.DataFrame:
        self.stock = self.__to_df(self.endpoint.get_stock(date, idDep))
        return self.stock

    def get_stocks(self) -> pd.DataFrame:        
        list_ = []
        
        for index, row in self.df_deposits.iterrows():
            list_.append(self.__to_df(self.endpoint.get_stock(idDeposito=row['idDeposito'])))
    
        self.stock = pd.concat(list_, ignore_index=True)

        # Add deposit description and branch description
        self.stock = pd.merge(
            self.stock,
            self.df_deposits, 
            on='idDeposito',
            how='left'
        ).reset_index()

        # Delete bloat articles
        self.stock = pd.merge(
            self.stock,
            self.df_bloat_articles,
            on='idArticulo',
            how='left'
        ).reset_index()
        self.stock = self.stock[self.stock.SIRVE.isna()]

        # Add categorization
        self.stock = pd.merge(
            self.stock,
            self.df_categorys[['idArticulo', 'GENERICO', 'MARCA']],
            on='idArticulo',
            how='left'
        )
 
        # Order by Sucursal 
        self.stock.sort_values(by="Sucursal", inplace=True)
        
        self.stock = self.stock.pivot_table(
            values='cantBultos',
            index=['idArticulo', 'dsArticulo', 'GENERICO', 'MARCA'],
            columns='Sucursal',
            aggfunc='sum',
        ).reset_index()

        # to-do: move data transformation to another method 

        return self.stock

    def to_excel(self) -> None:
        self.stock.to_excel(os.path.join(self.data_dir, "stock.xlsx"))

if __name__ == "__main__":
    endp = Endpoints()
    endp.login()
    stock = Stock(endp)
    stock.get_stocks()
    stock.to_excel()

    print(stock)
