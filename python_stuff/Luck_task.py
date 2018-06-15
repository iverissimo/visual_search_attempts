# -*- coding: utf-8 -*-
"""
Created 13th June 2018
Author: Ines V.

Descrip:  visual search display, similar to the one in Luck et al 
Independent hemispheric attentional systems mediate visual search
in split-brain patients
"""

from psychopy import visual, core, event #import some libraries from PsychoPy
import numpy as np
import random 
import math
#import pickle

#######################################

############# functions #################
# draw fixation cross function
def draw_fixation(posit,lineSize,linecolor): 
    
    t = lineSize/2.0
    vertical_line = visual.Line(win,start = (posit[0],posit[1]-t),end = (posit[0],posit[1]+t),lineColor = linecolor,lineWidth=linewidth)
    horizontal_line = visual.Line(win,start = (posit[0]-t,posit[1]),end = (posit[0]+t,posit[1]),lineColor = linecolor,lineWidth=linewidth)
    
    vertical_line.draw()
    horizontal_line.draw() 
    
# Calculate the number of degrees that correspond to a single pixel
# and then calculate distance in pixels
# dist_in_deg - distance in deg of visual angle
#h - height of screen, d - distance from monitor, r - vertical resolution
def ang2pix(dist_in_deg,h,d,r): 
    deg_per_px = math.degrees(math.atan2(0.5*h,d))/(0.5*r)
    dist_in_px = dist_in_deg/deg_per_px
    return dist_in_px 
    
#######################################

########## Initial parameters #########
# general info
num_blk = 2 #number of blocks
num_trl = 12 #number of trials
stim_time = 2.5 #stimulus presentation time (seconds)
iti = 3.4 #inter-trial-interval (seconds)
# screen info   
hRes = 1920 #900 #1920
vRes = 1080 #700 #1080  
screenHeight = 30 # height of the screen in cm 
screenDis = 71    # distance between screen and chinrest in cm     
backCol = 'black'
# fixation cross info
fixpos = (0,0)
fixlineSize = 15
fixcolor = 'white'
linewidth = 2
# stim info
sqr_siz_deg = 0.4 # length of square (in degres of visual angle)
sqr_siz_pix = ang2pix(sqr_siz_deg,screenHeight,screenDis,vRes) # length of square in pix
sqr_color_b = 'blue'
sqr_color_r = 'red'
set_num = [2,4,8]
right_dist_x_deg = [1.1,4.4]
dist_y_deg = 6.8/2
#limit of x and y axis for blue square (red positions will be relative to blue)
right_dist_min_x = ang2pix(right_dist_x_deg[0],screenHeight,screenDis,vRes) #min dist in x axis for right visual field
right_dist_max_x = ang2pix(right_dist_x_deg[1],screenHeight,screenDis,vRes) -  sqr_siz_pix #max dist in x axis for right visual field
left_dist_min_x = - right_dist_max_x #min dist in x axis for left visual field
left_dist_max_x = - right_dist_min_x #max dist in x axis for left visual field
dist_min_y = - ang2pix(dist_y_deg,screenHeight,screenDis,vRes) + sqr_siz_pix #min dist in y axis
dist_max_y = ang2pix(dist_y_deg,screenHeight,screenDis,vRes) - sqr_siz_pix #max dist in y axis
# all possible positions
right_poslist_x = np.arange(right_dist_min_x,right_dist_max_x,2*sqr_siz_pix)
left_poslist_x = np.arange(left_dist_min_x,left_dist_max_x,2*sqr_siz_pix)
poslist_y = np.arange(dist_min_y,dist_max_y,4*sqr_siz_pix)
#labels
trl_type = np.repeat([1,2],num_trl/2) #type of trial uni (1) or bilateral (2)
np.random.shuffle(trl_type)
set_siz = np.repeat(set_num,num_trl/len(set_num)) #set size
np.random.shuffle(set_siz)
lbl_distr = 2
lbl_trgt = 1 
side_type = np.repeat([1,2],num_trl/4) #unilateral trial can be left (1) or right (2)
np.random.shuffle(side_type)

# create a window
#win = visual.Window(size= (hRes, vRes), monitor="testMonitor", color = backCol, units="pix")
win = visual.Window(size= (hRes, vRes), color = backCol, units='pix',fullscr  = True, screen = 1,allowStencil=True)   
   
#pause
core.wait(2.0)

draw_fixation(fixpos,fixlineSize,fixcolor) #draw fixation 
win.flip() # flip the screen
core.wait(2.0) #pause

