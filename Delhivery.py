
#HIOS DATA Processing Product
#by:hitesh kumar regar


import ast
import xlsxwriter
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
workbook = xlsxwriter.Workbook('data.xlsx')
worksheet = workbook.add_worksheet()

#worksheet.write(row, col,key) in excl sheet write valye(key) at row,col position

keycol={
"uniq_id" :1,
"product_name" :2,
"product_url" :3,
"product_category" :4,
"product_sub_category" :5,
"upc" :6,
"brand" : 7,
"image" :8,
"discounted_price":9,
"retail_price":10,
"product_review_count":11,
"product_rating":12,
"ASIN":13,
"product_specifications":14,
"description":15
}

for key,val in keycol.items():
  worksheet.write(0,val-1,key)

def addItem(key,val,row,col):

  val=str(val).replace("\n"," ").replace("  "," ")
  if str(key)=="product_specifications" :
      psd=ast.literal_eval(str(val))
      list=psd.items()
      psd2=list[0][1]
      strr=""
      for a in psd2:
          if(a['key']=='ASIN'):
              worksheet.write(row,keycol[str(a['key'])]-1,a['value'])
          else:
              strr+=str(a['key']+":"+a['value']+",")
      worksheet.write(row,keycol[str(key)]-1,strr)
  else:
      worksheet.write(row,keycol[str(key)]-1,val)


def addTosheet(dic,r):
  c=0
  for key,val in dic.items():
      addItem(key,val,r,c)
      c=c+1


fp = open("data.txt")
r=0
errors=""
for i, line in enumerate(fp):
    try:
          print i
          if i==30600: # DUE TO EXCEL FILE LIMTED ROW
             break;
  	  r=r+1
  	  if len(line)>10:
            line=line.replace("\"\"","\"")
            line=line.replace("\"{","{")
            line=line.replace("}\"","}")
  	    dic=ast.literal_eval(line)
  	    addTosheet(dic,r)
    except:
      errors="error in line->"+str(i)+","
      pass

print "file saving....."
workbook.close()
print "ERROR LOGS:",errors






