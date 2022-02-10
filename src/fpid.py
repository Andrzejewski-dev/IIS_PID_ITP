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
        self.valveeU = []
        self.valveeQd = []
        self.Qo = []
        self.h_axis = []
        self.ins = ['DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD']
        self.outs = ['BDU', 'DU', 'SU', 'MU', 'Z', 'MD', 'SD', 'DD', 'BDD']

        self.e = ctrl.Antecedent(np.arange(-1, 1, 0.01), 'e')
        self.ce = ctrl.Antecedent(np.arange(-1, 1, 0.01), 'ce')
        self.cu = ctrl.Consequent(np.arange(-1, 1, 0.01), 'cu')

        self.e['DU'] = fuzz.trimf(self.e.universe, [-1.3, -1, -0.667])
        self.e['SU'] = fuzz.trimf(self.e.universe, [-1, -0.667, -0.333])
        self.e['MU'] = fuzz.trimf(self.e.universe, [-0.667, -0.333, 0.0])
        self.e['Z'] = fuzz.trimf(self.e.universe, [-0.333, 0.0, 0.333])
        self.e['MD'] = fuzz.trimf(self.e.universe, [0.0, 0.333, 0.667])
        self.e['SD'] = fuzz.trimf(self.e.universe, [0.333, 0.667, 1])
        self.e['DD'] = fuzz.trimf(self.e.universe, [0.667, 1, 1.33])

        self.ce['DU'] = fuzz.trimf(self.ce.universe, [-1.3, -1, -0.667])
        self.ce['SU'] = fuzz.trimf(self.ce.universe, [-1, -0.667, -0.333])
        self.ce['MU'] = fuzz.trimf(self.ce.universe, [-0.667, -0.333, 0.0])
        self.ce['Z'] = fuzz.trimf(self.ce.universe, [-0.333, 0.0, 0.333])
        self.ce['MD'] = fuzz.trimf(self.ce.universe, [0.0, 0.333, 0.667])
        self.ce['SD'] = fuzz.trimf(self.ce.universe, [0.333, 0.667, 1])
        self.ce['DD'] = fuzz.trimf(self.ce.universe, [0.667, 1, 1.33])

        self.cu['BDU'] = fuzz.trimf(self.cu.universe, [-1.25, -1, -0.75])
        self.cu['DU'] = fuzz.trimf(self.cu.universe, [-1, -0.75, -0.5])
        self.cu['SU'] = fuzz.trimf(self.cu.universe, [-0.75, -0.5, -0.25])
        self.cu['MU'] = fuzz.trimf(self.cu.universe, [-0.5, -0.25, 0])
        self.cu['Z'] = fuzz.trimf(self.cu.universe, [-0.25, 0.0, 0.25])
        self.cu['MD'] = fuzz.trimf(self.cu.universe, [0, 0.25, 0.5])
        self.cu['SD'] = fuzz.trimf(self.cu.universe, [0.25, 0.5, 0.75])
        self.cu['DD'] = fuzz.trimf(self.cu.universe, [0.5, 0.75, 1])
        self.cu['BDD'] = fuzz.trimf(self.cu.universe, [0.75, 1, 1.25])

        # BDU
        rules = [ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[0]], self.cu[self.outs[0]])]
        rules.append(ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[0]], self.cu[self.outs[0]]))
        rules.append(ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[1]], self.cu[self.outs[0]]))
        rules.append(ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[1]], self.cu[self.outs[0]]))
        rules.append(ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[0]], self.cu[self.outs[0]]))
        rules.append(ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[2]], self.cu[self.outs[0]]))
        # DU
        rules.append(ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[0]], self.cu[self.outs[1]]))
        rules.append(ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[1]], self.cu[self.outs[1]]))
        rules.append(ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[2]], self.cu[self.outs[1]]))
        rules.append(ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[3]], self.cu[self.outs[1]]))
        # SU
        rules.append(ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[4]], self.cu[self.outs[2]]))
        rules.append(ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[3]], self.cu[self.outs[2]]))
        rules.append(ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[2]], self.cu[self.outs[2]]))
        rules.append(ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[1]], self.cu[self.outs[2]]))
        rules.append(ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[0]], self.cu[self.outs[2]]))
        # MU
        rules.append(ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[0]], self.cu[self.outs[3]]))
        rules.append(ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[1]], self.cu[self.outs[3]]))
        rules.append(ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[2]], self.cu[self.outs[3]]))
        rules.append(ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[3]], self.cu[self.outs[3]]))
        rules.append(ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[4]], self.cu[self.outs[3]]))
        rules.append(ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[5]], self.cu[self.outs[3]]))
        # Z
        rules.append(ctrl.Rule(self.e[self.ins[0]] & self.ce[self.ins[6]], self.cu[self.outs[4]]))
        rules.append(ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[5]], self.cu[self.outs[4]]))
        rules.append(ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[4]], self.cu[self.outs[4]]))
        rules.append(ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[3]], self.cu[self.outs[4]]))
        rules.append(ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[2]], self.cu[self.outs[4]]))
        rules.append(ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[1]], self.cu[self.outs[4]]))
        rules.append(ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[0]], self.cu[self.outs[4]]))
        # MD
        rules.append(ctrl.Rule(self.e[self.ins[1]] & self.ce[self.ins[6]], self.cu[self.outs[5]]))
        rules.append(ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[5]], self.cu[self.outs[5]]))
        rules.append(ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[4]], self.cu[self.outs[5]]))
        rules.append(ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[3]], self.cu[self.outs[5]]))
        rules.append(ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[2]], self.cu[self.outs[5]]))
        rules.append(ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[1]], self.cu[self.outs[5]]))
        # SD
        rules.append(ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[2]], self.cu[self.outs[6]]))
        rules.append(ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[3]], self.cu[self.outs[6]]))
        rules.append(ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[4]], self.cu[self.outs[6]]))
        rules.append(ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[5]], self.cu[self.outs[6]]))
        rules.append(ctrl.Rule(self.e[self.ins[2]] & self.ce[self.ins[6]], self.cu[self.outs[6]]))
        # DD
        rules.append(ctrl.Rule(self.e[self.ins[3]] & self.ce[self.ins[6]], self.cu[self.outs[7]]))
        rules.append(ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[5]], self.cu[self.outs[7]]))
        rules.append(ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[4]], self.cu[self.outs[7]]))
        rules.append(ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[3]], self.cu[self.outs[7]]))
        # BDD
        rules.append(ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[4]], self.cu[self.outs[8]]))
        rules.append(ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[5]], self.cu[self.outs[8]]))
        rules.append(ctrl.Rule(self.e[self.ins[4]] & self.ce[self.ins[6]], self.cu[self.outs[8]]))
        rules.append(ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[5]], self.cu[self.outs[8]]))
        rules.append(ctrl.Rule(self.e[self.ins[5]] & self.ce[self.ins[6]], self.cu[self.outs[8]]))
        rules.append(ctrl.Rule(self.e[self.ins[6]] & self.ce[self.ins[6]], self.cu[self.outs[8]]))

        cu_ctrl = ctrl.ControlSystem(rules)
        reg_cu = ctrl.ControlSystemSimulation(cu_ctrl)

        # h, Q_d, Q_o, h_z
        temp = [0]

        self.fuzzy_pid['y'][0].append(0)
        self.fuzzy_pid['y'][1].append(self.h_axis[0])
        self.fuzzy_pid['y'][2].append(self.valveeQd[0])
        self.fuzzy_pid['y'][3].append((self.beta) * (math.sqrt(self.pid['h'][0])))
        self.fuzzy_pid['y'][4].append(self.pid['h_z'][0])
        e_delay = 0
        self.fuzzy_pid['k_u'] = self.valvee['u']

        for x in range(1, self.N):

            self.fuzzy_pid['k_e'].append(self.kp / self.fuzzy_pid['k_u'][-1])
            self.fuzzy_pid['k_ce'].append(
                (self.Td / self.Tp) / self.fuzzy_pid['k_u'][-1])

            e = self.h_ex - self.fuzzy_pid['y'][1][x - 1]
            ke = e * (1 / self.fuzzy_pid['k_e'][-1])
            temp.append(ke)
            if e > 1:
                e = 1
            elif e < -1:
                e = -1

            ce = e - e_delay
            ce *= (1 / self.Tp)
            ce *= (1 / self.fuzzy_pid['k_ce'][-1])
            if ce > 1:
                ce = 1
            elif ce < -1:
                ce = -1

            reg_cu.input['e'] = e
            reg_cu.input['ce'] = ce
            reg_cu.compute()
            cu = reg_cu.output['cu']
            self.fuzzy_pid['k_u'].append(cu * self.Tp + self.fuzzy_pid['k_u'][-1])

            self.valveeQd[x] = self.fuzzy_pid['k_u'][1] * self.fuzzy_pid['k_u'][-1]

            if (self.valveeQd[x] > self.Qd_max):
                self.valveeQd[x] = self.Qd_max
            elif (self.valveeQd[x] < self.Qd_min):
                self.valveeQd[x] = self.Qd_min

            self.fuzzy_pid['y'][0].append((x) * self.Tp)
            self.fuzzy_pid['y'][2].append(self.valveeQd[x])
            self.fuzzy_pid['y'][3].append(self.beta * (sqrt(self.fuzzy_pid['y'][1][x - 1])))
            self.fuzzy_pid['y'][1].append(((self.fuzzy_pid['y'][2][x] - self.fuzzy_pid['y'][3][x]) * self.Tp) / self.A + self.fuzzy_pid['y'][1][x - 1])
            self.fuzzy_pid['y'][4].append(self.pid['h_z'][x])

            e_delay = e

        jsonListFuzzy = []
        for i in range(0, (len(self.x)-1)):
                jsonListFuzzy.append({"x": float(round(self.fuzzy_pid['y'][0][i],2)), "h_z": self.fuzzy_pid['y'][4][i], "h": self.fuzzy_pid['y'][1][i],
                                      "Q_d": self.fuzzy_pid['y'][2][i], "Q_o": self.fuzzy_pid['y'][3][i],
                                      "e": self.fuzzy_pid['k_e'][i-1]})
