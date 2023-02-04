import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
plt.style.use('seaborn-pastel')


def avg(reward):
    list_avg = []
    n = len(reward)
    for i in range(n - 100):
        avg_100 = np.sum(reward[i: 100 + i]) / 100
        list_avg.append(avg_100)
    return np.array(list_avg)


reward_one = np.loadtxt("./rewards/reward_one.txt")
reward_two = np.loadtxt("./rewards/reward_two.txt")
reward_three = np.loadtxt("./rewards/reward_three.txt")
reward_four = np.loadtxt("./rewards/reward_four.txt")

avg_one = avg(reward_one)
avg_two = avg(reward_two)
avg_three = avg(reward_three)
avg_four = avg(reward_four)

y_one = []
y_two = []
y_three = []
y_four = []
x = []

N = len(avg_one)
count = 0

fig = plt.figure()
ax = plt.axes(xlim=(0, 100), ylim=(-1.1, 1.1))
line_one, = ax.plot([], [], lw=1, color='blue', label='Recompensa carro 1')
line_two, = ax.plot([], [], lw=1, color='red', label='Recompensa carro 2')
line_three, = ax.plot([], [], lw=1, color='black', label='Recompensa carro 3')
line_four, = ax.plot([], [], lw=1, color='green', label='Recompensa carro 4')
ax.legend()


def init():
    line_one.set_data([], [])
    line_two.set_data([], [])
    line_three.set_data([], [])
    line_four.set_data([], [])
    return line_one, line_two, line_three, line_four


def animate(i):
    global count
    x.append(i)
    y_one.append(avg_one[count])
    y_two.append(avg_two[count])
    y_three.append(avg_three[count])
    y_four.append(avg_four[count])
    line_one.set_data(x, y_one)
    line_two.set_data(x, y_two)
    line_three.set_data(x, y_three)
    line_four.set_data(x, y_four)
    count += 1
    return line_one, line_two, line_three, line_four


anim = FuncAnimation(fig, animate, init_func=init,
                     frames=np.linspace(0, 100, N - 5),
                     interval=0.1,
                     blit=True,
                     repeat=False)


plt.show()

# anim.save('recompensas_car.gif', writer='imagemagick')
