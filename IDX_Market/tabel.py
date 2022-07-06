import tkinter as tk
from tkinter import ttk

class Tabel(tk.Toplevel):
    
    def __init__(self,parent,dataframe):
        self.dataframe = dataframe
        super().__init__(parent)
        self.geometry('500x300')
        self.tipeoutput = tk.StringVar()
        self.resizable(False,False)
        self.buat_layout()
    
    
    def buat_tabel(self,root,dataframe):
        tbl = ttk.Treeview(root,
        column=tuple(dataframe.columns),
        show='headings')
        
        size = len(dataframe.columns)
        for i,column in enumerate(dataframe.columns):
            tbl.column(i,anchor= 'center', width=int(450/size), minwidth=100,stretch=True)

        for col in dataframe.columns:
            tbl.heading(col,text=col)
        
        for index,values in dataframe.iterrows():
            a = list(values)
            tbl.insert("", tk.END,values=a)
        return tbl
    def buat_layout(self):

        tabelframe = tk.Frame(self)
        tabelframe.pack(padx=5,pady=5)
        tabelframe.pack_propagate(0)


        btnframe = tk.Frame(self,width=300,height=100)
        btnframe.columnconfigure(1,weight=4)
        btnframe.columnconfigure(2,weight=2)
        btnframe.pack_propagate(0)
        btnframe.grid_propagate(0)
        btnframe.pack()

        #BuatTabel
        tabel = self.buat_tabel(tabelframe, self.dataframe)
        scrollbarH = ttk.Scrollbar(tabelframe, orient=tk.HORIZONTAL)
        scrollbarV = ttk.Scrollbar(tabelframe, orient=tk.VERTICAL, command=tabel.yview)
        tabel.grid(row=0,column=0,sticky = tk.NSEW)
        

        scrollbarV.grid(column=1,row=0,sticky=tk.NS)
        scrollbarH.grid(row=1,column=0,sticky = (tk.N,tk.S,tk.W,tk.E))    
        scrollbarH.configure(command=tabel.xview)    
        tabel.configure(
            xscroll = scrollbarH.set,
            yscroll = scrollbarV.set,
            xscrollcommand = scrollbarH.set
        )
        
        
        

        #Buat Tombol
        values = ['CSV','Excel','SQL','JSON']
        messagebox = ttk.Combobox(btnframe,values=values)
        messagebox.grid(
            row=0,
            column=1,
            padx=5,
            pady=5
        )

        savebtn = ttk.Button(btnframe,text='Simpan')
        savebtn.grid(
            row=0,
            column=2,
            padx=5,
            pady=5,
            ipady=5
        )

        
        