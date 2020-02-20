add_library('PeasyCam')
add_library('postfx')

x = 0.01
y = 0
z = 0
a = 10
b = 28
c = 8.0 / 3.0

points = []
speeds = []

cam = None
fx = None

def setup():
    # # Creating the output window
    # # and setting up the OPENGL renderer
    # size(800, 600, OPENGL)

    # # Initializing the cam object
    # cam = PeasyCam(this, 500)
    
    global cam, fx, depthShader, dofShader, buf1, buf2, buf3
    background(0)
    
    
    #size(870, 870, P3D)
    size(1000, 1000, P3D)
    #pixelDensity(2)
    cam = PeasyCam(this, 500)
    #perspective(PI/3.0, width/height, 1, 10000)
    fx = PostFX(this)
    frameRate(24)
    
    depthShader = loadShader("depth.glsl") 
    dofShader = loadShader("dof.glsl")
    depthShader.set("maxDepth", cam.getDistance())
    dofShader.set("aspect", width / float(height))
    dofShader.set("maxBlur", 0.02)
    dofShader.set("aperture", 0.08)

    buf1, buf2, buf3 = [createGraphics(width, height, P3D) for e in range(3)]
    buf1.smooth(8), buf2.shader(depthShader), buf3.shader(dofShader)

def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))

def drawScene(pg):
    global x, y, z, a, b, c
    # last two params set clipping planes
    pg.perspective(PI/3.0, width/height, 1, 10000)
    pg.beginDraw()
    pg.background(22, 25, 28)

    # Implementation of the differential equations
    dt = 0.01
    dx = (a * (y - x)) * dt
    dy = (x * (b - z) - y) * dt
    dz = (x * y - c * z) * dt
    x += dx 
    y += dy 
    z += dz 
    # x += noise(frameCount)/4
    # y += noise(frameCount)/4
    # z += noise(frameCount)/4
    
    speed = sqrt(dx**2 + dy**2 + dz**2)

    # Adding the position vectors to points ArrayList
    points.append(PVector(x, y, z))
    speeds.append(speed)
    
    #print(sum(speeds)/len(speeds))
    
    #pg.translate(0, 0, -80)
    pg.scale(6)
    
    
    pg.pushMatrix()
    pg.translate(x+noise(len(points)/100.0+frameCount/200.)/0.25, 
                 y+noise(len(points)/100.0+frameCount/200.)/0.25, 
                 z+noise(len(points)/100.0+frameCount/200.)/0.25)
    pg.noStroke()
    pg.fill(200)
    pg.sphere(0.5)
    pg.popMatrix()
    
    pg.strokeWeight(0.5)
    #pg.strokeWeight(sigmoid(speed)+0.5)
    #pg.stroke(255, 50)
    # pg.stroke(map(sigmoid(speed-1), 0, 1, 0, 255), 255)
    #pg.stroke(255, map(sigmoid(speed-2), 0, 1, 50, 200))
    
    pg.noFill()

    # Beginning plotting of points
    pg.beginShape()
    i=0
    for v, speed in zip(points, speeds):
        # Adding random color to the structure in each frame
        #stroke(random(0, 255), random(0, 255), random(0, 255))
        pg.stroke(map(sigmoid(2*(speed-1)), 0, 1, 50, 255), 255)
        #print(map(sigmoid(2*(speed-1)), 0, 1, 0, 255))
        pg.vertex(v.x+noise(i/100.0+frameCount/200.)/0.25, 
                  v.y+noise(i/100.0+frameCount/200.)/.25, 
                  v.z+noise(i/100.0+frameCount/200.)/.25)  # plotting the vertices
        i+=1

    pg.endShape()  # Drawing ends
    
    pg.endDraw()
    cam.getState().apply(pg)
    
    
def draw():
    drawScene(buf1) 
    drawScene(buf2)

    buf3.beginDraw()
    dofShader.set("tDepth", buf2)
    dofShader.set("focus", map(mouseX, 0, width, 0, 1))
    # focus 
    #dofShader.set("focus", 0.0)
    buf3.image(buf1, 0, 0)
    buf3.endDraw()
      
    cam.beginHUD()
    image(buf3, 0, 0)
    (fx
     .render()
     #.brightPass(0.25)
     #.bloom(0.2, 200, 40)
      .bloom(0.2, 200, 100)
      .noise(0.05, 0.2)
     
     #.rgbSplit(50)
     #.chromaticAberration()
     #.pixelate(map(mouseY, 0, height, 50, 1000))
     .compose())
    
    cam.endHUD()
    #saveFrame("frames/{}.png".format(frameCount))
