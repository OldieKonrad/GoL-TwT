import pygame
from GoL_class import GoL

pygame.init()

BLACK = (0, 0, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

WIDTH, HEIGHT = 800, 800
TILE_SIZE = 8
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
MAXGENERATIONS = 9999
FPS = 60

screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

def draw_grid(positions):
    for position in positions:
        col, row = position
        top_left = (col * TILE_SIZE, row * TILE_SIZE)
        pygame.draw.rect(screen, YELLOW, (*top_left, TILE_SIZE, TILE_SIZE))

    for row in range(GRID_HEIGHT):
        pygame.draw.line(screen, BLACK, (0, row * TILE_SIZE), (WIDTH, row * TILE_SIZE))

    for col in range(GRID_WIDTH):
        pygame.draw.line(screen, BLACK, (col * TILE_SIZE, 0), (col * TILE_SIZE, HEIGHT))


def main():
    gol = GoL(GRID_WIDTH, GRID_HEIGHT, MAXGENERATIONS)
    #gol.randomPopulate()
    gol.populateSpiral(4084)
    
    running = True
    playing = False

    
    while running:
        clock.tick(FPS)
        
        if gol.finished:
            pygame.display.set_caption(f"finished after generation: {gol.generation} cycletime: {gol.cycletime}")
            playing = False
        else:
            if playing:
                gol.nextGeneration()
                pygame.display.set_caption(f"Playing Generation: {gol.generation}")
            else:
                pygame.display.set_caption(f"Paused Generation: {gol.generation}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:           # quit game / close window
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                col = x // TILE_SIZE
                row = y // TILE_SIZE
                gol.toggleCell((col, row))   
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:     # toggle playing
                    playing = not playing

                if event.key == pygame.K_g:         # generate random population
                    gol.randomPopulate()
                    playing = False
 
                if event.key == pygame.K_c:         # reset board
                    gol.reset()
                    playing = False
                                       
                if event.key == pygame.K_n:         # single generation forward
                    gol.nextGeneration()
                    
        screen.fill(GREY)
        draw_grid(gol.curLivings)
        pygame.display.update()


    pygame.quit()

if __name__ == "__main__":
    main()