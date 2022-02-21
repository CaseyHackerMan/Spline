import pygame
import numpy as np

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)

r = 7 # radius for circles
n = 10 # number of points
spline_seg = 100 # spline segments

def lerp(x,p1,p2):
    return (p2-p1)*x+p1

def make_spline_func(points):
    n = len(points)-1
    points_copy = points.copy()
    def func(t):
        temp = points_copy.copy()
        for i in range(n):
            for j in range(n-i):
                temp[j] = lerp(t,temp[j],temp[j+1])
        return temp[0]
    return func

def spline_gen(points, n_seg):
    res = [points[0]]
    spline_func = make_spline_func(points)
    for t in range(1,n_seg):
        t /= n_seg
        res.append(spline_func(t))
    res.append(points[-1])
    return res
            
pygame.init()
root = pygame.display.set_mode((1000,1000))
window = np.array(root.get_size())

points = [np.random.rand(2)*window for _ in range(n)]

spline = spline_gen(points,spline_seg)

clock = pygame.time.Clock()
selected = None
running = True
while running:
    t = pygame.time.get_ticks()/5000%1
    for event in pygame.event.get():
        if (event.type == pygame.QUIT): 
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            click = np.array(event.pos)
            for i in range(n):
                if np.linalg.norm(points[i]-click) <= r:
                    selected = i
                    break
        if event.type == pygame.MOUSEBUTTONUP:
            selected = None
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                points = [np.random.rand(2)*window for _ in range(n)]
                spline = spline_gen(points,spline_seg)

    root.fill(BLACK)
    if selected != None:
        points[selected] = np.array(pygame.mouse.get_pos())
        spline = spline_gen(points,spline_seg)
    
    for i in range(n):
        pygame.draw.circle(root,WHITE,points[i],r,1)

    temp = points.copy()
    for i in range(n):
        for j in range(n-i-1):
            pygame.draw.line(root,WHITE,temp[j],temp[j+1],1)
            temp[j] = lerp(t,temp[j],temp[j+1])
    pygame.draw.circle(root,RED,temp[0],r)
    
    for i in range(len(spline)-1):
        pygame.draw.line(root,RED,spline[i],spline[i+1],3)

    pygame.draw.circle(root,WHITE,points[0],r)
    pygame.draw.circle(root,WHITE,points[-1],r)
            
    pygame.display.update()
    clock.tick(60)
        
pygame.quit()