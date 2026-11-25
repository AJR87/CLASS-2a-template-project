import pygame
from audio.pipeline import AudioPipeline
from engines.base_engine import BACKGROUND_COLOR, BaseEngine
import time 
import math

deltatimeActive = True

AUDIO_FILE = "/Users/ajr/Documents/CLASS-2a-template-project/audio/ytmp3free.cc_neffex-free-me-copyright-free-no134-youtubemp3free.org.mp3"


pipelineInstance = AudioPipeline(file_path=AUDIO_FILE)

pipelineInstance.load()


class PygameEngine(BaseEngine):
    
    
    def setup(self) -> None:
        
        pygame.init()
        # color of the framerate bar
        self.colorframe = (0, 255,0)
        # color of amp bar
        self.coloramp = (255,0,0)
        # sets screen size
        self.screen = pygame.display.set_mode((self.width, self.height))
        # works out the total frames in the signal by taking the length of the signal array and dividing it by the window size and uses floor division 
        # so that it is a whole number because theres no such thing as half a frame
        self.frameCount = (len(pipelineInstance.signal) // pipelineInstance.window_size)
        # divides the width of the window by the amoiunt of frsmes so that the bar extends fully to the end of the window and doesnt extend too far 
        self.stepSize = self.width / self.frameCount
        self.widthUpdate = 0    
        self.lastTime = time.perf_counter()
        # used to only print the delta time once 
        self.printedYet = False

        # sets both of these values to zero for later calculations
        self.deltaTotal = 0
        self.frameTotal = 0 

        # works out the track length
        self.tracklenSeconds = len(pipelineInstance.signal) / 22050
        # calculates how much the green bar should move based on the DISPLAY window size and the total track length in seconds
        self.pixelsPerSecond = self.width / self.tracklenSeconds
        # for calculating the width of the rectangle for amplitude
        self.rectwidth = 0
        self.smoothing = 10
        
        self.barWidth = 50
        self.slotSize = self.width / 6


        self.font = pygame.font.SysFont(None, 24)

        # this is the dictionary im using to display the values correctly
        # i am using the range of the minimum value and tghe maximum value to decide how tall the bar is on the visualisation
        # this is because some of the values are in decimals and are really small and some of them are really large so it would be impossible to see some of the other values change if it was based on only the raw numbers
        # norm is the actual value that is being read by the get features function and the smooth value is the ammount that is actually being shown and is being calculated using the math.exp function later on

        
        self.dataMinMax = {
            "amplitude": {
                "min" : float("inf"),
                "max" : float("-inf"),
                "color" : (255, 0, 0),
                "norm" : 0,
                "smooth" : 0},
            "bass" : {
                "min" : float("inf"),
                "max" : float("-inf"),
                "color" : (0, 255, 125),
                "norm" : 0,
                "smooth" : 0},
            "mid" : {
                "min" : float("inf"),
                "max" : float("-inf"),
                "color" : (255, 255, 0),
                "norm" : 0,
                "smooth" : 0},
            "treble" : {
                "min" : float("inf"),
                "max" :float("-inf"),
                "color": (0, 0, 255),
                "norm" : 0,
                "smooth" : 0},
                
            "cent" : {
                "min" : float("inf"),
                "max" : float("-inf"),
                "color" : (255, 0, 255),
                "norm" : 0,
                "smooth" : 0
            }
        }
        
        pygame.display.set_caption(self.title)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        return True

    def update(self, audio_features: dict) -> None:
        self.data = audio_features

        currentTime = time.perf_counter()
        delta_time = min(currentTime - self.lastTime, 1)

        #this loop checks the the current reading from data and tests to see if it is lower than the minimum or higher than the maximum
        # it then checks to see if the max subract the min is equal to zero because if it is then python will give a divisable by zero error when you try to run the "fraction = line"
        # if isnt 0 then it works out the amount that the value is above the miniumum of the range and divides by the total range to see where in the range it lands
        # which converts it into a decimal which will allow me to put it into the height of the bars later
        # 


        for feature in self.dataMinMax:
            if self.data[feature] > self.dataMinMax[feature]["max"]:
                self.dataMinMax[feature]["max"] = self.data[feature]
            
            if self.data[feature] < self.dataMinMax[feature]["min"]:
                self.dataMinMax[feature]["min"] = self.data[feature]

            if self.dataMinMax[feature]["max"] - self.dataMinMax[feature]["min"] == 0:
                fraction = 0
            else:
                fraction = (self.data[feature] - self.dataMinMax[feature]["min"]) / (self.dataMinMax[feature]["max"] - (self.dataMinMax[feature]["min"]))
            
            self.dataMinMax[feature]["norm"] = fraction

            self.dataMinMax[feature]["smooth"] = self.dataMinMax[feature]["smooth"] + (self.dataMinMax[feature]["norm"] - self.dataMinMax[feature]["smooth"]) * (1 - math.exp(-6 * delta_time))

        # this if statement prints the delta time only once like the worksheet asked me to do
        self.lastTime = currentTime
        if self.printedYet == False:
            print(delta_time)
            self.printedYet = True
        self.deltaTotal += delta_time

        # this is where it works out and prints the framerate
        if self.deltaTotal >= 0.1:
            print(self.frameTotal / self.deltaTotal)
            self.frameTotal = 0
            self.deltaTotal = 0
        self.frameTotal +=1
        # this line of code is what progresses the length of the green line by adding the step size ontop of the value of width size
        if deltatimeActive == False:
            self.widthUpdate += self.stepSize
        else:
            self.widthUpdate += self.pixelsPerSecond * delta_time
        # this is the line that takes amplitude from and sets rectWidth to 1000 times that value because otherwise you wouldnt be able to see the value changing because the number is too small
        self.rectwidth = int(self.data["amplitude"] * 1000)

        # this is the smoothing that is used to make the red bar that represents amlitude for the frame move more fluidly.
        # instead of just jumping to the current value of the window. it does this with rectwidth
        self.smoothing = (self.smoothing + ((self.rectwidth - self.smoothing) * (1 - math.exp(-6 * delta_time))))
        

    def render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        pygame.draw.rect(self.screen, self.dataMinMax["amplitude"]["color"], pygame.Rect(int(self.slotSize * 1 - self.barWidth / 2),600 -int(self.dataMinMax["amplitude"]["smooth"] * 300) ,self.barWidth,int(self.dataMinMax["amplitude"]["smooth"] * 300)))
        text = self.font.render("amplitude", True, (255,255,255))
        self.screen.blit(text, (int(self.slotSize * 1 - text.get_width() / 2), 610) )
       
        pygame.draw.rect(self.screen, self.dataMinMax["bass"]["color"], pygame.Rect(int(self.slotSize * 2 - self.barWidth / 2),600 -int(self.dataMinMax["bass"]["smooth"] * 300) ,self.barWidth,int(self.dataMinMax["bass"]["smooth"] * 300)))

        text = self.font.render("bass", True, (255,255,255))
        self.screen.blit(text, (int(self.slotSize * 2 - text.get_width() / 2), 610) )


        pygame.draw.rect(self.screen, self.dataMinMax["mid"]["color"], pygame.Rect(int(self.slotSize * 3 - self.barWidth / 2),600 -int(self.dataMinMax["mid"]["smooth"] * 300) ,self.barWidth,int(self.dataMinMax["mid"]["smooth"] * 300)))

        text = self.font.render("mid", True, (255,255,255))
        self.screen.blit(text, (int(self.slotSize * 3 - text.get_width() / 2), 610) )


        pygame.draw.rect(self.screen, self.dataMinMax["treble"]["color"], pygame.Rect(int(self.slotSize * 4 - self.barWidth / 2),600 -int(self.dataMinMax["treble"]["smooth"] * 300) ,self.barWidth,int(self.dataMinMax["treble"]["smooth"] * 300)))
        text = self.font.render("treble", True, (255,255,255))
        self.screen.blit(text, (int(self.slotSize * 4 - text.get_width() / 2), 610) )

        pygame.draw.rect(self.screen, self.dataMinMax["cent"]["color"], pygame.Rect(int(self.slotSize * 5 - self.barWidth / 2),600 -int(self.dataMinMax["cent"]["smooth"] * 300) ,self.barWidth,int(self.dataMinMax["cent"]["smooth"] * 300)))
        text = self.font.render("cent", True, (255,255,255))
        self.screen.blit(text, (int(self.slotSize * 5 - text.get_width() / 2), 610) )
        
        
        
        # this is what creates the green bar that extends based on time
        # it starts at 0 instead of 30 because its cooded to get right to the end of the window at the same point the window tops genorating frames
        pygame.draw.rect(self.screen, self.colorframe, pygame.Rect(0,70,self.widthUpdate,30))
        pygame.display.flip()
        # time.sleep(0.03)
        

    def teardown(self) -> None:
        pygame.quit()
