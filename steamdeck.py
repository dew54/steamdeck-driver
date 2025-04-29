import sdl2
import sdl2.ext


class SteamDeck:
    AXIS_THRESHOLD = 8000

    def __init__(self, joystick_id=0):
        sdl2.ext.init()
        sdl2.SDL_Init(sdl2.SDL_INIT_JOYSTICK)

        self.joystick = sdl2.SDL_JoystickOpen(joystick_id)
        if not self.joystick:
            raise RuntimeError("Could not open joystick")

        self.num_axes = sdl2.SDL_JoystickNumAxes(self.joystick)
        self.num_buttons = sdl2.SDL_JoystickNumButtons(self.joystick)

        self.axis_values = [0] * self.num_axes
        self.button_states = [False] * self.num_buttons
        self.events = []

    def poll(self):
        self.events = []
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_JOYAXISMOTION:
                axis = event.jaxis.axis
                value = event.jaxis.value
                if abs(value) < self.AXIS_THRESHOLD:
                    value = 0
                if self.axis_values[axis] != value:
                    self.axis_values[axis] = value
                    self.events.append(("axis", axis, value))

            elif event.type == sdl2.SDL_JOYBUTTONDOWN:
                button = event.jbutton.button
                self.button_states[button] = True
                self.events.append(("button_down", button))

            elif event.type == sdl2.SDL_JOYBUTTONUP:
                button = event.jbutton.button
                self.button_states[button] = False
                self.events.append(("button_up", button))

    def get_axis(self, axis_id):
        return self.axis_values[axis_id]

    def is_button_pressed(self, button_id):
        return self.button_states[button_id]

    def get_events(self):
        return self.events

    def close(self):
        sdl2.SDL_JoystickClose(self.joystick)
        sdl2.ext.quit()
