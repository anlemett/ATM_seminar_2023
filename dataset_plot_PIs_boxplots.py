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

PI_vertical_type = True
splitted_datasets = True
#PI_name = "timeOnLevelsPercent"
PI_name = "timeTMA"
#PI_name = "distanceChangePercent"
#PI_name = "additionalDistance"
notPMlegs = False

if PI_vertical_type:
    if PI_name == "timeOnLevelsPercent":
        PI_y_label = "Time Flown Level (\%)"
        figure_filename = "boxplot_time_on_levels_"
    else: #"timeTMA"
        PI_y_label = "Time in TMA (min)"
        figure_filename = "boxplot_time_in_TMA_"
    
    if splitted_datasets:
        DATASETS = ["TT_final_NORTH", "TT_final_SOUTH", "PM_final_NORTH", "PM_final_SOUTH", "nonPM_final_NORTH", "nonPM_final_SOUTH"]
        figure_filename = figure_filename + "6ds"
    else:
        DATASETS = ["TT_final", "PM_final", "nonPM_final"]
        figure_filename = figure_filename + "3ds"
        
    if notPMlegs:
        figure_filename = figure_filename + "_notPMlegs"
else: #horizontal
    if PI_name == "distanceChangePercent":
        PI_y_label = "Additional Distance (\%)"
        figure_filename = "boxplot_add_distance_"
    else:
        PI_y_label = "Additional Distance (NM)"
        figure_filename = "boxplot_add_distance_NM_"
        
    if splitted_datasets:
        DATASETS = ["TT_final_NORTH", "TT_final_SOUTH", "PM_final_NORTH", "PM_final_SOUTH", "nonPM_final_NORTH", "nonPM_final_SOUTH"]
        figure_filename = figure_filename + "6ds"
    else:
        DATASETS = ["TT_final", "PM_final", "nonPM_final"]
        figure_filename = figure_filename + "3ds"

PIs_dict = {}


DATA_DIR = os.path.join("data", AIRPORT_ICAO)
PIs_DIR = os.path.join(DATA_DIR, "PIs")


for dataset in DATASETS:
    
    if PI_vertical_type:
        input_filename = dataset + "_PIs_vertical_by_flights.csv"
        if notPMlegs:
            if dataset == "PM_final" or dataset == "PM_final_NORTH" or dataset == "PM_final_SOUTH":
                input_filename = dataset + "_PIs_vertical_by_flights_notPMlegs.csv"
            
    else: #horizontal:

        input_filename = dataset + "_PIs_horizontal_by_flights.csv"
        
    full_input_filename = os.path.join(PIs_DIR, input_filename)
    PIs_df = pd.read_csv(full_input_filename, sep=' ')
    
    #PIs_df = PIs_df[PIs_df['endDate']==191012]
    
    if dataset == "PM_final" or dataset == "PM_final_NORTH" or dataset == "PM_final_SOUTH":
        if notPMlegs:
            noLevels_df = PIs_df[PIs_df[PI_name]==0]
            print(len(noLevels_df))
            print(len(noLevels_df)/len(PIs_df))    #PM_final - 44%, PM_final_NORTH - 66%, PM_final_SOUTH - 34%
    
    if PI_vertical_type and not splitted_datasets:
        if dataset == "TT_final":
            dataset_name = "TT"
           
        elif dataset == "PM_final":
            dataset_name = "PM"
            
        else: # nonPM
            dataset_name = "nonPM"
           
    else: # horizontal and 6 datasets vertical
           
        if dataset == "TT_final_NORTH":
            dataset_name = "TT NORTH"
            
        elif dataset == "TT_final_SOUTH":
            dataset_name = "TT SOUTH"
            
        elif dataset == "PM_final_NORTH":
            dataset_name = "PM NORTH"
            
        elif dataset == "PM_final_SOUTH":
            dataset_name = "PM SOUTH"
        
        elif dataset == "nonPM_final_NORTH":
            dataset_name = "nonPM NORTH"
            
        elif dataset == "nonPM_final_SOUTH":
            dataset_name = "nonPM SOUTH"

    if PI_vertical_type:
         PIs_dict[dataset_name] = PIs_df[PI_name]
    else:
        if PI_name == "additionalDistance":
            PIs_dict[dataset_name] = PIs_df[PI_name].add(12)
        else:
            add_dist_series = PIs_df[PI_name].add(12)
            ref_dist_series = PIs_df['referenceDistance']
            PIs_dict[dataset_name] = add_dist_series.div(ref_dist_series).multiply(100)
    
    PI_median = PIs_dict[dataset_name].median()
    PI_mean = PIs_dict[dataset_name].mean()
    PI_std = statistics.stdev(PIs_dict[dataset_name])
    PI_min = PIs_dict[dataset_name].min()
    PI_max = PIs_dict[dataset_name].max()
        
    print(PI_median, PI_mean, PI_std, PI_min, PI_max)
    
    #print(PIs_dict[dataset_name])
   
print(len(PIs_dict))         

#fig, ax = plt.subplots(1, 1,figsize=(7,5))
fig, ax = plt.subplots(1, 1,figsize=(7,5), dpi = None)

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

if PI_vertical_type and not splitted_datasets:
    ax.set_xticklabels(["TT", "PM", "nonPM"], fontsize=16)
else:
    labels = ["  TT  NORTH", "  TT  SOUTH", "  PM  NORTH", "  PM  SOUTH", "nonPM NORTH", "nonPM SOUTH"]
    labels = ['\n'.join(wrap(x, 6)) for x in  labels]
    ax.set_xticklabels(labels, fontsize=16)
plt.ylabel(PI_y_label, fontsize=22)
plt.yticks(fontsize=16)


if PI_name == "additionalDistance":
    #plt.subplots_adjust(left=0.11, right=0.99, top=0.99, bottom=0.09)
    plt.subplots_adjust(left=0.135, right=0.99, top=0.99, bottom=0.12)
else:
    #plt.subplots_adjust(left=0.09, right=0.99, top=0.99, bottom=0.09)
    plt.subplots_adjust(left=0.11, right=0.99, top=0.99, bottom=0.12)
plt.tight_layout()

plt.savefig(os.path.join(PIs_DIR, figure_filename + ".eps"), dpi=300)

plt.show()