import math

class PID:
    def __init__(
        self, 
        h_0, 
        h_ex, 
        N, 
        A, 
        beta, 
        Tp,
        Ti,
        Td,
        kp,
        Qd_min = 0,
        Qd_max = None
    ):
        self.h_0 = h_0
        self.h_ex = h_ex
        self.N = N
        self.A = A
        self.beta = beta
        self.Tp = Tp
        self.Ti = Ti
        self.Td = Td
        self.kp = kp
        self.Qd_min = Qd_min
        self.Qd_max = Qd_max
        self.n_axis = []
        self.h_axis = []
        self.Qd_axis = []
        self.errors = [0, ]
        self.valveeU = []
        self.valveeQd = []
        self.Qo = []
    
    def run(self):
        h = self.h_0 # wysokosc bieząca [m]
        Q_d = 0 # natezenie dopływu [m3/s]

        for n in range(0, self.N):
            if n > 0:
                (h, Q_d) = self.loop(n, h, Q_d)
            self.n_axis.append(n)
            self.h_axis.append(h)
            self.Qd_axis.append(Q_d)

    def loop(self, n, h, Q_d):
        self.errors.append((self.h_ex - h) / 10)
        self.valveeU.append(
            (self.kp * (self.errors[-1] + (self.Tp / self.Ti) * sum(
                self.errors) + (self.Td / self.Tp) * (
                                             self.errors[1] - self.errors[-1]))) / 10)

        if (self.valveeU[-1] <= self.Qd_min):
            self.valveeQd.append(self.Qd_min)
        elif (self.valveeU[-1] >= self.Qd_max):
            self.valveeQd.append(self.Qd_max)
        else:
            self.valveeQd.append(self.valveeU[-1])

        self.Qo.append(self.beta * math.sqrt(h))
        h = max(min(((-self.Qo[-1] + self.valveeQd[-1]) * self.Tp / self.A + h), 10), 0)
        Q_d = self.valveeQd[-1]

        return (h, Q_d)
