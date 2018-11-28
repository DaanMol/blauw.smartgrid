import matplotlib.pyplot as plt
cost_list = []
with open("text.txt", "r") as f:
    text = f.read().strip('\n').split(',')
    for number in text:
        number = number.replace(' ', '')
        number = number.replace('\n', '')
        number = number.replace('[', '')
        number = number.replace(']', '')
        cost_list.append(int(number))
print(cost_list)
plt.hist(cost_list, bins=25)
plt.title("10k K-Means with hillclimber")
plt.xlabel("Cost")
plt.ylabel("Frequency")
plt.show()
