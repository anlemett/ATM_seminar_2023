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
from textwrap import wrap

AIRPORT_ICAO = "ENGM"

splitted_datasets = True
PI_name = "timeOnLevelsPercent"

PI_y_label = "Time Flown Level (\%)"
figure_filename = "boxplot_time_on_levels_PM_"
    
if splitted_datasets:
        DATASETS = ["PM_final_NORTH", "PM_final_SOUTH"]
        figure_filename = figure_filename + "2ds"
else:
    DATASETS = ["PM_final"]
    figure_filename = figure_filename + "1ds"
        
PIs_dict = {}


DATA_DIR = os.path.join("data", AIRPORT_ICAO)
PIs_DIR = os.path.join(DATA_DIR, "PIs")


for dataset in DATASETS:
    
    input_filename = dataset + "_PIs_vertical_by_flights.csv"
    full_input_filename = os.path.join(PIs_DIR, input_filename)
    
    PIs_df = pd.read_csv(full_input_filename, sep=' ')
    
    input_filename = dataset + "_PIs_vertical_by_flights_notPMlegs.csv"
    full_input_filename = os.path.join(PIs_DIR, input_filename)

    PIs_noLegs_df = pd.read_csv(full_input_filename, sep=' ')
    
    if not splitted_datasets:
          
        dataset1_name = "PM"
        dataset2_name = "PM no seq.legs"
           
    else: # 2 datasets vertical
           
        if dataset == "PM_final_NORTH":
            dataset1_name = "PM NORTH"
            dataset2_name = "PM NORTH no deq.legs"
             
        elif dataset == "PM_final_SOUTH":
            dataset1_name = "PM SOUTH"
            dataset2_name = "PM SOUTH no seq.legs"
    
    PIs_dict[dataset1_name] = PIs_df[PI_name]
    PIs_dict[dataset2_name] = PIs_noLegs_df[PI_name]
    
    PI_median = PIs_dict[dataset1_name].median()
    PI_mean = PIs_dict[dataset1_name].mean()
    PI_std = statistics.stdev(PIs_dict[dataset1_name])
    PI_min = PIs_dict[dataset1_name].min()
    PI_max = PIs_dict[dataset1_name].max()
        
    print(PI_median, PI_mean, PI_std, PI_min, PI_max)

    PI_median = PIs_dict[dataset2_name].median()
    PI_mean = PIs_dict[dataset2_name].mean()
    PI_std = statistics.stdev(PIs_dict[dataset2_name])
    PI_min = PIs_dict[dataset2_name].min()
    PI_max = PIs_dict[dataset2_name].max()
    
    print(PI_median, PI_mean, PI_std, PI_min, PI_max)
      

fig, ax = plt.subplots(1, 1,figsize=(7,5), dpi = None)
#fig, ax = plt.subplots(1, 1,figsize=(7,5))
#fig, ax = plt.subplots(1, 1,figsize=(4,3))

dimgray = (105/255,105/255,105/255)

box_plot = ax.boxplot(PIs_dict.values(), sym='+', patch_artist=True)
   
for element in ['boxes']:
    plt.setp(box_plot[element], color=dimgray)

for element in ['whiskers', 'caps', 'medians']:
    plt.setp(box_plot[element], color=dimgray)
        
for element in ['fliers']:
    plt.setp(box_plot[element], markeredgecolor = dimgray, alpha = 0.1)

for patch in box_plot['boxes']:
    patch.set(facecolor='lightgray')
    #patch.set_alpha(0.5)

for whisker in box_plot['whiskers']:
    whisker.set(linestyle ="--")

if not splitted_datasets:
    ax.set_xticklabels(["PM", "PM no seq.legs"], fontsize=16)
else:
    labels = ["PM NORTH", "  PM NORTH no seq.legs", "PM SOUTH", "  PM SOUTH no seq.legs"]
    labels = ['\n'.join(wrap(x, 11)) for x in  labels]
    ax.set_xticklabels(labels, fontsize=16)

plt.ylabel(PI_y_label, fontsize=22)
plt.yticks(fontsize=16)


#plt.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.1)
plt.subplots_adjust(left=0.11, right=0.99, top=0.99, bottom=0.125)

plt.tight_layout()

plt.savefig(os.path.join(PIs_DIR, figure_filename + ".eps"), dpi=300)

plt.show()
