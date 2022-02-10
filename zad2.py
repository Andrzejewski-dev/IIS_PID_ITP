import matplotlib.pyplot as plt
import math
import numpy as np

# wartości stałe
# Q0 = 0.2 # natezenie odpływu [m3/s]
h_0 = 0 # wartość początkowa wyskości zbiornika [m]
h_ex = 1500 # oczekiwana wysokosc w zbiorniku [m]
N = 1000 # czas trwania [s]
A = 4 # pole powierzchni podstawy zbiornika [m2]
beta = 0.25 # współczynnik wypływu [m(5/2)/s]
Tp = 4

P=Tp
I=1
D=0.3
kp = 0.01

e_ns = []

# Q_d = 


# regulacja
def regulator(h):
    return h_ex - h

# sterowanie
def sterowanie(n, e_n):
    suma = 0
    for ee in e_ns:
        suma += ee

    return kp * (e_n + ((P/I) * suma) + ((D/P) * (e_n - e_ns[n - 1])))

# wartość natęzenia dopływu
def doplyw(u_n):
    return 0 # TODO

# wartośc poziomu substancji
def poziom(u_n):
    return 0 # TODO

def loop(n, h, Q_d):
    e_n = regulator(h)
    e_ns.append(e_n)
    u_n = sterowanie(n, e_n) 

    Q_0 = beta * math.sqrt(h)
    h_delta = h_ex - h
    Q_d = (A * (h_delta / Tp)) + Q_0 


    if Q_d > 200:
        Q_d = 200
    if Q_d < 0:
        Q_d = 0

    h = ((1/A) * ((-beta * math.sqrt(h)) + Q_d) * Tp) + h

    return (h, Q_d)


def main():
    n_axis = range(N)
    h_axis = []
    Qd_axis = []  

    h = h_0 # wysokosc bieząca [m]
    Q_d = 1 # natezenie dopływu [m3/s]

    for n in n_axis:
        if n > 0:
            (h, Q_d) = loop(n, h, Q_d)
        h_axis.append(h)
        Qd_axis.append(Q_d)


    plt.plot(n_axis, h_axis)
    plt.plot(n_axis, Qd_axis)
    plt.show()

if __name__ == "__main__":
    main()
