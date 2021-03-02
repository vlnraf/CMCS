# SIR Simulation

It's a simple scrit that run an epidemic simulation

An example of what you can get:  
- ![Simulation](https://user-images.githubusercontent.com/43886147/109726410-ffbe7880-7bb2-11eb-9f0f-05fb836a64e3.mp4)  
- ![Graph](https://user-images.githubusercontent.com/43886147/109726435-0816b380-7bb3-11eb-9dde-6a5cf8c11c52.mp4)

For the math behind the collision of the spheres, and the change of direction see the following link: (it's the math used on the script, but could be wrong 😅, there is no physic like the mass of the balls or other stuffs like that, cause not needed for the simulation)  

[Ball Collision](https://github.com/vlnraf/CMCS/blob/master/continous_models/simulation/Ball%20collision.pdf)

### Requirements

You need **python 3.6+** in order to execute the script. Clone the repository and install all the dependencies with the following command
```sh
pip install -r requirements.txt
```

### Usage

First of all run the command
```sh
python simulation.py -h
```
to see all the parameters that can be passed. You should see something like that
```sh
usage: simulation.py [-h] [-r RESOLUTION] [-g] [--nameSim NAMESIM] [--nameGraph NAMEGRAPH]
                     [--npersons NPERSONS] [--seconds SECONDS]

optional arguments:
  -h, --help            show this help message and exit
  -r RESOLUTION, --resolution RESOLUTION
                        Render the movie at resolution WxH
  -g, --graph           type this flag if you want to compute the graph
  --nameSim NAMESIM     Name of the file where save the simulation video , use .mp4
  --nameGraph NAMEGRAPH
                        Name of the file where save the graph video , use .mp4
  --npersons NPERSONS   number of persons to initialize
  --seconds SECONDS     time of the output video in seconds, take in consideration that every second
                        correspond to 1 day
```
