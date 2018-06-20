# -*- coding: utf-8 -*-
"""
Created 13th June 2018
Author: Ines V.

Descrip:  visual search display, similar to the one in Luck et al 
Independent hemispheric attentional systems mediate visual search
in split-brain patients
"""

from psychopy import visual, core, event 
import numpy as np
import random 
import math
#import itertools
import pickle

#######################################

############# functions #################
# draw fixation cross function
def draw_fixation(posit,lineSize,linecolor,linewidth): 
    
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

# determines list with random positions of x and y, taking into account the set size
def rand_pos(pos_x,pos_y,set_size):
    
    combinations = [[a,b] for a in pos_x for b in pos_y]
    poslist_xy = random.sample(combinations,set_size)
    return poslist_xy

#######################################

########## Initial parameters #########
# general info
num_blk = 2 #total number of blocks
num_trl = 24 #total number of trials
no_trgt = 0.2 #amount of trials that have no target (from 0-1)
num_bi = num_trl/2 #number of bilateral trials
num_uni = num_trl/4 #number of unilateral trials (for one side)
stim_time = 2.5 #stimulus presentation time (seconds)
iti = 3.4 #inter-trial-interval (seconds)
trial_index = np.zeros((num_blk,num_trl),dtype=int) #array to save all indexes used
pos_trl = np.array(np.zeros((1,num_trl)),object) #array to save all positions used in trials of 1 block
pos_blk = np.array(np.zeros((num_blk,num_trl)),object) #array to save all positions used in all blocks
RT_trl = np.array(np.zeros((num_blk,num_trl)),object) #array for all RTs
# screen info   
hRes = 1920 #900 #1920
vRes = 1080 #700 #1080  
screenHeight = 30 #height of the screen in cm 
screenDis = 71    #distance between screen and chinrest in cm     
backCol = 'black'
# fixation cross info
fixpos = (0,0) #position
fixlineSize = 15
fixcolor = 'white'
linewidth = 2
# stim info
sqr_siz_deg = 0.4 #length of square (in degres of visual angle)
sqr_siz_pix = ang2pix(sqr_siz_deg,screenHeight,screenDis,vRes) #length of square in pix
sqr_color_b = 'blue'
sqr_color_r = 'red'
set_num = [2,4,8] #number of items in each set 
right_dist_x_deg = [1.1,4.4] #min and max distance for right VF in degrees
dist_y_deg = 6.8/2 #half size of vertical VF in degrees
#limit of x and y axis for blue square (red positions will be relative to blue)
right_dist_min_x = ang2pix(right_dist_x_deg[0],screenHeight,screenDis,vRes) #min dist in x axis for right visual field
right_dist_max_x = ang2pix(right_dist_x_deg[1],screenHeight,screenDis,vRes) -  sqr_siz_pix #max dist in x axis for right visual field
left_dist_min_x = - right_dist_max_x #min dist in x axis for left visual field
left_dist_max_x = - right_dist_min_x #max dist in x axis for left visual field
dist_min_y = - ang2pix(dist_y_deg,screenHeight,screenDis,vRes) + sqr_siz_pix #min dist in y axis
dist_max_y = ang2pix(dist_y_deg,screenHeight,screenDis,vRes) - sqr_siz_pix #max dist in y axis
# all possible positions in VF in pix
right_poslist_x = np.arange(right_dist_min_x,right_dist_max_x,2*sqr_siz_pix)
left_poslist_x = np.arange(left_dist_min_x,left_dist_max_x,2*sqr_siz_pix)
poslist_y = np.arange(dist_min_y,dist_max_y,4*sqr_siz_pix)
#labels
# 22-bilateral, 12-unilateral RVF, 11-unilateral LVF
trl_type = np.append(np.repeat([22],num_bi),[np.repeat([12],num_uni),np.repeat([11],num_uni)])
#0-target absent, 1-target present
trgt_type_bi = np.append(np.repeat([0],round(num_bi*no_trgt)),np.repeat([1],round(num_bi*(1-no_trgt))))
trgt_type_uni = np.append(np.repeat([0],round(num_uni*no_trgt)),np.repeat([1],round(num_uni*(1-no_trgt))))
trgt_type = np.append(trgt_type_bi,[trgt_type_uni,trgt_type_uni])

for i in range(len(set_num)-1): #set size equal distribution between trls
    if i == 0:
        set_type_bi = np.append(np.repeat(set_num[i],num_bi/len(set_num)),np.repeat(set_num[i+1],num_bi/len(set_num)))
        set_type_uni = np.append(np.repeat(set_num[i],num_uni/len(set_num)),np.repeat(set_num[i+1],num_uni/len(set_num)))
    else:
        set_type_bi = np.append(set_type_bi,np.repeat(set_num[i+1],num_bi/len(set_num)))
        set_type_uni = np.append(set_type_uni,np.repeat(set_num[i+1],num_uni/len(set_num)))

set_type = np.append(set_type_bi,[set_type_uni,set_type_uni])

