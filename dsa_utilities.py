import ParticleData

from math import *


def calculate_distance(data: ParticleData, particles: list):
    # Calculates the distance between two particles
    p1 = [data.get_x(particles[0]), data.get_y(particles[0]), data.get_z(particles[0])]
    p2 = [data.get_x(particles[1]), data.get_y(particles[1]), data.get_z(particles[1])]
    num_points = len(p1[0])

    distance = []  # will contain the distance btw the particles
    for t in range(num_points):  # time step loop
        distance.append(0)
        for i in range(3):
            distance[t] += (p1[i][t] - p2[i][t]) ** 2
        distance[t] = sqrt(distance[t])

    return distance

def ask_particles():
    # particle numbers input handling
    particles_input = input("Enter id of the particles separated by a space:")
    particles_needed = particles_input.split(" ")
    particles_needed = list(dict.fromkeys(particles_needed))  # to get rid of duplicates
    try:
        particles_needed.remove('')
    except ValueError:
        pass
    particles_needed = [int(i) for i in particles_needed]  # converting from string to int
    print("Particles: ", particles_needed)
    return particles_needed

