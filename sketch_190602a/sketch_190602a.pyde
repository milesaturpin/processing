
num_points=20
buffer=100
points=[]
edges=[]
edge_weights=[]
points_v = []
p=0.1
randomSeed(10)

def setup():
    global points, edges, edge_weights, points_v
    size(1000, 1000)
    background(0.5*22, 0.5*25, 0.5*28)
    points = [[random(buffer, width-buffer), 
               random(buffer, height-buffer)] for i in range(num_points)]
    points_v = [[map(random(1,10), 1, 10, -1, 1),
                 map(random(1,10), 1, 10, -1, 1)] for _ in range(num_points)]
    
    edges = [[int(random(0,int(1/p)) < 1) for _ in range(num_points)] 
             for _ in range(num_points)]
    
    
    
    edge_weights = [[0 for _ in range(num_points)] 
             for _ in range(num_points)]
    

    
    
def draw():
    global edge_weights, points, points_v
    
    ### Update
    
    # Update point pos
    for i in range(num_points):
        # Detect wall collision
        if points[i][0] < 1 or points[i][0] > width:
            points_v[i][0] = -1*points_v[i][0]
        if points[i][1] < 1 or points[i][1] > height:
            points_v[i][1] = -1*points_v[i][1]
        
        # Update pos
        points[i][0] += 4*points_v[i][0]
        points[i][1] += 4*points_v[i][1]
    
    # Generate edge weights
    for i in range(num_points):
        for j in range(i, num_points):
                if edges[i][j] == 1:
                    #edge_weights[i][j] = noise(i,j,0.01*frameCount)
                    x1, y1 = points[i]
                    x2, y2 = points[j]
                    edge_weights[i][j] = exp(-0.003*sqrt((x2-x1)**2 + (y2-y1)**2))
    ### Draw
    
    background(0.5*22, 0.5*25, 0.5*28)
    # Draw lines
    for i in range(num_points):
        for j in range(i, num_points):
            if edges[i][j] == 1:
                stroke(edge_weights[i][j]*255, 225)
                strokeWeight(map(edge_weights[i][j], 
                                 0, 1, 
                                 0, 10))
                line(points[i][0], points[i][1], 
                    points[j][0], points[j][1])
    
    # Draw points
    strokeWeight(10)
    stroke(255)
    for x, y in points:
        point(x, y)
    

    
    
