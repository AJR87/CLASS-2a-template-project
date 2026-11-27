import pygame
from audio.pipeline import AudioPipeline
from engines.base_engine import BACKGROUND_COLOR, BaseEngine
import time 
import math

deltatimeActive = True






class PygameEngine(BaseEngine):
    
    
    def setup(self) -> None:
        
        pygame.init()
        # color of the progress bar
        self.colorframe = (0, 255,0)
        # sets screen size
        self.screen = pygame.display.set_mode((self.width, self.height))

        

        self.widthUpdate = 0
        self.lastTime = time.perf_counter()
        # used to only print the delta time once 
        self.printedYet = False

        # sets both of these values to zero for later calculations
        self.deltaTotal = 0
        self.frameTotal = 0 

        # works out the track length
        self.tracklenSeconds = pygame.mixer.Sound(self.audioFile).get_length()
        # calculates how much the green bar should move based on the DISPLAY window size and the total track length in seconds
        self.pixelsPerSecond = self.width / self.tracklenSeconds
        # for calculating the width of the rectangle for amplitude
        self.rectwidth = 0
        self.smoothing = 10

        # bar width and slot size are set here so that the bars are centered based on the window width and they arent hard coded
        
        self.barWidth = 50
        self.slotSize = self.width / 6

        # settings for the text i use underneath the bars

        self.font = pygame.font.SysFont(None, 24)

        # used to sync the music to the bars

        self.musicPosition = 0

        self.backgroundColor = BACKGROUND_COLOR

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
            },
            "onset" : {
                "min" : float("inf"),
                "max" : float("-inf"),
                "color" : (255, 255, 255),
                "norm" : 0,
                "smooth" : 0
            }
        }
        
        # loads the music using the pygame engine ready to run it later when syncing the bars 
        
        pygame.mixer.music.load(self.audioFile)
        
        pygame.display.set_caption(self.title)

    # this is where im binding the arrow keys to the. background color using the pygame syntax that i found in the documentation
    
    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
            
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                self.backgroundColor = (40, 0, 80)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.backgroundColor = (0, 0, 80)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                self.backgroundColor = (80, 0, 80)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.backgroundColor = (40, 40, 80)
        return True

    def update(self, audio_features: dict) -> None:
        self.data = audio_features

        # this stops and starts the music manually instead of looping it so that it can eliminate the desync between the bars and the music output
        
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.play()
            
        # used to find out where in the music the program currently is at so that the bars can sync with it. uses max() and zero because get_pos() returns -1 which will make python count  down from the end of the song
        # and the % is used to loop back to the begining of the song

        self.musicPosition = max(0, pygame.mixer.music.get_pos() / 1000 ) % self.tracklenSeconds
        self.widthUpdate = (self.musicPosition / self.tracklenSeconds) * self.width

        currentTime = time.perf_counter()
        delta_time = min(currentTime - self.lastTime, 1)

        #this loop checks the the current reading from data and tests to see if it is lower than the minimum or higher than the maximum
        # it then checks to see if the max subract the min is equal to zero because if it is then python will give a divisable by zero error when you try to run the "fraction = line"
        # if isnt 0 then it works out the amount that the value is above the miniumum of the range and divides by the total range to see where in the range it lands
        # which converts it into a decimal which will allow me to put it into the height of the bars later
        # moves smooth part of the way towards norm each frame so the bars glide instead of jumping the share it moves depends on deltatime so its the same speed at any frame rate 6 is how fast it catches up


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

        self.lastTime = currentTime

        # this if statement prints the delta time only once like the worksheet asked me to do
        if self.printedYet == False:
            print(delta_time)
            self.printedYet = True
        self.deltaTotal += delta_time

        # this is where it works out and prints the framerate
        if self.deltaTotal >= 1:
            print(self.frameTotal / self.deltaTotal)
            self.frameTotal = 0
            self.deltaTotal = 0
        self.frameTotal +=1
        # this line of code is what progresses the length of the green line by adding the step size ontop of the value of width size
       
        # if deltatimeActive == False:
        #     self.widthUpdate += self.stepSize
        # else:
        #     self.widthUpdate += self.pixelsPerSecond * delta_time
        
        # this is the line that takes amplitude from and sets rectWidth to 1000 times that value because otherwise you wouldnt be able to see the value changing because the number is too small
        self.rectwidth = int(self.data["amplitude"] * 1000)

        # this is the smoothing that is used to make the red bar that represents amlitude for the frame move more fluidly.
        # instead of just jumping to the current value of the window. it does this with rectwidth
        self.smoothing = (self.smoothing + ((self.rectwidth - self.smoothing) * (1 - math.exp(-6 * delta_time))))
        

    def render(self) -> None:
        self.screen.fill(self.backgroundColor)

        # the rectangles color is different depending on what i have put in the dictionary in self.dataMinMax
        # the x axis of where each bar is on the screen is dependant on the width of the screen and is calculated by multiplying the slot size by what slot the bar will fit into and subtracting that by the width of the bar divided by two so that the center of the bar is at the evenly spaced slots on the screen
        # the y axis of where each bar is on the screen is set 600 subtract to the value of smooth multiplied by 300 due to the way that pygame calculates the y axis
        # the width the bar is set to self.barWidth and can be changed in setup()
        # the height of the actual bar is set to smooth multiplied by 300 and since pygame calculates it downwards it extends to 600

        pygame.draw.rect(self.screen, self.dataMinMax["amplitude"]["color"], pygame.Rect(int(self.slotSize * 1 - self.barWidth / 2),600 - int(self.dataMinMax["amplitude"]["smooth"] * 300) ,self.barWidth,int(self.dataMinMax["amplitude"]["smooth"] * 300)))

        # text is set self.font.render which uses the the name of the value that is being recorded and true means it has smooth edges and the value at the end is the color of the text 
        # self.screen.blit uses the text variable to decide what is going to be outputted onto the screen and its location is decided the same way as the bars using the slots and finds out the text width with .get_width dividing it by two and subtracting it from the slotsize so the center lines up 

        text = self.font.render("amplitude", True, (255,255,255))
        self.screen.blit(text, (int(self.slotSize * 1 - text.get_width() / 2), 610) )

       
        pygame.draw.rect(self.screen, self.dataMinMax["bass"]["color"], pygame.Rect(int(self.slotSize * 2 - self.barWidth / 2),600 - int(self.dataMinMax["bass"]["smooth"] * 300) ,self.barWidth,int(self.dataMinMax["bass"]["smooth"] * 300)))

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
