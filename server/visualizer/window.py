## @package Window
#  This is the window class, it creates a window and mainains all its contents
import pygame, os, sys
from pygame.locals import *
from spriteClasses import Unit
from timePeriod import TimePeriod
import threading
##This class defines the window object. Visualizer protocol
# calls methods on the window object to change the state of the
# visualizer
class Window(object):
    ## Global variables for Window
    windowDimensions = [1280,1050]

    #Dimensions of Subviews
    viewDimensions={"l":{"dimensions":(1280, 640), "upperLeftCorner":(0, 0)},
                    "s1":{"dimensions":(608, 342), "upperLeftCorner":(0, 682 )},
                    "s2":{"dimensions":(608, 342), "upperLeftCorner":(672, 682)}}
    
    timePeriodConversion = {0:"farPast", 1:"past", 2:"present"}

    #Period names as well as default background colors
    periodNames = {'farPast':[100,0,0], 'past':[0,100,0], 'present':[0,0,100]} # red, blue, green

    #Period dimensions, in terms of map, a 10 by 10 map would be (10,10)
    periodDimensions = (21,21)

    #Delay time between frams. In milliseconds
    delaytime = 100

    ## sets up Window object
    def __init__(self, config={}):
        pygame.init()
        self.status = {}
        self.views = {}
        self.timePeriods = {}
        self.playerNames = []
        self.nameLayer = None
        windim = Window.windowDimensions
        try:
            windim[0] = config["width"]
        except:
            pass
        try:
            windim[1] = config["height"]
        except:
            print config
        Window.viewDimensions={"l":{"dimensions":(windim[0], int(windim[1] * .6)),
                                    "upperLeftCorner":(0,0)},
                               "s1":{"dimensions":(int(windim[0] * .475)
                                                   ,int(windim[1] * .325)),
                                     "upperLeftCorner":(0,int(windim[1] * .65))},
                               "s2":{"dimensions":(int(windim[0] * .475)
                                                   ,int(windim[1] * .325)), 
                                     "upperLeftCorner":(int(windim[0] * .52),int(windim[1] * .65))}}
        
        self.display = pygame.display.set_mode(windim)
        self.setUpTimePeriods()
        self.animations = False
        pygame.display.update()
        self.handleEvents()

    def handleEvents(self):
        def inner():
            while True:
                event = pygame.event.wait()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit(0)
                    if event.key == K_1:
                        self.focusOn('farPast')
                    elif event.key == K_2:
                        self.focusOn('past')
                    elif event.key == K_3:
                        self.focusOn('present')
                    elif event.key == K_MINUS:
                        Window.delaytime +=10
                        print "Increasing Speed..."
                    elif event.key == K_PLUS:
                        if Window.delaytime >=10:
                            Window.delaytime -=10
                            print "Decreasing Speed..."
        threading.Thread(target=inner).start()

        
    def addPlayers(self, username1, username2):
        font = pygame.font.Font(os.path.join('visualizer/fonts', 'game_over.ttf') , 100)
        displayRect = self.display.get_rect()
        displayWidth = displayRect.width
        self.playerNames.append({'image':font.render(username1, 1, [250,0,0]), 'rect': None})
        self.playerNames[0]['rect'] = self.playerNames[0]['image'].get_rect(topleft = (10, 10))
        self.playerNames.append({'image':font.render(username2, 1, [0,0,250]), 'rect': None})
        self.playerNames[1]['rect'] = self.playerNames[1]['image'].get_rect(topright = (displayWidth-10,10))
        
    def drawNames(self):
        if self.playerNames:
            self.nameLayer.blit(self.playerNames[0]['image'], self.playerNames[0]['rect'])
            self.nameLayer.blit(self.playerNames[1]['image'], self.playerNames[1]['rect'])
    
    ## initializes 3 TimePeriod objects and gives them their initial subview name
    def setUpTimePeriods(self):
        for name, color in Window.periodNames.iteritems():
            self.timePeriods[name] = TimePeriod(name, self.viewDimensions['l']['dimensions'], Window.periodDimensions, color)
        self.timePeriods['farPast'].presentView = 's1'
        self.timePeriods['past'].presentView = 'l'
        self.timePeriods['present'].presentView = 's2'
        self.createSubViews()
    
    ## creates subviews on the display for the TimePeriods to be drawn in
    def createSubViews(self):
        self.nameLayer = self.display.subsurface(self.display.get_rect())
        for name, dict in self.viewDimensions.iteritems():
            rectangle = pygame.Rect(dict["upperLeftCorner"], dict["dimensions"])
            self.views[name] = self.display.subsurface(rectangle)
        self.updateScreen()

    ## iterates through created TimePeriods and clears the surfaces
    #  usually prior to re-drawing screen
    def clearTimePeriodSurfaces(self):
        for name, item  in self.timePeriods.iteritems():
            item.clearGroups()
            
    ## changes the largest subview so that focus is changed to requested
    #  timeperiod
    # @param focusPeriod- the name of the requested TimePeriod (i.e. 'past')
    def focusOn(self, focusPeriod):
        print "changing focus..."
        oldView = self.timePeriods[focusPeriod].presentView
       # print "*%(1)s" %{'1':oldView}
        for name, period in self.timePeriods.iteritems():
            if period.presentView == 'l':
               # print "*found large view"
                period.presentView = oldView
                self.timePeriods[focusPeriod].presentView = 'l'
        if self.animations:
            self.updateScreen()

    ## instead of calling pygame.display.update(), call this to update all
    #  TimePeriods and their subviews
    def updateScreen(self):
        for name, period in self.timePeriods.iteritems():
            period.updateTimePeriod()
            pygame.transform.scale(period.baseLayer, self.viewDimensions[period.presentView]['dimensions'], self.views[period.presentView])
        self.drawNames()
        pygame.time.delay(Window.delaytime)
        pygame.display.update()


    ## iterates through the status to find the requested id, and it to the
    #  appropriate sprite group and TimePeriod
    # @param id- an objectID (int)
    def add(self, id):  
        #print "looking for ", id
        for period, dictionary in self.status.iteritems():
            for type, list in dictionary.iteritems():
                for item in list:
                    if item['objectID'] == id:
                        #print "  adding ", id
                        if type == 'Unit':
                            self.timePeriods[period].addUnit(item)
                        if type == 'Building':
                            self.timePeriods[period].addBuilding(item)
                        if type == 'Terrain':
                            self.timePeriods[period].addTerrain(item)
                        if type == 'Portal':
                            self.timePeriods[period].addPortal(item)                            
                            
        if self.animations:
            self.updateScreen()
                        
    ## remove(self, id)
    #  iterates through TimePeriods, calling each period's remove method
    #  to remove the requested object
    def remove(self, id):
        for name, period in self.timePeriods.iteritems():
            period.remove(id)
    
    ## moves the object with objectID "id" to the requested x,y coordinate
    #  @param id- an objectID; targeX/Y- target coords. (all are ints)
    def move(self, id, targetX, targetY):
         """
         Game Logic should handle this
         print "moving unit to ", "(", targetX, ",", targetY,")..."
         if targetX >= periodDimensions[0] or targetY >= periodDimensions[1]:
         raise Exception("**********Tried moving outside of range")
         """
         found = False
         for name, period in self.timePeriods.iteritems():
            period.takeStep(id)
            if self.animations:
                self.updateScreen()
            if period.move(id, targetX, targetY):
                found = True
            if self.animations:
                self.updateScreen()
    
    ## calls attack and reset for the requested ID to each TimePeriod
    #  this causes the object to strike in the direction of the target, but
    #  does NOT cause it to move to (targetX,targetY)
    #  @param attackerID- objectID; targetX/Y- target coords (all ints)
    def attack(self, attackerID, targetX, targetY):
        #print "attacking...."
        for name, period in self.timePeriods.iteritems():
            period.attack(attackerID, targetX, targetY)
            if self.animations:
                self.updateScreen()
    
    ## calls hurt on each TimePeriod for id, "id's" hp is then decremented
    #  by changeHP
    # @param id- an object id (int); changeHP- the change in hp, (+ hurt, - heal)
    def hurt(self, id, changeHP):
        for name, period in self.timePeriods.iteritems():
            period.hurt(id, changeHP)
    
    def hungerDamage(self, player, period, damage):
        self.timePeriods[Window.timePeriodConversion[period]].hungerDamage(player, damage)
    
    ## causes a civil engineer "id" to swing its pickaxe in the direction
    #  of target.
    # @param id- object id (int); targetX/targetY- requested coords (ints)
    def build(self, id, targetX, targetY):
        for name, period in self.timePeriods.iteritems():
            period.build(id, targetX, targetY)
            
    def paint(self, id, targetX, targetY):
        for name, period in self.timePeriods.iteritems():
            period.paint(id, targetX, targetY)
    
    ## trains a unit to be a certain type of unit
    # @param
    def train(self, id, newUnitTypeID):
        for name, period in self.timePeriods.iteritems():
            period.train(id)

    def cancel(self, id):
        for name, period in self.timePeriods.iteritems():
            period.cancel(id)

    def warp(self, id, targetZ):
        temp = None
        for name, period in self.timePeriods.iteritems():
            temp = period.warpOut(id)
            if temp != None:
                break
        if temp!=None:
            self.timePeriods[Window.timePeriodConversion[targetZ]].units.add(temp)
        else:
            print "Unit ", id, " not found."
    
    ## replaces old status dictionary with newStatus
    # @param newStatus- a status dictionary.
    def updateStatus(self, newStatus):
        self.status.update(newStatus)
