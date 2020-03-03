
add_library('controlp5')

cp5 = None
slider1 = None

def setup():
    global cp5, slider1
    size(500,500)
    cp5 = ControlP5(this)
    
    slider1 = (
        cp5
        .addSlider("slider")
        .setSize(200,20)
        .setPosition(20,20)
        .setRange(0,255))
    slider1.label = "Background"
    
def draw():
    #cp5.draw()
    background(slider1.getValue())
    
    
