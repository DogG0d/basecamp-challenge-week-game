import pygame
from constant import Mouse

class Keyboard:
    def __init__(self):  # Initiate keyboard manager
        self.current_key_states = None
        self.previous_key_states = None
    

    def process_input(self):  # Update current and previous keyboard state
        self.previous_key_states = self.current_key_states
        self.current_key_states = pygame.key.get_pressed()
    
    
    def is_key_down(self, keyCode):
        if self.current_key_states is None:
            return False
        return self.current_key_states[keyCode] == True
    

    def any_key_down(self, keycodes: list):
        return any(self.is_key_down(keycode) for keycode in keycodes)
    
    
    
    def is_key_pressed(self, keyCode):
        if self.current_key_states is None or self.previous_key_states is None:
            if self.current_key_states is None:
                return False
            else:
                return self.current_key_states[keyCode]
        return self.current_key_states[keyCode] == True and self.previous_key_states[keyCode] == False
    

    def any_key_pressed(self, keycodes: list):
        return any(self.is_key_pressed(keycode) for keycode in keycodes)
    
    
    def is_key_released(self, keyCode):
        if self.current_key_states is None or self.previous_key_states is None:
            return False
        return self.current_key_states[keyCode] == False and self.previous_key_states[keyCode] == True

class Mouse:
    def __init__(self):  # Initiate mouse manager
        self.previous_key_states = None
        self.current_key_states = None

        self.previous_key_states: dict[int, bool]
        self.current_key_states: dict[int, bool]
    

    def process_input(self, events) -> None:  # Update current and previous mouse state
        self.previous_key_states = self.current_key_states
        self.current_key_states = pygame.mouse.get_pressed(5)
        self.events = [event for event in events if event.type in [pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION, pygame.MOUSEWHEEL]]

        self.events: list[pygame.event.Event]
    
    
    def isKeyDown(self, keyCode: Mouse) -> bool:
        if self.current_key_states is None:
            return False
        return self.current_key_states[keyCode] == True
    

    def anyKeyDown(self, keycodes: list[Mouse]):
        return any(self.isKeyDown(keycode) for keycode in keycodes)
    
    
    def isKeyPressed(self, keyCode: Mouse) -> bool:
        if self.current_key_states is None or self.previous_key_states is None:
            if self.current_key_states is None:
                return False
            else:
                return self.current_key_states[keyCode]
        return self.current_key_states[keyCode] == True and self.previous_key_states[keyCode] == False
    

    def anyKeyPressed(self, keycodes: list[Mouse]) -> bool:
        return any(self.isKeyPressed(keycode) for keycode in keycodes)
    
    
    def isKeyReleased(self, keyCode: Mouse) -> bool:
        if self.current_key_states is None or self.previous_key_states is None:
            return False
        return self.current_key_states[keyCode] == False and self.previous_key_states[keyCode] == True
    

    def is_scrolling_up(self) -> bool:
        for event in self.events:
            if event.type == pygame.MOUSEWHEEL:
                return event.precise_y > 0
    

    def is_scrolling_down(self) -> bool:
        for event in self.events:
            if event.type == pygame.MOUSEWHEEL:
                return event.precise_y < 0


class InputStream:
    def __init__(self):  # Initiate input manager
        self.keyboard = Keyboard()
        self.keyboard: Keyboard
        self.mouse = Mouse()
    

    def process_input(self, events: list[pygame.event.Event]):
        self.keyboard.process_input()
        self.mouse.process_input(events)
    
    
    def get_keyboard(self) -> Keyboard:
        return self.keyboard
    

    def get_mouse(self) -> Mouse:
        return self.mouse
