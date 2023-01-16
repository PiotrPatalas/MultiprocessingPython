import math
import time
import multiprocessing
import itertools
import matplotlib.pyplot as plt
import os
from PyPDF2 import PdfReader
import re

#odczyt i wyodrębnienie tekstu z pliku PDF za pomocą biblioteki PyPDF2 - POCZĄTEK

pdffileobj = open('sample3.pdf', 'rb') # otwieramy plik w trybie binarnym 
reader = PdfReader(pdffileobj) #inicjalizujemy obiekt reader 

iloscStron = len(reader.pages)
print(iloscStron)

page_content=""                
for page_number in range(iloscStron):
    page = reader.pages[page_number]
    page_content += page.extract_text()
    
#odczyt i wyodrębnienie tekstu z pliku PDF za pomocą biblioteki PyPDF2 - KONIEC

test_sub = "a"
res = [i.start() for i in re.finditer(test_sub, page_content)]

print("String" + test_sub + "wystepuje na popzycjach" + str(res))


# filetxt=open(r"./pliktxt.txt","a")
# filetxt.writelines(page_content)


# dlt=
# plt.bar(no_processes, times, color='b', width = 0.3)
# plt.xlabel("Liczba procesów")
# plt.ylabel("Czas działania")
# plt.title("Wyszukiwanie wzorca w tekście\nZakres wartosci ["+str(lb)+", " + str(ub)+"]")
# plt.savefig("wzorzec_w_tekscie_["+str(lb)+", " + str(ub)+"].png")
# plt.show()
