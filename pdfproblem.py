import pyPdf  
def getPDFContent(path):
    content = ""
    num_pages = 10
    p = file(path, "rb")
    pdf = pyPdf.PdfFileReader(p)
    for i in range(0, num_pages):
        content += pdf.getPage(i).extractText() + "\n"
    content = "______________________".join(content.replace(u"\xa0", " ").strip().split())     
    return content 

if __name__=="__main__":
    print getPDFContent("demo.pdf")
