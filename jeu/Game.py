import pygame
pygame.init()
import pytmx
import pyscroll



class Game:

    def __init__(self):

        # fenetre du jeu
        self.screen = pygame.display.set_mode((400,400))
        pygame.display.set_caption("Titre du jeu ")

        # charger carte format tmx
        tmx_data = pytmx.util_pygame.load_pygame('map.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom =1
        # dessiner groupe de calque

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=1)

    def run(self):
        # boucle du jeu
        running = True
        while running:

            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running =False
        pygame.quit()


