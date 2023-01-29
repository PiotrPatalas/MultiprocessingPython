import time
from multiprocessing.pool import Pool
from multiprocessing.process import Process
import matplotlib.pyplot as plt
import os
from PyPDF2 import PdfReader
import re
import numpy as np


def outputMatchingIndexes(res):
    filetxt = open(r"./Output/pliktxt.txt", "a")
    filetxt.writelines(str(res))


def splitString(string, n):
    # split the string into words
    words = string.split()
    # calculate the number of words in each part
    words_per_part = len(words) / n
    # calculate the number of characters in each part
    chars_per_part = len(string) / n
    # initialize the list of tuples
    parts = []
    # initialize the number of words in the current part
    words_in_part = 0
    # initialize the number of characters in the current part
    chars_in_part = 0
    # initialize the current part
    part = ''
    # loop through the words
    for word in words:
        # add the word to the current part
        part += word + ' '
        # increase the number of words in the current part
        words_in_part += 1
        # increase the number of characters in the current part
        chars_in_part += len(word) + 1
        # if the number of words in the current part is greater than the number of words in each part
        if words_in_part >= words_per_part:
            # add the current part to the list of tuples
            parts.append((part, chars_in_part))
            # reset the number of words in the current part
            words_in_part = 0
            # reset the number of characters in the current part
            chars_in_part = 0
            # reset the current part
            part = ''
    # if the current part is not empty
    if part:
        # add the current part to the list of tuples
        parts.append((part, chars_in_part))
    # return the list of tuples
    return parts


def bruteForce(text, pattern):
    # initialize the list of indexes
    indexes = []
    # loop through the string
    for i in range(len(text)):
        # loop through the pattern
        for j in range(len(pattern)):
            # if the characters do not match
            if text[i + j] != pattern[j]:
                # break out of the inner loop
                break
            # if the characters match and we have reached the end of the pattern
            if j == len(pattern) - 1:
                # append the index to the list of indexes
                indexes.append(i)
    # return the list of indexes
    return indexes


def findStringInPart(test_sub):
    test_sub_text = test_sub[0]
    pattern = 'Python'
    t1 = time.time()
    bruteForce(test_sub_text, pattern)
    t2 = time.time()
    return (t2-t1)


def drawPlots(no_processes, times, iloscStron):
    fig = plt.figure(figsize=(15, 10))
    plt.bar(no_processes, times, color="yellowgreen", width=0.3)
    plt.xlabel("Liczba procesów")
    plt.ylabel("Czas działania [s]")
    plt.title("Konwersja PDF o dlugosci " + str(iloscStron) +
              " stron do txt następnie wyszukiwanie wzorca w tekście \nZależnie od ilosci procesorów [ 1 - " + str(os.cpu_count()) + "]")
    plt.savefig("wzorzec_w_tekscie_.png")

    plt.bar_label(plt.bar(no_processes, times,
                  color="yellowgreen", width=0.3), padding=3)

    plt.show()
    print("Wykres został zapisany do pliku wzorzec_w_tekscie_.png")


def main():
    # odczyt PDF z PyPDF2
    # otwieramy plik w trybie binarnym
    times = []  # tablica z czasami potrzebna do rysowania wykresu
    no_processes = []  # tablica z liczba procesów
    aviableCPUs = 6  # liczba dostępnych procesorów
    # czas otwarcia pliku jest na tyle mały że nie będę go brał pod uwagę
    pdffileobj = open('Sample/sample2.pdf', 'rb')
    reader = PdfReader(pdffileobj)  # inicjalizujemy obiekt reader
    iloscStron = len(reader.pages)

    print("Ilosc stron: ", iloscStron)
    print("Dostępna liczba procesorów", aviableCPUs)

    # przerabiamy plik na stringa
    page_content = ""
    t1 = time.time()
    for page_number in range(0, iloscStron):
        page = reader.pages[page_number]
        page_content += page.extract_text()
    print("Czas przerabiania: ", time.time()-t1)
    print('\n')
    print('\n')

    for CORES in range(aviableCPUs, 0, -1):
        no_processes.append(CORES)
        sst1 = time.time()
        listOfStrings = splitString(page_content, CORES)
        sst2 = time.time()
        with Pool(processes=CORES) as pool:
            t1 = time.time()
            results = pool.map_async(findStringInPart, listOfStrings)

            #print("Czasy szukania: ", results)
            for result in results.get():
                print(f'Got result: {result}', flush=True)
            t2 = time.time()
        print("Liczba procesów:", CORES, "\nCzas:", t2 - t1, "\n")
        times.append(t2 - t1)

    print("Tablica liczba procesów: ", no_processes)
    drawPlots(no_processes, times, iloscStron)

    # #Przygotowujemy tablice przedzialow
    #         iloscProcesorow = CORES
    #         przedzial = iloscStron // iloscProcesorow
    #         listOfIntervals = []
    #         start = 0
    #         for i in range(iloscProcesorow):
    #             if i == iloscProcesorow -1:
    #                 end = iloscStron
    #             else:
    #                 end = start + przedzial
    #             listOfIntervals.append((start, end - 1))
    #             start = end
    #         print("Lista przedziałów: ", listOfIntervals)

    #     print(f"Wczytanie pliku trwało: {finish_time1 - start_time1} sekund")
    #     print(f"Konwersja na txt: {finish_time2 - start_time2} sekund")
    #     print(f"Wyszukiwanie trwało: {finish_time3 - start_time3} sekund")


if __name__ == "__main__":
    main()
