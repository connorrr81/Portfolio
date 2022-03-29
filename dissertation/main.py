# %% Import libraries
import os
import pprint
import texttable
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import json
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from pathlib import Path

from mydir.get_line_ids import get_line_ids
from mydir.get_line_stats import get_line_stats
from mydir.gen2tensor import gen2tensor
from mydir.summary_statistics import get_number_of_species, get_bases_mct, get_number_of_unique_taxon
from mydir.get_species import get_species_tree
from mydir.plot_processing import plot_tree, plot_heatmap
from mydir.NaiveBayes import NaiveBayes


# %% Define environment variables

ROOTPATH = Path('C:/Users/CLaug/Documents/toDukeFromBold')
DATAPATH = ROOTPATH.joinpath('animalia')

GENOMEFILE = DATAPATH.joinpath('BinReps_Nucaln.txt')

# %% Get file counts related to line length and to genetic information

line_len_counts, line_gen_counts = get_line_stats(GENOMEFILE)

# %% Get line IDs specified line length and with specified genetic information

line_ids = get_line_ids(GENOMEFILE, 901, gen_ids='-ACGT')

# %% Open processed sequence file
import json

path = os.getcwd()
parent = os.path.dirname(path)

TREEFILE = parent + "\mydir\\tree.csv"
SEQFILE = parent + "\mydir\line_ids.json"
OUTFILE = parent + "results.csv"
DIR = parent + "\mydir"

with open(SEQFILE,encoding='utf-8-sig', errors='ignore') as f: 
  line_ids = json.load(f, strict=False)

tree_df = pd.read_csv(TREEFILE, index_col="BOLD_ID")

        
# %% Produce summary of the line_ids

species = get_number_of_species(line_ids)
summary_df = pd.DataFrame(columns=["A", "T", "G", "C", "-"])
insect_df = insect_df[insect_df["Order"]=="Lepidoptera"]
for taxa in insect_df["Family"].unique():
    mean_summary = get_bases_mct(line_ids, insect_df[insect_df["Family"]==taxa])
    mean_summary = mean_summary.rename(index=taxa)
    summary_df = summary_df.append(mean_summary)
    
print(summary_df.to_latex())

#print("Number of species:", species)
#UniqueTaxon = get_number_of_unique_taxon(insect_df)

# %% Which Genus, Family, Order does this Species belong to?
DIR_IN = DIR+"\low_prec.csv"
sp_list = pd.read_csv(DIR_IN, header=None)
sp_list = sp_list.iloc[0,:]

#poorly perform species
poor_df = pd.DataFrame(columns=["Genus", "Family", "Order"])
for sp in sp_list:
    #print(sp)
    #print(insect_df[insect_df["Species"]==sp]["Genus"].values[0])
    poor_df.loc[sp] = pd.Series({'Genus':insect_df[insect_df["Species"]==sp]["Genus"].values[0], 
                                 'Family':insect_df[insect_df["Species"]==sp]["Family"].values[0], 
                                 'Order':insect_df[insect_df["Species"]==sp]["Order"].values[0]})
    

# %% Wilcoxon test
from scipy.stats import wilcoxon
DIR_IN = DIR+"\\acc_scores.csv"
acc_list = pd.read_csv(DIR_IN, header=None)
x = acc_list.iloc[0,:]  #model 1: 1 chnage per mutation
y = acc_list.iloc[1,:]  #model 2: 5 changes per mutation

print(wilcoxon(x,y))
# %% Produce the phylogentic tree of the species in line_ids

#tree_df = get_species_tree()
ids_df = pd.DataFrame(data=line_ids.keys())

# Filter tree to include the BOLD that are present in the list of sequences
reduced_tree_df = tree_df[tree_df.index.isin(ids_df[0])]
#reduced_tree_df.to_csv("tree.csv")


# %% Clean the species names ONLY FOR MODEL INPUT
plot_df = pd.DataFrame(index = [0], columns=["Order", "Family", "Genus", "Species"])
for i in range(0, 5):
    reduced_tree_df = tree_df[tree_df.index.isin(ids_df[0])]
    reduced_tree_df.reset_index(inplace=True)
    reduced_tree_df = reduced_tree_df[~reduced_tree_df["Species"].str.contains('sp\.$', na=False, regex=True)]
    vc = reduced_tree_df["Species"].value_counts()
    mutiple_sample_species = vc[vc > i].index.values.tolist()
    reduced_tree_df = reduced_tree_df[reduced_tree_df["Species"].isin(mutiple_sample_species)]
    reduced_tree_df = reduced_tree_df.set_index("BOLD_ID")
        
    insect_df = reduced_tree_df[reduced_tree_df["Class"] == "Insecta"]
    
    plot_df = plot_df.append(get_number_of_unique_taxon(insect_df), ignore_index=True)

plot_df = plot_df.reset_index()    
# %% Plot number of sample per species
from matplotlib import cm
import seaborn as sns

df = plot_df.melt(id_vars=["index"],
                  value_vars=["Species", "GenuSupervised machine learning methods have been utilised to solve the species classification problem \cite{Weitschek2013}.s", "Family", "Order"],
                  value_name = "Count",
                  var_name="Taxonomic Group")

df = df[df["Count"]>0]

sns.set(rc={"figure.figsize":(10,5)})
sns.set_style("ticks")
sns.set_context("talk")
sample_plot = sns.barplot("index", "Count", data=df, hue="Taxonomic Group")
# colourid = 0
# for taxa in ["Species", "Genus", "Family", "Order"]:
#     sample_plot = sns.barplot("index", "Count", 
#                               data=df[df["Taxonomic Group"]== taxa],
#                               label=taxa,
#                               color=sns.color_palette("Paired")[colourid])
#     colourid=colourid+1

sample_plot.set(yscale='log')
sample_plot.set_xlabel("Sequences per species")
sample_plot.legend(ncol=1, loc="upper right", frameon=True)

 
plt.savefig("SamplePlot.png", dpi=200)
   
# %% Produce a tree for insects, bees and cats
bees_df = reduced_tree_df[reduced_tree_df["Family"] == "Megachilidae"]
cats_df = reduced_tree_df[reduced_tree_df["Family"] == "Felidae"]
insect_df = reduced_tree_df[reduced_tree_df["Class"] == "Insecta"]

#%% Plot tree for bees
lim = 128
#plot_tree(bees_df[:lim], lim, 'genetic_tree_bees.png')
#plot_tree(cats_df[:lim], lim, 'genetic_tree_cats.png')
plot_tree(insect_df[:lim], lim, 'genetic_tree_insects.png')

# %% Similarity investigation
    
#plot_heatmap(bees_df, line_ids, parent + 'heatmap_bees.png')
#plot_heatmap(cats_df, line_ids, parent + 'heatmap_cats.png')
plot_heatmap(insect_df, line_ids, parent + 'heatmap_insects.png')


#%% Naive Bayes Classification

NaiveBayes(insect_df, line_ids, "Family", False)


