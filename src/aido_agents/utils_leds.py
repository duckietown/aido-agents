import numpy as np

from aido_schemas import LEDSCommands, RGB

__all__ = [
    "get_normal_LEDs",
    "get_blinking_LEDs_left",
    "get_blinking_LEDs_right",
    "get_braking_LEDs",
    "get_blinking_LEDs_emergency",
    "get_rotation",
]

dark = RGB(0.1, 0.1, 0.1)
blue = RGB(0.0, 0.0, 1.0)
green = RGB(0.0, 1.0, 0.0)
white = RGB(0.6, 0.6, 0.6)
yellow = RGB(1.0, 1.0, 0.0)
red = RGB(0.5, 0.0, 0.0)
red_more = RGB(1.0, 0.0, 0.0)
orange = RGB(1.0, 0.5, 0.3)

phase2leds = {
    "left": LEDSCommands(
        center=blue,
        back_left=yellow,
        back_right=red,
        front_left=yellow,
        front_right=white,
    ),
    "right": LEDSCommands(
        center=blue,
        back_left=red,
        back_right=yellow,
        front_left=white,
        front_right=yellow,
    ),
    "none": LEDSCommands(center=blue, back_left=red, back_right=red, front_left=white, front_right=white),
    "brake": LEDSCommands(
        center=blue,
        back_left=red_more,
        back_right=red_more,
        front_left=white,
        front_right=white,
    ),
    "emergency1": LEDSCommands(
        center=yellow,
        back_left=red,
        back_right=yellow,
        front_left=red,
        front_right=yellow,
    ),
    "emergency2": LEDSCommands(
        center=red, back_left=yellow, back_right=red, front_left=yellow, front_right=red
    ),
    "rot1": LEDSCommands(center=red, front_left=green, back_left=blue, back_right=yellow, front_right=dark),
    "rot2": LEDSCommands(center=dark, front_left=red, back_left=green, back_right=blue, front_right=dark),
    "rot3": LEDSCommands(center=red, front_left=dark, back_left=red, back_right=green, front_right=blue),
    "rot4": LEDSCommands(center=blue, front_left=green, back_left=dark, back_right=red, front_right=green),
    "rot5": LEDSCommands(center=green, front_left=blue, back_left=blue, back_right=dark, front_right=red),
}
PHASE_SLOW: float = 0.5


def get_braking_LEDs(t: float) -> LEDSCommands:
    phases = ["brake"]
    return get_phased(t, phases, PHASE_SLOW)


def get_normal_LEDs(t: float) -> LEDSCommands:
    phases = ["none"]
    return get_phased(t, phases, PHASE_SLOW)


def get_blinking_LEDs_right(t: float) -> LEDSCommands:
    phases = ["right", "none"]
    return get_phased(t, phases, PHASE_SLOW)


def get_blinking_LEDs_left(t: float) -> LEDSCommands:
    phases = ["left", "none"]
    return get_phased(t, phases, PHASE_SLOW)


def get_blinking_LEDs_emergency(t: float) -> LEDSCommands:
    phases = ["emergency1", "emergency2"]
    return get_phased(t, phases, phase_period=0.4)


def get_rotation(t: float) -> LEDSCommands:
    phases = ["rot1", "rot2", "rot3", "rot4", "rot5"]
    return get_phased(t, phases, phase_period=0.4)


def get_phased(t: float, phases, phase_period: float) -> LEDSCommands:
    phase_index = int(np.round(t / phase_period))
    phase = phases[phase_index % len(phases)]
    led_commands = phase2leds[phase]
    return led_commands