trls = np.vstack((trl_type,set_type))
trls = np.vstack((trls,trgt_type)) #info about trials (3xnum_trl with type,#set,trgt)
trls_idx = range(0,num_trl) #range of indexes for all trials

# create a window
#win = visual.Window(size= (hRes, vRes), monitor="testMonitor", color = backCol, units="pix")
win = visual.Window(size= (hRes, vRes), color = backCol, units='pix',fullscr  = True, screen = 1,allowStencil=True)   

pp = '0' #raw_input("Participant number: ")
 
#pause
core.wait(2.0)

for j in range(num_blk): #start block
    
    text = 'Block %i' %(j+1)
    BlockText = visual.TextStim(win, text=text, color='white', height=50, pos = (0,140))
    text2 = 'Press spacebar to start'
    PressText = visual.TextStim(win, text=text2, color='white', height=30, pos = (0,-140))
    
    BlockText.draw()
    PressText.draw()
    draw_fixation(fixpos,fixlineSize,fixcolor,linewidth) #draw fixation 
    win.flip()
    event.waitKeys(keyList = 'space') 

    draw_fixation(fixpos,fixlineSize,fixcolor,linewidth) #draw fixation 
    win.flip() # flip the screen
    core.wait(2.0) #pause
    
    np.random.shuffle(trls_idx) #shuffle indexes to guarantee random trials
    
    for i in range(num_trl): #start trials
        
        if trls[0,trls_idx[i]] == 11: #unilateral left VF
            
            poslist_xy = rand_pos(left_poslist_x,poslist_y,trls[1,trls_idx[i]])
            
        elif trls[0,trls_idx[i]] == 12: #unilateral right VF
            
            poslist_xy = rand_pos(right_poslist_x,poslist_y,trls[1,trls_idx[i]])
        
        else: #bilateral VF
        
            poslist_xy_left = rand_pos(left_poslist_x,poslist_y,trls[1,trls_idx[i]]/2)
            poslist_xy_right = rand_pos(right_poslist_x,poslist_y,trls[1,trls_idx[i]]/2)      
            poslist_xy = np.vstack((poslist_xy_left,poslist_xy_right))

    
        if trls[2,trls_idx[i]] == 1: #target present
                for k in range(trls[1,trls_idx[i]]):
                    if k == 0: # target
                        blue_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                       lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_b,
                                       fillColorSpace='rgb',pos=(poslist_xy[0][0],poslist_xy[0][1]-sqr_siz_pix))
                        red_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                      lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_r,
                                      fillColorSpace='rgb',pos=(poslist_xy[0][0],poslist_xy[0][1]))

                    else: #distractor
                        blue_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                       lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_b,
                                       fillColorSpace='rgb',pos=(poslist_xy[k][0],poslist_xy[k][1]))
                        red_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                      lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_r,
                                      fillColorSpace='rgb',pos=(poslist_xy[k][0],poslist_xy[k][1]-sqr_siz_pix))
            
                    blue_sqr.draw()
                    red_sqr.draw()          
                              
        else: #target absent
                for k in range(trls[1,trls_idx[i]]): #distractors
                    blue_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                       lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_b,
                                       fillColorSpace='rgb',pos=(poslist_xy[k][0],poslist_xy[k][1]))
                    red_sqr = visual.Rect(win=win,units='pix',width=sqr_siz_pix,height=sqr_siz_pix,
                                      lineColor=backCol,lineColorSpace='rgb',fillColor=sqr_color_r,
                                      fillColorSpace='rgb',pos=(poslist_xy[k][0],poslist_xy[k][1]-sqr_siz_pix))
            
                    blue_sqr.draw()
                    red_sqr.draw()          
        
        draw_fixation(fixpos,fixlineSize,fixcolor,linewidth) #draw fixation        
        win.flip() #flip the screen
        
        t0 = core.getTime() #get the time (seconds)
        key = [] # reset key to nothing 
           
        while not key:
            key = event.getKeys(keyList = ['space'])
            if core.getTime()-t0 > stim_time:
                break
        
        RT = core.getTime() - t0
        
        if RT > stim_time:
            RT_trl[j][i] = float('nan') #if response takes longer than stim period, then put nan
        else:
            RT_trl[j][i] = RT #else save actual RT
        
        pos_trl[0][i] = np.array(poslist_xy) #all positions in trial
    pos_blk[j][:] = pos_trl # positions for all blocks and trials 
    trial_index[j][:] = trls_idx #index for all blocks and trials
    
    win.flip() # flip the screen
    core.wait(iti) #pause    

dict_var = {'labels':trls,'index':trial_index,'positions':pos_blk,'RT':RT_trl}

#save data of interest
with open('data_Luck_pp_' + pp + '.pickle', 'wb') as write_file:
    pickle.dump(dict_var, write_file,protocol=pickle.HIGHEST_PROTOCOL)

#cleanup
win.close() #close display
core.quit()
