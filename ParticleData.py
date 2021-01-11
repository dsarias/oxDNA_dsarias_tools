class ParticleData:
    """Stores location and time data  for all particles in a run. The particle ID is a key to a dictionary containing
    the index of lists where the location and time data is found"""
    indexes = dict()
    # TODO make the data structure contain the filename
    def __init__(self, particles_input):
        num_particles = len(particles_input)
        self.x = [[] for i in range(num_particles)]  # list of empty lists that will contain particle x location
        self.y = [[] for i in range(num_particles)]  # list of empty lists that will contain particle x location
        self.z = [[] for i in range(num_particles)]  # list of empty lists that will contain particle x location
        self.t = [[] for i in range(num_particles)]  # list of empty lists that will contain particle x location

        for i, particle_id in enumerate(particles_input):  # adds particle ids and indexes to the dictionary
            self.indexes[particle_id] = i

    def append_data(self, particle_id, x_value, y_value, z_value, t_value):
        index = self.indexes[particle_id]
        self.x[index].append(x_value)
        self.y[index].append(y_value)
        self.z[index].append(z_value)
        self.t[index].append(t_value)

    def get_particles(self):
        return self.indexes.keys()

    def get_x(self, particle_id):
        return self.x[self.indexes[particle_id]]

    def get_y(self, particle_id):
        return self.y[self.indexes[particle_id]]

    def get_z(self, particle_id):
        return self.z[self.indexes[particle_id]]

    def get_t(self, particle_id):
        return self.t[self.indexes[particle_id]]

    def get_data(self, particle_id):
        index = self.indexes[particle_id]
        return self.x[index], self.y[index], self.z[index], self.t[index]

