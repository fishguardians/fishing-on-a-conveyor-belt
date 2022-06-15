class MyImage:
    img = None
    name = ''

    def __init__(self,name):
        self.name = name
        self.img = cv2.imread(name)

myImage = MyImage('10_left.jpeg')
