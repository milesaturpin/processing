#add_library('PeasyCam')

w=500
h=500
face_size=100
last_face=None
face=None
period=3*24.0
freq=1/period


def setup():
    global last_face, face
    size(w,h)
    background(255)
    
    last_face = Face()
    face = Face()
    last_face.draw()
    
    
def samp_normal(locs, scales, dim=1):
    if dim==1:
        return locs*2+scales*2*randomGaussian()
    else:
        return [locs[i]*2 + scales[i]*2*randomGaussian() for i in range(dim)]
    

def draw():
    global face, last_face
    background(255)
    pushMatrix()
    translate(w/2,h/2)
    
    fill(0,0,0,255)
    noStroke()
    
    #pushMatrix()
    #translate(*face_size,h/2)
    #circle(0,0,samp_normal([50],[5])[0])
    
    
    cycle_pos = (frameCount%period)*freq*PI
    weight = cos(cycle_pos)*0.5 + 0.5
    #weight = (cos(sin(cycle_pos + PI))*0.5 + 0.5)**10
    #print(weight)

    # Sample new face 
    if weight == 1.0:
        last_face = face
        face = Face()

    avg_face = average_faces(last_face, face, weight)
    avg_face.draw()
    
    popMatrix()
    
def mouseClicked():
    global last_face, face
    last_face = face
    face = Face()
    
class Face():
    
    def __init__(self,
        left_eye_params=None, 
        right_eye_params=None, 
        # left_brow_params=None,
        # right_brow_params=None,
        mouth_params=None, 
        nose_params=None,
        ):
             
        eye_size=samp_normal(7,2.5)        
        if left_eye_params is None:
            self.left_eye_params = [
                samp_normal(-40,20), 
                samp_normal(-50,10),
                eye_size]
        else:
            self.left_eye_params = left_eye_params
            
        if right_eye_params is None:
            self.right_eye_params = [
                samp_normal(40,20), 
                samp_normal(-50,10), 
                eye_size]
        else:
            self.right_eye_params = right_eye_params
            
        # if left_brow_params is None:
        #     self.left_brow_params = [
        #         self.left_eye_params[0]+samp_normal(-5,10),
        #         self.left_eye_params[1]+samp_normal(-15,5),
        #         self.left_eye_params[0]+samp_normal(5,10),
        #         self.left_eye_params[1]+samp_normal(-15,5)]
        # else:
        #     self.left_brow_params = left_brow_params
        
        # if right_brow_params is None:
        #     self.right_brow_params = [
        #         self.right_eye_params[0]+samp_normal(-5,10),
        #         self.right_eye_params[1]+samp_normal(-15,5),
        #         self.right_eye_params[0]+samp_normal(5,10),
        #         self.right_eye_params[1]+samp_normal(-15,5)]
        # else:
        #     self.right_brow_params = right_brow_params
            
        #self.mouth_params = [0,25, samp_normal(10,1)]
        anchor_height = samp_normal(10,5)
        if mouth_params is None:
            self.mouth_params = [
                samp_normal(-30,15),
                samp_normal(10,15),
                -5*2,
                anchor_height,
                5*2,
                anchor_height,
                samp_normal(30,15),
                samp_normal(10,15),]
        else:
            self.mouth_params = mouth_params

        anchor_w = samp_normal(0,3)
        if nose_params is None:
            # self.nose_params = [
            #     samp_normal(0,5),
            #     samp_normal(-40,7),
            #     samp_normal(0,5),
            #     samp_normal(-15,7),]
            self.nose_params = [
                samp_normal(0,5),
                samp_normal(-40,7),
                anchor_w,
                -25*2,
                anchor_w,
                -25*2,
                samp_normal(0,5),
                samp_normal(-15,7),]
        else:
            self.nose_params = nose_params


    def draw(self):
        noStroke()
        circle(*self.left_eye_params)
        circle(*self.right_eye_params)
        stroke(0)
        strokeWeight(2)
        noFill()
        bezier(*self.mouth_params)
        bezier(*self.nose_params)
        # line(*self.left_brow_params)
        # line(*self.right_brow_params)
    
def average_faces(face1, face2, weight):
    """Create new face by averaging parameters of input faces."""
    avg_face = Face(
        average_lists(face1.left_eye_params, face2.left_eye_params, weight),
        average_lists(face1.right_eye_params, face2.right_eye_params, weight),
        # average_lists(face1.left_brow_params, face2.left_brow_params, weight),
        # average_lists(face1.right_brow_params, face2.right_brow_params, weight),
        average_lists(face1.mouth_params, face2.mouth_params, weight),
        average_lists(face1.nose_params, face2.nose_params, weight))
    return avg_face

def average_lists(lst1, lst2, weight):
    return [weight*elt1 + (1-weight)*elt2 for elt1, elt2 in zip(lst1, lst2)]
        
    
        
        
