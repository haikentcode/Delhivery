# <@ HIOS product >
# by Hitesh kumar regar , Ashok Kumar Bhukhar ( Intern )
# mapping b/w file1,file2,file3 data column 'Vender Sku Code' and 'Product Code'
# where file1,file2,file3 are pannel file
# 
#  |Delhivery Code        | Amazon Code | Flipkart |Jabong |
#  ---------------------------------------------------------
#  |process_commmon_code  | xyzpqrstuv  | abcdefgk | hknmuy|
#

#!/usr/bin/env python

import ast
import xlsxwriter
import sys
import csv
import re
from Tkinter import *
from tkFileDialog import askopenfilename
reload(sys)

class popupWindow(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Company Name")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()

class vendor(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.ofname="output"
        self.filecompany={}
        self.pack()
        self.filelist=[] 
        self.mainDic={}  # use for stor final result e.g. process_common_code: amazon->fdffdsf,flipkart->fdfdfdf   
        self.workbook = xlsxwriter.Workbook("masterfile"+'.xlsx')
        self.worksheet = self.workbook.add_worksheet()
    def pfile(self,file):
         print "file:",file
    def GUI(self):
        Button(text='Add File', command=self.addfile).pack(fill=X)
        Button(text='Create Master File', command=self.makeMaterFile).pack(fill=X)

    
    def addfile(self):
       fname=askopenfilename()
       cname=""
       if len(fname)>0:
         self.w=popupWindow(self.master)
         self.master.wait_window(self.w.top)
         cname=self.w.value 
       self.filecompany[fname]=cname

    def makeMaterFile(self):
       for fileis,company in self.filecompany.items():
            self.hios(fileis,company)
        
       print self.mainDic.items() 
       print "file saving ......"
       self.finalXlFile()
       print "file saved"

    def hios(self,file,company):
      with open(file) as csvfile:
         sp=csv.reader(csvfile, delimiter=',', quotechar='|')
         i=0
         column={}
         try:
          for row in sp:
            if i==0:
              for clm in row:
                 column[clm]=len(column)  
              print column.items() 

            else:
              vendor_code=row[column['Vendor Sku Code']]
              product_code=row[column['Product Code']]
              #print vendor_code,product_code
              #now we decide type product
              if "Size" in column.keys():
                  self.sizeProces(product_code,vendor_code,row[column["Size"]],company)
              else:
                  self.stringProcess(product_code,vendor_code,company)    
            i+=1
         except:
           print row
           pass

    def sizeProces(self,product_code,vendor_code,Size,company):
              vendor_code=vendor_code.upper()
              vendor_code=vendor_code.replace("-","").replace("_","").replace(" ","").replace("\\","").replace("/","").replace(".","").replace(",","")
              Size=Size.upper()
              if not vendor_code.endswith(Size):
                     vendor_code=vendor_code+Size.upper()

              #further processing
              
              process_common_code=vendor_code
              self.mainData(process_common_code,company,product_code)       


    def stringProcess(self,product_code,vendor_code,company):
                    vendor_code=vendor_code.upper()
                    listw=re.split(r'[-_\s]\s*',vendor_code)
                    listw.sort()
                    process_common_code='_'.join(listw)
                    #further processing
                    self.mainData(process_common_code,company,product_code)
                    

    def mainData(self,process_common_code,company,product_code):
                       if process_common_code in self.mainDic.keys():
                              self.mainDic[process_common_code][company]=product_code
                       else:
                              self.mainDic[process_common_code]={}
                              self.mainDic[process_common_code][company]=product_code
    def finalXlFile(self):
         keycolm={}
         keycolm["Common Code"]=0
         self.worksheet.write(0,len(keycolm)-1,"Common Code")
         i=1
         for key,line in self.mainDic.items():
               self.worksheet.write(i,keycolm["Common Code"],str(key))
               for skey,sline in line.items():
                     if not skey in keycolm:
                           keycolm[skey]=len(keycolm)
                           self.worksheet.write(0,len(keycolm)-1,str(skey))
                     self.worksheet.write(i,keycolm[skey],str(sline))
               i+=1       
         self.workbook.close() 


if __name__=="__main__":
  tk=Tk()
  obj=vendor(tk)
  obj.GUI()
  obj.mainloop()
  tk.destroy()          
