import pygame
import random
import pdb


pygame.init()
pygame.key.set_repeat(100, 100)
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

    # GENERIC LIFE THINGS
    NEIGHBORS = [(x, y) for x in range(-1,2)
                 for y in range(-1,2) if (x,y) != (0,0)]

    # USEFUL OFFSETS FOR SCROLLING
    OFFSET_UP = (0,10)
    OFFSET_DOWN = (0,-10)
    OFFSET_LEFT = (10, 0)
    OFFSET_RIGHT = (-10, 0)

class PygWin:

    def __init__(self, windowwidth, windowheight, title):
        self.fps = Globals.FPS
        self.clock = pygame.time.Clock()
        self.title = title
        self.__screen_init(windowwidth, windowheight)
        self.exit = False
        self.fulldraw = True
        self.grid = LifeGrid(150,50)
        self.grid.randomlife()
        self.delay = 10
        self.scroll = (0,11)
        self.updaterects = []

    @classmethod
    def new(cls):
        newwindow = PygWin(Globals.WINDOWWIDTH, Globals.WINDOWHEIGHT,
                           Globals.TITLE)
        newwindow.main()

    def main(self):
        while not self.exit:
            renderlist = []
            self.updaterects.clear()

            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit = True
                    
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.set_scroll(Globals.OFFSET_UP)                     
                    if event.key == pygame.K_DOWN:
                        self.set_scroll(Globals.OFFSET_DOWN)
                    if event.key == pygame.K_LEFT:
                        self.set_scroll(Globals.OFFSET_LEFT)
                    if event.key == pygame.K_RIGHT:
                        self.set_scroll(Globals.OFFSET_RIGHT)

                    if event.key == pygame.K_ESCAPE:
                        self.exit = True
                        
            gridsurface, gridrects = self.grid.rendergrid()
            if not self.fulldraw:
                for rect in gridrects:
                    rect.move_ip((self.scroll[0],self.scroll[1]))

                self.updaterects.extend(gridrects)
            
            renderlist.append(SurfWithCoords(gridsurface,
                                             self.scroll))
            
            fpssurf = Globals.FONT.render(str(self.clock.get_fps())[:2], True,
                                          Globals.WHITE,
                                          Globals.BLACK)
            renderlist.append(SurfWithCoords(fpssurf, (0,0)))
            self.updaterects.append(fpssurf.get_rect())



            
            
            

            
            self.grid.calclife()
            self.delay = 10
            
            
            
            if self.fulldraw:
                self.__screen_update(renderlist, True)
                self.fulldraw = False
            else:
                self.__screen_update(renderlist)

            
            if self.exit:
                self.quit()

            
            self.clock.tick(Globals.FPS)

    def __screen_init(self, windowwidth, windowheight):
        self.mainsurf = pygame.display.set_mode((windowwidth, windowheight))
        self.mainsurf.fill(Globals.BLACK)
        pygame.display.set_caption(self.title)



    def __screen_update(self, drawlist, fullupdate=False):
        if fullupdate:
            self.mainsurf.fill(Globals.BLACK)

        itemstodraw = []
        for item in drawlist:
            itemstodraw.append(item.getsequence())
            
        self.mainsurf.blits(blit_sequence=itemstodraw, doreturn=0)
                   
        if fullupdate:
            pygame.display.update()
        else:
            pygame.display.update(self.updaterects)
        

    def quit(self):
        pygame.quit()

    def set_scroll(self, offset):
        self.scroll = tuple(sum(x) for x in zip(offset, self.scroll))
        self.fulldraw = True


class LifeGrid():

    def __init__(self, gridwidth, gridheight):
        self.gridheight = gridheight
        self.gridwidth = gridwidth
        self.gridlist = [[0 for y in range(gridheight)]
                         for x in range(gridwidth)]
        self.bounds = [(0,0), (gridwidth - 1, gridheight - 1 )]
        self.oldgrid = []
        self.oldsurface = False

    def randomlife(self):
        for x in range(self.gridwidth):
            for y in range(self.gridheight):
                if (random.randint(0,100)) >= 90:
                    self.gridlist[x][y] = 1
        
    def rendergrid(self):
        charsample = Globals.FONT.render("\u2591", True,
                                            Globals.RED)

        gridsurf = self.surf_ops()
        charblits = []

        for x in range(self.gridwidth):
            for y in range(self.gridheight):
                if not self.comparegrids(x, y):
                    if self.gridlist[x][y] == 0:
                        char = "\u2591"
                    else:
                        char = "\u2588"
                    
                    charsurf = Globals.FONT.render(char, True,
                                                   Globals.RED, Globals.BLACK)
                    charwidth = charsample.get_width()
                    charheight = charsample.get_height()
                    charblits.append([charsurf, (x * charwidth,
                                                y * charheight)])

        
        charrects = gridsurf.blits(blit_sequence=charblits)
        self.oldsurface = gridsurf
        return gridsurf, charrects

    def calclife(self):
        newlifegrid = []
        expansions = []
        for x in range(self.gridwidth):
            newlifegrid.append([])
            for y in range(self.gridheight):
                outofbounds=[]
                livingneighbors = 0
                for neighborloc in Globals.NEIGHBORS:
                    neighbor = (x + neighborloc[0], y + neighborloc[1])
                    if (neighbor[0] >= self.bounds[0][0]) \
                        and (neighbor[1] >= self.bounds[0][1]) \
                        and (neighbor[0] <= self.bounds[1][0]) \
                        and (neighbor[1] <= self.bounds[1][1]):
                        livingneighbors += self.gridlist[neighbor[0]][neighbor[1]]
                    else:
                        outofbounds.append(neighborloc)
                        
                
                if livingneighbors < 2:
                    newlifegrid[x].append(0)
                elif livingneighbors == 2:
                    newlifegrid[x].append(self.gridlist[x][y])
                elif livingneighbors == 3:
                    if self.gridlist[x][y] == 0:
                        newlifegrid[x].append(1)
                        expansions.append(outofbounds)                      
                    else:
                        newlifegrid[x].append(self.gridlist[x][y])
                else:
                    newlifegrid[x].append(0)

        
        self.oldgrid = self.gridlist
        self.gridlist = newlifegrid
     #   self.expandgrid(expansions, self.gridlist)

    def expandgrid(self, expandloc, grid):
        xinsert = False
        yinsert = False
        xextend = False
        yextend = False

  #      for loc in expandloc:
  #          if loc[0] < len(grid)

    def comparegrids(self, x, y):
        try:
            if self.gridlist[x][y] == self.oldgrid[x][y]:
                return True
            else:
                return False
        except:
            return False

    def surf_ops(self):

        if not self.oldsurface:
            samplesurface = Globals.FONT.render("\u2591", True,
                                            Globals.RED)
            surfwidth = samplesurface.get_width() * len(self.gridlist)
            surfheight = samplesurface.get_height() * len(self.gridlist[0])
            newsurface = pygame.Surface((surfwidth, surfheight))
            return newsurface
        else:
            return self.oldsurface


class SurfWithCoords:

    def __init__(self, surface, coordinates):
        self.surface = surface
        self.coord = coordinates
        self.rect = surface.get_rect()

    def getsequence(self):
        return (self.surface, self.coord)

if __name__=='__main__':
    PygWin.new()
