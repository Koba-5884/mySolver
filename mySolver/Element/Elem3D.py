from .Element import Elem

class Elem3D4(Elem):

    ### ‚Ü‚¾ƒeƒXƒg‚µ‚Ä‚È‚¢ ###

    def __init__(self, ID, nodes, section):

        super().__init__(ID, nodes, section)

    def compute_Ke(self):

        node1 = self.nodes[0]
        node2 = self.nodes[1]
        node3 = self.nodes[2]
        node4 = self.nodes[2]

        X = np.matrix([[    1.0,     1.0,     1.0,     1.0], 
                       [node1.x, node2.x, node3.x, node4.x], 
                       [node1.y, node2.y, node3.y, node4.y],
                       [node1.z, node2.z, node3.z, node4.z]])

        X_inv = X.I

        B = np.matrix([[X_inv[0, 1],         0.0,         0.0, X_inv[1, 1],         0.0,         0.0, X_inv[2, 1],         0.0,         0.0, X_inv[3, 1],         0.0,         0.0],
                       [        0.0, X_inv[0, 2],         0.0,         0.0, X_inv[1, 2],         0.0,         0.0, X_inv[2, 2],         0.0,         0.0, X_inv[3, 2],         0.0],
                       [        0.0,         0.0, X_inv[0, 3],         0.0,         0.0, X_inv[1, 3],         0.0,         0.0, X_inv[2, 3],         0.0,         0.0, X_inv[3, 3]], 
                       [X_inv[0, 2], X_inv[0, 1],         0.0, X_inv[1, 2], X_inv[1, 1],         0.0, X_inv[2, 2], X_inv[2, 1],         0.0, X_inv[3, 2], X_inv[3, 1],         0.0],
                       [        0.0, X_inv[0, 3], X_inv[0, 2],         0.0, X_inv[1, 3], X_inv[1, 2],         0.0, X_inv[2, 3], X_inv[2, 2],         0.0, X_inv[3, 3], X_inv[3, 2]],
                       [X_inv[0, 3],         0.0, X_inv[0, 1], X_inv[1, 3],         0.0, X_inv[1, 1], X_inv[2, 3],         0.0, X_inv[2, 1], X_inv[3, 3],         0.0, X_inv[3, 1]]])

        
        E =  self.section.material.E
        nu = self.section.material.nu
        

        D = E / ((1 + nu) * (1 - 2 * nu)) * np.matrix([[1 - nu,     nu,     nu,              0.0,              0.0,              0.0],
                                                       [    nu, 1 - nu,     nu,              0.0,              0.0,              0.0],
                                                       [    nu,     nu, 1 - nu,              0.0,              0.0,              0.0],
                                                       [   0.0,    0.0,    0.0, (1 - 2 * nu) / 2,              0.0,              0.0],
                                                       [   0.0,    0.0,    0.0,              0.0, (1 - 2 * nu) / 2,              0.0],
                                                       [   0.0,    0.0,    0.0,              0.0,              0.0, (1 - 2 * nu) / 2]])

        V = np.linalg.det(X) / 6
                          
        self.Ke = B.T * D * B * V


