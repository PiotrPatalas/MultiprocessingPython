import math
import time
import multiprocessing
import itertools
import matplotlib.pyplot as plt
import os
from PyPDF2 import PdfReader
import re


def main():
    # odczyt PDF z PyPDF2
    start_time1 = time.perf_counter()
    # otwieramy plik w trybie binarnym
    pdffileobj = open('Sample/sample4.pdf', 'rb')
    finish_time1 = time.perf_counter()
    reader = PdfReader(pdffileobj)  # inicjalizujemy obiekt reader

    
    iloscStron = len(reader.pages)
    print("Ilosc stron: ", iloscStron)
    print("Ilosc procesorów", os.cpu_count())

    page_content = ""
    start_time2 = time.perf_counter()
    for page_number in range(iloscStron):
        page = reader.pages[page_number]
        page_content += page.extract_text()
    finish_time2 = time.perf_counter()
    
    

    test_sub = "or"
    start_time3 = time.perf_counter()
    res = [i.start() for i in re.finditer(test_sub, page_content)]
    finish_time3 = time.perf_counter()

    outputMatchingIndexes(res)
    print(f"Wczytanie pliku trwało: {finish_time1 - start_time1} sekund")
    print(f"Konwersja na txt: {finish_time2 - start_time2} sekund")
    print(f"Wyszukiwanie trwało: {finish_time3 - start_time3} sekund")
    drawPlots(iloscStron)

def pdfToText():
    


def drawPlots(iloscStron):
    fig = plt.figure(figsize=(15, 10))
    plt.bar(1, 15, color='b', width=0.3)
    # plt.bar(no_processes, times, color='b', width = 0.3)
    plt.xlabel("Liczba procesów")
    plt.ylabel("Czas działania [s]")
    plt.title("Konwersja PDF o dlugosci " + str(iloscStron) + " stron do txt następnie wyszukiwanie wzorca w tekście \nZależnie od ilosci procesorów [ 1 - " + str(os.cpu_count()) + "]")
    # plt.savefig("wzorzec_w_tekscie_["+str(lb)+", " + str(ub)+"].png")
    plt.show()


def outputMatchingIndexes(res):
    filetxt = open(r"./Output/pliktxt.txt", "a")
    filetxt.writelines(str(res))


if __name__ == "__main__":
    main()
