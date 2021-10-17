import time
from dataclasses import dataclass
from typing import cast, Optional

import numpy as np
import yaml

from aido_schemas import (
    Context,
    DB20Commands,
    DB20ObservationsPlusState,
    EpisodeStart,
    GetCommands,
    JPGImage,
    PWMCommands,
)
from duckietown_world import construct_map, DuckietownMap, get_lane_poses, GetLanePoseResult
from .utils_images import jpg2rgb
from .utils_leds import get_blinking_LEDs_left, get_blinking_LEDs_right, get_braking_LEDs

__all__ = ["FullAgentConfig", "FullAgent"]


@dataclass
class FullAgentConfig:
    pass


class FullAgent:
    config: FullAgentConfig = FullAgentConfig()
    dtmap: Optional[DuckietownMap]
    pose: np.ndarray

    def init(self, context: Context):
        context.info("FullAgent init()")
        self.dtmap = None

    def _init_map(self, map_data: dict):
        self.dtmap = construct_map(map_data)

    def on_received_seed(self, data: int):
        np.random.seed(data)

    def on_received_episode_start(self, context: Context, data: EpisodeStart):
        # This is called at the beginning of episode.
        context.info(f'Starting episode "{data.episode_name}".')

    def on_received_observations(self, context: Context, data: DB20ObservationsPlusState):
        myname = data.your_name
        # context.info(f'myname {myname}')
        # state = data.state.duckiebots

        if self.dtmap is None:
            context.info("Loading map")
            yaml_str = cast(str, data.map_data)
            map_data = yaml.load(yaml_str, Loader=yaml.SafeLoader)
            self._init_map(map_data)
            context.info("Loading map done")

        mystate = data.state.duckiebots[myname]
        self.pose = mystate.pose

        # context.info(f'state {state}')
        # Get the JPG image
        camera: JPGImage = data.camera
        # Convert to numpy array
        _rgb = jpg2rgb(camera.jpg_data)

    def on_received_get_commands(self, context: Context, data: GetCommands):
        pose: np.array = self.pose

        # context.info('Which lane am I in?')

        t0 = time.time()
        possibilities = list(get_lane_poses(self.dtmap, pose))
        if not possibilities:  # outside of lane:
            speed = 0.05
            turn = 0.1

            led_commands = get_braking_LEDs(data.at_time)

        else:
            glpr: GetLanePoseResult = possibilities[0]
            lane_pose = glpr.lane_pose
            # context.info(debug_print(lane_pose))
            #
            k = 0.1
            speed = 0.1
            turn = -k * lane_pose.relative_heading

            if turn > 0:
                led_commands = get_blinking_LEDs_left(data.at_time)
            else:
                led_commands = get_blinking_LEDs_right(data.at_time)

        pwm_left = speed - turn
        pwm_right = speed + turn

        pwm_commands = PWMCommands(motor_left=pwm_left, motor_right=pwm_right)

        commands = DB20Commands(pwm_commands, led_commands)
        dt = time.time() - t0
        context.write("commands", commands)
        # context.info(f"commands computed in {dt:.3f} seconds")

    def finish(self, context: Context):
        context.info("finish()")
