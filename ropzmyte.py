import math
import matplotlib.pyplot as plt
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

h = ctrl.Antecedent(np.arange(0, 1500, 1), 'h')
q = ctrl.Antecedent(np.arange(0, 15, 1), 'q')
Zawor = ctrl.Consequent(np.arange(0, 17000, 1), 'Zawor')
h.automf(3)
q.automf(3)
Zawor['low'] = fuzz.trimf(Zawor.universe, [0, 0, 13000])
Zawor['medium'] = fuzz.trimf(Zawor.universe, [0, 13000, 25000])
Zawor['high'] = fuzz.trimf(Zawor.universe, [13000, 25000, 25000])
rule1 = ctrl.Rule(h['poor'] | q['poor'], Zawor['high'])
rule2 = ctrl.Rule(h['average'], Zawor['medium'])
rule3 = ctrl.Rule(h['good'] | q['good'], Zawor['low'])
Zawor_ctrl = ctrl.ControlSystem([rule1, rule2, rule3])
Q = ctrl.ControlSystemSimulation(Zawor_ctrl)



def Regulator(kp, e, Tp, Ti, Td, n):
    u = []
    for i in range(1, n):
        u0 = kp * (e[i] + (Tp / Ti) * sum(e) + (Td / Tp) * e[i] - e[i - 1])
        u.append(u0)
    # plt.plot(u)
    return u


def Zaworek(reg, n, wart_zad):
    Q = []
    for i in range(n - 1):
        Q0 = reg[i] * 0.1
        Q.append(Q0)

    # plt.plot(Q)
    return Q

def regulatorRozmyty(poziom,zawor):
    Q.input['h'] = poziom
    Q.input['q'] = zawor
    Q.compute()
    Q0=Q.output['Zawor']
    #print("Q0: "+str(Q0))
    return Q0



def obiekt(Tp, A, B, Qd, n, poj_min, wart_zad, kp, Ti, Td):
    # A-Przekroj
    # B-Beta
    # Qd-Doplyw
    h = []
    h0 = poj_min
    h1 =h0
    skok = []
    uchyb0 = 0
    uchyb = []
    u0 = 0
    u = []
    s = 0
    e = []
    Q = []

    Q1=Qd
    suma_e=0
    for i in range(n):
        # obiekt
        Qd=Q1
        sqrth0=math.sqrt(h1)
        h0 = Tp * ((1 / A) * Qd - (B / A) * sqrth0) + h1
        if(h0<0):
            h0=0
        h1=h0
        # print("H: "+str(h1))
        # print(h1)
        h.append(h0)
        s = wart_zad
        skok.append(s)
        # uchyb
        e0 = wart_zad - h0
        e.append(e0)
        suma_e +=e0
        # regulator
        u0 = kp * (e0 + (Tp / Ti) * suma_e + (Td / Tp) * e0 - e[i - 1])
        # u0=regulatorRozmyty(h0, Q1)
        # print(kp * (e0 + (Tp / Ti) ))
        # print(u0)
        u.append(u0)
        # zawor
        Q0 = (u0 / wart_zad)
        Q.append(Q0)
        Q1=Q0
    fig, (ax1, ax2) = plt.subplots(2, 1)
    ax1.plot(h)
    ax1.plot(skok)
    ax1.plot(e)
    ax1.set_xlabel('n')
    ax1.set_ylabel('Poziom substancji')

    ax1.legend(('Poziom', 'Wartość zadana', 'Uchyb'),
               loc='upper right')
    ax1.grid(True)
    ax2.grid(True)
    #ax2.plot(u)
    ax2.plot(Q)

    # plt.show()
    return h


Tp = 4
Ti = 1
Td = 0.3
przekroj = 4
beta = 0.25
doplyw = 1
liczba_probek = 1000
pojemnosc_poczatkowa = 0
wartosc_zadana = 1500
kp = 0.01

obiekt(Tp, przekroj, beta, doplyw, liczba_probek, pojemnosc_poczatkowa, wartosc_zadana, kp, Ti, Td)

plt.show()
x=input("koniec")
#Tp = 0.3
#Ti = 0.5
#Td = 0.5
#przekroj = 4
#beta = 0.25
#doplyw = 10
#liczba_probek = 50000
#pojemnosc_poczatkowa = 0
#wartosc_zadana = 1500
#kp = 0.01