from CONFIG import os,PATH,DRIVERPATH,FILEPATH,json
from selenium import webdriver
from bs4 import BeautifulSoup as Soup
import pandas as pd
import snoop

_emitenIDX_api = f"https://idx.co.id/umbraco/Surface/StockData/GetSecuritiesStock?code=&sector=&board=&start={0}&length={5000}"
_FILEDATAEMITEN = 'list_data_emiten'
_stockIDX_api = "https://idx.co.id/umbraco/Surface/ListedCompany/GetTradingInfoSS?code=###&length=^^^"

@snoop
def openfile(filename,mode,data='',SAVEPATH=FILEPATH):
    with open(SAVEPATH+filename+'.json',mode) as file:
        if mode == 'w':
            if data=='':
                print("File data tidak terdefinisi")
                raise NameError
            try:
                data = eval(data)
            except:
                pass
            json.dump(data,file)
            
        else:
            return json.load(file)

class IDx_Grabber:
    s = webdriver.chrome.service.Service(DRIVERPATH)
    def __init__(self):
        self.emitenCatalog = self.get_data_emiten()

    @staticmethod
    def stockJSONtoDFrame(jsonresult,duration):
        dataset = {
            "Date":[],
            "Previous":[],
            "OpenPrice":[],
            "FirstTrade":[],
            "High":[],
            "Low":[],
            "Close":[],
            "Change":[],
            "Volume":[],
            "Value":[],
            "Offer":[],
            "OfferVolume":[],
            "Bid":[],
            "ListedShares":[]

        }
        for history in jsonresult[:duration+1]:
            for key in dataset.keys():
                try:
                    jsonresult = history[key]
                except:
                    result = ""
                dataset[key].append(jsonresult)

        dataframe = pd.DataFrame(dataset)
        return dataframe    
    

    @staticmethod
    def get_history_emiten(code,duration,typeoutput='DataFrame',oldData=None):
        if oldData is not None:
            dataframe = IDx_Grabber.stockJSONtoDFrame(oldData,duration)
        else:
            link = _stockIDX_api.replace("###", code)
            link = link.replace("^^^", str(duration))
            
            result = eval(IDx_Grabber.request_data(link))
            result = result['replies']
            dataframe = IDx_Grabber.stockJSONtoDFrame(result,duration)

        if typeoutput=='json':
            return result
        elif typeoutput ==('json','dframe'):
            return result,dataframe        
        else:
            return dataframe

    @staticmethod
    def request_data(link):
        browser= webdriver.Chrome(service=IDx_Grabber.s)
        browser.get(link)
        hasil = browser.page_source
        browser.close()
        html = Soup(hasil,'html.parser')

        return html.find('pre').text
    

    def get_data_emiten(self):
        try:
            return openfile(_FILEDATAEMITEN,'r')
        except:
            openfile(_FILEDATAEMITEN+'lengkap', 'w',IDx_Grabber.request_data(_emitenIDX_api))
            apiExtract = openfile(_FILEDATAEMITEN +'lengkap','r')

            dumplist = {
                "Kode":[],
                "Catalog":[]

            }
            for emiten in apiExtract['data']:
                kode = emiten["Code"]
                strabbv = f"{kode} - {emiten['Name']}"
                
                dumplist["Kode"].append(kode)
                dumplist["Catalog"].append(strabbv)
            
            openfile(_FILEDATAEMITEN, 'w',dumplist)
            return dumplist
         

            
        
    