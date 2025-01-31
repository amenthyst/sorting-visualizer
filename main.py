import pygame
import random

pygame.init()

# TODO: shell sort, bucket sort, selection sort, bogo sort, screen saver mode
max_amount = 1000

# create a window
screen = pygame.display.set_mode(flags=pygame.FULLSCREEN)
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
                    plotter.toggleGen(self.on_click)
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


    def handle_event(self, event):
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
                self.on_enter(self.text)
                pygame.draw.rect(screen, "black", pygame.Rect(x + 2, y + 2, w, h))
                self.text = ""
                self.active = False
            elif event.key == pygame.K_BACKSPACE:
                # deletes last character
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
        self.txt_surface = FONT.render(self.text, True, "white")

    def handle_surfaces(self):
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

    def process(self):
        self.handle_surfaces()
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
        self.endless = True

        # for endless mode
        self.current_sort = 0
        self.sorting = False
        self.shuffling = False
        self.finishing = False
        self.lengths = [100, 200, max_amount, max_amount, 300, max_amount, max_amount, max_amount, max_amount]

    def initialize_array(self,length):
        self.currentgen = None
        for char in str(length):
            if not char.isnumeric():
                return
        length = int(length)
        self.array = []
        for i in range(length):
            self.array.append(i)
        self.draw_whole_array()

    def draw_whole_array(self, clear=True, color_info={}):
        # leaving a portion of the screen for UI
        size = (screen.get_size()[0] - (screen.get_size()[0] - max_amount), screen.get_size()[1])

        if clear:
            self.clear()
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

    def shuffle(self):
        for i in range(len(self.array) - 1, 0, -1):
            # pick a random index from 0 to i
            j = random.randint(0, i)

            # swap arr[i] with the element at random index
            self.array[i], self.array[j] = self.array[j], self.array[i]
            self.draw_whole_array()
            yield True

    def clear(self):
        rect = pygame.Surface((screen.get_size()[0]-(screen.get_size()[0] - max_amount), screen.get_size()[1]))
        rect.fill("black")
        screen.blit(rect, (0, 0))

    def finish(self):
        for i in range(len(self.array)):
            color_dict = {}
            for j in range(i+1):
                color_dict[j] = ArrayPlotter.gradient[round(j * (len(ArrayPlotter.gradient) / len(self.array)))]
            self.draw_whole_array(color_info=color_dict)
            yield True



    def toggleGen(self, gen):
        # abstraction innit
        self.currentgen = gen()
    def toggleFinish(self):
        self.currentgen = self.finish()
    def process(self):

        if not self.finished:
            self.toggleFinish()
            self.finished = True
        if not self.finished:
            self.draw_whole_array()

        try:
            if self.currentgen is not None:
                next(self.currentgen)
        except StopIteration:
            if self.currentgen.__name__ == self.finish.__name__ or self.array != sorted(self.array):
                self.finished = True
            else:
                self.finished = False
            self.currentgen = None

    def process_endless(self, sorts):
        if self.currentgen is None:
            self.currentgen = self.finish()
        sorting_names = [x.__name__ for x in sorts]
        finish = self.finish.__name__
        shuffle = self.shuffle.__name__
        if self.finishing:
            self.currentgen = self.finish()
            self.finishing = False
        if self.shuffling:
            self.currentgen = self.shuffle()
            self.shuffling = False
        if self.sorting:
            self.currentgen = sorts[self.current_sort]()
        try:
            if self.currentgen is not None:
                next(self.currentgen)
        except StopIteration:
            name = self.currentgen.__name__
            if name == finish:
                pygame.time.delay(1000)
                self.initialize_array(self.lengths[self.current_sort])
                self.currentgen = self.shuffle()
            elif name == shuffle:
                pygame.time.delay(1500)
                self.currentgen = sorts[self.current_sort]()
            elif name in sorting_names:
                self.currentgen = self.finish()
                self.current_sort += 1
                if self.current_sort >= len(sorts):
                    self.current_sort = 0







