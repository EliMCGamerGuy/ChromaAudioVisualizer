from pychroma import Sketch
from random import randint
import pyaudio
from decimal import Decimal
import audioop
import os
import curses
vagueLoudnessValue = 0
cls = lambda: os.system('cls' if os.name=='nt' else 'clear')

global callback
def callback(in_data, frame_count, time_info, status): # Audio Capture Setup #1
    global vagueLoudnessValue
    vagueLoudnessValue = audioop.rms(bytes(in_data), WIDTH) #THIS NUMBER GOES UP IF I YELL!
    return in_data, pyaudio.paContinue

class MySketch(Sketch):
    config_path = 'config.json'

    def setup(self): #tuning controls
        self.reduction = 200
        self.reduceTimer = 20
        self.adjustAmount = 2
        self.avgAdjustThreshold = Decimal(1.25)
        self.reportClipping = True
        self.autoAdjust = True
        self.averagingSampleCount = 40
        self.colorDisableThreshhold = 10

        self.basered = 1 # color controls
        self.basegreen = 15
        self.baseblue = 1

        self.minred = 0 
        self.mingreen = 15
        self.minblue = 0

        self.maxred = 255
        self.maxgreen = 255
        self.maxblue = 255

        self.red = 0 # beyond this point are no more changable values
        self.green = 0
        self.blue = 0
        self.frame_rate = 30
        self.activeReduceTimer = 0
        self.avgClrAdjCalculator = []
        for i in range(1,self.averagingSampleCount):
            self.avgClrAdjCalculator.append(0)
        self.avgVLVCalculator = []
        for i in range(1,self.averagingSampleCount):
            self.avgVLVCalculator.append(0)
        self.avgClrAdj = 0
        self.avgVLV = 0
        self.keyboard.color_mode('rgb')
        self.mouse.color_mode("rgb")

        #Audio capture setup #2
        p = pyaudio.PyAudio()
        searching = True
        idtosearch = 0
        while searching:
            device_info = p.get_device_info_by_index(idtosearch)
            print(f"Testing audio device {device_info['name']}...")
            if "stereo mix" in device_info['name'].casefold() or "loopback" in device_info['name'].casefold() or "voicemeeter aux output" in device_info['name'].casefold():
                print(f"{device_info['name']} is loopback! Starting...")
                searching = False
                break
            else:
                print(f"{device_info['name']} isn't loopback, continuing...")
                idtosearch += 1
            continue
        global WIDTH
        global RATE
        global DEVICE
        WIDTH = 2
        RATE = int(device_info['defaultSampleRate'])
        DEVICE = device_info['index']
        print(device_info)
        
        global stream 
        stream = p.open(
            format=p.get_format_from_width(WIDTH),
            input_device_index=DEVICE,
            channels=2,
            rate=RATE,
            input=True,
            stream_callback=callback)

        print(f"Audio device {device_info['name']} accepted!")
        stream.start_stream()
        cls()
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

    def update(self):
        global stream
        if stream.is_stopped():
            stream.start_stream()
    
    
        coloradj = Decimal(vagueLoudnessValue / self.reduction)
        if coloradj == 0:
            coloradj = Decimal(0.000001)
        self.red = int(self.basered * coloradj)
        self.green = int(self.basegreen * coloradj)
        self.blue = int(self.baseblue * coloradj)
        if not self.activeReduceTimer == 0:
            self.activeReduceTimer -= 1

        self.avgClrAdjCalculator.append(coloradj)
        self.avgClrAdjCalculator.pop(0)

        for sample in self.avgClrAdjCalculator:
            self.avgClrAdj += sample
            
        try:
            self.avgClrAdj = Decimal(self.avgClrAdj/self.averagingSampleCount)
        except:
            self.avgClrAdj = Decimal(0.000001)

        self.avgVLVCalculator.append(vagueLoudnessValue)
        self.avgVLVCalculator.pop(0)

        for sample in self.avgVLVCalculator:
            self.avgVLV += sample
            
        try:
            self.avgVLV = Decimal(self.avgVLV/self.averagingSampleCount)
        except:
            self.avgVLV = Decimal(0.000001)

        if self.red < self.minred:
            self.red = self.minred
        if self.green < self.mingreen:
            self.green = self.mingreen
        if self.blue < self.minblue:
            self.blue = self.minblue

        isClipping = False
        clippingOn = ""
        if self.red > self.maxred or self.red > 255:
            self.red = self.maxred
            isClipping = True
            clippingOn = clippingOn+"R"
        else:
            clippingOn = clippingOn+" "
        if self.green > self.maxgreen or self.green > 255:
            self.green = self.maxgreen
            isClipping = True
            clippingOn = clippingOn+" G"
        else:
            clippingOn = clippingOn+"  "
        if self.blue > self.maxblue or self.blue > 255:
            self.blue = self.maxblue
            isClipping = True
            clippingOn = clippingOn+" B"
        else:
            clippingOn = clippingOn+"  "

        if self.red < 10:
            r = f"00{self.red}"
        elif self.red < 100:
            r = f"0{self.red}"
        else:
            r = self.red

        if self.green < 10:
            g = f"00{self.green}"
        elif self.green < 100:
            g = f"0{self.green}"
        else:
            g = self.green

        if self.blue < 10:
            b = f"00{self.blue}"
        elif self.blue < 100:
            b = f"0{self.blue}"
        else:
            b = self.blue

        adjustChange = "=0"
        if isClipping:
            self.reduction += self.adjustAmount
            adjustChange = f"+{self.adjustAmount}"
            self.activeReduceTimer = self.reduceTimer

        if self.activeReduceTimer == 0 and self.avgClrAdj <= self.avgAdjustThreshold and not (self.reduction - self.adjustAmount) < 1:
            self.reduction -= self.adjustAmount
            adjustChange = f"-{self.adjustAmount}"
            self.activeReduceTimer = self.reduceTimer
        
        level = "#"
        level = level + ("#" * int(coloradj * 8))
        
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "" +
            f"Updated Values: R{r} G{g} B{b}\n"+
           (f"CLIPPING ON: {clippingOn}\n" if self.reportClipping else "") +
            f"Vague Loudness Value: {vagueLoudnessValue}\n" +
            f"Average Vague Loudness Value: {self.avgVLV}\n" +
            f"Reduction Amount: {self.reduction}\n" +
            f"Color Adjustment: x{str(coloradj)}\n" +
            f"Average Color Adjustment: x{str(self.avgClrAdj)}\n" +
            f"Adjustment Change: {adjustChange}\n" +
            f"Adjustment Timer: {self.activeReduceTimer}\n" +
           (f"COLOR DISABLED\n" if self.avgVLV < self.colorDisableThreshhold else "COLOR ENABLED\n") +
            f"LEVEL: {level[:200]}\n")
        self.stdscr.refresh()

    
    def render(self):
        if self.avgVLV < self.colorDisableThreshhold:
            self.keyboard.clear()
            self.mouse.clear()
        else:
            self.keyboard.set_static([self.red, self.green, self.blue])
            self.mouse.set_static([self.red, self.green, self.blue])
    
