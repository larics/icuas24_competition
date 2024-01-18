#!/usr/bin/env python

"""
graph_gen.py: Generates a graph of the environment given a set of parameters.
"""

from dataclasses import dataclass
from matplotlib import pyplot as plt
from matplotlib.patches import Rectangle
import yaml


@dataclass
class IndoorFarm:
    """IndoorFarm: A class that represents an indoor farm.

    Attributes:
        row_count: The number of rows of plant beds.
        col_count: The number of columns of plant beds.
        height_count: The number of levels of plant beds.
        plant_bed_width: The width of each plant bed. Width is the row direction.
        plant_bed_length: The length of each plant bed. Length is the column direction.
        plant_bed_height: The height of each plant bed. Height is the vertical direction.
        row_spacing: The spacing between each row of plant beds.
        col_spacing: The spacing between each column of plant beds.
        height_spacing: The spacing between each level of plant beds.
        x_offset: The x offset of the indoor farm from the origin (0, 0, 0).
        y_offset: The y offset of the indoor farm from the origin (0, 0, 0).
        z_offset: The z offset of the indoor farm from the origin (0, 0, 0).
        safety_distance: The safety distance between the drone and the plant bed.
    """
    row_count: int
    col_count: int
    height_count: int
    plant_bed_width: float
    plant_bed_length: float
    plant_bed_height: float
    row_spacing: float
    col_spacing: float
    height_spacing: float
    x_offset: float
    y_offset: float
    z_offset: float
    safety_distance: float = 0.5

    @classmethod
    def from_yaml(cls, filename: str):
        """from_yaml: Creates an IndoorFarm object from a YAML file."""
        with open(filename, 'r', encoding='utf-8') as stream:
            config = yaml.safe_load(stream)
            return cls(
                row_count=config['row_count'],
                col_count=config['col_count'],
                height_count=config['height_count'],
                plant_bed_width=config['plant_bed_width'],
                plant_bed_length=config['plant_bed_length'],
                plant_bed_height=config['plant_bed_height'],
                row_spacing=config['row_spacing'],
                col_spacing=config['col_spacing'],
                height_spacing=config['height_spacing'],
                x_offset=config['x_offset'],
                y_offset=config['y_offset'],
                z_offset=config['z_offset'],
                safety_distance=config['safety_distance']
            )


def draw_2d_indoor_farm(indoor_farm: IndoorFarm):
    """draw_indoor_farm: Draws a plot of the indoor farm."""
    fig = plt.figure()
    ax = fig.add_subplot(111)
    for row in range(indoor_farm.row_count):
        for col in range(indoor_farm.col_count):
            x = indoor_farm.x_offset + col * \
                (indoor_farm.plant_bed_width + indoor_farm.col_spacing)
            y = indoor_farm.y_offset + row * \
                (indoor_farm.plant_bed_length + indoor_farm.row_spacing)
            rectangle = Rectangle(
                (x, y), indoor_farm.plant_bed_width, indoor_farm.plant_bed_length)
            ax.add_patch(rectangle)

    for row in range(indoor_farm.row_count + 1):
        for col in range(indoor_farm.col_count + 1):
            y = indoor_farm.y_offset - indoor_farm.row_spacing/2 + row * \
                (indoor_farm.plant_bed_length + indoor_farm.row_spacing)
            x = col * indoor_farm.plant_bed_width + (indoor_farm.col_spacing/2) + \
                (col-1) * indoor_farm.col_spacing + indoor_farm.x_offset
            x2 = indoor_farm.x_offset + indoor_farm.plant_bed_width/2 + col * \
                (indoor_farm.plant_bed_width + indoor_farm.col_spacing)

            ax.scatter(x, y, color='r')
            if col == 0:
                x -= indoor_farm.safety_distance
                ax.scatter(x, y, color='y')
            if col == indoor_farm.col_count:
                x += indoor_farm.safety_distance
                ax.scatter(x, y, color='y')
            if col >= indoor_farm.col_count:
                continue
            ax.scatter(x2, y, color='g')
    ax.set_xlim([0, 30])
    ax.set_ylim([0, 30])
    plt.show()


if __name__ == "__main__":
    draw_2d_indoor_farm(IndoorFarm.from_yaml('scripts/indoor_farm.yaml'))
