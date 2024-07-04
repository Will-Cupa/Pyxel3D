import pyxel
import math 

WIDTH = 1920
HEIGHT = 1080
FOV = 150


def readObjFile(file):
	f = open(file, "r")

	pointTab = []
	faceTab = []

	for line in f:
	  if line.split()[0] == 'v':
	  	x = float(line.split()[1])
	  	y = float(line.split()[2])
	  	z = float(line.split()[3])
	  	pointTab.append(Point(x,y,z))
	  if line.split()[0] == 'f':
	  	s = ''
	  	for let in line.split()[1]:
	  		if let == '/' or let == ' ' or let == '\n':
	  			break
	  		else:
	  			s += let

	  	p1 = pointTab[int(s)-1]

	  	s = ''
	  	for let in line.split()[2]:
	  		if let == '/' or let == ' ' or let == '\n':
	  			break
	  		else:
	  			s += let

	  	p2 = pointTab[int(s)-1]

	  	s = ''
	  	for let in line.split()[3]:
	  		if let == '/' or let == ' ' or let == '\n':
	  			break
	  		else:
	  			s += let

	  	p3 = pointTab[int(s)-1]

	  	faceTab.append(Face(p1,p2,p3,8, False))

	return Object(faceTab)



class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z


	def addPoints(self, other):
		self.x += other.x
		self.y += other.y
		self.z += other.z

	def scale(self, val):
		self.x *= val
		self.y *= val
		self.z *= val

	def subPoints(self, other):
		return Point(self.x - other.x, self.y - other.y, self.z - other.z)

	def divide(self, val):
		return Point(self.x/val,self.y/val,self.z/val)

	def vectorTo(self, other):
		return Point(other.x - self.x, other.y - self.y, other.z - self.z)

	def vectorLength(self):
		return math.sqrt(self.x**2 + self.y**2 + self.z**2)

	def crossProduct(self, other):
		return Point(self.y*other.z - self.z*other.y, \
					 self.z*other.x - self.x*other.z, \
					 self.x*other.y - self.y*other.x)

	def dotProduct(self, other):
		return self.x * other.x + self.y * other.y + self.z * other.z

	def normalize(self):
		return self.divide(self.vectorLength())

	def screenCoord(self, camera):
		Dx = self.x - camera.x
		Dy = self.y - camera.y
		Dz = self.z - camera.z

		if Dz < 0 :
			return (FOV/Dz * Dx + WIDTH/2, FOV/Dz * Dy + HEIGHT/2)
		else:
			return (0,0)


class Face:
	def __init__(self, p1, p2, p3, col, norm):
		self.p1 = p1
		self.p2 = p2
		self.p3 = p3
		self.col = col
		self.norm = norm

	def getNormal(self):
		v1 = self.p1.vectorTo(self.p2)
		v2 = self.p1.vectorTo(self.p3)
		normal = v1.crossProduct(v2)
		return normal.normalize()

	def scale(self, val):
		p1.scale(val)
		p2.scale(val)
		p3.scale(val)

	def draw(self, camera):
		
		if(self.p1.screenCoord(camera) == (0,0) or \
		   self.p2.screenCoord(camera) == (0,0) or \
		   self.p3.screenCoord(camera) == (0,0)):
			pass

		elif camera.vectorTo(p1).normalize().dotProduct(self.getNormal()) < 0:
			pyxel.trib(*self.p1.screenCoord(camera), *self.p2.screenCoord(camera), *self.p3.screenCoord(camera), self.col)
			



class Object:
	def __init__(self, faceList):
		self.faceList = faceList

	def scale(self, val):
		for face in self.faceList:
			face.scale(val)

	def draw(self, camera):
		for face in self.faceList:
			face.draw(camera)

p1 = Point(0,0,0)
p2 = Point(20,10,10)
p3 = Point(20,0,10)

p4 = Point(0,0,0)
p5 = Point(-10,10,10)
p6 = Point(-10,0,10)

f1 = Face(p1,p2,p3, 1, True)
f2 = Face(p6,p4,p5, 2, True)

f3 = Face(p3,p5,p2, 4, False)
f4 = Face(p3,p5,p6, 4, False)

obj = Object([f1,f2,f3,f4])

obj2 = readObjFile("cube.obj")



cam = Point(1,1,1)
light = Point(1,0,0)


class App:
    def __init__(self):
        pyxel.init(WIDTH, HEIGHT, title="3D", fps=60, quit_key=pyxel.KEY_ESCAPE, display_scale=4)
        pyxel.run(self.update, self.draw)

    def update(self):
    	if pyxel.btn(pyxel.KEY_Z):
    		cam.z -= 1
    	elif pyxel.btn(pyxel.KEY_S):
    		cam.z += 1

    	if pyxel.btn(pyxel.KEY_Q):
    		cam.x -= 1
    	elif pyxel.btn(pyxel.KEY_D):
    		cam.x += 1

    	if pyxel.btn(pyxel.KEY_E):
    		cam.y -= 1
    	elif pyxel.btn(pyxel.KEY_A):
    		cam.y += 1

    def draw(self):
        pyxel.cls(3)
        obj2.draw(cam)
        pyxel.line(WIDTH/2,HEIGHT/2 -10,WIDTH/2,HEIGHT/2 +10, 0)
        
        
App()