# Get lots ball bouncing around the screen YES
# Get lots ball elastic bound with other balls YES
# Get people moving and infecting each other YES
# Implement recovery Yes
# Plot a graph of the infected/recovered and eventually deaths too YES
# Implement Death
# Implement probability of contract infection (now is always 100%)
# Improve the parser to not do all this if in the main
# Refactor the Renderer class to be more readeable :)


import numpy as np
import matplotlib.pyplot as plt
import sys
import time
import parser
from matplotlib import animation

COLOR_MAP = {
    "S": "#848484",
    "I": "#E0301E",
    "R": "#00A260",
}


class Ball(plt.Circle):
    '''
    Its a Ball class that inherit from plt.Circle object, so i can use this class to plot it on the canvas
    and define other methods to define other stuffs like movements, collision, etc.
    '''
    def __init__(self, xy, radius, vx, vy, **kwargs):
        '''
        input:
            xy: x and y coordinates on the plan
            radius: radius of the ball
            vx: velocity on x axis
            vy: velocity on y axis
        '''
        super().__init__(xy,radius)
        self.x, self.y = xy[0], xy[1]
        self.radius = radius
        self.vx = vx
        self.vy = vy
        self.set(**kwargs)

    def move(self):
        '''
            Move function, it permit to move the ball on the canvas. So this function update the position of the ball
        '''
        if(self.x - self.radius < 0 or self.x + self.radius > self.w): # Collision with walls
            self.vx *= -1
        if(self.y - self.radius < 0 or self.y + self.radius > self.h): # Collision with walls
            self.vy *= -1
        self.x += self.vx
        self.y += self.vy
        self.set_center((self.x,self.y))

    def set_vx(self, vx):
        self.vx = vx / 1.5

    def set_vy(self, vy):
        self.vy = vy / 1.5

    def set_w(self, w):
        self.w = w

    def set_h(self, h):
        self.h = h

class Person(Ball):
    '''
    This class inherit all the attributes of the ball to draw it on the canvas, but it permit to distinguish different kind of peoples.
    '''

    def __init__(self, id, xy, radius, vx, vy, status, **kwargs):
        super().__init__(xy, radius, vx, vy, **kwargs)
        self.id = id
        self.status = status
        self.color_map = COLOR_MAP
        self.set_color(self.color_map[status])
        self.time_infected = 0
        self.time_recovery = 8 * 60 # 60 because it go 60 frames per second

    def collision(self, pop, t):
        for p in range(self.id+1, len(pop)): # id+1 or you ever collide with yourself :)
            dx = self.x - pop[p].x # distance from the other balls on x axis
            dy = self.y - pop[p].y # distance from the other balls on y axis

            dist_squared = dx**2 + dy**2 # norm of ||d||^2
            fx = dx / np.sqrt(dist_squared) # normalized direction on x axis to achive unit vector
            fy = dy / np.sqrt(dist_squared) # normalized direction on y axis to achive unit vector
            if(dist_squared < (self.radius + pop[p].radius)**2):
                self.set_vx(self.vx + (0.02 * fx)) #update the velocity on x axis with unit direction and constant
                self.set_vy(self.vy + (0.02 * fy)) #update the velocity on y axis with unit direction and constant
                pop[p].set_vx(- (self.vx + (0.02 * fx))) #update the velocity of hitted ball on y axis with unit direction and constant
                pop[p].set_vy(- (self.vy + (0.02 * fy))) #update velocity of hitted ball on y axis with unit direction and constant
                if(self.status == "I" and pop[p].status == "S"):
                    pop[p].set_time_infection(t)
                    pop[p].set_status("I")
                elif(self.status == "S" and pop[p].status == "I"):
                    self.set_time_infection(t)
                    self.set_status("I")



    def recovery(self, t):
        if(self.status == "I" and ((t - self.time_recovery) >= self.time_infected)):
            self.set_status("R")
            self.set_color(self.color_map["R"])

    def set_status(self, status):
        self.status = status
        self.set_color(self.color_map[status])

    def set_time_infection(self, t):
        self.time_infected = t


