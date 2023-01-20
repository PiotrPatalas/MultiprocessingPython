import math
import time
from multiprocessing.pool import Pool
import itertools
import matplotlib.pyplot as plt
import os
from PyPDF2 import PdfReader, PdfFileWriter, PdfWriter, PageRange, PdfMerger
import re
import numpy as np


def outputMatchingIndexes(res):
    filetxt = open(r"./Output/pliktxt.txt", "a")
    filetxt.writelines(str(res))
    
  
def main():
    # odczyt PDF z PyPDF2
    # otwieramy plik w trybie binarnym
    times = []  # tablica z czasami potrzebna do rysowania wykresu
    no_processes = []  # tablica z liczba procesów
    aviableCPUs = 6 # liczba dostępnych procesorów 
    # czas otwarcia pliku jest na tyle mały że nie będę go brał pod uwagę
    pdffileobj = open('Sample/sample2.pdf', 'rb')
    reader = PdfReader(pdffileobj)  # inicjalizujemy obiekt reader
    iloscStron = len(reader.pages)
    
    print("Ilosc stron: ", iloscStron)
    print("Ilosc procesorów", aviableCPUs)

    def pdfToTxt(input):
        print("Test: ", input)
        startpage = input[0][0]
        endpage = input[0][1]
        page_content = ""
        for page_number in range(startpage, endpage):
            page = reader.pages[page_number]
        page_content += page.extract_text()
        return page_content

    # dzielimy plik PDF na ilość części odpowiadajacych ilości procesów

    for CORES in range(1, aviableCPUs+1):
            no_processes.append(CORES)                                                   
    #Przygotowujemy tablice przedzialow         
            iloscProcesorow = CORES
            przedzial = iloscStron // iloscProcesorow
            listOfIntervals = []
            start = 0
            for i in range(iloscProcesorow):
                if i == iloscProcesorow -1:
                    end = iloscStron
                else:
                    end = start + przedzial
                listOfIntervals.append((start, end - 1))
                start = end
            print("Lista przedziałów: ", listOfIntervals)
            
            with Pool(processes=CORES) as pool:
                result = str(pool.map_async(pdfToTxt, listOfIntervals))
                for result in result.get():
                    print(f'Got result: {result}', flush=True)
               
        #pageContent = pdfToTxt(listOfIntervals[0], listOfIntervals[1])
        
        #test_sub = "a"
        #outputMatchingIndexes(res)
        
    
#     for page_number in range(iloscStron):
#         page = reader.pages[page_number]
#         page_content += page.extract_text()
    
    # pdfToTxt(startpage, endpage)
    # 
#     print(f"Wczytanie pliku trwało: {finish_time1 - start_time1} sekund")
#     print(f"Konwersja na txt: {finish_time2 - start_time2} sekund")
#     print(f"Wyszukiwanie trwało: {finish_time3 - start_time3} sekund")
#     drawPlots(iloscStron)


# def drawPlots(iloscStron):
#     fig = plt.figure(figsize=(15, 10))
#     plt.bar(1, 15, color='b', width=0.3)
#     # plt.bar(no_processes, times, color='b', width = 0.3)
#     plt.xlabel("Liczba procesów")
#     plt.ylabel("Czas działania [s]")
#     plt.title("Konwersja PDF o dlugosci " + str(iloscStron) + " stron do txt następnie wyszukiwanie wzorca w tekście \nZależnie od ilosci procesorów [ 1 - " + str(os.cpu_count()) + "]")
#     # plt.savefig("wzorzec_w_tekscie_["+str(lb)+", " + str(ub)+"].png")
#     plt.show()

if __name__ == "__main__":
    main()
