import pygame
import random

pygame.init()
screen_size = (1300, 650)

# create a window
screen = pygame.display.set_mode(screen_size)
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

    def process(self, screen):
        mousePos = pygame.mouse.get_pos()
        self.surface.fill(self.fillColors['normal'])
        if self.rect.collidepoint(mousePos):
            self.surface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0]:
                self.surface.fill(self.fillColors['pressed'])
                if not self.isPressed:
                    plotter.toggleGen(screen, self.on_click)
                    self.isPressed = True
            else:
                self.isPressed = False
        self.surface.blit(self.textsurf, [
            self.rect.width/2 - self.textsurf.get_rect().width/2,
            self.rect.height/2 - self.textsurf.get_rect().height/2
        ])
        screen.blit(self.surface, self.rect)

class InputBox:
    def __init__(self, x, y, width, height, inactive_text, on_enter):
        self.rect = pygame.Rect(x,y,width, height)
        self.inactive_color = (0,255,0)
        self.active_color = (255,0,0)
        self.color = self.inactive_color
        self.text = ""
        self.txt_surface = FONT.render(self.text, True, "white")
        self.inactive_surf = FONT.render(inactive_text, True, (47,50,56))
        self.current_surf = self.inactive_surf
        self.active = False
        self.on_enter = on_enter


    def handle_event(self, event, screen):
        x, y, w, h = self.rect
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.on_enter(self.text,screen)
                pygame.draw.rect(screen, "black", pygame.Rect(x + 2, y + 2, w, h))
                self.text = ""
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                # deletes last character
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        self.txt_surface = FONT.render(self.text, True, "white")

    def handle_surfaces(self,screen):
        x,y,w,h = self.rect
        if self.text == "":
            # clear the input box
            pygame.draw.rect(screen, "black", pygame.Rect(x+2,y+2,w,h))
            self.current_surf = self.inactive_surf
        else:
            if self.active:
                pygame.draw.rect(screen, "black", pygame.Rect(x + 2, y + 2, w, h))
            self.current_surf = self.txt_surface
        if self.active:
            self.color = self.active_color
        else:
            self.color = self.inactive_color

    def process(self, screen):
        self.handle_surfaces(screen)
        screen.blit(self.current_surf, (self.rect.x + 24, self.rect.y + 8))
        # Blit the rect.
        pygame.draw.rect(screen, self.color, self.rect, 2)


class ArrayPlotter:
    gradient = tuple(zip(
        (list(reversed(range(256))) + [0] * 256),
        (list(range(256)) + list(reversed(range(256)))),
        ([0] * 256 + list(range(256)))))

    # sin gle t o n.
    def __init__(self):
        self.array = []
        self.finished = False
        self.currentgen = None

    def initialize_array(self,length,screen):
        for char in str(length):
            if not char.isnumeric():
                return
        length = int(length)
        self.array = []
        for i in range(length):
            self.array.append(i)
        self.draw_whole_array(screen)

    def draw_whole_array(self, screen, clear=True, color_info={}):
        # leaving a portion of the screen for UI
        size = (screen.get_size()[0] - 300, screen.get_size()[1])

        if clear:
            self.clear(screen)
        # dividing makes the bars fit on the screen no matter how many there are
        width = size[0] / len(self.array)

        base_height = size[1] / len(self.array)

        for i in range(len(self.array)):
            height = self.array[i] * base_height + base_height
            x = i * width
            y = size[1] - height
            if i in color_info:
                pygame.draw.rect(screen, color_info[i], pygame.Rect(x, y, width, height))
            else:
                pygame.draw.rect(screen, "white", pygame.Rect(x, y, width, height))

    def shuffle(self, screen):
        for i in range(len(self.array) - 1, 0, -1):
            # pick a random index from 0 to i
            j = random.randint(0, i)

            # swap arr[i] with the element at random index
            self.array[i], self.array[j] = self.array[j], self.array[i]
            self.draw_whole_array(screen)
            yield True

    def clear(self, screen):
        rect = pygame.Surface((1000, 650))
        rect.fill("black")
        screen.blit(rect, (0, 0))

    def finish(self, screen):
        for i in range(len(self.array)):
            color_dict = {}
            for j in range(i+1):
                color_dict[j] = ArrayPlotter.gradient[round(j * (len(ArrayPlotter.gradient) / len(self.array)))]
            self.draw_whole_array(screen, False, color_dict)
            yield True



    def toggleGen(self, screen, gen):
        # abstraction innit
        self.currentgen = gen(screen)
    def toggleFinish(self, screen):
        self.currentgen = self.finish(screen)
    def process(self, screen):

        if not self.finished:
            self.toggleFinish(screen)
            self.finished = True
        if not self.finished:
            self.draw_whole_array(screen)
        try:
            if self.currentgen is not None:
                next(self.currentgen)
        except StopIteration:
            if self.currentgen.__name__ == self.finish.__name__ or self.array != sorted(self.array):
                self.finished = True
            else:
                self.finished = False
            self.currentgen = None



