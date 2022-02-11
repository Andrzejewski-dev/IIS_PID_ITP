import math
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import numpy as np
import matplotlib.pyplot as plt

class FPID:
    def __init__(
        self,
        h_0, 
        h_ex, 
        N, 
        A, 
        beta,
        Tp,
        Td,
        kp,
        Qd_min = 0,
        Qd_max = None
    ) -> None:
        self.N = N
        self.beta = beta
        self.Tp = Tp
        self.h_0 = h_0
        self.h_ex = h_ex
        self.A = A
        self.Td = Td
        self.kp = kp
        self.Qd_min = Qd_min
        self.Qd_max = Qd_max
        self.errors = [0, ]
        self.valveeU = [0.1, ]
        self.valveeQd = [0, ]
        self.Qo = []
        self.h_axis = [0, ]
        self.k_e = []
        self.k_ce = []
        self.k_u = []
        self.ins = ['DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD']
        self.outs = ['BDU', 'DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD', 'BDD']
        self.pid_y = [[], [], [], [], []]
        self.n_axis = [0, ]

        rules = self.setRules()
        cu_ctrl = ctrl.ControlSystem(rules)
        reg_cu = ctrl.ControlSystemSimulation(cu_ctrl)
        temp = [0]
        self.pid_y[0].append(0)
        self.pid_y[1].append(self.h_axis[0])
        self.pid_y[2].append(self.valveeQd[0])
        self.pid_y[3].append((self.beta) * (math.sqrt(self.h_axis[0])))
        self.pid_y[4].append(self.h_ex)
        e_delay = 0
        self.valveeU = self.valveeU

        for x in range(1, self.N):
            self.n_axis.append(self.Tp * x)
            self.k_e.append(self.kp / self.valveeU[-1])
            self.k_ce.append(
                (self.Td / self.Tp) / self.valveeU[-1])

            e = self.h_ex - self.pid_y[1][x - 1]
            ke = e * (1 / self.k_e[-1])
            temp.append(ke)
            if e > 1:
                e = 1
            elif e < -1:
                e = -1

            ce = e - e_delay
            ce *= (1 / self.Tp)
            ce *= (1 / self.k_ce[-1])
            if ce > 1:
                ce = 1
            elif ce < -1:
                ce = -1

            reg_cu.input['e'] = e
            reg_cu.input['ce'] = ce
            reg_cu.compute()
            cu = reg_cu.output['cu']
            self.valveeU.append(cu * self.Tp + self.valveeU[-1])

            self.valveeQd.append(0)
            self.valveeQd[x] = self.valveeU[1] * self.valveeU[-1]

            if (self.valveeQd[x] > self.Qd_max):
                self.valveeQd[x] = self.Qd_max
            elif (self.valveeQd[x] < self.Qd_min):
                self.valveeQd[x] = self.Qd_min

            self.pid_y[0].append((x) * self.Tp)
            self.pid_y[2].append(self.valveeQd[x])
            self.pid_y[3].append(self.beta * (math.sqrt(self.pid_y[1][x - 1])))
            self.pid_y[1].append(((self.pid_y[2][x] - self.pid_y[3][x]) * self.Tp) / self.A + self.pid_y[1][x - 1])
            self.pid_y[4].append(self.h_ex)
            self.h_axis.append(self.pid_y[1][-1])

            e_delay = e
        
    def setRules(self):
        self.e = ctrl.Antecedent(np.arange(-1, 1, 0.01), 'e')
        self.ce = ctrl.Antecedent(np.arange(-1, 1, 0.01), 'ce')
        self.cu = ctrl.Consequent(np.arange(-1, 1, 0.01), 'cu')

        self.e = {
            'DU': fuzz.trimf(self.e.universe, [-1.3, -1, -0.667]),
            'SU': fuzz.trimf(self.e.universe, [-1, -0.667, -0.333]),
            'MU': fuzz.trimf(self.e.universe, [-0.667, -0.333, 0.0]),
            'Z': fuzz.trimf(self.e.universe, [-0.333, 0.0, 0.333]),
            'MD': fuzz.trimf(self.e.universe, [0.0, 0.333, 0.667]),
            'SD': fuzz.trimf(self.e.universe, [0.333, 0.667, 1]),
            'DD': fuzz.trimf(self.e.universe, [0.667, 1, 1.33])
        }

        self.ce = {
            'DU': fuzz.trimf(self.ce.universe, [-1.3, -1, -0.667]),
            'SU': fuzz.trimf(self.ce.universe, [-1, -0.667, -0.333]),
            'MU': fuzz.trimf(self.ce.universe, [-0.667, -0.333, 0.0]),
            'Z': fuzz.trimf(self.ce.universe, [-0.333, 0.0, 0.333]),
            'MD': fuzz.trimf(self.ce.universe, [0.0, 0.333, 0.667]),
            'SD': fuzz.trimf(self.ce.universe, [0.333, 0.667, 1]),
            'DD': fuzz.trimf(self.ce.universe, [0.667, 1, 1.33])
        }
        
        self.cu = {
            'BDU': fuzz.trimf(self.cu.universe, [-1.25, -1, -0.75]),
            'DU': fuzz.trimf(self.cu.universe, [-1, -0.75, -0.5]),
            'SU': fuzz.trimf(self.cu.universe, [-0.75, -0.5, -0.25]),
            'MU': fuzz.trimf(self.cu.universe, [-0.5, -0.25, 0]),
            'Z': fuzz.trimf(self.cu.universe, [-0.25, 0.0, 0.25]),
            'MD': fuzz.trimf(self.cu.universe, [0, 0.25, 0.5]),
            'SD': fuzz.trimf(self.cu.universe, [0.25, 0.5, 0.75]),
            'DD': fuzz.trimf(self.cu.universe, [0.5, 0.75, 1]),
            'BDD': fuzz.trimf(self.cu.universe, [0.75, 1, 1.25])
        }

        rules = [
            ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[0]], self.cu[self.outs[0]]),
            ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[0]], self.cu[self.outs[0]]),
            ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[1]], self.cu[self.outs[0]]),
            ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[1]], self.cu[self.outs[0]]),
            ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[0]], self.cu[self.outs[0]]),
            ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[2]], self.cu[self.outs[0]]),
            ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[0]], self.cu[self.outs[1]]),
            ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[1]], self.cu[self.outs[1]]),
            ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[2]], self.cu[self.outs[1]]),
            ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[3]], self.cu[self.outs[1]]),
            ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[4]], self.cu[self.outs[2]]),
            ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[3]], self.cu[self.outs[2]]),
            ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[2]], self.cu[self.outs[2]]),
            ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[1]], self.cu[self.outs[2]]),
            ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[0]], self.cu[self.outs[2]]),
            ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[0]], self.cu[self.outs[3]]),
            ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[1]], self.cu[self.outs[3]]),
            ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[2]], self.cu[self.outs[3]]),
            ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[3]], self.cu[self.outs[3]]),
            ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[4]], self.cu[self.outs[3]]),
            ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[5]], self.cu[self.outs[3]]),
            ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[6]], self.cu[self.outs[4]]),
            ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[5]], self.cu[self.outs[4]]),
            ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[4]], self.cu[self.outs[4]]),
            ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[3]], self.cu[self.outs[4]]),
            ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[2]], self.cu[self.outs[4]]),
            ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[1]], self.cu[self.outs[4]]),
            ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[0]], self.cu[self.outs[4]]),
            ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[6]], self.cu[self.outs[5]]),
            ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[5]], self.cu[self.outs[5]]),
            ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[4]], self.cu[self.outs[5]]),
            ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[3]], self.cu[self.outs[5]]),
            ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[2]], self.cu[self.outs[5]]),
            ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[1]], self.cu[self.outs[5]]),
            ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[2]], self.cu[self.outs[6]]),
            ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[3]], self.cu[self.outs[6]]),
            ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[4]], self.cu[self.outs[6]]),
            ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[5]], self.cu[self.outs[6]]),
            ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[6]], self.cu[self.outs[6]]),
            ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[6]], self.cu[self.outs[7]]),
            ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[5]], self.cu[self.outs[7]]),
            ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[4]], self.cu[self.outs[7]]),
            ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[3]], self.cu[self.outs[7]]),
            ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[4]], self.cu[self.outs[8]]),
            ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[5]], self.cu[self.outs[8]]),
            ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[6]], self.cu[self.outs[8]]),
            ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[5]], self.cu[self.outs[8]]),
            ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[6]], self.cu[self.outs[8]]),
            ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[6]], self.cu[self.outs[8]]),
        ]
     
        return rules
        