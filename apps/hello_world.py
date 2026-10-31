"""Hello World for PicoWare 2.5 on the ClockworkPi PicoCalc."""

from picoware.system.buttons import BUTTON_BACK, BUTTON_ESCAPE
from picoware.system.vector import Vector


def start(view_manager) -> bool:
    """Draw once when PicoWare opens the application."""
    draw = view_manager.draw
    draw.clear()
    draw.text(Vector(24, 136), "Hello, World!")
    draw.text(Vector(24, 168), "Esc / Back to exit")
    draw.swap()
    return True


def run(view_manager) -> None:
    """Let PicoWare poll input and return to its previous view on exit."""
    input_manager = view_manager.input_manager
    if input_manager.button in (BUTTON_BACK, BUTTON_ESCAPE):
        input_manager.reset()
        view_manager.back()


def stop(view_manager) -> None:
    """No resources to release; PicoWare restores the previous view."""
