import matplotlib.pyplot as plt
import math

# wartości stałe
# Q0 = 0.2 # natezenie odpływu [m3/s]
h_0 = 0 # wartość początkowa wyskości zbiornika [m]
h_ex = 2 # oczekiwana wysokosc w zbiorniku [m]
N = 120 # czas trwania [s]
A = 4 # pole powierzchni podstawy zbiornika [m2]
beta = 1 # współczynnik wypływu [m(5/2)/s]
Tp = 1

# Q_d = 


# regulacja
def regulator(h):
    return h_ex - h

# sterowanie
def sterowanie(e_n):
    return 0 # TODO

# wartość natęzenia dopływu
def doplyw(u_n):
    return 0 # TODO

# wartośc poziomu substancji
def poziom(u_n):
    return 0 # TODO

def loop(n, h, Q_d):
    # e_n = regulator(h)
    # u_n = sterowanie(e_n) 
    # Q_d = doplyw(u_n) 
    # h = poziom(Q_d) 


    # h_delta = h_ex - h
    Q_0 = beta * math.sqrt(h)
    
    h_next = ((1/A) * ((-beta * math.sqrt(h)) + Q_d) * Tp) + h
    h_delta = h_ex - h
    Q_d = (A * (h_delta / Tp)) + Q_0

    if Q_d > 2:
        Q_d = 2
    if Q_d < 0:
        Q_d = 0

    h = h_next
    # (A * h_delta)/Tp = Q_d - Q_0

    return (h, Q_d)


def main():
    n_axis = range(N)
    h_axis = []
    Qd_axis = []  

    h = h_0 # wysokosc bieząca [m]
    Q_d = 0 # natezenie dopływu [m3/s]

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
