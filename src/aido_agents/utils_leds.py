import numpy as np

from aido_schemas import LEDSCommands, RGB

__all__ = [
    "get_normal_LEDs",
    "get_blinking_LEDs_left",
    "get_blinking_LEDs_right",
    "get_braking_LEDs",
]

blue = RGB(0.0, 0.0, 0.8)
white = RGB(0.6, 0.6, 0.6)
yellow = RGB(1.0, 1.0, 0.0)
red = RGB(0.6, 0.6, 0.6)
red2 = RGB(1.0, 0.0, 0.0)
orange = RGB(1.0, 0.5, 0.3)

phase2leds = {
    "left": LEDSCommands(
        center=blue, back_left=yellow, back_right=red, front_left=yellow, front_right=white,
    ),
    "right": LEDSCommands(
        center=blue, back_left=red, back_right=yellow, front_left=white, front_right=yellow,
    ),
    "none": LEDSCommands(center=blue, back_left=red, back_right=red, front_left=white, front_right=white),
    "brake": LEDSCommands(center=blue, back_left=red2, back_right=red2, front_left=white,
                          front_right=white, ),
    "emergency1": LEDSCommands(center=yellow, back_left=orange, back_right=yellow, front_left=orange,
                               front_right=yellow, ),
    "emergency2": LEDSCommands(center=orange, back_left=yellow, back_right=orange, front_left=yellow,
                               front_right=orange, ),
}
PHASE_SLOW = 0.5


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
    phases = ["emergency1", "none", "emergency2", "none"]
    return get_phased(t, phases, phase_period=0.2)


def get_phased(t: float, phases, phase_period: float) -> LEDSCommands:
    phase_index = int(np.round(t / phase_period))
    phase = phases[phase_index % len(phases)]
    led_commands = phase2leds[phase]
    return led_commands
