from random import randint

import numpy
from flask import Flask, render_template, request

app = Flask(__name__)

do_zapisu = [""]


@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('file.html')


@app.route('/file', methods=['POST'])
def plik_otworz():
    plik = request.form['file']

    with open(plik, "r") as fin:
        nazwa = fin.readline()

    with open(plik, 'r') as fin:
        data = fin.read().splitlines(True)
    with open(plik, 'w') as fout:
        fout.writelines(data[1:])

    plik_save = plik.replace('.txt','')
    stan_gry = [[krok for krok in line.strip()] for line in open(plik_save + "_save.txt", "r")]

    data = [[krok for krok in line.strip()] for line in open(plik, "r")]
    do_zapisu[0] = przepisz(data)
    data = podpowiedz(data)

    return render_template('result.html', val=data, h=len(data), w=len(data[0]), gracz = nazwa,save = stan_gry,s=len(stan_gry),k=len(stan_gry[0]))

def wyswietl_tablice(tablica_wejsciowa):
    for i in range(len(tablica_wejsciowa)):
        print("|", end='')
        for j in range(len(tablica_wejsciowa[0])):
            print(tablica_wejsciowa[i][j], "|", end = '')
        print("")

def przepisz(tablica_wejsciowa):
    x = len(tablica_wejsciowa)
    y = len(tablica_wejsciowa[0])
    podpowiedzi = numpy.empty([x, y], dtype=str)

    for i in range(x):
        for j in range(y):
            liczba_dookola = 0

            if tablica_wejsciowa[i][j] == "1":
                liczba_dookola += 1
            if tablica_wejsciowa[i][j] == "0":
                liczba_dookola += 0


            podpowiedzi[i][j] = liczba_dookola

    return podpowiedzi


@app.route('/sprawdz', methods=['POST'])
def sprawdz():

    return render_template('fail.html')

@app.route('/save', methods=['POST'])
def zapisz():
    plik = request.form['save']
    plik_gracz = plik.replace('.txt','')
    plik_save = plik_gracz + "_save.txt"
    if plik:
        try:
            f = open(plik, "w")

            f.write(plik_gracz+"\n")
            for i in range(len(do_zapisu[0])):
                line = ""
                for j in range(len(do_zapisu[0][i])):
                    line += do_zapisu[0][i][j]
                line += "\n"
                f.write(line)
            f.close()
        except:
            pass

    plik_zapis = request.form['txt']
    print(plik_zapis)
    if plik_save:
        try:
            f = open(plik_save, "w")
            f.write(plik_zapis)
            f.close()
        except:
            pass

    return render_template('file.html')


def podpowiedz(tablica_wejsciowa):

    x = len(tablica_wejsciowa)
    y = len(tablica_wejsciowa[0])
    podpowiedzi = numpy.empty([x, y], dtype=str)


    for i in range(x):
        for j in range(y):
            liczba_dookola = 0
            for k in range(-1, 2):
                for l in range(-1, 2):

                    try:
                        if tablica_wejsciowa[i + k][j + l] == "1":
                            liczba_dookola += 1

                    except IndexError:
                        pass


            podpowiedzi[i][j] = liczba_dookola


    return podpowiedzi


if __name__ == "__main__":
    app.run(debug=True)
