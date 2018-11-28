import matplotlib.pyplot as plt
import numpy as np

for i in range(1,4):
    cost_list = []
    with open(f"text_info_random{i}_10k.txt", "r") as f:
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
    bins = np.linspace(min(cost_list), max(cost_list))
    plt.hist(cost_list, bins, alpha=0.5, label=f"Wijk {i}")
# print(cost_list)
# plt.hist(cost_list, bins=25)
plt.title("10k Random walk")
plt.xlabel("Cost")
plt.ylabel("Frequency")
plt.legend(loc='upper right')
plt.show()
