import pygame
import sys
import os

# check if scores.txt exists and create it if not
scores_file = 'Data/scores.txt'

if not os.path.exists(scores_file):
    with open(scores_file, 'w') as file:
        # Write some initial content to the file if needed
        file.write('')


def show_start_screen():
    # initialize Pygame and create screen
    pygame.init()
    pygame.font.init()
    scores_on = False
    screen = pygame.display.set_mode((800, 600))
    background_image = pygame.image.load("Data/background2.jpg")
    background_image = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
    
    
    # create buttons
    new_game_button = pygame.Rect(300, 200, 200, 50)
    highscore_button = pygame.Rect(300, 300, 200, 50)
    exit_button = pygame.Rect(300, 400, 200, 50)
    screen.blit(background_image, (0, 0))


    button_font = pygame.font.SysFont(None, 40)
    score_font = pygame.font.SysFont("arial", 30)
    new_game_text = button_font.render('New Game', True, (255, 255, 255))
    highscore_text = button_font.render('High Scores', True, (255, 255, 255))
    exit_text = button_font.render('Exit', True, (255, 255, 255))

    # Load the audio file
    pygame.mixer.music.load('Data/chill-abstract-intention.mp3')

    # Play the music on a loop
    pygame.mixer.music.play(-1)

    

    # start the game when the "new game" button is clicked
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if new_game_button.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    from Mirman3 import main
                    main()  # assuming your Pacman game function is named run_game
                      # call the Pacman game function
                elif highscore_button.collidepoint(event.pos) and scores_on == False:
                    # Load scores from file
                    with open('Data/scores.txt', 'r') as f:
                        scores = f.readlines()

                    # create text for top 5 scores
                    for i, score in enumerate(scores):
                        score_text = score_font.render(score.strip(), True, (255, 255, 255))
                        screen.blit(score_text, (50, 50 + i * 50))

                    scores_on = True
                elif highscore_button.collidepoint(event.pos) and scores_on == True:
                    background_color = pygame.Color('black')
                    screen.blit(background_image, (0, 0))
                    scores_on = False

                      
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    

        # draw buttons and other elements
        
        pygame.draw.rect(screen, (255, 0, 0), new_game_button)
        pygame.draw.rect(screen, (0, 255, 0), highscore_button)
        pygame.draw.rect(screen, (0, 0, 255), exit_button)

        screen.blit(new_game_text, (new_game_button.x + 30, new_game_button.y + 10))
        screen.blit(highscore_text, (highscore_button.x + 20, highscore_button.y + 10))
        screen.blit(exit_text, (exit_button.x + 75, exit_button.y + 10))
        
        pygame.display.update()

show_start_screen()