class Renderer():
    '''
    Render class.
    This class draw all the objects in the frame, but do not have any buisness logic.
    '''

    def __init__(self, nameSim,nameGraph, pop, frames, wh, graph):
        self.nameSim = nameSim
        self.nameGraph = nameGraph
        self.frames = frames
        self.graph = graph
        self.color_map = COLOR_MAP
        self.k = 0
        self.fig = plt.figure(0)
        self.fig.set_dpi(100)
        self.fig.set_size_inches(wh[0], wh[1])
        ax = plt.axes([0,0,1,1], xlim=(0, wh[0]), ylim=(0, wh[1]), frameon=False)
        plt.xticks([])
        plt.yticks([])
        self.history_i = []
        self.history_s = []
        self.history_r = []
        self.x = np.linspace(1, int(self.frames / 60), int(self.frames))
        self.pop = pop
        for p in self.pop:
            p.set_w(wh[0])
            p.set_h(wh[1])
            ax.add_artist(p)
        self.update()

    def animate(self, t):
        self.progress_indicator("Simulation rendering: ", t)

        for p in self.pop:
            p.move()
            p.collision(self.pop, int(t))
            p.recovery(int(t))

        if(self.graph):
            i, r, s = self.count()
            self.history_i.append(i)
            self.history_r.append(r)
            self.history_s.append(s)

    def plotter(self, t):
        self.progress_indicator("Graph Rendering: ", t)
        self.ln1.set_data(self.x[0:t], self.history_i[0:t])
        self.ln2.set_data(self.x[0:t], self.history_r[0:t])
        self.ln3.set_data(self.x[0:t], self.history_s[0:t])
        return self.ln1, self.ln2, self.ln3,

    def count(self):
        infected = 0
        susceptibles = 0
        recovered = 0
        for p in self.pop:
            if(p.status == "I"):
                infected +=1
            elif(p.status == "R"):
                recovered +=1
            elif(p.status == "S"):
                susceptibles +=1

        return infected, recovered, susceptibles

    def progress_indicator(self, name, t):
        rounded, step_value = frames_to_percentage(self.frames)
        step_value = round(step_value + 0.5)
        if((t % step_value) == 0):
            self.k += 1 + rounded
            if(self.k >= 100):
                self.k = 100

        print("\r",name ,round(self.k - 0.5),"/ 100%", end="")
        sys.stdout.flush()


    def update(self):
        anim = animation.FuncAnimation(self.fig, self.animate, frames=self.frames, interval=1, repeat=False)
        self.save_mp4(anim)
        plt.close()
        self.k = 0
        if(self.graph):
            print("\n")
            self.fig2 = plt.figure(1)
            self.fig2.set_dpi(100)
            self.fig2.set_size_inches(15, 8)
            plt.tight_layout()
            ax = plt.axes()
            ax.set_xlim(0, self.frames / 60)
            ax.set_ylim(0, len(self.pop)) 
            ax.set_ylabel("Persons")
            ax.set_xlabel("Days")
            self.ln1, = plt.plot([],[], lw=2, color=self.color_map['I'])
            self.ln2, = plt.plot([],[], lw=2, color=self.color_map['R'])
            self.ln3, = plt.plot([],[], lw=2, color=self.color_map['S'])
            plt.legend(['infected','recovered','susceptibles'])
            ani = animation.FuncAnimation(self.fig2, self.plotter, frames=self.frames, interval=1, blit=True, repeat=False)
            self.save_graph_mp4(ani)
            # self.plotter()
            print("\nInfected: ", self.history_i[-1])
            print("Recovered: ", self.history_r[-1])
            print("Susceptibles: ", self.history_s[-1])

    def save_mp4(self, anim):
        anim.save(self.nameSim, writer = "ffmpeg", fps = 60)

    def save_graph_mp4(self, anim):
        anim.save(self.nameGraph, writer = "ffmpeg", fps = 60)


def seconds_to_frames(seconds, frames_per_sec):
    return seconds * frames_per_sec

def frames_to_percentage(frames):
    step_value = frames / 100
    rounded = find_approximation(step_value, round(step_value + 0.5))
    return rounded , step_value

def find_approximation(step_value, step_value_rounded):
    return (100 - ((100 * step_value) / step_value_rounded)) / 100


def main():
    args = parser.parse_cli()
    graph = args.graph
    if(args.resolution):
        wh = args.resolution.split('x')
        w = int(wh[0]) / 100
        h = int(wh[1]) / 100
    if(args.nameSim):
        nameSim = args.nameSim
    if(args.nameGraph):
        nameGraph = args.nameGraph
    if(not graph and nameGraph != "graph.mp4"):
        print("Add -g to save the graph")
        return -1

    if(args.npersons):
        num_people = args.npersons
    if(args.seconds):
        seconds = args.seconds
        frames = seconds_to_frames(seconds, 60)


    peoples = []
    paziente_0 = Person(0, (5, 5), 0.05, 0.009, 0.008, "I")
    peoples.append(paziente_0)
    for i in range(1, num_people):
        x_pos = np.random.uniform(0.5,w-0.5)
        y_pos = np.random.uniform(0.5,h-0.5)
        x_vel = np.random.uniform(-0.01, 0.01)
        y_vel = np.random.uniform(-0.01, 0.01)
        pop = Person(i, (x_pos,y_pos), 0.05, x_vel ,y_vel, "S")
        peoples.append(pop)

    Renderer(nameSim, nameGraph, peoples, frames, (w,h), graph)

if __name__ == "__main__":
        main()
