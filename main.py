#!/usr/bin/python3
# Displays a white window with a blue circle in the middle
# Basic arcade program

# Imports =========================================
import arcade
# import random



# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 1024
SCREEN_TITLE = "Santa Kill adventure"
SPRITE_SCALING = 0.5


MOVEMENT_SPEED = 5

TEXTURE_RIGHT = 0
TEXTURE_LEFT = 1
TEXTURE_UP = 2
TEXTURE_DOWN = 3




class Player(arcade.Sprite):

    def __init__(self):
        super().__init__()

        self.textures = []
        # Load a left facing texture and a right facing texture.
        # mirrored=True will mirror the image we load.

        # define texture facing RIGHT ---
        texture = arcade.load_texture("images/robot/robot_walk0.png")
        self.textures.append(texture)
        # define texture facing LEFT ----
        texture = arcade.load_texture("images/robot/robot_walk0.png", mirrored=True)
        self.textures.append(texture)


        # define texture for up -------
        texture = arcade.load_texture("images/robot/robot_climb0.png")
        self.textures.append(texture)
        # define texture for down  ----
        texture = arcade.load_texture("images/robot/robot_walk0.png")
        self.textures.append(texture)




        self.scale = SPRITE_SCALING

        # By default, face right.
        self.set_texture(TEXTURE_RIGHT)

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        # Figure out if we should face left or right
        if self.change_x < 0:
            self.texture = self.textures[TEXTURE_LEFT]
        elif self.change_x > 0:
            self.texture = self.textures[TEXTURE_RIGHT]

        # Figure out if we should face left or right
        if self.change_y < 0:
            self.texture = self.textures[TEXTURE_DOWN]
        elif self.change_y > 0:
            self.texture = self.textures[TEXTURE_UP]

        if self.left < 0:
            self.left = 0
        elif self.right > SCREEN_WIDTH - 1:
            self.right = SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > SCREEN_HEIGHT - 1:
            self.top = SCREEN_HEIGHT - 1


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
		self.enemies_list = arcade.SpriteList()
		self.all_sprites = arcade.SpriteList()



	def setup(self):
		"""
			Get the game ready to play
		"""
		# Set the background color
		# Set up the player

		# Set up the player
		self.player_sprite = Player()
		self.player_sprite.center_y = self.height / 2
		self.player_sprite.left = 10
		self.all_sprites.append(self.player_sprite)
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
	        self.player_sprite.change_y = 5

	    if symbol == arcade.key.DOWN:
	        self.player_sprite.change_y = -5

	    if symbol == arcade.key.LEFT:
	        self.player_sprite.change_x = -5

	    if symbol == arcade.key.RIGHT:
	        self.player_sprite.change_x = 5

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
	        self.player_sprite.change_y = 0

	    if (
			symbol == arcade.key.LEFT
	        or symbol == arcade.key.RIGHT
	    ):
	        self.player_sprite.change_x = 0

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
		self.all_sprites.update()


		# Keep the player on screen
		if self.player_sprite.top > self.height:
			self.player_sprite.top = self.height
		if self.player_sprite.right > self.width:
			self.player_sprite.right = self.width
		if self.player_sprite.bottom < 0:
			self.player_sprite.bottom = 0
		if self.player_sprite.left < 0:
			self.player_sprite.left = 0

	def on_draw(self):
		"""
		Draw all game objects
		"""
		arcade.start_render()


		# -----------------------------
		self.all_sprites.draw()


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
