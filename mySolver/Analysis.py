import numpy as np

class AnalysisStatic():

    def add_nodes(self, node_list):
        self.nodes = node_list

    def add_elems(self, elem_list):
        self.elems = elem_list

    def add_loads(self, load_list):
        self.loads = load_list

    def add_constraints(self, constraint_list):
        self.constraints = constraint_list

    def analyze(self):

        self.compute_Ke()
        self.compute_K()
        self.compute_F()
        self.compute_u()
        self.solve()

    def compute_Ke(self):

        for elem in self.elems:
            elem.compute_Ke()

    def compute_K(self):

        self.K = np.matrix([[0.0 for i in range(2 * len(self.nodes))] for i in range(2 * len(self.nodes))])

        for elem in self.elems:
            for i1, node1 in enumerate(elem.nodes):
                for i2, node2 in enumerate(elem.nodes):
                    self.K[2 * node1.index    , 2 * node2.index    ] += elem.Ke[2 * i1    , 2 * i2    ]
                    self.K[2 * node1.index + 1, 2 * node2.index    ] += elem.Ke[2 * i1 + 1, 2 * i2    ]
                    self.K[2 * node1.index    , 2 * node2.index + 1] += elem.Ke[2 * i1    , 2 * i2 + 1]
                    self.K[2 * node1.index + 1, 2 * node2.index + 1] += elem.Ke[2 * i1 + 1, 2 * i2 + 1]

    def compute_F(self):
        
        self.F = np.matrix([[0.0] for i in range(2 * len(self.nodes))])

        for load in self.loads:
            
            node = load[0]
            degree = load[1]
            value = load[2]

            self.F[2 * node.index + degree - 1, 0] = value

    def compute_u(self):

        self.u = np.matrix([[0.0] for i in range(2 * len(self.nodes))])

        self.a = [True  for i in range(2 * len(self.nodes))]
        self.b = [False for i in range(2 * len(self.nodes))]


        for constraint in self.constraints:

            node = constraint[0]
            degree = constraint[1]
            value = constraint[2]

            self.a[2 * node.index + degree - 1] = False
            self.b[2 * node.index + degree - 1] = True

            self.u[2 * node.index + degree - 1] = value


    def solve(self):

        K_a = self.K[self.a]
        K_b = self.K[self.b]

        self.K_aa = K_a[:, self.a]
        self.K_ab = K_a[:, self.b]
        self.K_ba = K_b[:, self.a]
        self.K_bb = K_b[:, self.b]

        self.u_b = self.u[self.b]

        self.F_a = self.F[self.a]


        self.u_a = np.linalg.solve(self.K_aa, self.F_a - self.K_ab * self.u_b)

        self.F_b = self.K_ba * self.u_a + self.K_bb * self.u_b

        j = 0

        for i in range(len(self.a)):

            if self.a[i]:
                self.u[i] = self.u_a[j]
                j += 1

        for i in range(len(self.nodes)):

            self.nodes[i].u = self.u[2 * i    , 0]
            self.nodes[i].v = self.u[2 * i + 1, 0]

    def write(self, output_file):

        with open(output_file, 'w') as f:

            f.write(f"{'ID':^4}{'u':^15}{'v':^15}\n")
            
            for node in self.nodes:
                f.write(f"{node.ID:4}{node.u:15.10f}{node.v:15.10f}\n")
