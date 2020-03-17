import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# disease settings
SICK_TIME = 14
SILENT_SPREAD_TIME = 3
DEATH_RATE = 0.03
IMMUNE_TIME = np.inf

# envirionment settings
POPULATION = 1000000
SOCIAL_CONNECTION_FACTOR = 0.3
SICK_CONNECTION_FACTOR = 0.05

# run settings
TIMESTEPS = 365*2

def plot(time_series):
    healthy = []
    silent = []
    sick = []
    immune = []
    dead = []
    for data in time_series:
        healthy.append(data["healthy"])
        silent.append(data["silent"])
        sick.append(data["sick"])
        immune.append(data["immune"])
        dead.append(data["dead"])
    x = range(len(time_series))
    plt.plot(x, healthy, label="healthy")
    plt.plot(x, silent, label="silent")
    plt.plot(x, sick, label="sick")
    plt.plot(x, immune, label="immune")
    plt.plot(x, dead, label="dead")
    plt.legend()
    plt.show()


def main():
    print("Running once")

    time_series = []
    new_dist = defaultdict(lambda: 0)
    new_dist["new_sick"] = 1/POPULATION
    new_dist["sick"] = 1/POPULATION
    new_dist["healthy"] = 1 - 1/POPULATION
    time_series.append(new_dist)

    for step in range(TIMESTEPS):
        new_dist = defaultdict(lambda: 0)
        last = time_series[-1]

        # simple transitions
        if step - SILENT_SPREAD_TIME >= 0:
            dist = time_series[step - SILENT_SPREAD_TIME]
            new_dist["new_sick"] += dist["new_silent"]

        if step - SILENT_SPREAD_TIME - SICK_TIME >= 0:
            dist = time_series[step - SILENT_SPREAD_TIME - SICK_TIME]
            new_dist["new_dead"] += dist["new_sick"]*DEATH_RATE
            new_dist["new_immune"] += dist["new_sick"]*(1 - DEATH_RATE)

        if step - SILENT_SPREAD_TIME - SICK_TIME - IMMUNE_TIME >= 0:
            dist = time_series[step - SILENT_SPREAD_TIME - SICK_TIME - IMMUNE_TIME]
            new_dist["new_healthy"]+= dist["new_immune"]

        # concentration based transitions
        new_dist["new_silent"] += last["healthy"] * \
                                last["sick"]*SICK_CONNECTION_FACTOR
        new_dist["new_silent"] += last["healthy"] * \
                                last["silent"]*SOCIAL_CONNECTION_FACTOR

        # collect full results
        new_dist["silent"] += last["silent"] + new_dist["new_silent"] - new_dist["new_sick"]
        new_dist["sick"] += last["sick"] + new_dist["new_sick"] - new_dist["new_dead"] - new_dist["new_immune"]
        new_dist["dead"] += last["dead"] + new_dist["new_dead"]
        new_dist["immune"] += last["immune"] + new_dist["new_immune"] - new_dist["new_healthy"]
        new_dist["healthy"] += last["healthy"] + new_dist["new_healthy"] - new_dist["new_silent"]
        time_series.append(new_dist)

    plot(time_series)

if __name__ == '__main__':
    main()
