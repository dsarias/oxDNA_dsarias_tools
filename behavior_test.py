# This program will run a succession of oxDNA simulations with increasing oriceps grip distance to test the behavior

import os

# os.chdir("/home/naitsaves/Documents/OricepsSimulations/oriceps3nm_v3/r2/oriceps3nm_v3r2_oxBehaviorTest")

os.system("pwd")
if os.path.exists("output"):
        os.system("rm -r output")
os.system("mkdir output")
os.system("mkdir output/trajectories")
os.system("mkdir output/lastconf")
os.system("mkdir output/energy")

if os.path.exists("output_relax"):
        os.system("rm -r output_relax")
os.system("mkdir output_relax")
os.system("mkdir output_relax/trajectories")
os.system("mkdir output_relax/lastconf")
os.system("mkdir output_relax/energy")


def write_mutual_trap(distance):

        forces_text = ["{\n",
                                        "type = mutual_trap\n",
                                        "particle = 1341\n",
                                        "ref_particle = 822\n",
                                        "stiff = 0.1\n",
                                        "r0 = {}\n".format(distance),
                                        "PBC = 1\n",
                                        "}\n",

                                        "{\n",
                                        "type = mutual_trap\n",
                                        "particle = 822\n",
                                        "ref_particle = 1341\n",
                                        "stiff = 0.1\n",
                                        "r0 = {}\n".format(distance),
                                        "PBC = 1\n"
                                        "}\n",


                                        "{\n",
                                        "type = mutual_trap\n",
                                        "particle = 3933\n",
                                        "ref_particle = 3302\n",
                                        "stiff = 0.1\n",
                                        "r0 = {}\n".format(distance),
                                        "PBC = 1\n",
                                        "}\n",

                                        "{\n",
                                        "type = mutual_trap\n",
                                        "particle = 3302\n",
                                        "ref_particle = 3933\n",
                                        "stiff = 0.1\n",
                                        "r0 = {}\n".format(distance),
                                        "PBC = 1\n",
                                        "}\n"
                                     ]

        with open("forces", "w") as f:
                # Open and write the file that contains the forces
                f.writelines(forces_text)


#Parameters set to match recommendations by Doye et al. (arXiv:2004.05052)
def write_input(steps, input_config, output_conf,output_log, output_traj,print_int,output_energy):

        input_text = """
##############################
####  PROGRAM PARAMETERS  ####
##############################
backend = CUDA
backend_precision = mixed
CUDA_list = verlet
use_edge = 1
interaction_type = DNA2
sim_type = MD #Defaults to MD so not needed

##############################
####    SIM PARAMETERS    ####
##############################
steps = {}
newtonian_steps = 103
diff_coeff = 2.50
thermostat = brownian

T = 300K
dt = 0.005
verlet_skin = 0.05
max_density_multiplier = 5

salt_concentration = 1.0

max_io = 10.0

##############################
####    INPUT / OUTPUT    ####
##############################
topology = top.top
conf_file = {}

lastconf_file = {}
log_file = {}

trajectory_file = {}
print_conf_interval = {}


energy_file = {}
print_energy_every = 1000

refresh_vel = 1
no_stdout_energy = 1
restart_step_counter = 1

time_scale = linear
box_type=orthogonal

external_forces = 1
external_forces_file = forces
""".format(steps, input_config, output_conf,output_log, output_traj,print_int,output_energy)
        with open("input", "w") as f:
                # Open and write the file that contains the forces
                f.writelines(input_text)


# This next portion will run a loop that will run consecutive oxDNA simulations with different grip distances

steps_relax = 5000000  # steps in relaxation step
steps =5000000  # steps in testing step

input_config = "last_conf_sim.conf" # the initial input config file

grip_distances = [i for i in range(4, 65, 2)]

#Save folders
output_traj_dir = "output/trajectories/"
output_conf_dir = "output/lastconf/"
output_energy_dir = "output/energy/"

output_relax_traj_dir = "output_relax/trajectories/"
output_relax_conf_dir = "output_relax/lastconf/"
output_relax_energy_dir = "output_relax/energy/"

for r0 in grip_distances:
    os.system('date +"%T"')
    os.system("echo 'r0 = {}'".format(r0)) #Print current r

    #naminf of files
    output_config_name = "gq_v3_r1_{}nm.last.conf".format(r0)  #output last config file
    output_traj_name = "gq_v3_r1_{}nm.dat".format(r0)  # output last config file
    energy_name = "energy_{}nm.dat".format(r0)  # output last config file

    #Forces
    write_mutual_trap(r0)  # mutual trap force file

    #setting up paths for relaxation
    output_conf = output_relax_conf_dir+output_config_name
    output_log = "output_relax/log.log"
    output_traj = output_relax_traj_dir+output_traj_name
    print_int = int(steps_relax/100)
    output_energy = output_relax_energy_dir + energy_name

    # Running relaxation
    os.system("echo 'Running relaxation step'")
    
    write_input(steps_relax, input_config, output_conf,output_log, output_traj,print_int,output_energy)

    os.system("oxDNA input")

    input_config = output_conf  #testing step will take in the last config from the relaxation step

    #setting up paths for testing
    output_conf = output_conf_dir+output_config_name
    output_log = "output/log.log"
    output_traj = output_traj_dir+output_traj_name
    print_int = int(steps/100)
    output_energy = output_energy_dir + energy_name

    # testing phase
    os.system("echo 'Running testing step'")
    write_input(steps, input_config, output_conf,output_log, output_traj,print_int,output_energy)
    os.system("oxDNA input")

    input_config = output_conf  # next loop will take in the config of the previous loop

