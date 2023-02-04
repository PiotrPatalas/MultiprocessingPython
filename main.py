import time
import multiprocessing
import matplotlib.pyplot as plt
import os
from PyPDF2 import PdfReader


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
    indexes = []
    for i in range(len(text)):
        for j in range(len(pattern)):
            if text[i + j] != pattern[j]:
                break
            if j == len(pattern) - 1:
                indexes.append(i)
    return indexes


def findStringInPart(test_sub):
    test_sub_text = test_sub[0]
    pattern = 'Jezus'
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
    pdffileobj = open('Sample/bibliax2.pdf', 'rb')
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
        print("Czas dzielenie stringa", sst2 - sst1)
        t1 = time.time()

        for i in range(CORES-1, -1, -1):
            p = [multiprocessing.Process(
                target=findStringInPart, args=(listOfStrings[i],))]
        for i in p:
            i.start()
        for i in p:
            i.join()
        t2 = time.time()
        print("Liczba procesów:", CORES, "\nCzas:", t2 - t1, "\n")
        times.append(t2 - t1)

    drawPlots(no_processes, times, iloscStron)


if __name__ == "__main__":
    main()
