import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("result_test_1.csv", sep=";")
data = df.to_numpy()

fig, axes = plt.subplots(4, 2, figsize=(18, 6))
fig.tight_layout()

axes[0, 0].set_title("IMU 1 Acceleration")
axes[0, 0].plot(data[:, 0], data[:, 1:4])
axes[0, 0].legend([r"$x$", r"$y$", r"$z$"])

axes[0, 1].set_title("IMU 1 Gyroscope")
axes[0, 1].plot(data[:, 0], data[:, 4:7])
axes[0, 1].legend([r"$x$", r"$y$", r"$z$"])

axes[1, 0].set_title("IMU 2 Acceleration")
axes[1, 0].plot(data[:, 0], data[:, 7:10])
axes[1, 0].legend([r"$x$", r"$y$", r"$z$"])

axes[1, 1].set_title("IMU 2 Gyroscope")
axes[1, 1].plot(data[:, 0], data[:, 10:13])
axes[1, 1].legend([r"$x$", r"$y$", r"$z$"])

axes[2, 0].set_title("Encoder 1")
axes[2, 0].plot(data[:, 0], data[:, 13])
axes[2, 1].set_title("Encoder 2")
axes[2, 1].plot(data[:, 0], data[:, 14])

axes[3, 0].set_title("Force 1")
axes[3, 0].plot(data[:, 0], data[:, 15])
axes[3, 1].set_title("Force 2")
axes[3, 1].plot(data[:, 0], data[:, 16])

plt.show()
