
#colorMode(HSB, 100)



def setup():
    global c1
    size(1000,400)
    colorMode(HSB, 100)
    c1 = color(40, 40, 50)
    c2 = color(60, 40, 50)
    background(c2)
    
def draw():
    pass
    c1 = color(40, 40, 50)
    c1 = color(5, 80, 90)
    c2 = color(60, 40, 50)
    #c2 = color(100, 60, 50)
    createGradient(0, 0, width, height/2, c1, c2, vert=False, smoother=False)
    createGradient(0, height/2, width, height/2, c1, c2, vert=False)
    
    
def createGradient(x, y, w, h, c1, c2, vert=True, smoother=True):
    
    if vert:
        for i in range(y, y+h):
            if smoother:
                inter = smoothstep(map(i, y, y+h, 0, 1))
            c = lerpColor(c1, c2, inter)
            stroke(c)
            line(x, i, x+w, i)
    else:
        for i in range(x, x+w):
            if smoother:
                inter = smoothstep(map(i, x, x+w, 0, 1))
            else:
                inter = map(i, x, x+w, 0, 1)
            c = lerpColor(c1, c2, inter)
            stroke(c)
            line(i, y, i, y+h)
            
            
def smoothstep(x):
    if x < 0:
        val = 0
    if 0 <= x < 1:
        val = 6*x**5 - 15*x**4 + 10*x**3
    else:
        val = 1
    return val
