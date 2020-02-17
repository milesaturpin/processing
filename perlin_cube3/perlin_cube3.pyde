add_library('PeasyCam')
add_library('postfx')

# Parameters
cubeSize = 300.0 
numBlocks = 12 # 4, 8, 12, 20
blockSize = 2.0 * cubeSize // numBlocks # 1, 0.5, 2
stride = cubeSize // numBlocks
noiseScale = 20.0 / cubeSize # 100, 20
sparsity = 2 # 2, 4

# Initialize values
cube = None
cam = None
fx = None
minNoise = 0
maxNoise = 1

def setup():
    global cam, fx, depthShader, dofShader
    background(0)
    #size(870, 870, P3D)
    size(1400,1400,P3D)
    cam = PeasyCam(this, 500)
    fx = PostFX(this)
    frameRate(24)

def draw():
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
    rotateX(frameCount * PI / 1000)
    rotateY(frameCount * PI / 500)

    # Navy: 18, 37, 54
    # Gray: 22, 25, 28
    background(0.5*22, 0.5*25, 0.5*28)
    
    # Camera center
    #fill(100, 0, 0)
    #box(10)
    # Centering for the camera
    reCent = stride * (numBlocks - 1) / 2
    translate(-reCent, -reCent, -reCent)
    
    for zi in range(numBlocks):
        for yi in range(numBlocks):
            for xi in range(numBlocks):
                x, y, z = xi * stride, yi * stride, zi * stride
                noiseVal = cube[zi][yi][xi]
                # Change upper bound on size
                sizeVal = map(noiseVal, 0, 1, 0, 1)
                
                # Compute color
                #color1 = [227, 227, 237]
                #color2 = [30, 30, 34]
                color1 = [30, 30, 34]
                # Red
                #color2 = [200, 30, 24]
                color2 = [227, 227, 237]
                c_interp = [map(noiseVal, 0, 1, c1, c2) 
                          for c1, c2 in zip(color1, color2)]
                fill(c_interp[0], c_interp[1], c_interp[2], 255)
                # gray = 255 * (1 - noiseVal)
                # fill(gray, gray, gray, 255)
                noStroke()
                pushMatrix()
                translate(x, y, z)
                box(sizeVal * blockSize)
                popMatrix()
                
    cam.beginHUD()
    (fx
     .render()
     #.brightPass(0.25)
     .bloom(0.2, 200, 40)
     .noise(0.05, 0.2)
     
     #.rgbSplit(50)
     #.chromaticAberration()
     #.pixelate(500)
     .compose())
    cam.endHUD()
