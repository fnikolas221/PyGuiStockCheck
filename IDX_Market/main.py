from CONFIG import ttk,tk,os,PATH,simpledialog
from combobox import AutocompleteCombobox
from grabber import IDx_Grabber,openfile
from tabel import Tabel
import datetime
from pandas import DataFrame as DF

class Logs:
    LOGSPATH = PATH+"/output/logs/"
    def __init__(self):
        self.today = datetime.datetime.now() #DatetTimeObj
        self.STR_TODAY = datetime.datetime.strftime(self.today,"%Y-%m-%d")
        self.logs = {}
        self.SavePath = Logs.LOGSPATH+self.STR_TODAY+"/"
        try:
            self.actionLOGS = openfile('actions','r',SAVEPATH=Logs.LOGSPATH)
        except:
            self.actionLOGS = {
                "DateTime":[],
                "Action":[]
            }
            openfile('actions', 'w',self.actionLOGS,Logs.LOGSPATH)
    
    def _update(self):
        self.today = datetime.datetime.now() #DatetTimeObj
        self.STR_TODAY = datetime.datetime.strftime(self.today,"%Y-%m-%d")
        openfile('actions', 'w',self.actionLOGS,Logs.LOGSPATH)
    def writeAction(self,action):
        self._update()
        self.actionLOGS["DateTime"].append(self.today.isoformat())
        self.actionLOGS["Action"].append(action)

    def writeLogs(self,code,dataframe,jsonresult):
        self._update()
        try:
            self.logs = self.getLogs()
            self.logs["DateTime Access"].append(self.today.isoformat())
            self.logs["Kode Emiten"].append(code)
            self.logs["Banyak Hari"].append(int(dataframe.size))
        except:
            self.logs = {
                "DateTime Access":[self.today.isoformat()],
                "Kode Emiten":[code],
                "Banyak Hari":[int(dataframe.size)]
            }

        
        if not os.path.isdir(self.SavePath):
            os.mkdir(self.SavePath)

        openfile('logs', 'w',data=self.logs)
        openfile(code, 'w',data=jsonresult,SAVEPATH=self.SavePath)

    def getActionLogs(self):
        return openfile('actions','r',SAVEPATH=Logs.LOGSPATH)
    def getLogs(self):
        return openfile('logs', 'r')

    def get_emitenLogs(self,code):
        try:
            return openfile(code, 'r',SAVEPATH=self.SavePath)
        except:
            return None  
#Normal function
def to_dataframe(dictionary):
    data = DF(dictionary)
    return data

#Instantiate
LogsApp = Logs()

class Program(tk.Tk):

    def __init__(self,listemiten):
        super().__init__()
        self._listemiten = listemiten
        self.EMITENVAL = tk.StringVar()
        self.title("Pengecek Saham Harian")
        self.geometry('600x300')
        self.resizable(False,False)
        self.create_app()

    def _createtable(self,dataframe):
        if dataframe is not None:
            tabel = Tabel(self, dataframe)

    def getStock(self):
        var = str(self.EMITENVAL.get())
        if var in ['',None]:
            tk.messagebox.showerror(
                title='Emiten Kosong',
                message='Pilih Dulu Emitennya apa')
            return None

        banyakHari = simpledialog.askinteger(
            'Banyak Hari', 
            "Berapa Banyak Hari Mau Ditampilkan",
            parent=self,
            minvalue=1,
            maxvalue=100)

        code = var[:var.find("-")].strip()
        
        
        datapool = IDx_Grabber.get_history_emiten(
            code,
            typeoutput =('json','dframe'),
            duration = banyakHari,
            oldData= LogsApp.get_emitenLogs(code)
            )
        
        dframe = datapool[1]

        LogsApp.writeAction("Mendapatkan data saham dari "+code)
        LogsApp.writeLogs(code, dframe, datapool[0])
        
        return dframe
    def getLogs(self):
        dataframe = to_dataframe(LogsApp.getActionLogs())
        return dataframe
    def create_app(self):
        frame1 = tk.Frame(self,height=50,width=300)
        frame1.columnconfigure(0,weight=1)
        frame1.columnconfigure(1,weight=3)
        frame1.pack(fill=tk.BOTH,ipady=5,pady=20)
        frame1.pack_propagate(0)
        frame1.grid_propagate(0)

        frame2 = tk.Frame(self,height=550,width=300)
        frame2.columnconfigure(0,weight=2)
        frame2.columnconfigure(1,weight=4)
        frame2.columnconfigure(2,weight=2)
        frame2.pack(fill=tk.BOTH)
        frame2.pack_propagate(0)
        frame2.grid_propagate(0)        

        #Judul
        judul = ttk.Label(
            frame1,
            text='IDX STOCK GRABBER',
            font=('Helvetica',18)
            )
        judul.grid(
            column =1,
            row = 0,
            sticky= tk.NW
        )
        #Membuat Button Logs
        logsBtn = ttk.Button(frame1,text="Logs")
        logsBtn.grid(row=0,
            column=0,
            ipadx=3,
            padx=30,
            ipady=3,
            sticky=tk.SW
        )

        logsBtn.bind(
            '<Button-1>',
            lambda event : self._createtable(self.getLogs())
        )
        #Membuat Entry

        box = AutocompleteCombobox(frame2,width=40,textvariable=self.EMITENVAL)
        box.set_completion_list(self._listemiten)
        box.grid(
            padx=100,
            column=1,
            row=0,
            sticky=tk.N
        )
        
        #Membuat Button Cari
        caribtn = ttk.Button(frame2,text='Cari')
        caribtn.bind(
            '<Button-1>',
            lambda event: self._createtable(self.getStock())
            )
        caribtn.grid(
            ipadx=3,
            ipady=8,
            row = 1,
            column=1,
            pady=40,
            sticky=tk.N            
        )
        pass

if __name__ == '__main__':
    print("hello")
    stock = IDx_Grabber()
    app = Program(stock.emitenCatalog['Catalog'])
    
    app.mainloop()
