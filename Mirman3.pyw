import sys
import os
import math, random, pygame



pygame.mixer.init()
pygame.display.init()
pygame.font.init()

# check if scores.txt exists and create it if not
scores_file = 'Data/scores.txt'

if not os.path.exists(scores_file):
    with open(scores_file, 'w') as file:
        # Write some initial content to the file if needed
        file.write('')

# Set window size
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)

class Game(object):
    """ The game itself. """
    def __init__(self):
        """ Initialize Game object. """
        # set level
        self.level = 0
        self.game_ended = False
        self.screen_width = 1000
        self.screen_height = 800
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF)
        self.font = pygame.font.Font(None, 36)
        self.player_name = "John doe"
        self.paused = False
        
        # load sound for level advance
        
        self.score = 0
        self.wall_group = pygame.sprite.Group()

        # Add sprites to the group
        # left and right sprites
        wall1_image = pygame.image.load("Data/wall_topleft2.bmp")
        wall1 = Wall(game=self, image=wall1_image, x=0, y=0)
        self.wall_group.add(wall1)
        wall2 = Wall(game=self, image=wall1_image, x=0, y=450)
        self.wall_group.add(wall2)
        wall1_image = pygame.image.load("Data/wall_topleft2.bmp")
        wall3 = Wall(game=self, image=wall1_image, x=950, y=0)
        self.wall_group.add(wall3)
        wall4 = Wall(game=self, image=wall1_image, x=950, y=450)
        self.wall_group.add(wall4)
        #bottom and top sprites of wall
        wall2_image = pygame.image.load("Data/wall_bottom.bmp")
        wall5 = Wall(game=self, image=wall2_image, x=50, y=0)
        self.wall_group.add(wall5)
        wall6 = Wall(game=self, image=wall2_image, x=50, y=750)
        self.wall_group.add(wall6)
        #middle screen sprites
        wall7 = Wall(game=self, image=wall1_image, x=200, y=225)
        self.wall_group.add(wall7)
        wall8 = Wall(game=self, image=wall1_image, x=750, y=225)
        self.wall_group.add(wall8)
        wall3_image = pygame.image.load("Data/wall5.bmp") # podłóżny cienki, 300 x 10
        wall4_image = pygame.image.load("Data/wall6.bmp") # pionowy cienki, 10 x 300
        wall9 = Wall(game=self, image=wall3_image, x=100, y=660)
        self.wall_group.add(wall9)
        wall10 = Wall(game=self, image=wall4_image, x=100, y=460)
        self.wall_group.add(wall10)

        wall11 = Wall(game=self, image=wall3_image, x=100, y=140)
        self.wall_group.add(wall11)
        wall12 = Wall(game=self, image=wall4_image, x=100, y=150)
        self.wall_group.add(wall12)
        
        wall13 = Wall(game=self, image=wall3_image, x=590, y=140)
        self.wall_group.add(wall13)
        wall14 = Wall(game=self, image=wall4_image, x=880, y=150)
        self.wall_group.add(wall14)

        wall15 = Wall(game=self, image=wall3_image, x=590, y=660)
        self.wall_group.add(wall15)
        wall16 = Wall(game=self, image=wall4_image, x=880, y=460)
        self.wall_group.add(wall16)
        wall17 = Wall(game=self, image=wall3_image, x=350, y=300)
        self.wall_group.add(wall17)
        wall18 = Wall(game=self, image=wall3_image, x=350, y=550)
        self.wall_group.add(wall18)

        
        


        # Create a sprite group for the Pacman
        self.pacman_sprites = pygame.sprite.Group()
        # Load the images
        pacman_circle = pygame.image.load("Data/pacmancircle.png").convert_alpha()
        pacman_halfopen = pygame.image.load("Data/pacmanhalfopen.png").convert_alpha()
        pacman_open = pygame.image.load("Data/pacmanopen.png").convert_alpha()

        # Create a list of images for animation
        pacman_anim = [pacman_circle, pacman_halfopen, pacman_open, pacman_halfopen]


        # Create the Pacman sprite
        self.pacman = Pacman(game=self, images=pacman_anim, x=500, y=400)
        self.pacman_sprites.add(self.pacman)
        self.redghost = Red(game=self, x = 500, y = 200)
        self.ghost_sprites = pygame.sprite.Group()
        self.ghost_sprites.add(self.redghost)
        
        self.green = Red(game = self, x =100, y = 100)  # create a new object of the Red class
        self.ghost_sprites.add(self.green)

        self.yellow = Red(game = self, x =900, y = 100)  # create a new object of the Red class
        self.ghost_sprites.add(self.yellow)

        self.blue = Red(game = self, x =100, y = 700)  # create a new object of the Red class
        self.ghost_sprites.add(self.blue)

        #create points 
        self.point_group = pygame.sprite.Group()
        self.points_image = pygame.image.load('Data/points.png').convert_alpha()

        # Create points every 50 pixels of free space
        for x in range(0, self.screen_width, 51):
            for y in range(0, self.screen_height, 51):
                # Check if the current position is free of walls and not too close to the player
                if not self.check_collisions(x, y):
                    self.point_group.add(Points(self, self.points_image, x, y))

        

    def draw_walls(self):
        self.wall_group.draw(screen)

    def draw_pacman(self):
        self.pacman_sprites.draw(screen)
    def draw_points(self):
        self.point_group.draw(screen)
    def draw_ghosts(self):
        self.ghost_sprites.draw(screen)

    def save_score(self, name, score):
        
        # Read the scores from the file and parse them into a list of tuples
        with open('Data/scores.txt', 'r') as file:
            scores = [tuple(line.strip().split(': ')) for line in file]

            # Append the new score as a tuple to the list
            scores.append((name, score))

            # Sort the list in descending order based on the score
            scores.sort(key=lambda x: int(x[1]), reverse=True)

            # Keep only the top 6 scores by slicing the list
            top_scores = scores[:6]

        # Write the top 6 scores back to the file
        with open('Data/scores.txt', 'w') as file:
            for name, score in top_scores:
                file.write(f'{name}: {score}\n')

    def get_player_name(self):
        

        # Create a black background surface for the text field
        input_surface = pygame.Surface((200, 50))
        input_surface.fill((0, 0, 0))
        input_font = pygame.font.SysFont("arial", 30)

        # Create a rectangular area for the text input box
        input_box = pygame.Rect(200, 300, 200, 50)
        input_box2 = pygame.Rect(200, 200, 200, 50)

        # Set the initial text and color for the text input box
        input_text = ""
        input_color = pygame.Color("White")

        # Set text indicating that you need a name
        input_news = "Give me your name"

        # Game loop
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # If the player presses a key, add it to the text input box
                    if event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                        input_surface.fill((0, 0, 0))
                        
                    elif event.key == pygame.K_RETURN:
                        return input_text
                    else:
                        input_text += event.unicode

            # Render the text input box surface with the current text and color
            input_surface = input_font.render(input_text, True, input_color)

            
            # Draw the input box and the text
            pygame.draw.rect(screen, (0, 0, 0), input_box)
            input_surface.blit(input_font.render(input_text, True, input_color), (0, 0))
            screen.blit(input_surface, (input_box.x + 5, input_box.y + 5))

            # Draw the rectangular area for the text input box onto the screen
            pygame.draw.rect(screen, pygame.Color("Black"), input_box, 2)

            # Render the text input box surface with the current text and color
            input_surface2 = input_font.render(input_news, True, input_color)

            # Draw the text input box surface onto the screen
            screen.blit(input_surface2, (input_box2.x + 5, input_box2.y + 5))


            # Update the display
            pygame.display.update()
        return input_text
        
    def check_collisions(self, x, y):
        for wall in self.wall_group:
            if wall.rect.collidepoint(x, y):
                return True
        return False
        
        
       
        
    def play(self):
        screen = pygame.display.set_mode((1000, 800))
        clock = pygame.time.Clock()
        background_image = pygame.image.load("Data/blackscreen.bmp")

        # Game loop
        self.running = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.paused = not self.paused  # toggle the paused flag
                        if self.paused:
                            print("Paused")  # print a message if the game is paused

            if not self.paused:  # only update the game if it's not paused
                # update the game logic here
                    


            
                
                # Draw the sprites
                if not self.game_ended:

                    # Blit background image onto the screen
                    screen.blit(background_image, (0, 0))
                    self.draw_walls()
                    self.draw_pacman()
                    self.draw_points()
                    self.draw_ghosts()
                
                    # Render the score and blit it onto the screen
                    score_surface = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
                    score_rect = score_surface.get_rect(topright=(self.screen_width - 10, 10))
                    self.screen.blit(score_surface, score_rect)
                    self.point_group.update()
                    self.pacman.update()
                    self.ghost_sprites.update()
                    
                    

                    

                    pygame.display.flip()
                    
                    # Limit the frame rate
                    clock.tick(60)

            # Check for game over condition
            if self.pacman.lives <= 0:
                self.game_ended = True
                self.end()
                self.running = False

            # Quit pygame if window closed
            try:
                if not pygame.display.get_surface():
                    raise SystemExit
                    self.game_ended = True
                    self.running = False
                    pygame.quit()
                    sys.exit()
            except SystemExit:
                self.game_ended = True
                self.running = False
                pygame.quit()
                sys.exit()
                
                
        



    

    def end(self):
        """ End the game. """
        # show 'Game Over' for 5 seconds
        
        font = pygame.font.SysFont(None, 90)
        end_message = font.render("Game Over", True, (255, 0, 0))
        end_rect = end_message.get_rect(center=(pygame.display.get_surface().get_width()/2, pygame.display.get_surface().get_height()/2))
        pygame.display.get_surface().blit(end_message, end_rect)
        pygame.display.flip()
        self.game_ended = True
        self.running = False
        input_text = ""  # define input_text variable
        # call get_player_name() method and assign the returned value to player_name variable
        self.player_name = self.get_player_name()
        
        
        
        self.save_score(self.player_name, self.score)
        pygame.time.delay(2000)
        from MirmanStart import show_start_screen
        show_start_screen()

        
        
        
        pygame.quit()
        sys.exit()
        

    def win(self):
        """ End the game. """
        # show "YOU WIN" for 5 seconds
        font = pygame.font.SysFont(None, 110)
        end_message = font.render("You Win!", True, (255, 255, 0))
        end_rect = end_message.get_rect(center=(pygame.display.get_surface().get_width()/2, pygame.display.get_surface().get_height()/2))
        pygame.display.get_surface().blit(end_message, end_rect)
        pygame.display.flip()
        pygame.time.delay(7000)
        input_text = ""  # define input_text variable
        # call get_player_name() method and assign the returned value to player_name variable
        self.player_name = self.get_player_name()
        self.save_score(self.player_name, self.score)
        self.game_ended = True
        self.running = False
        
        pygame.time.delay(1000)
        
        pygame.quit()
        exit()

