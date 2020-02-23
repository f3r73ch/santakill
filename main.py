#!/usr/bin/python3
# Displays a white window with a blue circle in the middle
# Basic arcade program

# Imports =========================================
import arcade
# import random



# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 960
SCREEN_TITLE = "Santa Kill adventure"
# SPRITE_SCALING = 0.5
CHARACTER_SCALING = 0.75


MOVEMENT_SPEED = 5

TEXTURE_RIGHT = 0
TEXTURE_LEFT = 1
TEXTURE_UP = 2
TEXTURE_DOWN = 3

# Constants used to track if the player is facing left or right
RIGHT_FACING = 0
LEFT_FACING = 1

# 
UPDATES_PER_FRAME=7



def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]




class PlayerCharacter(arcade.Sprite):
    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0

        # Track out state -------------
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.scale = CHARACTER_SCALING

        # Adjust the collision box. Default includes too much empty space
        # side-to-side. Box is centered at sprite center, (0, 0)
        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        # --- Load Textures ---

        # Images from Kenney.nl's Asset Pack 3
        main_path = "images/robot/robot"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}_idle.png")

        # Load textures for walking into a list 
        # this list is then used to be iterated through and hence make their textures available
        # 
        self.walk_textures = []
        for i in range(8):
            texture = load_texture_pair(f"{main_path}_walk{i}.png")
            self.walk_textures.append(texture)

    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Idle animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]


class Santakill(arcade.Window):
	"""
	Santa kill
		Game where your character is santa claus that embarks in an adventure
	"""
	def __init__(self, width, height, title):
		"""
			Initialize the game
		"""
		super().__init__(width, height, title)
		# Set up the empty sprite lists
		self.player_list = None
		self.coin_list = None

		# Set up the player
		self.score = 0
		self.player = None


	def setup(self):
		"""
			Get the game ready to play
		"""

		# Set up the player
		self.player_list = arcade.SpriteList()
		self.player=PlayerCharacter()

		#  add the player sprite to the list of sprites related with the player 
		#  -------
		self.player_list.append(self.player)

		# Unpause everything and reset the collision timer
		self.paused = False



	def on_key_press(self, symbol, modifiers):

	    """Handle user keyboard input
	    Q: Quit the game
	    P: Pause/Unpause the game
	    Arrows: Move Up, Left, Down, Right

	    Arguments:
	        symbol {int} -- Which key was pressed
	        modifiers {int} -- Which modifiers were pressed
	    """
	    if symbol == arcade.key.Q:
	        # Quit immediately
	        arcade.close_window()

	    if symbol == arcade.key.P:
	        self.paused = not self.paused

	    if symbol == arcade.key.UP:
	    	print("clicking up")
	    	self.player.change_y = 5

	    if symbol == arcade.key.DOWN:
	        self.player.change_y = -5

	    if symbol == arcade.key.LEFT:
	        self.player.change_x = -5

	    if symbol == arcade.key.RIGHT:
	        self.player.change_x = 5

	def on_key_release(self, symbol: int, modifiers: int):
	    """Undo movement vectors when movement keys are released

	    Arguments:
	        symbol {int} -- Which key was pressed
	        modifiers {int} -- Which modifiers were pressed
	    """
	    if (
	        symbol == arcade.key.UP
	        or symbol == arcade.key.DOWN
	    ):
	        self.player.change_y = 0

	    if (
			symbol == arcade.key.LEFT
	        or symbol == arcade.key.RIGHT
	    ):
	        self.player.change_x = 0

	def on_update(self, delta_time: float):
		"""Update the positions and statuses of all game objects
		If paused, do nothing
		Arguments:
		delta_time {float} -- Time since the last update
		"""
		# If paused, don't update anything
		if self.paused:
			return



		# Update everything
		self.player_list.update()
		self.player_list.update_animation()


		# Keep the player on screen
		if self.player.top > self.height:
			self.player.top = self.height
		if self.player.right > self.width:
			self.player.right = self.width
		if self.player.bottom < 0:
			self.player.bottom = 0
		if self.player.left < 0:
			self.player.left = 0

	def on_draw(self):
		"""
		Draw all game objects
		"""
		arcade.start_render()


		# -----------------------------
		self.player_list.draw()


## 
# Main code entry point ---------------------------------------
## 
if __name__ == "__main__":
	# Create a new santa kill adventure  window
	santa_game = Santakill(
		int(SCREEN_WIDTH ), int(SCREEN_HEIGHT ), SCREEN_TITLE
	)

	# Setup to play
	santa_game.setup()
	# 
	arcade.run()
