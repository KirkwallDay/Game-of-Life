import pygame
import random
import pdb

pygame.init()

class Globals:
    # COLORS
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    DARKBLUE = (27,53,96)
    RED = (170, 13, 13)

    # PYGAME GENERIC STUFF
    FPS = 60
    FONT = pygame.font.SysFont("arial", 10)
    WINDOWWIDTH = 640
    WINDOWHEIGHT = 480
    TITLE = "Basic Window"

class PygWin:

    def __init__(self, windowwidth, windowheight, title):
        self.fps = Globals.FPS
        self.clock = pygame.time.Clock()
        self.title = title
        self.__screen_init(windowwidth, windowheight)
        self.exit = False
        self.firstrun = True
        self.grid = LifeGrid(12, 12)
        self.grid.randomlife()

    @classmethod
    def new(cls):
        newwindow = PygWin(Globals.WINDOWWIDTH, Globals.WINDOWHEIGHT,
                           Globals.TITLE)
        newwindow.main()

    def main(self):
        while not self.exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True

            
            fpssurf = Globals.FONT.render(str(self.clock.get_fps())[:2], True,
                                          Globals.WHITE)
            self.mainsurf.fill(Globals.BLACK, fpssurf.get_rect())
            self.mainsurf.blit(fpssurf, (0,0))
            if self.firstrun:
                self.__screen_update(fpssurf.get_rect(), True)
                self.firstrun = False
            else:
                self.__screen_update(fpssurf.get_rect())

            
            if self.exit:
                self.quit()

            
            self.clock.tick(Globals.FPS)

    def __screen_init(self, windowwidth, windowheight):
        self.mainsurf = pygame.display.set_mode((windowwidth, windowheight))
        self.mainsurf.fill(Globals.BLACK)
        pygame.display.set_caption(self.title)



    def __screen_update(self, updaterects, fullupdate=False):
        if fullupdate:
            pygame.display.update()
        else:
            pygame.display.update(updaterects)

    def quit(self):
        pygame.quit()


class LifeGrid():

    def __init__(self, gridheight, gridwidth):
        self.gridheight = gridheight
        self.gridwidth = gridwidth
        self.gridlist = [

    def randomlife(self):
        for x in range(self.gridwidth):
            for y in range(self.gridheight):
                if (random.randint(0,100)) >= 90:
                    self.gridlist[x][y] = 1
        
    def rendergrid(self):
        samplesurface = Globals.FONT.render(str(self.gridlist[0][0]), True,
                                            Globals.RED)
        surfwidth = samplesurface.get_rect()[0] * len(self.gridlist[0])
        surfheight = samplesurface.get_rect()[1] * len(self.gridlist)

if __name__=='__main__':
    #pdb.set_trace()
    PygWin.new()
