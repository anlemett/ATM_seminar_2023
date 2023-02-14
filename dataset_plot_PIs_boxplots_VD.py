import pandas as pd
import os
import matplotlib.pyplot as plt

#conda install -c conda-forge mscorefonts

#from matplotlib import font_manager
#print(font_manager.findfont("Times New Roman") )

# activate latex text rendering
#plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "Times New Roman"
#plt.rcParams["font.family"] = "serif"
#plt.rcParams["font.serif"] = "Times New Roman"
#plt.rcParams['font.weight']= 'bold'

from matplotlib import rcParams
rcParams.update({'figure.autolayout': False})

import statistics
#from textwrap import wrap

AIRPORT_ICAO = "ENGM"

splitted_datasets = False

PI_name = "VD"

PI_y_label = "Vertical Deviation (ft x min.)"
figure_filename = "boxplot_VD_"

DATASETS = ["TT", "PM", "nonPM"]
figure_filename = figure_filename + "3ds"
        
        
PIs_dict = {}


DATA_DIR = os.path.join("data", AIRPORT_ICAO)
PIs_DIR = os.path.join(DATA_DIR, "PIs")


for dataset in DATASETS:
    
    input_filename = dataset + "_VD.csv"
            
        
    full_input_filename = os.path.join(PIs_DIR, input_filename)
    PIs_df = pd.read_csv(full_input_filename, sep=',',
        names = ['flightId', 'VD', 'date', 'something1', 'something2'])
    PIs_df.set_index(['flightId'], inplace=True)
    #print(PIs_df.head(1))
        
    PIs_dict[dataset] = PIs_df['VD']
    
    PI_median = PIs_dict[dataset].median()
    PI_mean = PIs_dict[dataset].mean()
    PI_std = statistics.stdev(PIs_dict[dataset])
    PI_min = PIs_dict[dataset].min()
    PI_max = PIs_dict[dataset].max()
        
    #print(dataset_name, PI_name, PI_median, PI_mean, PI_std, PI_min, PI_max)
    
    #print(dataset_name + " " + PI_name + f" {PI_median:.2f}" + f" {PI_min:.2f}" + f" {PI_max:.2f}")
    
    # median/mean/std/min/max    
    print(dataset + " " + PI_name + f" {PI_median:.2f}" + f" {PI_mean:.2f}" + f" {PI_std:.2f}" +
            f" {PI_min:.2f}" + f" {PI_max:.2f}")
    
               
#print(len(PIs_dict))         

#fig, ax = plt.subplots(1, 1,figsize=(7,5))
fig, ax = plt.subplots(1, 1,figsize=(7,5), dpi = None)

boxprops = dict(linestyle='--', linewidth=1, color='gray')
meanpointprops = dict(marker='s', markersize=5, markeredgecolor='dimgrey', markerfacecolor='grey')
box_plot = ax.boxplot(PIs_dict.values(), sym='+', boxprops=boxprops, meanprops=meanpointprops, patch_artist=True, showmeans=True)

###########Gray version###################

#dimgray = (105/255,105/255,105/255)
   
#for element in ['boxes', 'whiskers', 'caps', 'medians']:
#    plt.setp(box_plot[element], color=dimgray)
        
#for element in ['fliers']:
#    plt.setp(box_plot[element], markeredgecolor = dimgray, alpha = 0.1)

#for patch in box_plot['boxes']:
#    patch.set(facecolor='lightgray')

#for whisker in box_plot['whiskers']:
#    whisker.set(linestyle ="--")

###########Color version###################

# Colors are from: https://colorbrewer2.org/#type=diverging&scheme=RdYlBu&n=3
# 3 data classes, diverging, colorblind safe, print friendly
orange_rgb = (252,141,89)
yellow_rgb = (255,255,191)
blue_rgb = (145,191,219)

orange = tuple(c/255 for c in orange_rgb)
yellow = tuple(c/255 for c in yellow_rgb)
blue = tuple(c/255 for c in blue_rgb)

if not splitted_datasets:
    colors = [orange, yellow, blue]
else:
    colors = [orange, orange, yellow, yellow, blue, blue]

for patch, color in zip(box_plot['boxes'], colors):
    patch.set_facecolor(color)
    #patch.set_alpha(0.5)

for flier, color in zip(box_plot['fliers'], colors):
    #flier.set(markeredgecolor = color, alpha = 0.9)
    flier.set(markeredgecolor = 'darkgray', alpha = 0.9)
    
for element in ['whiskers', 'caps', 'medians']:
    plt.setp(box_plot[element], color='dimgray')

for whisker in box_plot['whiskers']:
    whisker.set(linestyle ="--")

########################################

ax.set_xticklabels(["TT", "PM", "nonPM"], fontsize=16)

plt.ylabel(PI_y_label, fontsize=22)
plt.yticks(fontsize=16)

plt.tight_layout()

plt.savefig(os.path.join(PIs_DIR, figure_filename + ".eps"), dpi=300)

plt.show()
