add_library('PeasyCam')

x = 0.01
y = 0
z = 0
a = 10
b = 28
c = 8.0 / 3.0

points = []

def setup():
    # Creating the output window
    # and setting up the OPENGL renderer
    size(800, 600, OPENGL)

    # Initializing the cam object
    perspective(PI/3.0, width/height, 1, 10000)
    cam = PeasyCam(this, 500)
    

def draw():
    global x, y, z, a, b, c
    background(22, 25, 28)

    # Implementation of the differential equations
    dt = 0.01
    dx = (a * (y - x)) * dt
    dy = (x * (b - z) - y) * dt
    dz = (x * y - c * z) * dt
    x += dx
    y += dy
    z += dz
    
    speed = sqrt(dx**2 + dy**2 + dz**2)

    # Adding the position vectors to points ArrayList
    points.append(PVector(x, y, z))
    translate(0, 0, -80)
    scale(6)
    strokeWeight(0.5)
    stroke(255, 50)
    noFill()

    # Beginning plotting of points
    beginShape()
    for v in points:
        # Adding random color to the structure in each frame
        #stroke(random(0, 255), random(0, 255), random(0, 255))
        vertex(v.x, v.y, v.z)  # plotting the vertices

    endShape()  # Drawing ends
