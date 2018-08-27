#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 21 16:45:03 2018

@author: inesverissimo
"""


# -*- coding: utf-8 -*-
"""
Created 6th June 2018
Author: Ines V.

Descrip: Try out script for simple visual search task
"""

from psychopy import visual, core, event, monitors #import some libraries from PsychoPy
import numpy as np
import random 
import pickle
import os
import math
import pyglet

#######################################
### functions ###
# draw fixation cross function
def draw_fixation(posit,lineSize,linecolor,linewidth): 
    
    t = lineSize/2.0
    vertical_line = visual.Line(win,start = (posit[0],posit[1]-t),end = (posit[0],posit[1]+t),lineColor = linecolor,lineWidth=linewidth)
    horizontal_line = visual.Line(win,start = (posit[0]-t,posit[1]),end = (posit[0]+t,posit[1]),lineColor = linecolor,lineWidth=linewidth)
    
    vertical_line.draw()
    horizontal_line.draw() 
    
# transform polar coordinates to cartesian
    
def pol2cart(hyp, theta):  
    x = hyp * np.cos(np.deg2rad(theta))
    y = hyp * np.sin(np.deg2rad(theta))
    return(x, y)
    
# Calculate the number of degrees that correspond to a single pixel
# and then calculate distance in pixels
# dist_in_deg - distance in deg of visual angle
#h - height of screen, d - distance from monitor, r - vertical resolution
def ang2pix(dist_in_deg,h,d,r): 
    deg_per_px = math.degrees(math.atan2(0.5*h,d))/(0.5*r)
    dist_in_px = (x / deg_per_px for x in dist_in_deg)#dist_in_deg/deg_per_px
    return dist_in_px 

# determines list with random positions of x and y, taking into account the set size
def rand_pos(pos_x,pos_y,set_size):
    
    combinations = [[a,b] for a in pos_x for b in pos_y]
    poslist_xy = random.sample(combinations,set_size)
    return poslist_xy


########## Initial parameters #########
# paths to images
dir_item = '/Users/inesverissimo/Desktop/imagens/items'
dir_bckg = '/Users/inesverissimo/Desktop/imagens/background'
# general info
num_blk = 2 #number of blocks
num_trl = 27 #number of trials
perc_tgrt = 0.7 #fraction of trials with target present 
# screen info 
screenHeight = 30 #height of the screen in cm 
screenDis = 71    #distance between screen and chinrest in cm       
hRes = 1920 #900 #1920
vRes = 1080#700 #1080      
backCol = 'black'
# fixation cross info
fixpos = (0,0)
fixlineSize = 15
fixcolor = 'white'
linewidth = 4
# stim info
num_bckg = len(next(os.walk(dir_bckg))[2]) #number of possible background images
num_distr = len(next(os.walk(dir_item))[2])-1 #number of possible distractor images
set_siz = [1,4,6]#[1,4,10] 
dist = 360/max(set_siz) #distance between stim (degrees)
pos_dgr = np.arange(0,360,dist) #all pos (degree)
ecc_deg = np.array([4,8,10])#[3,6,9]) # eccentricity in degrees
ecc_pix = np.array(tuple(ang2pix(ecc_deg,screenHeight,screenDis,vRes))) # eccentricity in pixels
stim_time = 2.5 #stimulus presentation time (seconds)
iti = 3.4 #inter-trial-interval (seconds)

#########

RT_trl = np.array(np.zeros((num_blk,num_trl)),object) #array for all RTs
img_index = np.zeros((num_blk,num_trl),dtype=int) #array to save all indexes used


set_idx = np.zeros((num_blk,num_trl),dtype=int) #array to save item indexes used
trgt_idx = np.zeros((num_blk,num_trl),dtype=int) #array to save target/no target indexes used
bckg_idx = np.zeros((num_blk,num_trl),dtype=int) #array to save background indexes used

pos_trl = np.array(np.zeros((1,num_trl)),object) #array to save all positions used in trials of 1 block
pos_blk = np.array(np.zeros((num_blk,num_trl)),object) #array to save all positions used in all blocks

    
#######################################
    
# x,y position arrays
zr = np.zeros(len(pos_dgr)) # inicialize all pos in same ecc
poslist_x = np.append([zr,zr],[zr],axis=0)
poslist_y = np.append([zr,zr],[zr],axis=0)

for w in range(len(ecc_deg)): #all possible x and y positions for every eccentricity
    (xpos,ypos) = pol2cart(ecc_pix[w],pos_dgr)
    poslist_x[w] = xpos
    poslist_y[w] = ypos

## define type of trials
#number of items in set, equally distributed along trials     
set_type = np.empty((0,num_trl/len(set_siz))) 

for g in range(len(set_siz)):
    it = np.repeat(set_siz[g],num_trl/len(set_siz))
    set_type = np.append(set_type, [it])
 
# ecc, equally distributed for same set sizes
trl_ecc = np.empty((0,(num_trl/len(set_siz))/len(ecc_deg)))    

for g in range(len(ecc_deg)):
    it = np.repeat(ecc_deg[g],round((num_trl/len(set_siz))/len(ecc_deg)))
    trl_ecc = np.append(trl_ecc, [it])

trl_ecc_all = np.tile(trl_ecc,len(set_siz)) #repeat for all set sizes
   
#0-target absent, 1-target present, equally distr. along ecc
trl_type = np.append(np.repeat([1],round((num_trl/len(set_siz))/len(ecc_deg))*perc_tgrt),[np.repeat([0],round((num_trl/len(set_siz))/len(ecc_deg)*(1-perc_tgrt)))])

trl_type_all = np.tile(trl_type,len(ecc_deg)*len(set_siz)) #repeat for all set sizes
    
#info about trials (3xnum_trl with #set,ecc,trgt)
trls = np.vstack((set_type,trl_ecc_all))
trls = np.vstack((trls,trl_type_all))
trls_idx = range(0,num_trl) #range of indexes for all trials      

# create a window
#win = visual.Window(size=(hRes,vRes),monitor="testMonitor",screen=0,fullscr=True,color=backCol,units="pix",winType='pyglet')
win = visual.Window(size=(hRes,vRes),units="pix",color=backCol,screen=1,winType='pyglet')
#win = visual.Window(size=(hRes,vRes),units="pix",viewPos=[1280,0],color=backCol,screen=1,winType='pyglet')

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
    
    #shuffle indexes to guarantee random trials
    np.random.shuffle(trls_idx) 
    
    # indexes for backgrounds to use in block
    cur_bckg = np.random.choice(num_bckg-1, num_trl)
         
    for i in range(num_trl): #start trials
        
        #draw background
        img_bckg = visual.ImageStim(win,image=dir_bckg+"/back%d.jpg"%(cur_bckg[i]),units="pix",pos = (0,0))
        img_bckg.draw()
        #draw fixation
        draw_fixation(fixpos,fixlineSize,fixcolor,linewidth)        
        
        # define positions according to current set size and ecc
        ecc_idx = np.where(ecc_deg == trls[1,trls_idx[i]]) #index for eccentricity
        ecc_idx = ecc_idx[0][0]
        
        poslist_xy = rand_pos(poslist_x[ecc_idx],poslist_y[ecc_idx],int(trls[0,trls_idx[i]]))
        
        # define distractors to use in trial
        img_distr_idx = np.random.choice(num_distr-1, int(trls[0,trls_idx[i]]))

        if trls[2,trls_idx[i]] == 1: #target present
                for k in range(int(trls[0,trls_idx[i]])):
                    if k == 0: # target
                        img_trgt = visual.ImageStim(win,image=dir_item+"/trgt.png",units="pix",pos = poslist_xy[k])
                        img_trgt.draw()
                        
                    else: #distractor
                        img_distr = visual.ImageStim(win,image=dir_item+"/dist%d.png"%(img_distr_idx[k-1]),units="pix",pos = poslist_xy[k])
                        img_distr.draw()     
               
        else: #target absent
                for k in range(int(trls[0,trls_idx[i]])): #distractors
                    img_distr = visual.ImageStim(win,image=dir_item+"/dist%d.png"%(img_distr_idx[k]),units="pix",pos = poslist_xy[k])    
                    img_distr.draw()   
                            
        win.flip()
        
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
        
    #img_index[j][i] = img_distr_idx # image index for all blocks and trials
    win.flip() # flip the screen
    core.wait(iti) #pause    

#dict_var = {'RT':RT_trl,'indexes':img_index}

#save data of interest
#with open('data_FNemo_pp_' + pp + '.pickle', 'wb') as write_file:
#    pickle.dump(dict_var, write_file,protocol=pickle.HIGHEST_PROTOCOL)

#cleanup
win.close() #close display
core.quit()

