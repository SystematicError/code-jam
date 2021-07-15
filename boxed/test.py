
import playsound
def play():
    playsound.playsound('boxed/music/up-down.wav')


while True:
    select = int(input('Enter value'))
    if select== 1:
        play()

# import pygame
# pygame.init()

# pygame.mixer.init()
# sounda = pygame.mixer.Sound('boxed\music\music.mp3')
# sounda.play()

# while pygame.mixer.get_busy():
#     pygame.time.delay(10)
#     pygame.event.poll()