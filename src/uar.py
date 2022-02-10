import math

class UAR:
    def __init__(
        self, 
        h_0, 
        h_ex, 
        N, 
        A, 
        beta, 
        Tp,
        Qd_min = 0,
        Qd_max = None
    ):
        self.h_0 = h_0
        self.h_ex = h_ex
        self.N = N
        self.A = A
        self.beta = beta
        self.Tp = Tp
        self.Qd_min = Qd_min
        self.Qd_max = Qd_max
        self.n_axis = []
        self.h_axis = []
        self.Qd_axis = []
    
    def run(self):
        self.n_axis = []
        self.h_axis = []
        self.Qd_axis = []  

        h = self.h_0 # wysokosc bieząca [m]
        Q_d = 0 # natezenie dopływu [m3/s]

        for n in range(self.N):
            if n > 0:
                (h, Q_d) = self.loop(n, h, Q_d)
            self.n_axis.append(n)
            self.h_axis.append(h)
            self.Qd_axis.append(Q_d)

    def loop(self, n, h, Q_d):
        Q_0 = self.beta * math.sqrt(h)
        
        h_next = ((1/self.A) * ((-self.beta * math.sqrt(h)) + Q_d) * self.Tp) + h
        h_delta = self.h_ex - h
        Q_d = (self.A * (h_delta / self.Tp)) + Q_0

        if self.Qd_max is not None and Q_d > self.Qd_max:
            Q_d = self.Qd_max
        if self.Qd_min is not None and Q_d < self.Qd_min:
            Q_d = self.Qd_min

        h = h_next

        return (h, Q_d)
