add_library('PeasyCam')
add_library('postfx')
add_library('controlp5')

# Parameters
cubeSize = 300.0 
numBlocks = 12 # 4, 8, 12, 20
blockSizeParam = 1 # 1, 0.5, 2
blockSize = blockSizeParam * cubeSize // numBlocks 
stride = cubeSize // numBlocks
noiseScaleParam = 20.0 # 100, 20
noiseScale = noiseScaleParam / cubeSize 
sparsity = 4 # 2, 4

# Initialize values
cube = None
cam = None
fx = None
minNoise = 0
maxNoise = 1

#sizeSlider = Slider(0.5, 2, 1)
cp5 = None
sizeSlider = None
sparsitySlider = None
noiseSlider = None
#cp5_controls = [sizeSlider, sparsitySlider]
#sizeSliderValue = 1
#slider = Slider()

def setup():
    global cam, fx, depthShader, dofShader, buf1, buf2, buf3 
    global cp5, sizeSlider, sparsitySlider, noiseSlider
    background(0)
    #size(870, 870, P3D)
    size(1200, 1200, P3D)
    cam = PeasyCam(this, 200)
    #perspective()
    #pixelDensity(2)
    fx = PostFX(this)
    
    frameRate(24)
    
    depthShader = loadShader("depth.glsl") 
    dofShader = loadShader("dof.glsl")
    depthShader.set("maxDepth", cam.getDistance())
    dofShader.set("aspect", width / float(height))
    dofShader.set("maxBlur", 0.02)
    dofShader.set("aperture", 0.04)

    buf1, buf2, buf3 = [createGraphics(width, height, P3D) for e in range(3)]
    buf1.smooth(8), buf2.shader(depthShader), buf3.shader(dofShader)
    
    cp5 = ControlP5(this)
    #name, minimum, maximum, default value (float), x, y, width, height
    sizeSlider = cp5.addSlider("Size", 0.25, 4, 1., 20, 20, 200, 20)
    sparsitySlider = cp5.addSlider("Sparsity", 0, 20, 2, 20, 60, 200, 20)
    noiseSlider = cp5.addSlider("Noise Scale", 0, 200, 20, 20, 100, 200, 20)
    
    #sizeSlider.position(200,200)
    #sizeSlider.label = 'Block Size'

def updateGlobalParams():
    global cubeSize, numBlocks, blockSizeParam, blockSize, stride, noiseScaleParam, noiseScale, sparsity
    global sizeSlider, sparsitySlider, noiseSlider
    
    cubeSize = 300.0 
    numBlocks = 12 # 4, 8, 12, 20
    #sizeSlider.value()
    blockSizeParam = sizeSlider.getValue()
    #blockSizeParam = 1 # 1, 0.5, 2
    blockSize = blockSizeParam * cubeSize // numBlocks 
    stride = cubeSize // numBlocks
    noiseScaleParam = noiseSlider.getValue() # 100, 20
    noiseScale = noiseScaleParam / cubeSize 
    
    sparsity = sparsitySlider.getValue() # 2, 4
    

def drawScene(pg):
    
    # Update global params based on slider values
    updateGlobalParams()

    pg.perspective(PI/3.0, width/height, 1, 10000)
    pg.beginDraw()
    noiseDetail(5, 0.5)
    period = 2*24.0
    freq = 1/period
    
    getNoiseVal = lambda x, y, z, t: (
        noise((x + t*numBlocks) * noiseScale,
              (y + t*numBlocks) * noiseScale,
              (z + t*numBlocks) * noiseScale))
    
    def getNoiseCube(t):
        # Need separate flat cubes so can normalize noise samples separately
        # since they have different min's and max's
        flatCube = [getNoiseVal(x, y, z, t)
                    for x in range(numBlocks)
                    for y in range(numBlocks)
                    for z in range(numBlocks)]
        minNoise = min(flatCube)
        maxNoise = max(flatCube)
        cube = [[[map(getNoiseVal(x, y, z, t), minNoise, maxNoise, 0, 1) ** sparsity
                  for x in range(numBlocks)]
                 for y in range(numBlocks)]
                for z in range(numBlocks)]
        return cube
    
    cubeDesc = getNoiseCube(frameCount//period)
    cubeAsc = getNoiseCube(frameCount//period+1)
    cyclePos = (frameCount%period)*freq*PI
    
    mergeCubes = lambda x, y, z: (
         (cos(cyclePos)*0.5 + 0.5) * cubeDesc[x][y][z]
        + (cos(cyclePos-PI)*0.5 + 0.5) * cubeAsc[x][y][z])

    cutSmallValues = lambda x: 0 if x < 0.01 else x

    cube = [[[mergeCubes(x, y, z)
              for x in range(numBlocks)]
             for y in range(numBlocks)]
            for z in range(numBlocks)]

    # Set rotation speed
    pg.rotateX(frameCount * PI / 1000)
    pg.rotateY(frameCount * PI / 500)

    # Navy: 18, 37, 54
    # Gray: 22, 25, 28
    pg.background(0.5*22, 0.5*25, 0.5*28)
    
    # Camera center
    #fill(100, 0, 0)
    #box(10)
    # Centering for the camera
    reCent = stride * (numBlocks - 1) / 2
    pg.translate(-reCent, -reCent, -reCent)
    
    for zi in range(numBlocks):
        for yi in range(numBlocks):
            for xi in range(numBlocks):
                x, y, z = xi * stride, yi * stride, zi * stride
                noiseVal = cube[zi][yi][xi]
                # Change upper bound on size
                sizeVal = map(noiseVal, 0, 1, 0, 1)
                
                # Compute color
                color1 = [227, 227, 237]
                color2 = [30, 30, 34]
                
                #color1 = [30, 30, 34]
                #color2 = [227, 227, 237]
                
                #color1 = [30, 30, 34]
                # Red
                #color1 = [200, 30, 24]
                #color2 = [30, 30, 200]
                #color2 = [227, 227, 237]
                c_interp = [map(noiseVal, 0, 1, c1, c2) 
                          for c1, c2 in zip(color1, color2)]
                pg.fill(c_interp[0], c_interp[1], c_interp[2], 220)
                # gray = 255 * (1 - noiseVal)
                # fill(gray, gray, gray, 255)
                pg.noStroke()
                #pg.stroke(0)
                #pg.strokeWeight(1)
                pg.pushMatrix()
                pg.translate(x, y, z)
                pg.box(sizeVal * blockSize)
                pg.popMatrix()
                
    pg.endDraw()
    cam.getState().apply(pg)
    cp5.setAutoDraw(False)
    
# def gui():
#     #currCameraMatrix = new PMatrix3D(g3.camera);
#     #camera()
#     cp5.draw()
#     #g3.camera = currCameraMatrix;

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
     .bloom(0.2, 200, 40)
     .noise(0.05, 0.2)
     
     #.rgbSplit(50)
     #.chromaticAberration()
     #.pixelate(500)
     .compose())
    
    cp5.draw()
    
    cam.endHUD()
    
    # This is necessary so that dragging the slider doesn't move the camera
    cam.setMouseControlled(True)
    #is_inside_list = [control.isInside() for control in cp5_controls]
    if sparsitySlider.isInside() or sizeSlider.isInside() or noiseSlider.isInside():
        cam.setMouseControlled(False)
    
    #saveFrame("frames/{}.png".format(frameCount))