k = 0 #counter for left vs right visual field

for i in range(num_trl):
    
    if trl_type[i] == 1: #unilateral trial
        
        if side_type[k] == 1: #left field
            poslist_xy = np.vstack((np.random.choice(left_poslist_x,set_siz[i]),np.random.choice(poslist_y,set_siz[i])))
        else: #right field
            poslist_xy = np.vstack((np.random.choice(right_poslist_x,set_siz[i]),np.random.choice(poslist_y,set_siz[i])))
        
        k += 1 #increment counter
        
        poslist_lbl = np.append(np.full((1,len(poslist_xy[0])-1),lbl_distr),lbl_trgt)
        poslist = np.vstack((poslist_xy,poslist_lbl))

        for j in range(set_siz[i]):
            if poslist[2][j] == 1: # target
                blue_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                       lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_b,
                                       fillColorSpace='rgb',pos=(poslist[0][j],poslist[1][j]-sqr_siz_pix))
                red_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                      lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_r,
                                      fillColorSpace='rgb',pos=(poslist[0][j],poslist[1][j]))

            else: #distractor
                blue_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                       lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_b,
                                       fillColorSpace='rgb',pos=(poslist[0][j],poslist[1][j]))
                red_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                      lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_r,
                                      fillColorSpace='rgb',pos=(poslist[0][j],poslist[1][j]-sqr_siz_pix))
            
            blue_sqr.draw()
            red_sqr.draw()          
        draw_fixation(fixpos,fixlineSize,fixcolor) #draw fixation    
        win.flip() # flip the screen
        core.wait(stim_time) #pause 
        
    else: #bilateral trial
        
        poslist_x = np.append(np.random.choice(left_poslist_x,set_siz[i]/2),np.random.choice(right_poslist_x,set_siz[i]/2))
        poslist_xy = np.vstack((poslist_x,np.random.choice(poslist_y,set_siz[i])))
       
        poslist_lbl = np.append(np.full((1,len(poslist_xy[0])-1),lbl_distr),lbl_trgt)
        poslist = np.vstack((poslist_xy,poslist_lbl))

        for j in range(set_siz[i]):
            if poslist[2][j] == 1: # target
                blue_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                       lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_b,
                                       fillColorSpace='rgb',pos=(poslist[0][j],poslist[1][j]-sqr_siz_pix))
                red_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                      lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_r,
                                      fillColorSpace='rgb',pos=(poslist[0][j],poslist[1][j]))

            else: #distractor
                blue_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                       lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_b,
                                       fillColorSpace='rgb',pos=(poslist[0][j],poslist[1][j]))
                red_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                      lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_r,
                                      fillColorSpace='rgb',pos=(poslist[0][j],poslist[1][j]-sqr_siz_pix))
            
            blue_sqr.draw()
            red_sqr.draw()          
        draw_fixation(fixpos,fixlineSize,fixcolor) #draw fixation    
        win.flip() # flip the screen
        core.wait(stim_time) #pause 
    
    draw_fixation(fixpos,fixlineSize,fixcolor) #draw fixation 
    win.flip() # flip the screen
    core.wait(iti) #pause    
        
#cleanup
win.close() #close display
core.quit()

"""
pos_b_sqr_x = 100 #blue square y position 
pos_b_sqr_y = 100 #blue square y position
pos_r_sqr_x = pos_b_sqr_x#red square y position 
pos_r_sqr_y = pos_b_sqr_y-sqr_siz_pix #red square y position
 
#######################################

# create a window
#win = visual.Window(size= (hRes, vRes), monitor="testMonitor", color = backCol, units="pix")
win = visual.Window(size= (hRes, vRes), color = backCol, units='pix',fullscr  = True, screen = 1,allowStencil=True)   
   
#pause
core.wait(2.0)

blue_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                       lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_b,
                       fillColorSpace='rgb',pos=(pos_b_sqr_x,pos_b_sqr_y))
red_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                       lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_r,
                       fillColorSpace='rgb',pos=(pos_r_sqr_x,pos_r_sqr_y))

draw_fixation(fixpos,fixlineSize,fixcolor) #draw fixation 
win.flip() # flip the screen
core.wait(2.0) #pause

draw_fixation(fixpos,fixlineSize,fixcolor) #draw fixation 
blue_sqr.draw()
red_sqr.draw()
win.flip() # flip the screen
core.wait(10.0) #pause 

"""