plotter = ArrayPlotter()
plotter.initialize_array(100)
def bubble_sort():
    array = plotter.array
    sorted = True
    for i in range(len(array)):
        for j in range(len(array)-i-1):
            if array[j] > array[j+1]:
                array[j], array[j+1] = array[j+1], array[j]
                sorted = False
            plotter.draw_whole_array(color_info={j+1: "red"})
            yield True
        if sorted:
            return


def insertion_sort():
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
            plotter.draw_whole_array(color_info={i:"red"})
            yield True

def merge_sort():
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
            plotter.draw_whole_array(color_info={k:"red"})
            yield True
        while i < n1:
            # if there are still unprocessed element in left subarray they are added to main array
            array[k] = L[i]
            i += 1
            k += 1
            plotter.draw_whole_array(color_info={k:"red"})
            yield True
        while j < n2:
            # if there are still unprocessed element in right subarray they are added to main array
            array[k] = R[j]
            j += 1
            k += 1
            plotter.draw_whole_array(color_info={k: "red"})
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


def quick_sort():
    array = plotter.array

    def partition(array, low, high):
        pivot = array[high]
        i = low - 1
        for j in range(low, high):
            if array[j] < pivot:
                i += 1
                array[i], array[j] = array[j], array[i]
                plotter.draw_whole_array(color_info={i + 1: "red", high: "blue"})
                yield True

        array[i + 1], array[high] = array[high], array[i + 1]
        plotter.draw_whole_array(color_info={i + 1: "red", high: "blue"})
        return i + 1

    def quick_sort(array, low, high):
        if low < high:
            pi = yield from partition(array, low, high)
            yield from quick_sort(array, low, pi - 1)
            yield from quick_sort(array, pi + 1, high)

    yield from quick_sort(array, 0, len(array) - 1)


def shaker_sort():
    array = plotter.array
    start = 0
    end = len(array)-1
    swapped = True
    while swapped:
        swapped = False
        # forwards
        for i in range(start,end):
            if array[i] > array[i+1]:
                array[i], array[i+1] = array[i+1], array[i]
                swapped = True
                plotter.draw_whole_array(color_info={i: "red"})
                yield True
        if not swapped:
            break
        swapped = False
        end -= 1
        # backwards
        for i in range(end-1, start-1, -1):
            if array[i] > array[i+1]:
                array[i], array[i + 1] = array[i + 1], array[i]
                swapped = True
                plotter.draw_whole_array(color_info={i: "red"})
                yield True
        if not swapped:
            break
        start += 1

def counting_sort():
    array = plotter.array
    M = max(array)
    count_array = [0] * (M+1)
    # fill count array
    for num in array:
        count_array[num] += 1
    # get prefix sum of array
    for i in range(1,M+1):
        count_array[i] += count_array[i-1]
    output = [0] * len(array)
    for i in range(len(array)-1, -1, -1):
        output[count_array[array[i]] - 1] = array[i]
        count_array[array[i]] -= 1
        plotter.draw_whole_array(color_info={i:"red"})
        yield True
    for i in range(len(array)):
        array[i] = output[i]
        plotter.draw_whole_array(color_info={i: "red"})
        yield True

def heap_sort():
    array = plotter.array
    def heapify(array, length, i):
        # i is index of root
        largest = i
        # left child of root node
        left = 2 * i + 1
        # right child of root node
        right = 2 * i + 2

        # if left child is bigger than root node
        if left < length and array[left] > array[largest]:
            largest = left
        # if right child is bigger than root node
        if right < length and array[right] > array[largest]:
            largest = right

        # if largest is not root
        if largest != i:
            array[i], array[largest] = array[largest], array[i]

            plotter.draw_whole_array(color_info={largest: "red"})
            yield True
            yield from heapify(array,length,largest)
    def heap_sort(array):
        length = len(array)

        # build heap
        for i in range(length, -1, -1):
            yield from heapify(array,length,i)

        # extract root (max element) from heap 1 by 1
        for i in range(length-1, 0, -1):
            array[i], array[0] = array[0], array[i]
            plotter.draw_whole_array(color_info={i: "red"})
            yield True
            # heapify after max element is taken, get next max element
            yield from heapify(array,i,0)
        return array
    yield from heap_sort(array)

