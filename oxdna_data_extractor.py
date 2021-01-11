# This program will parse through oxDNA output configuration files to get distance vs time of specified particles

# My modules
from ParticleData import *


def calculate_particle_num(file_name):
    """this function will calculate the number of particles in the configuration file"""

    try:  # opens the file and counts line with exception handling
        with open(file_name) as f:
            # initiating variables used in loop below
            keep_searching = True

            for i, line in enumerate(f):
                # find particle number by checking where first time step ends
                if keep_searching:
                    if line[0:3] == "t =" and i > 2:  # will break the loop once second time step is found
                        num_particle = i - 3  # to account for the 3 header lines in file
                        keep_searching = False  # so it doesn't keep looking for time steps after particle num found

    except FileNotFoundError:
        print("File not found! Please remake selection")
        return False

    line_count = i + 1
    num_time_step = line_count/(num_particle + 3)  # total num lines / lines per time step

    print("Number of lines in file: ", line_count)
    print("Number of particles: ", num_particle)
    print("Number of time steps: ", num_time_step)

    return True, num_particle, num_time_step


def extract_position_info(line):
    """this function extracts the position info from the line read"""
    values = line.split(" ")
    values = [float(i) for i in values]
    x = values[0]
    y = values[1]
    z = values[2]
    return x, y, z


def extract_data(file_name: str, particles_needed: list):
    """this function will open the file and parse through the data"""
    num_header_lines = 3
    particles_needed.sort()  # needed during data extraction step
    # calculate file information
    confirmation, num_particle, num_time_step = calculate_particle_num(file_name)
    while not confirmation:
        confirmation, num_particle, num_time_step = calculate_particle_num(file_name)

    # extract data needed
    data = ParticleData(particles_needed)  # initiates the object that will contain data extracted
    num_lines_in_set = num_particle + num_header_lines  # number of lines in one time step
    target_lines = [val + num_header_lines for val in particles_needed]  # moving targets lines to first position

    # iterate through lines to find lines which contain the information for our particles
    with open(file_name) as f:
        for line_index, line in enumerate(f):

            if line_index % num_lines_in_set == 0:  # the lines containing the time info
                t = float(line.split(" ")[2])  # extracts the time

            if line_index in target_lines:
                target_index = target_lines.index(line_index)  # index of the target line found
                particle_id = particles_needed[target_index]  # id of the particle corresponding to the target
                x, y, z = extract_position_info(line)  # location data extracted
                target_lines[target_index] += num_lines_in_set  # move target to next time step
                data.append_data(particle_id, x, y, z, t)  # appends data

    return data, True
