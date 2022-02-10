import matplotlib.pyplot as plt
from pid import PID

# uar = UAR(
#     h_0 = 0,
#     h_ex = 2,
#     N = 120,
#     A = 4,
#     beta = 1,
#     Tp = 1
# )
# uar.run()


pid = PID(
    h_0 = 0,
    h_ex = 2,
    N = 10000,
    A = 2.5,
    beta = 0.25,
    Tp = 0.05,
    Ti = 0.75,
    Td = 0.05,
    kp = 1.0,
    Qd_min = 0,
    Qd_max = 1
)
pid.run()

plt.plot(pid.n_axis, pid.h_axis)
plt.plot(pid.n_axis, pid.Qd_axis)
plt.show()
