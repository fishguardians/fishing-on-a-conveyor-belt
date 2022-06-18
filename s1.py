import numpy as np

class Segments:
    def __init__(self):
        # create a 7seg model
        self.flags = [];
        self.segments = [];
        h1 = [[0, 1.0],[0, 0.1]];       # 0
        h2 = [[0, 1.0],[0.45, 0.55]];   # 1
        h3 = [[0, 1.0],[0.9, 1.0]];     # 2
        vl1 = [[0, 0.2],[0, 0.5]];      # 3 # upper-left
        vl2 = [[0, 0.2],[0.5, 1.0]];    # 4
        vr1 = [[0.8, 1.0],[0, 0.5]];    # 5 # upper-right
        vr2 = [[0.8, 1.0], [0.5, 1.0]]; # 6
        self.segments.append(h1);
        self.segments.append(h2);
        self.segments.append(h3);
        self.segments.append(vl1);
        self.segments.append(vl2);
        self.segments.append(vr1);
        self.segments.append(vr2);

    # process an image and set flags
    def digest(self, number):
        # reset flags
        self.flags = [];

        # check res to see if it's a one
        h, w = number.shape[:2];
        if w < 0.5 * h:
            self.flags.append(5);
            self.flags.append(6);
            return;

        # check for segments
        for a in range(len(self.segments)):
            seg = self.segments[a];
            # get bounds
            xl, xh = seg[0];
            yl, yh = seg[1];
            # convert to pix coords
            xl = int(xl * w);
            xh = int(xh * w);
            yl = int(yl * h);
            yh = int(yh * h);
            sw = xh - xl;
            sh = yh - yl;
            # check
            count = np.count_nonzero(number[yl:yh, xl:xh] == 255);
            if count / (sh * sw) > 0.5: # 0.5 is a sensitivity measure
                self.flags.append(a);

    # returns the stored number (stored in self.flags)
    def getNum(self):
        # hardcoding outputs
        if self.flags == [0,2,3,4,5,6]:
            return 0;
        if self.flags == [5,6]:
            return 1;
        if self.flags == [0,1,2,4,5]:
            return 2;
        if self.flags == [0,1,2,5,6]:
            return 3;
        if self.flags == [1,3,5,6]:
            return 4;
        if self.flags == [0,1,2,3,6]:
            return 5;
        if self.flags == [0,1,2,3,4,6]:
            return 6;
        if self.flags == [0,5,6]:
            return 7;
        if self.flags == [0,1,2,3,4,5,6]:
            return 8;
        if self.flags == [0,1,2,3,5,6]:
            return 9;
        # ERROR
        return -1;