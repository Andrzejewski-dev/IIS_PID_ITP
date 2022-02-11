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
        self.defE = {
            'DU': [-1.3, -1, -0.667],
            'SU': [-1, -0.667, -0.333],
            'MU': [-0.667, -0.333, 0.0],
            'Z': [-0.333, 0.0, 0.333],
            'MD': [0.0, 0.333, 0.667],
            'SD': [0.333, 0.667, 1],
            'DD': [0.667, 1, 1.33]
        }
        self.defCe = {
            'DU': [-1.3, -1, -0.667],
            'SU': [-1, -0.667, -0.333],
            'MU': [-0.667, -0.333, 0.0],
            'Z': [-0.333, 0.0, 0.333],
            'MD': [0.0, 0.333, 0.667],
            'SD': [0.333, 0.667, 1],
            'DD': [0.667, 1, 1.33]
        }
        self.defCu = {
            'BDU': [-1.25, -1, -0.75],
            'DU': [-1, -0.75, -0.5],
            'SU': [-0.75, -0.5, -0.25],
            'MU': [-0.5, -0.25, 0],
            'Z': [-0.25, 0.0, 0.25],
            'MD': [0, 0.25, 0.5],
            'SD': [0.25, 0.5, 0.75],
            'DD': [0.5, 0.75, 1],
            'BDD': [0.75, 1, 1.25]
        }
        self.defRules = {
            'BDU': [
                ('DU', 'DU'),
                ('SU', 'DU'),
                ('DU', 'SU'),
                ('SU', 'SU'),
                ('MU', 'DU'),
                ('DU', 'MU')
            ],
            'DU': [
                ('Z', 'DU'),
                ('MU', 'SU'),
                ('SU', 'MU'),
                ('DU', 'Z')
            ],
            'SU': [
                ('DU', 'MD'),
                ('SU', 'Z'),
                ('MU', 'MU'),
                ('Z', 'SU'),
                ('MD', 'DU')
            ],
            'MU': [
                ('SD', 'DU'),
                ('MD', 'SU'),
                ('Z', 'MU'),
                ('MU', 'Z'),
                ('SU', 'MD'),
                ('DU', 'SD')
            ],
            'Z': [
                ('DU', 'DD'),
                ('SU', 'SD'),
                ('MU', 'MD'),
                ('Z', 'Z'),
                ('MD', 'MU'),
                ('SD', 'SU'),
                ('DD', 'DU')
            ],
            'MD': [
                ('SU', 'DD'),
                ('MU', 'SD'),
                ('Z', 'MD'),
                ('MD', 'Z'),
                ('SD', 'MU'),
                ('DD', 'SU')
            ],
            'SD': [
                ('DD', 'MU'),
                ('SD', 'Z'),
                ('MD', 'MD'),
                ('Z', 'SD'),
                ('MU', 'DD')
            ],
            'DD': [
                ('Z', 'DD'),
                ('MD', 'SD'),
                ('SD', 'MD'),
                ('DD', 'Z')
            ],
            'BDD': [
                ('DD', 'MD'),
                ('SD', 'SD'),
                ('MD', 'DD'),
                ('DD', 'SD'),
                ('SD', 'DD'),
                ('DD', 'DD')
            ]
        }
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

        for key, value in self.defE.items():
            self.e[key] = fuzz.trimf(self.e.universe, value)

        for key, value in self.defCe.items():
            self.ce[key] = fuzz.trimf(self.ce.universe, value)
        
        
        for key, value in self.defCu.items():
            self.cu[key] = fuzz.trimf(self.cu.universe, value)
            
        rules = []
        for cu, e_ces in self.defRules.items():
            for e_ce in e_ces:
                rules.append(ctrl.Rule(self.e[e_ce[0]] & self.ce[e_ce[1]], self.cu[cu]))

        return rules
        