class Wrapper(pygame.sprite.Sprite):
    """ A sprite that wraps around the screen. """
    def __init__(self, x, y):
        super().__init__()

    def update(self):
        """ Wrap sprite around screen. """
        if not self.game.game_ended:
            if self.rect.top > pygame.display.get_surface().get_height():
                self.rect.bottom = 0
                
            if self.rect.bottom < 0:
                self.rect.top = pygame.display.get_surface().get_height()
                
            if self.rect.left > pygame.display.get_surface().get_width():
                self.rect.right = 0
                
            if self.rect.right < 0:
                self.rect.left = pygame.display.get_surface().get_width()

    def die(self):
        """ Destroy self. """
        self.kill()

        
class Pacman(Wrapper):
    """ Nasz pacman gracza"""

    
        
    def __init__(self, game, images, x, y):
        """ Initialize ship sprite. """
        super().__init__(x = x, y = y)
        self.images = images
        self.lives = 1

        self.current_sprite = 0
        self.image = self.images[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.speed = 3
        self.sound = pygame.mixer.Sound("Data/pacman_chomp.wav")
        self.prev_pos = self.rect.copy()
        self.counter = 0
        self.rotatedimage = pygame.transform.rotate(self.image, 0)
        
        
      
   
        
    def update(self):
        """Move the character"""
        keys = pygame.key.get_pressed()
        dx = dy = 0

        #animation of pacman
        self.image = self.images[self.current_sprite]
        self.counter +=1
        if self.counter == 15:
            self.counter = 0
            self.current_sprite += 1
        if self.current_sprite == 4:
            self.current_sprite = 0

        #movement, rotation and sound
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.rotatedimage = pygame.transform.rotate(self.image, 180)
            if not self.sound_playing:
                self.sound.play()
                self.sound_playing = True
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.rotatedimage = pygame.transform.rotate(self.image, 0)
            if not self.sound_playing:
                self.sound.play()
                self.sound_playing = True
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.rotatedimage = pygame.transform.rotate(self.image, 90)
            if not self.sound_playing:
                self.sound.play()
                self.sound_playing = True
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.rotatedimage = pygame.transform.rotate(self.image, 270)
            if not self.sound_playing:
                self.sound.play()
                self.sound_playing = True

        if dx != 0 and dy != 0:
            dx /= 1.41
            dy /= 1.41

            
        self.image = self.rotatedimage

      
            
            
        # Reset the sound playing flag if the sound has finished
        if not pygame.mixer.get_busy():
            self.sound_playing = False

        # check for collisions with pacman
        collisions = pygame.sprite.spritecollide(self, self.game.wall_group, False)
        if collisions:
            # revert to previous position
            self.rect = self.prev_pos.copy()

        # update previous position
        self.prev_pos = self.rect.copy()

        # check for collisions with pacman
        collisions2 = pygame.sprite.spritecollide(self, self.game.ghost_sprites, False)
        if collisions2:
            self.lives -= 1
            print("life -1")
            self.game.end()



        super().update()
        



        
class Red(Wrapper):
    """ Nasz pacman gracza"""

    
        
    def __init__(self, game, x, y):
        """ Initialize ship sprite. """
        super().__init__(x = x, y = y)
        self.right1 = pygame.image.load("Data/red_right1.png").convert_alpha()
        self.right2 = pygame.image.load("Data/red_right2.png").convert_alpha()
        self.left1 = pygame.image.load("Data/red_left1.png").convert_alpha()
        self.left2 = pygame.image.load("Data/red_left2.png").convert_alpha()
        self.down1 = pygame.image.load("Data/red_down1.png").convert_alpha()
        self.down2 = pygame.image.load("Data/red_down2.png").convert_alpha()
        self.up1 = pygame.image.load("Data/red_up1.png").convert_alpha()
        self.up2 = pygame.image.load("Data/red_up2.png").convert_alpha()
        self.red_anim = [self.right1, self.right2, self.left1, self.left2,
                    self.down1, self.down2, self.up1, self.up2]
        self.red_anim_right = [self.right1, self.right2]
        self.red_anim_left = [self.left1, self.left2]
        self.red_anim_down = [self.down1, self.down2]
        self.red_anim_up = [self.up1, self.up2]
        
        
        self.current_sprite = 0
        self.image = self.red_anim[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game
        self.speed = 2
        self.prev_pos = self.rect.copy()
        self.counter = 0
        self.rotatedimage = pygame.transform.rotate(self.image, 0)
        
        self.randomside = 0
        self.sidecounter = 179

    def update(self):
        """Move the character"""
        if not self.game.game_ended:

            self.image = self.red_anim[self.current_sprite]
            self.counter +=1
            if self.counter == 15:
                self.counter = 0
                self.current_sprite += 1
            if self.current_sprite == 2:
                self.current_sprite = 0

            self.sidecounter += 1
            if self.sidecounter == 180:
                self.randomside = random.randint(0, 3)
                self.sidecounter = 0

            # 0 left, 1 right, 2 up, 3 down
            if self.randomside == 0:
                self.red_anim = self.red_anim_left
                self.rect.x -= self.speed

            if self.randomside == 1:
                self.red_anim = self.red_anim_right
                self.rect.x += self.speed

            if self.randomside == 2:
                self.red_anim = self.red_anim_up
                self.rect.y -= self.speed

            if self.randomside == 3:
                self.red_anim = self.red_anim_down
                self.rect.y += self.speed

            
                
                


            

            

            

            super().update()


    def change_color(self, color):
        """Change the color of the sprite"""
        new_image = self.image.copy()  # create a copy of the sprite image
        new_image.fill(color, special_flags=pygame.BLEND_RGB_MULT)  # fill the copy with the new color
        self.image = new_image  # set the copy as the new sprite image

        

    


    
        
        
            
        

class Wall(pygame.sprite.Sprite):
    def __init__(self, game, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

    def update(self):
        
        pass


        
        
class Points(pygame.sprite.Sprite):

    number = 0
    def __init__(self, game, image, x, y):
        super().__init__()
        Points.number += 1 
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.game = game

    def update(self):
        collisions2 = pygame.sprite.spritecollide(self, self.game.pacman_sprites, False)
        if collisions2:
            #self destroy and give points
            self.game.score += 10
            Points.number -= 1
            print("zostało", Points.number ,"do zebrania")
            if Points.number == 0:
                self.game.win()
                
            self.kill()

        
        


        


def main():
    pygame.init()
    pygame.font.init()
    mirman = Game()
    mirman.play()
# kick it off!
main()
sys.exit()
         

