from gpiozero import LED
import time
import threading 

class SevenSeg:
    def __init__(self, segs=[-1,-1,-1,-1,-1,-1,-1], digits=[-1,-1,-1]):
        for i in segs:
            if i == -1:
                print("Did not specify enough segments")
                return
        
        self.a = LED(segs[0])
        self.b = LED(segs[1])
        self.c = LED(segs[2])
        self.d = LED(segs[3])
        self.e = LED(segs[4])
        self.f = LED(segs[5])
        self.g = LED(segs[6])
          
        self.d1 = LED(digits[0])
        self.d2 = LED(digits[1])
        self.d3 = LED(digits[2])

        self.value1 = 0
        self.value2 = 0
        self.value3 = 0
                
        self.font = dict([(-1, []),
                (0, [self.a, self.b, self.c, self.d, self.e, self.f]),
                (1, [self.b, self.c]),
                (2, [self.a, self.b, self.g, self.e, self.d]),
                (3, [self.a, self.b, self.g, self.c, self.d]),
                (4, [self.f, self.g, self.b, self.c]),
                (5, [self.a, self.f, self.g, self.c, self.d]),
                (6, [self.a, self.f, self.g, self.c, self.d, self.e]),
                (7, [self.a, self.b, self.c]),
                (8, [self.a, self.b, self.c, self.d, self.e, self.f, self.g]),
                (9, [self.a, self.b, self.c, self.f, self.g])])


    def clear(self):
        self.a.off()
        self.b.off()
        self.c.off()
        self.d.off()
        self.e.off()
        self.f.off()
        self.g.off()
        self.d1.off()
        self.d2.off()
        self.d3.off()
    
    def displayValue(self):
        while True:
            self.d1.on()
            segs = self.font[self.value1]
            for s in segs:
                s.on()
            self.clear()
            
            self.d2.on()
            segs = self.font[self.value2]
            for s in segs:
                s.on()
            self.clear()

            self.d3.on()
            segs = self.font[self.value3]
            for s in segs:
                s.on()
            self.clear()

    def updateValue(self, value):
        # Limit to three digits

        if value>999:
            value = 999
        
        self.value1 = (value - value%100)//100
        self.value2 = ((value-self.value1*100) - value%10)//10
        self.value3 = value%10

        # Erase first digit
        if value <= 99:
            self.value1 = -1
        
        # Erase second digit
        if value <= 9:
            self.value2 = -1

    def start(self):
        displayThread = self.thread(self.displayValue)
        displayThread.start()

    class thread (threading.Thread):
        def __init__(self, func):
            threading.Thread.__init__(self)
            self.func = func 

        def run(self):
           self.func()

    def displayLoading(self):
        path = [(self.d1, self.a), (self.d2, self.a), (self.d3, self.a),
                (self.d3, self.b), (self.d3, self.g), (self.d2, self.g),
                (self.d1, self.g), (self.d1, self.e), (self.d1, self.d),
                (self.d2, self.d), (self.d3, self.d), (self.d3, self.c),
                (self.d3, self.g), (self.d2, self.g), (self.d1, self.g),
                (self.d1, self.f)]
        
        index = 0
        while True:
            seg = path[index]
            seg1 = path[index-1]
            seg2 = path[index-2]

            seg[0].on()
            seg[1].on()
            seg1[0].on()
            seg1[1].on()
            seg2[0].on()
            seg2[0].on()
            time.sleep(0.15)
            seg[0].off()
            seg[1].off()
            seg1[0].off()
            seg1[1].off()
            seg2[0].off()
            seg2[0].off()
            index += 1
            if index == len(path):
                index = 0

if __name__ == '__main__':
    disp = SevenSeg([18, 23, 24, 25, 8, 7, 12], [2, 3, 4])
    
    disp.value1 = 1
    disp.value2 = 2
    disp.value3 = 3

    disp.displayLoading()
