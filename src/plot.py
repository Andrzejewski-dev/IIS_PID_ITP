import matplotlib.pyplot as plt
from uar import UAR

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
    Qd_min = 0
    Qd_max = 1
)
pid.run()


plt.plot(uar.n_axis, uar.h_axis)
plt.plot(uar.n_axis, uar.Qd_axis)
plt.show()

if __name__ == "__main__":
    main()