import pygame
import random
import numpy as np
import librosa
from scipy.io.wavfile import write
pygame.init()
max_amount = 1000

# create a window
screen = pygame.display.set_mode((800,600))
pygame.display.set_caption("pygame Test")

# clock is used to set a max fps
clock = pygame.time.Clock()
FONT = pygame.font.SysFont('Arial', 20)


class Button:
    def __init__(self, x, y, width, height, text, on_click=None):

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.surface = pygame.Surface((self.width,self.height))
        self.rect = pygame.Rect(x,y,self.width,self.height)
        self.text = text
        self.on_click = on_click
        self.textsurf = FONT.render(self.text, False, (0,0,0))
        self.fillColors = {
            'normal': '#ffffff',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.isPressed = False

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.surface.fill(self.fillColors['normal'])
        if self.rect.collidepoint(mousePos):
            self.surface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.surface.fill(self.fillColors['pressed'])
                if not self.isPressed:
                    self.on_click()
                    self.isPressed = True
            else:
                self.isPressed = False
        self.surface.blit(self.textsurf, [
            self.rect.width/2 - self.textsurf.get_rect().width/2,
            self.rect.height/2 - self.textsurf.get_rect().height/2
        ])
        screen.blit(self.surface, self.rect)

def make_sound(pitch: float):
    sample = 44100
    # numpy stuff, i didn't write this myself.
    duration = 0.1
    each_sample_number = np.arange(duration*sample) # each sample index
    waveform = np.sin(2 * np.pi * each_sample_number * pitch / sample) # sine wave
    waveform_quiet = waveform * 0.3 # adjust volume
    waveform_integers = np.int16(waveform_quiet * 32767) # actual array made from waveform
    write('test.wav', sample, waveform_integers)






sound_arr = np.linspace(200,2000, num=1000)
print(type(sound_arr[0]))


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # clear the screen
    for pitch in sound_arr:
        make_sound(pitch)
        sound = pygame.mixer.Sound('test.wav')
        sound.play()
        pygame.time.delay(10)
        sound.stop()

    # draw to the screen
    # flip() updates the screen to make our changes visible
    pygame.display.flip()

    # how many updates per second

    clock.tick(1)
pygame.quit()