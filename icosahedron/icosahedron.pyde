
add_library('PeasyCam')
add_library('postfx')

cam = None
fx = None
colorgrid = [[color(random(0,100),100,100) for _ in range(10)] 
             for __ in range(10)]

def setup():
    global cam, fx, boxcolor
    size(800,800, P3D)
    colorMode(HSB, 100)
    cam = PeasyCam(this, 100)
    fx = PostFX(this)
    background(0,0,0)
    
def draw():
    global colorgrid
    background(0)
    noStroke()
    #stroke(255)
    
    
    reCent = width/2
    translate((-90)/2, -90/2)
    
    for i in range(0,100,10):
        for j in range(0,100,10):
            pushMatrix()
            translate(i,j,0)
            c = color(0,0,0)
            if (frameCount % 10) == 0:
                colorgrid[i/10][j/10] = color(random(0,100),80,100)
            c = colorgrid[i/10][j/10]
                
            fill(c)
            box(2)
            popMatrix()
    
    cam.beginHUD()
    (fx.render()
    .bloom(0.5, 20, 40)
    .noise(0.05, 0.2)
    .compose())
    cam.endHUD()
