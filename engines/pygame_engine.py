import pygame
from audio.pipeline import AudioPipeline
from engines.base_engine import BACKGROUND_COLOR, BaseEngine
import time 

deltatimeActive = False

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
        
        pygame.display.set_caption(self.title)

    def handle_events(self) -> bool:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return False
        return True

    def update(self, audio_features: dict) -> None:
        currentTime = time.perf_counter()
        delta_time = min(currentTime - self.lastTime, 0.1)
            
        # this if statement prints the delta time only once like the worksheet asked me to do
        self.lastTime = currentTime
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
        self.data = audio_features
        # this line of code is what progresses the length of the green line by adding the step size ontop of the value of width size
        if deltatimeActive == False:
            self.widthUpdate += self.stepSize
        else:
            self.widthUpdate += self.pixelsPerSecond * delta_time
        # this is the line that takes amplitude from and sets rectWidth to 1000 times that value because otherwise you wouldnt be able to see the value changing because the number is too small
        self.rectwidth = int(self.data["amplitude"] * 1000)
        

    def render(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        # this is the red line that extends its width based on the amplitude
        pygame.draw.rect(self.screen, self.coloramp, pygame.Rect(30,30,self.rectwidth,30))
        
        # this is what creates the green bar that extends based on time
        # it starts at 0 instead of 30 because its cooded to get right to the end of the window at the same point the window tops genorating frames
        pygame.draw.rect(self.screen, self.colorframe, pygame.Rect(0,70,self.widthUpdate,30))
        pygame.display.flip()
        # time.sleep(0.03)
        

    def teardown(self) -> None:
        pygame.quit()
