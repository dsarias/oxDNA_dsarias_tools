# This program will analyze the oxDNA data from the behavior_test
import os
import statistics
import matplotlib.pyplot as plt
import csv
import pickle

from oxdna_data_extractor import extract_data
from dsa_utilities import calculate_distance, ask_particles

# USER INPUTS
temp_bool = True;
while (temp_bool):

    temp_response = input("Would you like to use last run settings? (y/n)")
    if temp_response == "y" or temp_response == "Y":
        #load previous settings and run

        with open('.saved_behavior_settings','rb') as file:
            particles_needed = pickle.load(file)
            data_path = pickle.load(file)

        temp_bool = False
    elif temp_response == "n" or temp_response == "N":
        #ask for new inputs and save for future

        particles_needed = ask_particles()

        if len(particles_needed) > 2:
            continue

        data_path = input("Enter path of data:")
 
                
        with open('.saved_behavior_settings', 'wb') as file:
            #picklying (?) in file for next run
            pickle.dump(particles_needed, file)
            pickle.dump(data_path, file )

        temp_bool = False
    else:
        continue

#particles_needed = [376, 1588]  # the particle number for the two particles at the end of the legs
grip_separation = [i for i in range(20, 35, 1)] #TODO: make this automatic
os.chdir(data_path)

# Gheto way to get the grip separation list in the order that I want
grip_separation = [str(i) for i in grip_separation]
grip_separation.sort()
grip_separation = [float(i) for i in grip_separation]

all_files = os.listdir()
all_files.sort()

traj_file_names = []  # will contain the names of the trajectory files in the folder

for i, filename in enumerate(all_files):  # parsing through files and picking our trajectory files
    if ".dat" in filename and "energy" not in filename:
        traj_file_names.append(filename)
        print(filename)

# Extracting data from all the trajectory files:
data = []  # will contain position data for the needed particles within ParticleData classes
for i, file_name in enumerate(traj_file_names):
    data_temp, success_status = extract_data(file_name, particles_needed)  # extracts position data
    if not success_status:
        print("Error during data extraction. Quitting Program.")
        exit()
    data.append(data_temp)

# Calculating the leg separation
leg_separation = []  # will contain the distance the leg separation data for each data class
for i, this_data in enumerate(data):
    leg_separation_temp = calculate_distance(this_data, particles_needed)
    leg_separation.append(leg_separation_temp)

# Running statistics on the data extracted
avg_separation = []  # average leg separation of all the steps
std_separation = []  # standard deviation

for separation_data in leg_separation:
    avg_separation.append(statistics.mean(separation_data))
    std_separation.append(statistics.stdev(separation_data))

print(len(grip_separation), len(avg_separation), len(std_separation))
print(grip_separation)
#TODO: move plotting to another function?
# Plot the behavior
# plotting the points
plt.errorbar(grip_separation, avg_separation, std_separation, marker='o', linestyle="None")

# naming the x axis
plt.xlabel('Grip Separation')
# naming the y axis
plt.ylabel('Leg Separation')

# giving a title to my graph
plt.title('oxDNA Particle Data')

# function to show the plot
plt.show()


# Exporting the data
with open('analysis_data.csv', mode='w') as export_file:
    employee_writer = csv.writer(export_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    employee_writer.writerow(grip_separation)
    employee_writer.writerow(avg_separation)
    employee_writer.writerow(std_separation)

"""
check how many data files there are

for i in files:
    extract the leg distance, add to a list

do something with the data
"""
