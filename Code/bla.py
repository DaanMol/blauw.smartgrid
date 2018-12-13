from grid import Grid
from actions import Plots
# from bokeh import Bokeh
import matplotlib.pyplot as plt
import random
import time
import math
import copy
from batteries import MedBattery, LargeBattery, SmallBattery

options = [[17, 0, 0], [15, 1, 0], [13, 2, 0], [11, 3, 0], [9, 4, 0], [7, 5, 0], [5, 6, 0], [3, 7, 0], [1, 8, 0], [13, 0, 1], [11, 1, 1], [9, 2, 1], [7, 3, 1], [
5, 4, 1], [3, 5, 1], [1, 6, 1], [9, 0, 2], [7, 1, 2], [5, 2, 2], [3, 3, 2], [1, 4, 2], [5, 0, 3], [3, 1, 3], [1, 2, 3], [1, 0, 4]];
average = []
minimum = []
opt = []
num = 2
for j in range(25):
    i = options[j]
    cost_list = []
    with open(f"output_runs/batt_conf_400_{num}/batt_conf_{num}_[{i[0]}_{i[1]}_{i[2]}]_400.txt", "r") as f:
        # text = f.read()
        # cost_list.append(text)
        text = f.read().split('\n')
        for number in text:

            # number = number.replace(' ', '')
            # number = number.replace('\n', '')
            # number = number.replace('[', '')
            # number = number.replace(']', '')
            if number is not "":
                cost_list.append(int(number))
            # print(number, type(number))
    # bins = np.linspace(min(cost_list), max(cost_list))


    minimum.append(min(cost_list))
    average.append(sum(cost_list)/len(cost_list))
    opt.append(f"[{i[0]}_{i[1]}_{i[2]}]")


    # plt.hist(cost_list, bins=100, alpha=0.5, label=f"[{i[0]}_{i[1]}_{i[2]}]")
    plt.scatter(min(cost_list), sum(cost_list)/len(cost_list), label=f"[{i[0]}_{i[1]}_{i[2]}]")
    plt.text(min(cost_list) + 10, sum(cost_list)/len(cost_list) - 40, f"{i}")
plt.suptitle(f"400x randompositioning+k-means+hill for all possible battery configurations (grid {num})")
plt.title("notation: [small, medium, large] (number of batteries)")
plt.xlabel("min cost")
plt.ylabel("average cost")
# plt.xlim(22400, 24000)
# plt.ylim(23000, 25000)
plt.show()
