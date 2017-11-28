#!/usr/bin/env python
# -*- coding: latin-1 -*-

import os
import sys
import wx
from wx import *
import threading,time
import wx.lib.buttons
import rur_py.misc as misc  # a few global variables

cur_path = os.path.dirname(sys.argv[0])

misc.HOME = cur_path
misc.IMAGE_DIR = os.path.join(misc.HOME, "wxRUR", "rur_images")

App = wx.PySimpleApp(0) # (1) redirects print output to window;
                        # (0) to terminal

import wx.py as py           # For the interpreter
import rur_py.images as images # load all images
import rur_py.dialogs as rD    # contains various dialogs and exception classes
import rur_py.parser as parser
from rur_py.translation import _
from rur_py.world_display import WorldGUI
from rur_py.world_creation import Visible_world
from rur_py.robot_factory import New_improved_robot
from rur_py.lightning import LogWindow


class Robot(object):
    def __init__(self, app, col=1, row=1, orient='E', beepers=0, name=None, colour='grey'):
        self.app = app
        self.WorldDisplay = app.frame.WorldDisplay
        self.world = app.frame.WorldDisplay.world
        true_robot = self.world.addOneRobot(avenues=col,
                                        streets = row,
                                        orient_key=orient,
                                        beepers=beepers,
                                        name = name,
                                        colour = colour,
                                        better = True)
        self.robot = self.world.robot_dict[true_robot.name]
        self.name = true_robot.name
        self.world.object_dict[self.name] = True
        self.set_trace_style(style=0)
        self.update_refresh()

    def __del__(self):
        self.world.object_dict[self.name] = False
        self.update_refresh()
    #--- Robot actions

    def turn_off(self):
        self.__del__()

    def set_trace_style(self, style=0, colour='sea green'):
        self.robot.set_trace_style(style, colour)

    def move(self):
        x0, y0 = self.robot.getPos()
        try:
            self.robot.move() # may raise an exception
        except rD.HitWallException, mesg:
            rD.DialogHitWallError(mesg)
        x1, y1 = self.robot.getPos()
        style = self.robot.trace_style
        if style != 0 :
            orientation = self.robot._getOrientation()
            colour = self.robot.trace_colour
            self.robot.line_trace.append( (x0, y0, x1, y1, orientation, style, colour) )
        self.update_refresh()

    def turn_left(self):
        x, y = self.robot.getPos()
        style = self.robot.trace_style
        if style > 0 :
            orientation = self.robot._getOrientation()
            colour = self.robot.trace_colour
            self.robot.line_trace.append( (x, y, x, y, orientation, style, colour) )
        self.robot.turn_left()  # must occur after line_trace.append
        self.update_refresh()

    def turn_right(self):
        x, y = self.robot.getPos()
        style = self.robot.trace_style
        if style > 0 :
            orientation = self.robot._getOrientation()
            colour = self.robot.trace_colour
            self.robot.line_trace.append( (x, y, x, y, orientation, style, colour) )
        self.robot.turn_right()  # must occur after line_trace.append
        self.update_refresh()

    def turn(self, orient):
        x, y = self.robot.getPos()
        style = self.robot.trace_style
        if style > 0 :
            orientation = self.robot._getOrientation()
            colour = self.robot.trace_colour
            self.robot.line_trace.append( (x, y, x, y, orientation, style, colour) )
        self.robot.turn(orient)  # must occur after line_trace.append
        self.update_refresh()

    def pick_beeper(self):
        self.robot.pick_beeper() # may raise an exception
        self.update_refresh()

    def put_beeper(self):
        self.robot.put_beeper() # may raise an exception
        self.update_refresh()

    #--- functions

    def getPos(self):
        return self.robot.getPos()

    def getName(self):
        return self.robot.getName()

    def getNbBeepers(self):
        return self.robot.getNbBeepers()

    def setPos(self, col, row):
        self.robot._setPos(col,row)
        self.update_refresh()

    def setName(self, name):
        self.robot.setName(name)

    def setNbBeepers(self, beepers):
        self.robot._setNbBeepers(beepers)

    def getOrientation(self):
        return self.robot.getOrientation()

    def front_is_clear(self):
        return self.robot.front_is_clear()

    def left_is_clear(self):
        return self.robot.left_is_clear()

    def right_is_clear(self):
        return self.robot.right_is_clear()

    def is_clear(self, dir):
        return self.robot.is_clear(dir)

    def carries_beepers(self):
        return self.robot.any_beepers_in_beeper_bag()

    def on_beeper(self):
        return self.robot.on_beeper()

    def roll_dice(self, n):
        return self.robot.roll_dice(n)

    #--- display controls

    def update_refresh(self):
