import pygame as py
import random
import math

py.init()

class DrawInfo:
    BLACK = 0,0,0
    CREAM = 255,255,230
    ORANGE = 255,140,0
    MAGENTA = 255,0,255
    HELIOTROPE = 223,115,225
    BACKGROUND_COLOR = CREAM

    GRADIENTS = [
        (173, 216, 230),
        (128, 0, 128),
        (100, 149, 237)
    ]

    FONT = py.font.SysFont('Comic Sans MS', 20) 
    LGFONT = py.font.SysFont('Comic Sans MS', 30)
    SIDE_PAD = 100    #Padding from sides left and right
    TOP_PAD = 100     #Padding from top and bottom

    def __init__(self,width,height,lst):
        self.width = width
        self.height = height

        self.window = py.display.set_mode((width, height))
        py.display.set_caption("Sorting Visulaizer")
        self.set_list(lst)

    def set_list(self,lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        self.bar_width = round((self.width - self.SIDE_PAD) / len(lst)) #find total area to be able to draw the bars/blocks and divide it by length of lst to get total number of blocks 
        self.bar_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))  #First find total drawable area and divide it by max - min val to get the number of vals in range  (ex. max = 100 min = 1  range = 99)
        self.start_x = self.SIDE_PAD // 2


def draw(draw_info, algo_name, ascending):
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    title = draw_info.LGFONT.render(f"{algo_name} ~ {'Ascending' if ascending else 'Descending'}", 1, draw_info.ORANGE)
    draw_info.window.blit(title, ((draw_info.width / 2 - title.get_width() / 2, 5)))

    controls = draw_info.FONT.render("R ~ Reset | Space Bar ~ Sort | A ~ Ascending | D ~ Descending", 1, draw_info.MAGENTA)
    draw_info.window.blit(controls, ((draw_info.width / 2 - controls.get_width() / 2, 45)))
    
    sorting = draw_info.FONT.render("I ~ Insertion Sort | B ~ Bubble Sort", 1, draw_info.HELIOTROPE)
    draw_info.window.blit(sorting, ((draw_info.width / 2 - sorting.get_width() / 2, 75)))

    draw_list(draw_info)
    py.display.update()

def draw_list(draw_info, color_positions = {}, clear_bg = False):
    lst = draw_info.lst

    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, 
                      draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        py.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    for i, val in enumerate(lst):
        x = draw_info.start_x + i * draw_info.bar_width
        y = draw_info.height - (val - draw_info.min_val) * draw_info.bar_height
        
        color = draw_info.GRADIENTS[i % 3]

        if i in color_positions:
            colot = color_positions[i]
        
        py.draw.rect(draw_info.window,color,(x,y,draw_info.bar_width,draw_info.height))

    if clear_bg:
        py.display.update()


def generate_starting_list(n,min_val,max_val):
    lst = []

    for  _ in range(n):
        val = random.randint(min_val, max_val)
        lst.append(val)

    return lst


def bubble(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range (len(lst) - 1):
        for j in range (len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j + 1] = lst[j + 1], lst[j]
                draw_list(draw_info, {j: draw_info, j + 1: draw_info}, True)
                yield True
    return lst


def insertion(draw_info, ascending = True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        while True:
            ascending_sort = i > 0 and lst[i - 1] > current and ascending
            descending_sort = i > 0 and lst[i - 1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break

            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i: draw_info, i - 1: draw_info}, True)
            yield True

    return lst

def main():
    run = True
    clock = py.time.Clock()
    n = 50
    min_val = 0
    max_val = 100

    lst = generate_starting_list(n,min_val,max_val)
    draw_info = DrawInfo(800,600, lst)
    sorting = False
    ascending = True
    sorting_algo = bubble
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    while run:
        clock.tick(120)

        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)


        py.display.update()

        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                
            if event.type != py.KEYDOWN:
                continue
            if event.key == py.K_r:
                lst = generate_starting_list(n,min_val,max_val)
                draw_info.set_list(lst)
                sorting = False
            elif event.key == py.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algo(draw_info, ascending)
            elif event.key == py.K_a and not sorting:
                ascending = True
            elif event.key == py.K_d and not sorting:
                ascending = False
            elif event.key == py.K_i and not sorting:
                sorting_algo = insertion
                sorting_algo_name = "Insertion Sort"
            elif event.key == py.K_b and not sorting:
                sorting_algo = bubble
                sorting_algo_name = "Bubble Sort"
            

    py.quit()

if __name__ == "__main__":
    main()       
