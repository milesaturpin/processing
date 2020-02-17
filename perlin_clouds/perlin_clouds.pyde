
sparsity = 2
w = 300
h = w
d = w
numBlocks = 20
blockSize = w // numBlocks
stride = w // numBlocks
noiseScale = 40.0/w
add_library('PeasyCam')

cube = None
cubeDist = None
minNoise = None
maxNoise = None
distFromCent = lambda x, y, z: sqrt(
    (x - w/2)**2 + (y - h/2)**2 + (z - d/2)**2)
maxDistFromCent = sqrt(3 * (w / 2) ** 2)

def setup():
    global cube, cubeDist, minNoise, maxNoise
    background(255)

    size(800, 800, OPENGL)

    # Initializing the cam object
    cam = PeasyCam(this, 500)

    noiseDetail(5, 0.5)
    flatCube = [noise(x * noiseScale, y * noiseScale, z * noiseScale)
                for x in range(numBlocks)
                for y in range(numBlocks)
                for z in range(numBlocks)]
    minNoise = min(flatCube)
    maxNoise = max(flatCube)
    getNoise = lambda x, y, z: noise(
        x * noiseScale, y * noiseScale, z * noiseScale)
    # Square to make sparse
    cube = [[[map(getNoise(x, y, z), minNoise, maxNoise, 0, 1)**sparsity
              for x in range(numBlocks)]
             for y in range(numBlocks)]
            for z in range(numBlocks)]

    # Dist
    flatDist = [distFromCent(x, y, z)
                for x in range(numBlocks)
                for y in range(numBlocks)
                for z in range(numBlocks)]
    minDist = min(flatDist)
    maxDist = max(flatDist)
    cubeDist = [[[map(distFromCent(x, y, z), minDist, maxDist, 0, 1)
                  for x in range(numBlocks)]
                 for y in range(numBlocks)]
                for z in range(numBlocks)]
    frameRate(24)
    
i = 0

def draw():
    
    ### To remove changing behavior over time comment out from here:
    global i
    i += 1
    
    noiseDetail(5, 0.5)
    getNoise = lambda x, y, z: noise(
        x * noiseScale, y * noiseScale, z * noiseScale)
    flatCube = [getNoise(x+i, y+i, z+i)
                for x in range(numBlocks)
                for y in range(numBlocks)
                for z in range(numBlocks)]
    minNoise = min(flatCube)
    maxNoise = max(flatCube)
    
    # Square to make sparse
    cube = [[[map(getNoise(x+i, y+i, z+i), minNoise, maxNoise, 0, 1)**sparsity
              for x in range(numBlocks)]
             for y in range(numBlocks)]
            for z in range(numBlocks)]

    # Dist
    flatDist = [distFromCent(x, y, z)
                for x in range(numBlocks)
                for y in range(numBlocks)
                for z in range(numBlocks)]
    minDist = min(flatDist)
    maxDist = max(flatDist)
    cubeDist = [[[map(distFromCent(x, y, z), minDist, maxDist, 0, 1)
                  for x in range(numBlocks)]
                 for y in range(numBlocks)]
                for z in range(numBlocks)]
    ### TO here
    
    background(22, 25, 28)
    translate(-w / 2, -h / 2, -d / 2)
    #directionalLight(255, 255, 255, 1, -1, 1)
    for zi in range(numBlocks):
        for yi in range(numBlocks):
            for xi in range(numBlocks):
                x, y, z = xi * stride, yi * stride, zi * stride
                noiseVal = cube[zi][yi][xi]
                # Change upper bound on size
                sizeVal = map(noiseVal, 0, 1, 0, 1)
                distVal = cubeDist[zi][yi][xi]
                #if distVal > 0.25:
                c = 255 * (1-noiseVal)
                #print(distVal)
                
                fill(c, c, c,
                    #(distVal) * 
                    255)
                #fill(0, (1-distAdj) * 100)
                noStroke()
                pushMatrix()
                s=2*noiseVal**2
                s=0
                translate(x+s*random(0,1), y+s*random(0,1), z+s*random(0,1))
                box(sizeVal * blockSize)
                popMatrix()
