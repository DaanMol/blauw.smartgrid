import matplotlib.pyplot as plt
import numpy as np
minima = []
for i in range(1,2):
    cost_list = []
    with open(f"output_runs/text_info_random{i}_10k.txt", "r") as f:
        text = f.read().split('\n')
        counter = 0
        for number in text:
            counter += 1
            if number is not "":
                cost_list.append(int(number))
            if counter == 1000:
                break
    minim = min(cost_list)
    minima.append(minim)
    maxim = max(cost_list)
    print("random:", minim, maxim)
    plt.axvline(x=53188, color='r')
    plt.axvline(x=103030, color="r")
    plt.hist(cost_list, bins=20, alpha=0.5, label=f"Random walk")


    cost_list = []
    with open(f"output_runs/text_info_prior_hill{i}_1k.txt", "r") as f:
        text = f.read().split('\n')
        for number in text:
            if number is not "":
                cost_list.append(int(number))
    minim = min(cost_list)
    minima.append(minim)
    maxim = max(cost_list)
    print("prior hill:", minim, maxim)
    plt.hist(cost_list, bins=20, alpha=0.5, label=f"Priority + Hill")

    cost_list = []
    with open(f"output_runs/simulated_annealing{i}_1000.txt", "r") as f:
        text = f.read().split('\n')
        for number in text:
            if number is not "":
                cost_list.append(int(number))
    minim = min(cost_list)
    minima.append(minim)
    maxim = max(cost_list)
    print("random+anneal:", minim, maxim)
    plt.hist(cost_list, bins=20, alpha=0.5, label=f"Random + sim anneal")

    cost_list = []
    with open(f"output_runs/random_hill{i}_1000.txt", "r") as f:
        text = f.read().split('\n')
        for number in text:
            if number is not "":
                cost_list.append(int(number))
    minim = min(cost_list)
    minima.append(minim)
    maxim = max(cost_list)
    print("random+hill:", minim, maxim)
    plt.hist(cost_list, bins=100, alpha=0.5, label=f"Random + Hillclimber")

    # cost_list = []
    # with open(f"output_runs/text_k-means_hill{i}_1000.txt", "r") as f:
    #     text = f.read().split('\n')
    #     for number in text:
    #         if number is not "":
    #             cost_list.append(int(number))
    # plt.hist(cost_list, bins=20, alpha=0.5, label=f"Kmean and hill {i}")
totalmin = min(minima)
plt.axvline(x=totalmin, color="g")
plt.title(f"4 algorithms Wijk {i}, lowest cost: {totalmin}")
plt.xlabel("Cost")
plt.ylabel("Frequency")
plt.legend(loc='upper right')
plt.show()
