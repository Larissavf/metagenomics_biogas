"""
Voor het verwerken van de kraken_report.log files.
Er worden diverse plots gemaakt. 
Met vergelijkingen van de 4 verschillende niveaus in het onderzoek: Boven, midden, Onder en Pacques.
Die op verschillende manieren de top 10s van organismen die voorkomen in de samples

Als je de locatie of aantal samples wil veranderen moet je in de main aanpassen waar de read_input() wordt aangeroepen.

author: Larissa
date: 10-04-2024
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import venn
import os
import sys

def read_input(path_file):
    """
    inlezen van het bestand.
    In het log bestand hebben ze een soort boom gemaakt hierdoor zijn er veel spaties aanwezig die dus verwijderd worden.
    path_file: volledige pad naar het bestand
    """
    # maken van temp bestand om all verwijderde spaties en de kolom namen in aan te geven
    with open("../newtest.log", 'w') as writefile:
        column_names = "perc_frag\tcov_frag\tass_frag\trank_code\ttaxonomic_ID\ttaxonomic_name\n"
        writefile.write(column_names)
        with open(path_file, "r") as file:
            for line in file:
                line = line.replace(" ","")
                writefile.write(line)

    # maken van df
    df_boven = pd.read_csv("../newtest.log", sep=("\t"), )

    # verwijder temp bestand
    os.remove("../newtest.log")
    return df_boven

def del_human(df):
    """
    Verwijderen van mens in de in mens
    df: dataframe die je aangepast wil
    """
    # zoek de index die verwijderd moet worden
    euka_index = df[df["taxonomic_name"] == "Eukaryota"].index.tolist()
    homo_index = df[df["taxonomic_name"] == "Homosapiens"].index.tolist()

    # verwijder
    list_to_remove = list(range(euka_index[0], homo_index[0] +1))
    df = df.drop(list_to_remove)
    # thanks to aimee <3
    return df

def filtah(kraken, filtar):
    """
    filteren op de rank code, dus voorbeeld een G voor genus.
    kraken: dataframe die je gefilterd wil hebben.
    filtar: de rank code die je graag wil hebben
    """
    # welke rank codes er zijn in deze df
    values = set(kraken['rank_code'])

    #verwijderen van rows die niet voldoen aan rank code en filteren op toename
    phylo = [value if filtar in str(value) else "" for value in values]
    order_genus = kraken.loc[kraken['rank_code'].isin(phylo)].sort_values(by='perc_frag',  ascending=False)
    return  order_genus

def make_num(dataframe, changes):
    """
    changes de taxonomic to a number
    dataframw: df you want to change
    changes: is the dict with already some changes in
    """
    #dit is een beetje dom want de rank id maar ja ik heb dit gemaakt dus we gaan der mee verder:)

    if not changes:
        replace_with = 0
        #pak naam en vervang met cijfer zet beide in dict
        for replace in set(dataframe["taxonomic_name"]):
            replace_with +=1
            changes[replace_with] = replace
            dataframe.replace(replace, replace_with, inplace=True)
    #als der al een dataframe is translated
    else:
        #pak alleen namen die niet voorkomen in de dict
        filtered_list = [string for string in list(set(dataframe["taxonomic_name"])) if string not in list(changes.values())]
        #pak naam en vervang met cijfer
        for replace_with in changes:
            replace = changes[replace_with]
            dataframe.replace(replace, replace_with, inplace=True)
        if filtered_list:
        #pak naam en vervang met cijfer zet beide in dict
             for replace in filtered_list:
                replace_with +=1
                changes[replace_with] = replace
                dataframe.replace(replace, replace_with, inplace=True)
    #lijstje met meukjes
    list_string = dataframe['taxonomic_name'].tolist()
    return [str(x) for x in list_string], changes

def make_venn(df_boven_f, df_midden_f, df_onder_f, df_pacques_f):
    """
    Make a 4 pieces venn diagram using 
    'https://github.com/tctianchi/pyvenn'
    input: de 4 dfs die je wilt zien
    """

    #maak van de namen een cijfer
    changes = {}
    venn_b, changes_b = make_num(df_boven_f, changes)
    venn_m, changes_m = make_num(df_midden_f, changes_b)
    venn_o, changes_o = make_num(df_onder_f, changes_m)
    venn_p, changes_p = make_num(df_pacques_f,changes_o) 

    #plotten
    labels = venn.get_labels([venn_o, venn_m, venn_b, venn_p], fill=['percent'])
  
    fig, ax = venn.venn4(labels, names=['Onder', 'Midden', 'Boven', 'Pacques'])
    fig.savefig("../pic/venn.png")
    return changes_p, venn_b, venn_m, venn_o, venn_p

def intersect_org(intersect, df, changes_o):
    """
    makes a df of the top 10 organismen in the intersect between sets
    df: a dataframe from what you want to know the percentages of the org
    """
    #maak van cijfers namen
    l = []
    for num in list(intersect):
        org = changes_o[int(num)]
        l.append(org)
    intersect_df = df.loc[df['taxonomic_name'].isin(l)]
    return intersect_df


def make_intersect_bar_plot(intersect, df_boven, df_onder, df_midden, changes):
    """
    Maken van een bar plot met top 10 die in all dfs voorkomt.
    intersect: list van intersect organisme die overal voorkomen
    alle df's die je wilt
    changes: dict met de vertaling van de num naar org

    """

    #df met namen van intersect 3 levels
    df_intersect_b = intersect_org(intersect, df_boven, changes).sort_values(by='perc_frag',  ascending=False)[:10]
    df_intersect_o = intersect_org(intersect, df_onder, changes).sort_values(by='perc_frag',  ascending=False)[:10]
    df_intersect_m = intersect_org(intersect, df_midden, changes).sort_values(by='perc_frag',  ascending=False)[:10]

    # data
    species = list(df_intersect_o["taxonomic_name"])
    penguin_means = {
        "Onder": df_intersect_o["perc_frag"],
        "Midden": df_intersect_m["perc_frag"],
        "Boven": df_intersect_b["perc_frag"]
    }


    x = np.arange(len(species))  # the label locations
    width = 0.25  # the width of the bars
    multiplier = 0

    fig, ax = plt.subplots(layout='constrained')

    for attribute, measurement in penguin_means.items():
        offset = width * multiplier
        rects = ax.bar(x + offset, measurement, width, label=attribute)
        multiplier += 1

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Percentage coverage')
    ax.set_xlabel('organismen op niveau')
    ax.set_title("Meest voorkomende organismen in alle samples")
    ax.set_xticks(x + width, species)
    ax.legend(loc='upper right', ncols=3)
    plt.xticks(rotation=90)
    plt.yticks(range(1, 40))
    plt.rcParams["figure.figsize"] = (17,10)
    plt.savefig("../pic/intersect_of_3lvl.png")


    #thanks to matplotlib voorbeeld<3

def prep_data_TBR_plot(df_boven_f, df_boven, changes_o):
    """
    maak lijstjes van de top 10 organismen elk niveau
    en de bijbehorende percentages
    input: dataframe gefilterd op niveau en niet gefilterd
    """
    #prep data
    nums_b = list(df_boven_f["taxonomic_name"][:10])
    df_boven_10 = intersect_org(nums_b, df_boven, changes_o)
    l_boven_10 = list(df_boven_10["taxonomic_name"])
    perc_boven = list(df_boven_10["perc_frag"])
    return l_boven_10, perc_boven



def make_TBR_bar_plot(df_boven_f, df_boven, df_midden_f, df_midden, df_onder_f, df_onder, changes):
    """
    maak een bar plot in de volgorde van de TBR, dus van elk niveau de top 10
    input: van elk niveau de filterd en non filter versie
    """
    #prep data
    l_boven_10, perc_boven = prep_data_TBR_plot(df_boven_f, df_boven, changes)
    l_midden_10, perc_midden = prep_data_TBR_plot(df_midden_f, df_midden, changes)
    l_onder_10, perc_onder = prep_data_TBR_plot(df_onder_f, df_onder, changes)

    fig, ax = plt.subplots()


    y1 = range(1,11)
    y2= range(12,22)
    y3 = range(23,33)

    bar3 = ax.barh(y3, perc_boven, 0.9, label= "Boven")
    bar2 = ax.barh(y2, perc_midden, 0.9, label="Midden")
    bar1 = ax.barh(y1, perc_onder, 0.9, label="Onder")


    ax.set_xlabel('Percentage van voorkomen in sample')
    ax.set_ylabel('Microben')
    ax.set_title('top 10 microben per level')
    ax.set_yticks([1,2,3,4,5,6,7,8,9,10,12,13,14,15,16,17,18,19,20,21,23,24,25,26,28,29,30,31,32,27])
    ylabels = l_onder_10 + l_midden_10 + l_boven_10
    ax.set_yticklabels(ylabels)
    ax.legend()

    name_groups = ["Boven", "Midden", "Onder"]
    loc = 32.5
    for name in name_groups:
        ax.text(-12.6, loc,name, fontsize=12)
        loc -= 11
    plt.xticks(range(1, 40))
    plt.rcParams["figure.figsize"] = (15,13)
    plt.savefig("../pic/TBR_top10.png")



def make_intersec_df(set1, set2, df1, df2, changes_o):
    """
    intersect tussen 2 data
    set 1
    set 2
    df 1
    df 2
    """
    set1xset2 = set1.intersection(set2)
    df_set1 = intersect_org(set1xset2, df1, changes_o).sort_values(by='perc_frag',  ascending=False)[:10]
    df_set2 = intersect_org(set1xset2, df2, changes_o).sort_values(by='perc_frag',  ascending=False)[:10]
    return df_set1, df_set2

def make_pac_vs(df_bovxpac, df_pacxbov, name1, name2):
    """ 
    maak plotje dat je 2 df van kraken kan vergelijken met elkaar als ze bestaan uit de zelfde organismen
    df1: welk je eerst wel
    df2: welke je daarna wil
    name1: :)
    name2: :)
    """
    fig, ax = plt.subplots()

    y = np.array(range(0,10))

    #barren
    bar1 = ax.bar(y + 1/4, df_bovxpac["perc_frag"] , 0.4, label=name1)
    bar1 = ax.bar(y - 1/4, df_pacxbov["perc_frag"] , 0.4, label=name2)

    ax.set_ylabel('Percentage van voorkomen in sample')
    ax.set_xlabel('Microben')
    ax.set_title('top 10 microben per level')
    ax.set_xticks(y)
    ax.set_xticklabels(df_bovxpac["taxonomic_name"])

    #show plot
    ax.legend()
    plt.xticks(rotation=90)
    plt.rcParams["figure.figsize"] = (9,11)
    plt.savefig("../pic/" + name1 + "_vs_" + name2 + ".png")

def main():
    """
    Omdat het moet
    """
    #get dfs
    df_all_boven = read_input(sys.argv[1])
    df_all_midden = read_input(sys.argv[2])
    df_all_onder = read_input(sys.argv[3])
    df_all_pacques = read_input(sys.argv[4])
    
    #weg menselijke
    df_midden = del_human(df_all_midden)
    df_pacques = del_human(df_all_pacques)
    df_boven = del_human(df_all_boven)
    df_onder = del_human(df_all_onder)

    #filter op rank code
    df_midden_f = filtah(df_midden, "G")
    df_boven_f = filtah(df_boven, "G")
    df_onder_f = filtah(df_onder, "G")
    df_pacques_f = filtah(df_pacques, "G")

    #prachtige venn maken
    changes, venn_b, venn_m, venn_o, venn_p = make_venn( df_boven_f, df_midden_f, df_onder_f, df_pacques_f)   
    
    #sets 
    s_pac = set(venn_p)
    s_bov = set(venn_b)
    s_mid = set(venn_m)
    s_ond = set(venn_o)

    #intersect tussen 3 levels
    intersect = s_ond.intersection(s_bov, s_mid)

    #prachtige bar plot
    make_intersect_bar_plot(intersect, df_boven, df_midden, df_onder, changes)

    #prachtigere bar plot
    make_TBR_bar_plot(df_boven_f, df_boven, df_midden_f, df_midden, df_onder_f, df_onder, changes)

    #prachtige intersect tussen begin en eind
    # data prep
    df_bovxpac, df_pacxbov = make_intersec_df(s_bov, s_pac, df_boven, df_pacques, changes)
    df_midxpac, df_pacxmid = make_intersec_df(s_mid, s_pac, df_midden, df_pacques, changes)
    df_ondxpac, df_pacxond = make_intersec_df(s_ond, s_pac, df_onder, df_pacques, changes)
    make_pac_vs(df_bovxpac, df_pacxbov, "Boven", " Pacques")
    make_pac_vs(df_midxpac, df_pacxmid, "Midden", "Pacques")
    make_pac_vs(df_ondxpac, df_pacxond, "Onder", "Pacques")



if __name__ == "__main__":
    main()