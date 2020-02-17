

w = 200
h = w
d = w
blockSize = 0.5*w//10
stride = w//10
noiseScale = 0.02
add_library('PeasyCam')

def setup():
    background(255)
    
    size(800, 800, OPENGL)

    # Initializing the cam object
    cam = PeasyCam(this, 500)
    
def draw():
    background(255, 255, 255)
    translate(-w/2, -h/2, -d/2)
    
    for z in range(0, d, stride):
        for x in range(0, w, stride):
            for y in range(0, h, stride):
                noiseDetail(5, 0.5)
                fill(255 * noise(x * noiseScale, y * noiseScale, z * noiseScale), 25)
                noStroke()
                pushMatrix()
                translate(x, y, z )
                box(blockSize)
                popMatrix()
    
