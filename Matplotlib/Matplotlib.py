import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(-2, 60, 50)
y1 = x + 3  # 曲线 y1
y2 = 3 - x  # 曲线 y2
plt.figure()  # 定义一个图像窗口
plt.plot(x, y1)  # 绘制曲线 y1
plt.plot(x, y2)  # 绘制曲线 y2
plt.show()
