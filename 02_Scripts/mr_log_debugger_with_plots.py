import numpy as np, pandas as pd, os, matplotlib.pyplot as plt, re, argparse, seaborn as sns
from matplotlib.patches import Ellipse
# A function to parse Mister Log Data
# I.E. the outptus from MakeRotLib Program
# This function will read the .mrllog file and
# print out scatter plots of the custer with each
# cluster colored differently.
# Script usage: python3 mr_log_debugger_with_plots.py -mrllog_file_with_path /path/to/mrllog/file.mrllog

def scooby_doo():
    scoob = """
               / \__
             (    @\___
             /         O
           /   (_____/
         /_____/
    """
    return scoob

def parse_line_in_mrllog_file(lines):
    mchi_cln_array = np.zeros((len(lines), 20)) # 20 is arbitary here, it will be changed later in the code
    for i, line in enumerate(lines):
        values_between_mchi_stdd = re.findall(r'MCHI: (.*?) STDD:', line)
        values_between_cln_ichi = re.findall(r'CLN: (.*?) ICHI:', line)
        values_between_stdd_cdst = re.findall(r'STDD: (.*?) CDST:', line)
        assert values_between_mchi_stdd, f"Could not find any values between MCHI: and STDD: in {line}"+scooby_doo()
        if values_between_mchi_stdd: 
            cln_value = None
            if values_between_cln_ichi:
                cln_value = values_between_cln_ichi[0].split()[0]
            assert isinstance(cln_value, str), "Clustering number is not found."+scooby_doo()
            mchi_values = np.array([float(val) for val in values_between_mchi_stdd[0].split()])
            mchi_stdd_values = np.array([float(val) for val in values_between_stdd_cdst[0].split()])
            if i == 0:
                mchi_cln_array = np.zeros((len(lines), (len(mchi_values) * 2) + 1))
                
            for j, val in enumerate(mchi_values):
                mchi_cln_array[i, j] = float(val)
                mchi_cln_array[i, j+len(mchi_values)] = float(mchi_stdd_values[j])
            mchi_cln_array[i, -1] = int(cln_value)
    
    return mchi_cln_array

def parse_mrlog_avg_clust_cent_samples(lines):
    avg_clust_samples_array = np.zeros((len(lines), 2))
    for i, line in enumerate(lines):
        spline = line.split()
        avg_clust_samples_array[i,0] = float(spline[1])
        avg_clust_samples_array[i,1] = float(spline[3])
    return avg_clust_samples_array

# TODO SCATTER and HISTOGRAM PLOTS
# An elipse that was standard deviation by the standard deviation
def parse_mrllog_data(mrllog_file_with_path):
    rotamers = []
    centroids = []
    final_rotamers = []
    avg_clust_cent_dist = []
    end_of_file =[]
    current_array = None  # Variable to keep track of the current array to append lines
    #stop_at = "AVERAGE CLUSTER CENTROID DISTANCE"
    assert isinstance(mrllog_file_with_path, str), "Input must be a string"
    assert os.path.isfile(mrllog_file_with_path), f"{mrllog_file_with_path} file does not exist.\n\n"+scooby_doo()
    assert mrllog_file_with_path.endswith(".mrllog"), f"{mrllog_file_with_path} file does not end with the .mrllog file extension.\n\n"+scooby_doo()
    assert os.path.getsize(mrllog_file_with_path) > 0, f"{mrllog_file_with_path} file is empty.\n\n"+scooby_doo()

    with open(mrllog_file_with_path, "r") as out_file:
        for line in out_file:
            line = line.strip()
            if line == "ROTAMERS":
                current_array = rotamers
            elif line == "CENTROIDS":
                current_array = centroids
            elif line == "FINAL ROTAMERS":
                current_array = final_rotamers
            elif line == "AVERAGE CLUSTER CENTROID DISTANCE":
                current_array = avg_clust_cent_dist
            elif line == "AVG_CLUST_CENT_DST:":
                current_array = end_of_file
            else:
                if current_array is not None:
                    current_array.append(line.strip())

    rotamer_chis  = parse_line_in_mrllog_file(rotamers)
    del rotamers
    centroid_chis = parse_line_in_mrllog_file(centroids)
    del centroids
    final_rotamer_chis = parse_line_in_mrllog_file(final_rotamers)
    del final_rotamers
    avg_clust_dist = parse_mrlog_avg_clust_cent_samples(avg_clust_cent_dist)
    del avg_clust_cent_dist
    
    return [rotamer_chis, centroid_chis, final_rotamer_chis, avg_clust_dist]
    
def make_plots(mrllog_data,mrllog_file_with_path):
    mrllog_file_with_path = mrllog_file_with_path.replace(".mrllog", "")
    rotamers = mrllog_data[0]
    finals = mrllog_data[2]
    column_size = rotamers.shape[1]
    n_chis = (column_size -1)//2
    print(f"Found a total of {n_chis} NCHIS in the .mrllog file.")
    pairs = np.array([[i,i+1] for i in range(n_chis-1)])
    stdpairs = pairs + n_chis
    cluster_col = rotamers[:,-1]
    clust_data= mrllog_data[3]
    for p, pair in enumerate(pairs):
        plt.figure()
        current_pair = pair[0]
        next_pair = pair[1]+1
        current_std_pair = stdpairs[p][0]
        next_std_pair = stdpairs[p][1]+1
        print(f"Plotting: Chi {pair[0]+1} vs Chi {pair[1]+1}")
        ellipse_list = []
        for c, coords in enumerate(finals[:, current_pair:next_pair]):
            stds_coords = finals[:, current_std_pair:next_std_pair][c]
            ellipse = Ellipse(xy=coords, width=stds_coords[0], height=stds_coords[1], angle=0)
            ellipse_list.append(ellipse)
        print("We found a total of "+len(ellipse_list)+" ellipses. Now plotting...")
        joint_ax= sns.jointplot(x=rotamers[:, pair[0]], y=rotamers[:, pair[1]], hue=cluster_col, alpha=0.2,s=40,legend=False)
        scatter_ax = joint_ax.ax_joint
        scatter_ax.scatter(finals[:, pair[0]], finals[:, pair[1]], c='black', alpha=0.6, marker='*', s=10)
        for e in ellipse_list:
            scatter_ax.add_artist(e)
            e.set_clip_box(scatter_ax.bbox)
            e.set_alpha(0.5)
            e.set_facecolor('none')
            e.set_edgecolor('black')
        plt.xlabel(f"Chi {pair[0]+1}")
        plt.ylabel(f"Chi {pair[1]+1}")
        plt.tight_layout()
        plt.savefig(f"Chi_pair_{pair[0]+1}_vs_{pair[1]+1}_of_{mrllog_file_with_path}.png", dpi=300)
        plt.close()
    avg_clust_dist = mrllog_data[3]
    plt.figure()
    sns.barplot(x=avg_clust_dist[:,0].astype(int), y=avg_clust_dist[:,1])
    plt.ylabel("Samples")
    plt.xlabel("Cluster #")
    plt.savefig(f"Cluster_samples_of_{mrllog_file_with_path}.png", dpi=300)
    plt.close()
parser = argparse.ArgumentParser(description='Debug the MakeRotLib program with descriptive plots.') 
# Add arguments
parser.add_argument('-l', '--log_file', type=str, help='Input file path to the .mrllog file.')
# Parse the arguments
args = parser.parse_args()
# Global variables
mrllog_file_with_path = args.log_file
mrll_data = parse_mrllog_data(mrllog_file_with_path)
make_plots(mrll_data,mrllog_file_with_path)
