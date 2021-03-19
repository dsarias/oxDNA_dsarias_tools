# This program will run a succession of oxDNA simulations with increasing oriceps grip distance to test the behavior

import os

# os.chdir("/home/naitsaves/Documents/OricepsSimulations/oriceps3nm_v3/r2/oriceps3nm_v3r2_oxBehaviorTest")

os.system("pwd")
if os.path.exists("output"):
    os.system("rm -r output")
os.system("mkdir output")


def write_mutual_trap(distance):

    forces_text = ["{\n",
                    "type = mutual_trap\n",
                    "particle = 1001\n",
                    "ref_particle = 2053\n",
                    "stiff = 0.1\n",
                    "r0 = {}\n".format(distance),
                    "PBC = 1\n",
                    "}\n",

                    "{\n",
                    "type = mutual_trap\n",
                    "particle = 2053\n",
                    "ref_particle = 1001\n",
                    "stiff = 0.1\n",
                    "r0 = {}\n".format(distance),
                    "PBC = 1\n"
                    "}\n",


                    "{\n",
                    "type = mutual_trap\n",
                    "particle = 1002\n",
                    "ref_particle = 2052\n",
                    "stiff = 0.1\n",
                    "r0 = {}\n".format(distance),
                    "PBC = 1\n",
                    "}\n",

                    "{\n",
                    "type = mutual_trap\n",
                    "particle = 2052\n",
                    "ref_particle = 1002\n",
                    "stiff = 0.1\n",
                    "r0 = {}\n".format(distance),
                    "PBC = 1\n",
                    "}\n"
                   ]

    with open("forces", "w") as f:
        # Open and write the file that contains the forces
        f.writelines(forces_text)


def write_input(steps, input_config, output_conf, output_traj):

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

##############################
####    INPUT / OUTPUT    ####
##############################
topology = prova.top
conf_file = output/{}

lastconf_file = output/{}
log_file = output/log.log

trajectory_file = output/{}
print_conf_interval = 4000


energy_file = output/energy.dat
print_energy_every = 1000

refresh_vel = 1
no_stdout_energy = 1
restart_step_counter = 1

time_scale = linear
box_type=orthogonal

external_forces = 1
external_forces_file = forces
""".format(steps, input_config, output_conf, output_traj)
    with open("input", "w") as f:
        # Open and write the file that contains the forces
        f.writelines(input_text)


# This next portion will run a loop that will run consecutive oxDNA simulations with different grip distances

r0_initial = 3  # initial grip distance
steps_relax = 200000  # steps in relaxation step
steps = 400000  # steps in testing step

input_config_file = "../hclose.last.conf"  # the initial input config file

grip_distances = [i/2 for i in range(6, 40, 1)]

for r0 in grip_distances:
    os.system("echo 'r0 = {}'".format(r0))
    output_config_file = "gq_v1_r2_{}nm.last.conf".format(r0)  # output last config file
    output_traj_file = "gq_v1_r2_{}nm.dat".format(r0)  # output last config file

    write_mutual_trap(r0)  # mutual trap force file

    # relaxation phase
    os.system("echo 'Running relaxation step'")
    os.system('date +"%T"')
    write_input(steps_relax, input_config_file, output_config_file, output_traj_file)
    os.system("oxDNA input")

    # testing phase
    os.system("echo 'Running testing step'")
    write_input(steps, input_config_file, output_config_file, output_traj_file)
    os.system("oxDNA input")

    input_config_file = output_config_file  # next loop will take in the config of the previous loop