#        wx.Yield()
        self.world.DoDrawing()
        self.WorldDisplay.drawImage()
        self.WorldDisplay.Refresh()
#        wx.Yield()

    def set_images(self,north,south,east,west) :
        self.robot.set_images(north,south,east,west)
        self.world.DoDrawing()
        self.WorldDisplay.drawImage()
        self.WorldDisplay.Refresh()

class RURPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent, -1)
        self.parent = parent
        wx.EVT_SIZE(self, self.OnSize)
        # The following will occupy the space not used by the Layout Algorithm
        self.parent.WorldDisplay = WorldGUI(self, -1)

    def OnSize(self, event):
        wx.LayoutAlgorithm().LayoutWindow(self, self.parent.WorldDisplay)

class RURFrame(wx.Frame):
    def __init__(self,parent,titre,world_filename):
        wx.Frame.__init__(self, None, -1,  _(titre), size = (510, 550), style=wx.DEFAULT_FRAME_STYLE)
        self.parent=parent
        self.world_filename=world_filename
        icon = wx.EmptyIcon()
        icon.CopyFromBitmap(images.ICON)
        self.SetIcon(icon)
        self.statusbar = self.CreateStatusBar()
        self.Show(True)
        self.window = RURPanel(self)
        self.world = self.WorldDisplay.world
        if self.world_filename != None :
              try :
                  txt = open(self.world_filename, 'r').read()
              except:
                  rD.rurMessageDialog(
                         _("Fichier monde %s inexistant\nIl ne sera pas chargé")%
                         _(self.world_filename),
                         _("Fichier monde"))
                  return
              try :
                  txt = parser.FixLineEnding(txt)
                  flag = parser.ParseWorld(txt)
                  if not flag:
                      raise IOError
                  self.backup_dict = {} # used to 'reset' the world
                  exec txt in self.backup_dict # extracts avenues, streets, robot,
                                               # walls and beepers

                  av = self.backup_dict['avenues']
                  st = self.backup_dict['streets']
                  self.SetSize((120+40*av, 130+40*st))
                  self.world.resetDimensions(av, st)
                  for corner in self.world.beepers_dict:
                      del self.world.beepers_dict[corner] # empty, but keep reference
                  for corner in self.backup_dict['beepers']:
                      self.world.beepers_dict[corner] = self.backup_dict[
                                                                  'beepers'][corner]
                  for col, row in self.world.walls_list:
                      self.world.walls_list.remove((col, row)) # empty, but keep ref.
                  for col, row in self.backup_dict['walls']:
                      self.world.walls_list.append((col, row))
              except:
                  rD.rurMessageDialog(
                         _("Erreurs dans le fichier monde %s\nIl ne sera pas chargé")%
                         _(self.world_filename),
                         _("Fichier monde"))
        self.window.SetFocus()
        self.SendSizeEvent()  # added to attempt to solve problem on MacOS
        wx.EVT_CLOSE(self, self.OnClose)
        self.onExit=False

    def SetWorld(self,world_filename):
        self.world_filename=world_filename
        self.world = self.WorldDisplay.world
        if self.world_filename != None :
              try :
                  txt = open(self.world_filename, 'r').read()
              except:
                  rD.rurMessageDialog(
                         _("Fichier monde %s inexistant\nIl ne sera pas chargé")%
                         _(self.world_filename),
                         _("Fichier monde"))
                  return
              try :
                  txt = parser.FixLineEnding(txt)
                  flag = parser.ParseWorld(txt)
                  if not flag:
                      raise IOError
                  self.backup_dict = {} # used to 'reset' the world
                  exec txt in self.backup_dict # extracts avenues, streets, robot,
                                               # walls and beepers

                  av = self.backup_dict['avenues']
                  st = self.backup_dict['streets']
                  self.SetSize((120+40*av, 130+40*st))
                  self.world.resetDimensions(av, st)
                  for corner in self.world.beepers_dict:
                      del self.world.beepers_dict[corner] # empty, but keep reference
                  for corner in self.backup_dict['beepers']:
                      self.world.beepers_dict[corner] = self.backup_dict[
                                                                  'beepers'][corner]
                  for col, row in self.world.walls_list:
                      self.world.walls_list.remove((col, row)) # empty, but keep ref.
                  for col, row in self.backup_dict['walls']:
                      self.world.walls_list.append((col, row))
              except:
                  rD.rurMessageDialog(
                         _("Erreurs dans le fichier monde %s\nIl ne sera pas chargé")%
                         _(self.world_filename),
                         _("Fichier monde"))
        self.window.SetFocus()

    def OnClose(self, event):
        self.parent.onExit=True


