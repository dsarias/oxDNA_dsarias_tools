import matplotlib.pyplot as plt
from math import *

from ParticleData import ParticleData


def plot_distance_vs_time(data, particles):
    """Calculates the distance between two particles and plots it vs time"""
    p1 = [data.get_x(particles[0]), data.get_y(particles[0]), data.get_z(particles[0])]
    p2 = [data.get_x(particles[1]), data.get_y(particles[1]), data.get_z(particles[1])]
    num_points = len(p1[0])
    print(num_points)

    dist = []  # will contain the distance btw the particles
    for t in range(num_points):  # time step loop
        dist.append(0)
        for i in range(3):
            dist[t] += (p1[i][t] - p2[i][t]) ** 2
        dist[t] = sqrt(dist[t])

    plot_data(data.get_t(particles[0]), dist)

    return dist


def plot_data(x_data, y_data):
    # plotting the points
    plt.plot(x_data, y_data)

    # naming the x axis
    plt.xlabel('Time')
    # naming the y axis
    plt.ylabel('Position/Distance')

    # giving a title to my graph
    plt.title('oxDNA Particle Data')

    # function to show the plot
    plt.show()