plotter = ArrayPlotter()
plotter.initialize_array(100,screen)
def bubble_sort(screen):
    array = plotter.array
    sorted = True
    for i in range(len(array)):
        for j in range(len(array)-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                sorted = False
            plotter.draw_whole_array(screen,color_info={j+1: "red"})
            yield True
        if sorted:
            return


def insertion_sort(screen):
    array = plotter.array
    for i in range(1,len(array)):
        key = array[i]
        while True:
            unsorted = i > 0 and array[i-1] > key
            if not unsorted:
                break
            array[i] = array[i-1]
            i -= 1
            array[i] = key
            plotter.draw_whole_array(screen,color_info={i:"red"})
            yield True

def merge_sort(screen):
    array = plotter.array
    def merge(array,l,m,r):
        # n1 is length of left subarray, n2 is length of right subarray
        n1 = m - l + 1
        n2 = r - m
        L = [0] * (n1)
        R = [0] * (n2)
        for i in range(n1):
            # filling L with left part of array
            L[i] = array[l+i]
        for j in range(n2):
            # filling R with right part of array
            R[j] = array[m+1+j]

        i = 0 # index of left subarray
        j = 0 # index of right subarray
        k = l # index of main array
        while i < n1 and j < n2:
            # comparing elements of left array and right array, if left is smaller than it is put first in the array
            if L[i] <= R[j]:
                array[k] = L[i]
                i += 1
            else:
                array[k] = R[j]
                j += 1
            k += 1
            plotter.draw_whole_array(screen, color_info={k:"red"})
            yield True
        while i < n1:
            # if there are still unprocessed element in left subarray they are added to main array
            array[k] = L[i]
            i += 1
            k += 1
            plotter.draw_whole_array(screen, color_info={k:"red"})
            yield True
        while j < n2:
            # if there are still unprocessed element in right subarray they are added to main array
            array[k] = R[j]
            j += 1
            k += 1
            plotter.draw_whole_array(screen, color_info={k: "red"})
            yield True
        return array
    def merge_sort(array,l,r):
        if l < r:
            # midpoint
            m = (l+(r-1))//2
            yield from merge_sort(array, l, m)
            yield from merge_sort(array, m+1, r)
            yield from merge(array,l,m,r)
    yield from merge_sort(array,0,len(array)-1)
    return array



buttons = [Button(1050, 20, 100, 50, "Shuffle", plotter.shuffle),
           Button(1050, 70, 150, 50, "Bubble Sort", bubble_sort),
           Button(1050,120,150,50,"Insertion Sort", insertion_sort),
           Button(1050,170,150,50,"Merge Sort", merge_sort)]
input_boxes = [InputBox(1050, 600, 200, 40, "Set Array Length", plotter.initialize_array)]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in input_boxes:
            box.handle_event(event,screen)

    plotter.process(screen)
    # clear the screen
    for button in buttons:
        button.process(screen)
    for box in input_boxes:
        box.process(screen)
    # draw to the screen
    # flip() updates the screen to make our changes visible
    pygame.display.flip()

    # how many updates per second
    clock.tick(500)

pygame.quit()