class Horloge (threading.Thread) :
    def __init__(self,delay) :
        threading.Thread.__init__(self)
        self.delay = delay
    def run(self) :
        global App
        while True :
            time.sleep(delay)
            App.ProcessIdle()

def HandlerNone(event):
    pass

class Application():
    def __init__(self,title="wxRUR - Application",world=None):
        self.frame = RURFrame(self,title,world)
        self.onExit = False
        self.KeyDelay=0.01
        self.TimerPeriod=0.5
        self.onTimerEvent=HandlerNone
        wx.EVT_CHAR(self.frame.WorldDisplay, HandlerNone)
    def __del__(self):
        self.frame.OnClose()
    def SetWorld(self,world):
        if not self.onExit :
            self.frame.SetWorld(world)
    def SetBackgroundColour(self, colour="white"):
        if not self.onExit :
            self.frame.world.background_colour = wx.Brush(colour)
            self.frame.world.background_images_created = False
            self.frame.WorldDisplay.SetBackgroundColour(colour)
    def SetColours(self, background="white", maze="white", walls="brown", border="black"):
        if not self.onExit :
            self.frame.world.background_colour = wx.Brush(background)
            self.frame.world.maze_colour = wx.Brush(maze)
            self.frame.world.wall_outside_colour = border
            self.frame.world.wall_inside_colour = walls
            self.frame.world.background_images_created = False
            self.frame.WorldDisplay.SetBackgroundColour(background)
            self.frame.world.DoDrawing()
            self.frame.WorldDisplay.drawImage()
            self.frame.WorldDisplay.Refresh()
    def SetGridColours(self, grid="light grey", label="black"):
        if not self.onExit :
            self.frame.world.grid_colour = grid
            self.frame.world.wall_grid_colour = label
            self.frame.world.background_images_created = False
            self.frame.world.DoDrawing()
            self.frame.WorldDisplay.drawImage()
            self.frame.WorldDisplay.Refresh()
    def AddBeeper(self, col=1, row=1):
        if not self.onExit :
            if (col, row) in self.frame.world.beepers_dict:
                self.frame.world.beepers_dict[(col, row)] += 1
            else :
                self.frame.world.beepers_dict[(col, row)] = 1
            self.frame.world.background_images_created = False
            self.frame.world.DoDrawing()
            self.frame.WorldDisplay.drawImage()
            self.frame.WorldDisplay.Refresh()
    def RemoveBeeper(self, col=1, row=1):
        if not self.onExit :
            if (col, row) in self.frame.world.beepers_dict:
                self.frame.world.beepers_dict[(col, row)] -= 1
                if self.frame.world.beepers_dict[(col, row)] <= 0 :
                    del self.frame.world.beepers_dict[(col, row)]
            self.frame.world.background_images_created = False
            self.frame.world.DoDrawing()
            self.frame.WorldDisplay.drawImage()
            self.frame.WorldDisplay.Refresh()
    def SetBeeperColours(self, inside="white", border="cadet blue", numbers="black"):
        if not self.onExit :
            self.frame.world.beeper_outside_colour = border
            self.frame.world.beeper_inside_colour = inside
            self.frame.world.beeper_number_colour = numbers
            self.frame.world.background_images_created = False
            self.frame.world.DoDrawing()
            self.frame.WorldDisplay.drawImage()
            self.frame.WorldDisplay.Refresh()
    def InputString(self, text='', title="Saisie d'une chaine"):
        if not self.onExit :
            user_response = None
            dlg = wx.TextEntryDialog(None, text, title, '')
            if dlg.ShowModal() == wx.ID_OK:
                user_response = dlg.GetValue()
            dlg.Destroy()
            return user_response
    def InputInt(self, text='', title="Saisie d'un entier"):
        if not self.onExit :
            user_response = None
            dlg = wx.TextEntryDialog(None, text, title, '')
            if dlg.ShowModal() == wx.ID_OK:
                user_response = dlg.GetValue()
            dlg.Destroy()
            return int(user_response)
    def InputFloat(self, text='', title="Saisie d'un flottant"):
        if not self.onExit :
            user_response = None
            dlg = wx.TextEntryDialog(None, text, title, '')
            if dlg.ShowModal() == wx.ID_OK:
                user_response = dlg.GetValue()
            dlg.Destroy()
            return float(user_response)
    def TimerEventHandler(self,onTimerEvent=None,TimerPeriod=0.5) :
        if not self.onExit :
            if onTimerEvent != None :
                self.TimerPeriod=TimerPeriod
                self.onTimerEvent=onTimerEvent
    def KeyEventHandler(self,onKeyEvent=None,KeyDelay=0.01) :
        if not self.onExit :
            if onKeyEvent != None :
                self.KeyDelay=KeyDelay
                wx.EVT_CHAR(self.frame.WorldDisplay, onKeyEvent)
    def ShowMessage(self,text='',title='Message') :
        if not self.onExit :
            messageDialog = wx.MessageDialog(None, text, title, wx.OK )
            messageDialog.ShowModal()
            messageDialog.Destroy()
    def SetStatusText(self,text='                                          ') :
        if not self.onExit :
            self.frame.statusbar.SetStatusText(text)
    def MainLoop(self,duration=None,onTimerEvent=None,TimerPeriod=0.5,onKeyEvent=None,KeyDelay=0.01):
        self.onExit = False
        self.TimerEventHandler(onTimerEvent,TimerPeriod)
        self.KeyEventHandler(onKeyEvent,KeyDelay)
        evtloop = wx.EventLoop()
        old = wx.EventLoop.GetActive()
        wx.EventLoop.SetActive(evtloop)
        self.duration = duration
        self.start=time.clock()
        while not self.onExit and (duration==None or time.clock() < self.start + duration) :
            self.timeSpend = time.clock() - self.start
            for i in range(int(self.TimerPeriod/self.KeyDelay)) :
                self.timeSpend = time.clock() - self.start
                while evtloop.Pending():
                    self.timeSpend = time.clock() - self.start
                    evtloop.Dispatch()
                if self.onExit :
                    break
                time.sleep(self.KeyDelay)
                if self.onTimerEvent!=None and i==0:
                    self.onTimerEvent(None)
                if self.onExit :
                    break
            if self.onExit :
                break
        self.timeSpend = time.clock() - self.start
        wx.EventLoop.SetActive(old)
        if self.duration != None and self.timeSpend > self.duration :
            self.timeSpend = self.duration
        self.onExit = False
        return int(self.timeSpend)
    def TimeLoop(self) :
        return int(self.timeSpend)
    def ExitMainLoop(self) :
        self.onExit=True
    def Close(self) :
        beepers = self.frame.world.beepers_dict.keys()
        for beeper in beepers :
            del self.frame.world.beepers_dict[beeper]
        self.frame.Destroy()
    def Quit(self,G=globals()) :
        self.Close()
