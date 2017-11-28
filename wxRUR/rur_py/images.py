# RUR-PLE: Roberge's Used Robot - a Python Learning Environment
#    images.py - Contains all images for RUR-PLE
#    Version 0.8.7
#    Author: Andre Roberge    Copyright  2005
#    andre.roberge@gmail.com

import misc
import wx

try:
    PACMAN_S = wx.Image(misc.IMAGE_DIR+'/pacman_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    PACMAN_N = wx.Image(misc.IMAGE_DIR+'/pacman_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    PACMAN_E = wx.Image(misc.IMAGE_DIR+'/pacman_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    PACMAN_W = wx.Image(misc.IMAGE_DIR+'/pacman_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading pacman_?.png in RobotFactory.py"
    
try:
    GREY_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREY_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREY_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREY_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading robot_?.png in RobotFactory.py"

try:
    YELLOW_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/yellow_robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    YELLOW_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/yellow_robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    YELLOW_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/yellow_robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    YELLOW_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/yellow_robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading yellow_robot_?.png in RobotFactory.py"

try:
    GREEN_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/green_robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREEN_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/green_robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREEN_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/green_robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    GREEN_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/green_robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading green_robot_?.png in RobotFactory.py"

try:
    BLUE_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/blue_robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    BLUE_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/blue_robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    BLUE_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/blue_robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    BLUE_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/blue_robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading blue_robot_?.png in RobotFactory.py"

try:
    LIGHT_BLUE_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/light_blue_robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    LIGHT_BLUE_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/light_blue_robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    LIGHT_BLUE_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/light_blue_robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    LIGHT_BLUE_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/light_blue_robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading light_blue_robot_?.png in RobotFactory.py"

try:
    PURPLE_ROBOT_S = wx.Image(misc.IMAGE_DIR+'/purple_robot_s.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    PURPLE_ROBOT_N = wx.Image(misc.IMAGE_DIR+'/purple_robot_n.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    PURPLE_ROBOT_E = wx.Image(misc.IMAGE_DIR+'/purple_robot_e.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
    PURPLE_ROBOT_W = wx.Image(misc.IMAGE_DIR+'/purple_robot_w.png',
                      wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading purple_robot_?.png in RobotFactory.py"


try:
    ICON = wx.Image(misc.IMAGE_DIR+'/rur16x16.png',
                  wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print "Problem loading rur16x16.png in start.py"

try:
    HIT_WALL_IMAGE = wx.Image(misc.IMAGE_DIR+'/ouch.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading ouch.png in dialogs.py"

try:
    MINI_SPLASH = wx.Image(misc.IMAGE_DIR+'/splash_screen_small.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap()
except Exception,info:
    print __name__, info
    print " Problem loading splash_screen_small.png in dialogs.py"

