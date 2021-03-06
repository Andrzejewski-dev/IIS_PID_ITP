import matplotlib.pyplot as plt
from fpid import FPID

# uar = UAR(
#     h_0 = 0,
#     h_ex = 2,
#     N = 120,
#     A = 4,
#     beta = 1,
#     Tp = 1
# )
# uar.run()


fpid = FPID(
    h_0 = 0,
    h_ex = 2,
    N = 10000,
    A = 2.5,
    beta = 0.25,
    Tp = 0.05,
    Td = 0.05,
    kp = 1.0,
    Qd_min = 0,
    Qd_max = 1
)

plt.plot(fpid.n_axis, fpid.pid_y[2])
plt.plot(fpid.n_axis, fpid.pid_y[1])
plt.show()