def tim_sort():
    array = plotter.array
    MIN = 32
    def calcRun(length):
        runs = 0
        while length >= MIN:
            # bitwise stuff idk im just copying this algorithm
            runs |= length & 1
            length >>= 1
        return runs + length
    def insertionSort(array, left, right):
        for i in range(left+1, right+1):
            j = i
            while j > left and array[j] < array[j-1]:
                array[j], array[j-1] = array[j-1], array[j]
                plotter.draw_whole_array(color_info={j: "red"})
                yield True
                j -= 1
    def merge(array, l, m, r):
        len1 = m - l + 1
        len2 = r - m
        left = []
        right = []
        for i in range(len1):
            left.append(array[l + i])
        for i in range(len2):
            right.append(array[m + 1 + i])
        i = 0
        j = 0
        k = l
        while i < len1 and j < len2:
            if left[i] <= right[j]:
                array[k] = left[i]
                plotter.draw_whole_array(color_info={k: "red"})
                yield True
                i += 1
            else:
                array[k] = right[j]
                plotter.draw_whole_array(color_info={k: "red"})
                yield True
                j += 1
            k += 1
        while i < len1:
            array[k] = left[i]
            plotter.draw_whole_array(color_info={k: "red"})
            yield True
            i += 1
            k += 1
        while j < len2:
            array[k] = right[j]
            plotter.draw_whole_array(color_info={k: "red"})
            yield True
            j += 1
            k += 1
    def tim_sort(array):
        length = len(array)
        minruns = calcRun(length)
        # sort subarray "runs" with insertion sort
        for start in range(0, length, minruns):
            end = min(start + minruns - 1, length - 1)
            yield from insertionSort(array, start, end)
        size = minruns
        while size < length:
            for left in range(0, length, 2 * size):
                # left to mid: left array
                # mid+1 to right: right array
                # sort the two arrays with merge sort
                mid = min(left + size - 1, length - 1)
                right = min(left + (2*size) - 1, length - 1)
                if mid < right:
                     yield from merge(array, left, mid, right)
            # double size to sort 2 bigger arrays
            size *= 2
    yield from tim_sort(array)

def radix_sort():
    array = plotter.array
    # stable sorting algorithm to sort each digit
    def counting_sort(array, exp):
        n = len(array)
        output = [0] * n
        count = [0] * 10
        # store occurences of digits
        for i in range(0, n):
            index = array[i] // exp
            count[index % 10] += 1
        # prefix sum array
        for i in range(1,10):
            count[i] += count[i-1]
        i = n - 1
        while i >= 0:
            index = array[i] // exp
            # shift count 1 to the left
            output[count[index % 10] - 1] = array[i]
            count[index % 10] -= 1
            i -= 1
        i=0
        for i in range(n):
            array[i] = output[i]
            plotter.draw_whole_array(color_info={i: "red"})
            yield True

    def radix_sort(array):
        _max = max(array)
        exp = 1
        while _max / exp >= 1:
            yield from counting_sort(array, exp)
            exp *= 10
    yield from radix_sort(array)

sorts = [bubble_sort, insertion_sort, merge_sort, quick_sort, shaker_sort, counting_sort, heap_sort, tim_sort,
                 radix_sort]
def quit():
    pygame.quit()
    exit()


x = screen.get_size()[0] - 200

buttons = [
           Button(0,0,50,20,"Quit", quit),
           Button(x, 0, 150, 50, "Shuffle", plotter.shuffle)]
for i, sort in enumerate(sorts):
    buttons.append(Button(x, 150+i*50, 150, 50, sort.__name__, sort))


input_boxes = [InputBox(1050, 700, 200, 40, "Set Array Length", plotter.initialize_array)]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for box in input_boxes:
            box.handle_event(event)
    if plotter.endless:
        plotter.process_endless(sorts)
    else:
        plotter.process()
    # clear the screen
    for button in buttons:
        button.process()
    for box in input_boxes:
        box.process()
    # draw to the screen
    # flip() updates the screen to make our changes visible
    pygame.display.flip()

    # how many updates per second
    clock.tick(200)

pygame.quit()