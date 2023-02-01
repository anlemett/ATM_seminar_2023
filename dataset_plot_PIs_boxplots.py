import pandas as pd
import os
import matplotlib.pyplot as plt
#conda install -c conda-forge mscorefonts
#plt.rcParams["font.family"] = "Times New Roman"
plt.rcParams["text.usetex"] = True
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = "Times New Roman"
plt.rcParams["font.size"] = "8"
#import matplotlib.colors as mcolors
import statistics

AIRPORT_ICAO = "ENGM"

PI_vertical_type = True
splitted_datasets = True
PI_name = "timeOnLevelsPercent"
#PI_name = "timeTMA"
notPMlegs = False

if PI_vertical_type:
    if PI_name == "timeOnLevelsPercent":
        PI_y_label = "Time Flown Level (\%)"
        figure_filename = "time_on_levels_boxplot_"
    else: #"timeTMA"
        PI_y_label = "Time in TMA (min)"
        figure_filename = "time_in_TMA_boxplot_"
    
    if splitted_datasets:
        DATASETS = ["TT_final_NORTH", "TT_final_SOUTH", "PM_final_NORTH", "PM_final_SOUTH", "nonPM_final_NORTH", "nonPM_final_SOUTH"]
        figure_filename = figure_filename + "6ds"
    else:
        DATASETS = ["TT_final", "PM_final", "nonPM_final"]
        figure_filename = figure_filename + "3ds"
        
    if notPMlegs:
        figure_filename = figure_filename + "_notPMlegs"
else: #horizontal
    PI_name = "distanceChangePercentMean"
    PI_y_label = "Additional Distance [%]"
    #DATASETS = ["TT_final_NORTH", "TT_final_SOUTH", "PM_final_NORTH", "PM_final_SOUTH", "nonPM_final_NORTH", "nonPM_final_SOUTH"]
    DATASETS = ["TT_final_NORTH", "TT_final_SOUTH", "PM_final_SOUTH"]
    figure_filename = "add_distance_boxplot_"
    if splitted_datasets:
        figure_filename = figure_filename + "6ds"
    else:
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

    
    PIs_dict[dataset_name] = PIs_df[PI_name]
    
    PI_median = PIs_dict[dataset_name].median()
    PI_mean = PIs_dict[dataset_name].mean()
    PI_std = statistics.stdev(PIs_dict[dataset_name])
    PI_min = PIs_dict[dataset_name].min()
    PI_max = PIs_dict[dataset_name].max()
        
    print(PI_median, PI_mean, PI_std, PI_min, PI_max)
   
print(len(PIs_dict))         

fig, ax = plt.subplots(1, 1,figsize=(7,5))
#fig, ax = plt.subplots(1, 1,figsize=(4,3))

colors = [(178/255, 0.0, 77/255), (1.0, 213/255, 0.0), (0.0, 154/255, 178/255), (178/255, 213/255, 77/255), (0.0, 213/255, 178/255), (0.0, 77/255, 178/255)]

medianprops = dict(linestyle='-', linewidth=1, color='red')
flierprops = dict(marker='o', markerfacecolor='green', markersize=12,
                  markeredgecolor='none')

box_plot = ax.boxplot(PIs_dict.values(), sym='+', medianprops=medianprops, patch_artist=True)

for patch, color in zip(box_plot['boxes'], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.5)
    
for flier, color in zip(box_plot['fliers'], colors):
    flier.set(markeredgecolor = color, alpha = 0.5)
    
for whisker in box_plot['whiskers']:
    whisker.set(linestyle ="--")

if PI_vertical_type and not splitted_datasets:
    ax.set_xticklabels(["TT", "PM", "nonPM"], fontsize=8)
else:
    ax.set_xticklabels(["TT NORTH", "TT  SOUTH", "PM NORTH", "PM SOUTH", "nonPM NORTH", "nonPM SOUTH"], fontsize=8)  
plt.ylabel(PI_y_label, fontsize=8)
plt.yticks(fontsize=8)
#plt.subplots_adjust(left=0.16, right=0.99, top=0.99, bottom=0.14)
#plt.subplots_adjust(left=0.18, right=0.99, top=0.99, bottom=0.14)

# plot legend
import matplotlib.patches as mpatches
handles = []
if PI_vertical_type and not splitted_datasets:
    color_patch = mpatches.Patch(color=colors[0], alpha = 0.5, label='TT')
    handles += [color_patch]
    color_patch = mpatches.Patch(color=colors[1], alpha = 0.5, label='PM')
    handles += [color_patch]
    color_patch = mpatches.Patch(color=colors[2], alpha = 0.5, label='non PM')
    handles += [color_patch]
else:
    color_patch = mpatches.Patch(color=colors[0], alpha = 0.5, label='TT NORTH')
    handles += [color_patch]
    color_patch = mpatches.Patch(color=colors[1], alpha = 0.5, label='TT SOUTH')
    handles += [color_patch]
    color_patch = mpatches.Patch(color=colors[2], alpha = 0.5, label='PM NORTH')
    handles += [color_patch]
    color_patch = mpatches.Patch(color=colors[3], alpha = 0.5, label='PM SOUTH')
    handles += [color_patch]
    color_patch = mpatches.Patch(color=colors[4], alpha = 0.5, label='non PM NORTH')
    handles += [color_patch]
    color_patch = mpatches.Patch(color=colors[5], alpha = 0.5, label='non PM SOUTH')
    handles += [color_patch]

plt.legend(handles=handles, fontsize=8, edgecolor="black", loc="best", bbox_to_anchor=(0.0, 0.5, 0.5, 0.5))

plt.tight_layout()

plt.savefig(os.path.join(PIs_DIR, figure_filename + ".png"), dpi=300)

plt.show()
