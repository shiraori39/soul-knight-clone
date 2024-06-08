import pygame
import copy


class MiniMap:
    """
    A class to represent the mini-map in the game.

    Attributes
    ----------
    room_height : int
        The height of each room on the mini-map.
    room_width : int
        The width of each room on the mini-map.
    room_dimensions : tuple
        The dimensions of each room on the mini-map.
    offset_x : int
        The x-offset for drawing the mini-map.
    offset_y : int
        The y-offset for drawing the mini-map.
    game : Game
        The main game instance.
    current_room : Room or None
        The current room the player is in.
    current_x : int or None
        The x-coordinate of the current room.
    current_y : int or None
        The y-coordinate of the current room.
    color : tuple
        The color used to draw rooms.
    rooms : list
        A list of all rooms in the game.
    adjacent_rooms : list
        A list of rooms adjacent to the current room.
    visited_rooms : list
        A list of rooms that have been visited.
    draw_mini_map : bool
        Flag to determine if the mini-map should be drawn.

    Methods
    -------
    __init__(game):
        Initializes the MiniMap with the given game instance.
    add_room(room):
        Adds a room to the list of visited rooms.
    set_current_room(room):
        Sets the current room and updates adjacent rooms.
    set_adjacent_rooms():
        Sets the list of adjacent rooms.
    update():
        Updates the mini-map based on the current room.
    positions():
        Adjusts the positions of the rooms for drawing.
    draw_all(surface):
        Draws all visited rooms on the mini-map.
    draw(surface):
        Draws the current and adjacent rooms on the mini-map.
    """
    room_height = 25
    room_width = 36
    room_dimensions = (room_width, room_height)
    offset_x = 1150
    offset_y = 10

    def __init__(self, game):
        """
        Initializes the MiniMap with the given game instance.

        Parameters
        ----------
        game : Game
            The main game instance.
        """
        self.game = game
        self.current_room = None
        self.current_x, self.current_y = None, None
        self.color = (150, 148, 153)
        self.rooms = []
        self.adjacent_rooms = []
        self.visited_rooms = []
        self.draw_mini_map = True

    def add_room(self, room):
        """
        Adds a room to the list of visited rooms.

        Parameters
        ----------
        room : Room
            The room to add to the visited rooms list.
        """
        if [room.x, room.y] not in self.visited_rooms:
            self.visited_rooms.append([room.x, room.y])

    def set_current_room(self, room):
        """
        Sets the current room and updates adjacent rooms.

        Parameters
        ----------
        room : Room
            The room to set as the current room.
        """
        self.add_room(room)
        if self.current_room is not room:
            self.current_room = room
            self.current_x = self.current_room.x
            self.current_y = self.current_room.y
            self.set_adjacent_rooms()

    def set_adjacent_rooms(self):
        """
        Sets the list of adjacent rooms.
        """
        self.adjacent_rooms = copy.deepcopy(self.current_room.neighbours)

    def update(self):
        """
        Updates the mini-map based on the current room.
        """
        self.set_current_room(self.game.world_manager.current_room)
        self.positions()

    def positions(self):
        """
        Adjusts the positions of the rooms for drawing.
        """
        while self.current_x != 1 or self.current_y != 1:
            if self.current_x < 1:
                self.current_x += 1
                for room in self.adjacent_rooms:
                    room[0] += 1
            elif self.current_x > 1:
                self.current_x -= 1
                for room in self.adjacent_rooms:
                    room[0] -= 1
            if self.current_y < 1:
                self.current_y += 1
                for room in self.adjacent_rooms:
                    room[1] += 1
            elif self.current_y > 1:
                self.current_y -= 1
                for room in self.adjacent_rooms:
                    room[1] -= 1

    def draw_all(self, surface):
        """
        Draws all visited rooms on the mini-map.

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the mini-map on.
        """
        for i, room in enumerate(self.visited_rooms):
            position = (self.offset_x + room[1] * self.room_width * 1.2,
                        self.offset_y + room[0] * self.room_height * 1.2)
            pygame.draw.rect(surface, self.color, (*position, *self.room_dimensions), 4)
        position = (self.offset_x + self.current_room.y * self.room_width * 1.2,
                    self.offset_y + self.current_room.x * self.room_height * 1.2)
        pygame.draw.rect(surface, (210, 210, 210,), (*position, *self.room_dimensions))

    def draw(self, surface):
        """
        Draws the current and adjacent rooms on the mini-map.

        Parameters
        ----------
        surface : pygame.Surface
            The surface to draw the mini-map on.
        """
        if self.draw_mini_map:
            for room in self.adjacent_rooms:
                position = (self.offset_x + room[1] * self.room_width * 1.2,
                            self.offset_y + room[0] * self.room_height * 1.2)
                pygame.draw.rect(surface, self.color, (*position, *self.room_dimensions), 4)
            position = (self.offset_x + self.current_y * self.room_width * 1.2,
                        self.offset_y + self.current_x * self.room_height * 1.2)
            pygame.draw.rect(surface, (210, 210, 210,), (*position, *self.room_dimensions))
