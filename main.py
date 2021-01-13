# my modules
from oxdna_data_extractor import extract_data
from oxDNA_data_plotter import *
from ParticleData import *
from dsa_utilities import ask_particles
# other modules
from tkinter.filedialog import askopenfilename

# TODO extract the filename and save to the class too
# TODO get rid of tk file dialog 

def run_extractor():
    # ask for oxDNA file
    file_name = askopenfilename()  # asks for a file using a tk file dialog
    # file_name = "testFile.txt"  # for testing purposes
    print(file_name)  # for confirmation

    particles_needed = ask_particles()
    
    # extract particle location data from oxDNA file
    success_status: bool  # whether data extraction worked
    data: ParticleData  # ParticleData object containing data for all particles
    data, success_status = extract_data(file_name, particles_needed)
    if not success_status:
        print("Error during data extraction. Quitting Program.")
        return False

    return data


def run_plot(data, particles):
    plot_distance_vs_time(data, particles)


# data = run_extractor()
# run_plot(data, [8898, 9762])
