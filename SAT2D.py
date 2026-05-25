import math

class Vertex:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def mag(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def perp(self):
        return Vertex(-self.y, self.x)

    def proj(self, onto: Vertex):
        t = self.dot(onto) / onto.dot(onto)
        return Vertex(t * onto.x, t * onto.y)

    def __add__(self, other):
        return Vertex(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vertex(self.x - other.x, self.y - other.y)

class Polygon:
    def __init__(self, vertices):
        alter = []
        for vertex in vertices:
            alter.append(Vertex(vertex[0], vertex[1]))
        self.vertices = alter

    def transform(self, x=0,y=0):
        for vertex in self.vertices:
            vertex.x += x
            vertex.y += y

    def __str__(self):
        return f"Polygon with vertices: {[str(vertex) for vertex in self.vertices]}"

class SAT:
    @staticmethod
    def GetAxes(polygon: Polygon):
        axes = []
        for i in range(len(polygon.vertices)):
            axis = polygon.vertices[i] - polygon.vertices[i-1]
            axes.append(axis.perp())
        return axes

    @staticmethod
    def CheckCollision(poly1: Polygon, poly2: Polygon):
        axes1 = SAT.GetAxes(poly1)
        axes2 = SAT.GetAxes(poly2)

        for axis in axes1 + axes2:
            proj1 = []
            proj2 = []

            for vertex in poly1.vertices:
                proj1.append(math.copysign(vertex.proj(axis).mag(), vertex.proj(axis).x))
            for vertex in poly2.vertices:
                proj2.append(math.copysign(vertex.proj(axis).mag(), vertex.proj(axis).x))

            if min(proj2) <= min(proj1) <= max(proj2) or min(proj2) <= max(proj1) <= max(proj2) or\
                min(proj1) <= min(proj2) <= max(proj1) or min(proj1) <= max(proj2) <= max(proj1):
                    continue
            else:
                return False

        return True

def main():
    triangle = Polygon([(0, 0), (0, -4), (4, -4)])
    square = Polygon([(2, 0), (4, -2), (2, -4), (0, -2)])

    # fiddle with the transformation here!
    triangle.transform(0,0)

    print(SAT.CheckCollision(triangle, square))

if __name__ == "__main__":
    main()
