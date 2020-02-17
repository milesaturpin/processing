

pt2 = [255,255,255]
pt1 = [0, 102, 204]
t = 100
delt = [int((p2 - p1)/t) for (p1, p2) in zip(pt1, pt2)] 

def setup():
    size(500, 500)

rgb = pt1

def draw():
    global rgb
    background(rgb[0], rgb[1], rgb[2])
    if mousePressed:
        rgb = [rgbi + delti for rgbi , delti in zip(rgb, delt)]
        
