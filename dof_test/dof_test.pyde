add_library('peasycam')
colors, liste = [[0,189,202], [251,183,0], [255,17,79], [252,128,35], [0,108,254]], []

def setup():
    global depthShader, dofShader, cam, buf1, buf2, buf3, pnt
    size(900, 900, P3D)
    frameRate(1000)

    cam = PeasyCam(this, 900)
    cam.setMaximumDistance(width)
    pnt = createShape(BOX, 30)
    pnt.setStroke(False)

    depthShader, dofShader = loadShader("depth.glsl"), loadShader("dof.glsl")
    depthShader.set("maxDepth", cam.getDistance()*2)
    dofShader.set("aspect", width / float(height)), dofShader.set("maxBlur", 0.02), dofShader.set("aperture", 0.06)

    buf1, buf2, buf3 = [createGraphics(width, height, P3D) for e in range(3)]
    buf1.smooth(8), buf2.shader(depthShader), buf3.shader(dofShader)

    for e in range(300): liste.append(PVector(random(width), random(height), random(width))) 

def drawScene(pg):
    pg.beginDraw()
    pg.background(0)
    for i in range(len(liste)):
        pg.pushMatrix()
        pg.translate(liste[i].x-width/2, liste[i].y-width/2, liste[i].z-width/2)
        pg.shape(pnt)
        pnt.setFill(color(colors[i%5][0], colors[i%5][1], colors[i%5][2]))
        pg.popMatrix()
    pg.endDraw()
    cam.getState().apply(pg)

def draw():
    drawScene(buf1) 
    drawScene(buf2)

    buf3.beginDraw()
    dofShader.set("tDepth", buf2)
    dofShader.set("focus", map(mouseX, 0, width, .3, 1))
    buf3.image(buf1, 0, 0)
    buf3.endDraw()

    cam.beginHUD()
    image(buf3, 0, 0)
    cam.endHUD()
