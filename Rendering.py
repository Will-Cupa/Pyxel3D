import pyxel


WIDTH = 1920
HEIGHT = 1080
FOV = 85


class Point:
	def __init__(self, x, y, z):
		self.x = x
		self.y = y
		self.z = z


	def addPoints(self, other):
		self.x += other.x
		self.y += other.y
		self.z += other.z

	def subPoints(self, other):
		return Point(self.x - other.x, self.y - other.y, self.z - other.z)

	def vectorTo(self, other):
		return Point(other.x - self.x, other.y - self.y, other.z - self.z)


	def crossProduct(self, other):
		return Point(self.y*other.z - self.z*other.y, \
					 self.z*other.x - self.x*other.z, \
					 self.x*other.y - self.y*other.x)

	def dotProduct(self, other):
		return self.x + other.x * self.y + other.y * self.z + other.z


	def screenCoord(self, camera):
		Dx = self.x*(-1) - camera.x
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
		v2 = self.p2.vectorTo(self.p3)
		return v1.crossProduct(v2)


	def draw(self, camera):
		if(self.p1.screenCoord(camera) == (0,0) or \
		   self.p2.screenCoord(camera) == (0,0) or \
		   self.p3.screenCoord(camera) == (0,0)):
			pass
		elif self.p1.subPoints(camera).dotProduct(self.getNormal()) < 0:
			if self.norm:
				pyxel.line(WIDTH/2, HEIGHT/2, *self.getNormal().screenCoord(camera), 6)
				print(self.p1.subPoints(camera).dotProduct(self.getNormal()))
			pyxel.tri(*self.p1.screenCoord(camera), *self.p2.screenCoord(camera), *self.p3.screenCoord(camera), self.col)



class Object:
	def __init__(self, faceList):
		self.faceList = faceList

	def draw(self, camera):
		for face in self.faceList:
			face.draw(camera)

p1 = Point(0,0,0)
p2 = Point(20,10,10)
p3 = Point(20,0,10)

p4 = Point(0,0,0)
p5 = Point(-10,10,10)
p6 = Point(-10,0,10)

f1 = Face(p2,p3,p1, 1, True)
f2 = Face(p4,p5,p6, 2, True)

f3 = Face(p2,p3,p5, 4, False)
f4 = Face(p5,p6,p3, 4, False)

obj = Object([f1,f2,f3,f4])

cam = Point(1,1,1)



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
    		cam.x +=1

    def draw(self):
        pyxel.cls(3)
        obj.draw(cam)
        pyxel.line(WIDTH/2,HEIGHT/2 -10,WIDTH/2,HEIGHT/2 +10, 0)
        
        
App()