
w=750
h=750
num_circles=50
circ_size=float(w)/float(num_circles)
circ_slot_ratio = 0.66
noiseSeed(3)

def sigmoid(x):
    return 1.0 / (1.0 + exp(-x))
    
def extremizer(x, strength=10):
    return sigmoid(strength*(x-0.5))

def setup():
    
    size(w,h)
    background(0)
    pixelDensity(2)
    
def draw():
    background(0)
    
    pushMatrix()
    translate(circ_size/2.0,circ_size/2.0)
    
    for i in range(num_circles):
        for j in range(num_circles):
            pushMatrix()
            translate(circ_size*i, circ_size*j)
            
            #noiseDetail()
            scalar_noise = noise(i/10.0, j/10.0)
            fill(map(extremizer(scalar_noise, strength=20), 0,1, 0,255))
            noStroke()
            #ellipseMode(CORNER)
            circle(0,0, 
                   map(extremizer(scalar_noise), 
                       0, 1,
                        0, circ_slot_ratio*circ_size))
            popMatrix()
    popMatrix()
