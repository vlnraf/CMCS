import argparse
import sys

def parse_cli():
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument(
                "-r", "--resolution",
                help = "Render the movie at resolution WxH",
                default="800x800",
        )

        parser.add_argument(
                "-g", "--graph",
                help = "type this flag if you want to compute the graph",
                default=False,
                action="store_true"
        )

        parser.add_argument(
                "--nameSim",
                help = "Name of the file where save the simulation video , use .mp4",
                default="default.mp4",
        )

        parser.add_argument(
                "--nameGraph",
                help = "Name of the file where save the graph video , use .mp4",
                default="graph.mp4",
        )

        parser.add_argument(
                "--npersons",
                help = "number of persons to initialize",
                type=int,
                default=50,
        )

        parser.add_argument(
                "--seconds",
                help = "time of the output video in seconds, take in consideration that every second correspond to 1 day",
                type=int,
                default=20,
        )

        args = parser.parse_args()
        return args
    except argparse.ArgumentError as err:
        print(str(err))
        sys.exit(2)
