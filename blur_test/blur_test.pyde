add_library('peasycam')
add_library('postfx')

fx = None
cam = None

def setup():
    global fx, cam
    size(500,500, P3D)
    background(30)
    cam = PeasyCam(this, 500)
    fx = PostFX(this)

def draw():
    global fx, cam
    #pushMatrix()
    background(30)
    fill(0)
    box(100)
    fill(200,200,255)
    noStroke()
    sphere(60)
    
    #translate(-250,-250,-250)
    cam.beginHUD()
    (fx.render().bloom(0.5, 20, 40).noise(0.05, 0.2)
    #.pixelate(100)
    #.blur(3, 5)
    #.rgbSplit(200)
    .invert()
    .compose())
    cam.endHUD()
    #popMatrix()

    
