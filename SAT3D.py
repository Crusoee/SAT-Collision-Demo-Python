import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection


class VertexCountError(Exception):
    """Not enough vertices to create a face."""
    pass

class Vec3:
    def __init__(self, x=0, y=0, z=0):
        self.x=x
        self.y=y
        self.z=z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def dot(self, vec: Vec3):
        return self.x * vec.x + self.y * vec.y + self.z * vec.z

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z**2)
    
    def cross(self, vec: Vec3):
        return Vec3(self.y*vec.z - self.z*vec.y, self.z*vec.x - self.x*vec.z, self.x*vec.y - self.y*vec.x)

    def proj(self, onto: Vec3):
        if isinstance(onto, Vec3):
            t = self.dot(onto) / onto.dot(onto)
            return Vec3(t * onto.x, t * onto.y, t * onto.z)
        elif isinstance(onto, Face):
            norm = onto.norm()
            diff = self.proj(norm)
            return self - diff
        else:
            raise ValueError
        
    def norm(self):
        return Vec3(self.x/self.mag(), self.y/self.mag(), self.z/self.mag())

    def __add__(self, vec):
        return Vec3(self.x + vec.x, self.y + vec.y, self.z + vec.z)

    def __sub__(self, vec):
        return Vec3(self.x - vec.x, self.y - vec.y, self.z - vec.z)
    
    def __eq__(self, vec):
        return (self.x, self.y, self.z) == (vec.x, vec.y, vec.z)

class Face:
    def __init__(self, vertices: list):
        if len(vertices) < 3:
            raise VertexCountError
        self.vertices = []
        for v in vertices:
            self.vertices.append(Vec3(v[0],v[1],v[2]))

    def get_edges(self):
        edges = []
        for i in range(len(self.vertices)):
            e = self.vertices[i]-self.vertices[i-1]
            edges.append(e.norm())
        return edges
        
    def norm(self):
        try:
            v1 = self.vertices[1] - self.vertices[0]
            v2 = self.vertices[2] - self.vertices[0]
            return v1.cross(v2).norm()
        except:
            raise VertexCountError

class Polyhedron:
    def __init__(self, faces: list):
        self.faces = faces
        self.vertices = []
        self.update_vertices()

    def update_vertices(self):
        self.vertices.clear()
        for face in self.faces:
            for v in face.vertices:
                for v2 in self.vertices:
                    if v == v2:
                        break
                else:
                    self.vertices.append(v)

    def translate(self, x=0, y=0, z=0):
        for face in self.faces:
            for v in face.vertices:
                v.x += x
                v.y += y
                v.z += z
        self.update_vertices()

    def plot(self, ax=None, color="cyan", edgecolor="black", alpha=0.5):

            if ax is None:
                fig = plt.figure()
                ax = fig.add_subplot(111, projection='3d')

            polys = []

            for face in self.faces:
                poly = []

                for v in face.vertices:
                    poly.append([v.x, v.y, v.z])

                polys.append(poly)

            collection = Poly3DCollection(
                polys,
                facecolors=color,
                edgecolors=edgecolor,
                alpha=alpha
            )

            ax.add_collection3d(collection)

            # autoscale
            xs = [v.x for v in self.vertices]
            ys = [v.y for v in self.vertices]
            zs = [v.z for v in self.vertices]

            ax.set_xlim(min(xs), max(xs))
            ax.set_ylim(min(ys), max(ys))
            ax.set_zlim(min(zs), max(zs))

            ax.set_box_aspect([1,1,1])

            return ax

class SAT3D:
    @staticmethod
    def CheckCollision(poly1: Polyhedron, poly2: Polyhedron):
        axes = []
        for face in poly1.faces + poly2.faces:
            axes.append(face.norm())

        for face1 in poly1.faces:
            edges1 = face1.get_edges()
            for face2 in poly2.faces:
                edges2 = face2.get_edges()
                for edge1 in edges1:
                    for edge2 in edges2:
                        axes.append(edge1.cross(edge2))

        for axis in axes:
            proj1 = [vertex.dot(axis) for face in poly1.faces for vertex in face.vertices]
            proj2 = [vertex.dot(axis) for face in poly2.faces for vertex in face.vertices]

            min1, max1 = min(proj1), max(proj1)
            min2, max2 = min(proj2), max(proj2)

            if max1 < min2 or max2 < min1:
                return False

        return True



def main():

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    pyramid = Polyhedron([Face([[-10,-10,0],[10,-10,0],[10,10,0],[-10,10,0]]),
                          Face([[10,-10,0],[10,10,0],[0,0,10]]),
                          Face([[10,10,0],[-10,10,0],[0,0,10]]),
                          Face([[-10,10,0],[-10,-10,0],[0,0,10]]),
                          Face([[-10,-10,0],[10,-10,0],[0,0,10]])])
    
    cube = Polyhedron([
        Face([[-10,-10,-10],[10,-10,-10],[10,10,-10],[-10,10,-10]]),
        Face([[-10,-10,10],[10,-10,10],[10,10,10],[-10,10,10]]),
        Face([[-10,-10,-10],[10,-10,-10],[10,-10,10],[-10,-10,10]]),
        Face([[-10,10,-10],[10,10,-10],[10,10,10],[-10,10,10]]),
        Face([[-10,-10,-10],[-10,10,-10],[-10,10,10],[-10,-10,10]]),
        Face([[10,-10,-10],[10,10,-10],[10,10,10],[10,-10,10]])
    ])

    cube.translate(20.01)
    
    print(SAT3D.CheckCollision(pyramid, cube))

    pyramid.plot(ax)
    cube.plot(ax)

    plt.show()

main()
