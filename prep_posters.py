import html
import os
import glob
import pandas as pd
import pdftitle
from html.parser import HTMLParser
import numpy as np
import math
import re

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        if tag=="a": 
            self.link = attrs[0][1]

# hardcoded titles where pdftitle didn't work
problems = { 307990 : "Towards better understanding of developmental disorders from integration of spatial single-cell transcriptomics and epigenomics",
    348147 : "Predicting Dog Traits with SNP Data",
    336596 : "CRISPR-TTN: Informing optimization of guide RNA design by metric learning CRISPR-cas9 off-target propensity using a two tower network", 
    22256 : 'Predicting patient-level phenotypes from single-cell data',
    337100 : "Identifying Drought-Resistant Genes from RNA-seq Data in Oryza sativa", 
    337184 : "Predicting soybean crop resiliency from glycine max sequence using clustering algorithms"}

# other fixes
toremove = { "Final Report: " : "", 
    "ML4FG Report: " : "", 
    "aTransformer" : "a Transformer", 
    "\ufb01" : "fi", 
    "\ufb03" : "ffi", 
    "usingGradient" : "using Gradient", 
    "NeuralNetworks" : "Neural Networks",
    "Ex- pression" : "Expression",
    "\u2013" : "-",
    ",and" : ", and" }

# name fixes
author_fix = { "NAIK" : "Naik"}


pdfs = glob.glob("final project reports/*.pdf")
titles = {}
for f in pdfs: 
    f_clean = re.sub("LATE_", "", f)
    bn = os.path.basename(f_clean)
    ss = bn.split("_")
    user_id = int(ss[1])
    title = problems[user_id] if (user_id in problems) else pdftitle.get_title_from_file(f)
    for k,v in toremove.items(): 
        title = re.sub(k, v, title)
    titles[user_id] = title

htmls = glob.glob("video_links/*.html")

parser = MyHTMLParser()

# Project groups can be downloaded from Courseworks (People -> Project Groups -> Import(!) -> Download Course Roster)
groups = pd.read_csv("Project groups.csv")
poster_data = {}
for i,f in enumerate(htmls):
    f_clean = re.sub("LATE_", "", f)
    bn = os.path.basename(f_clean)
    _,user_id,_ = bn.split("_")
    user_id = int(user_id)
    groupname = groups.loc[groups.canvas_user_id == user_id,"group_name"].item()
    if not isinstance(groupname, str): 
        authors = [groups.loc[groups.canvas_user_id == user_id,"name"].item()]
    else: 
        authors = list(groups.loc[groups.group_name == groupname,"name"])
    lines = "".join(open(f,"r").readlines())
    parser.feed(lines)
    link = parser.link
    authors = " & ".join(authors)
    for k,v in author_fix.items(): 
        authors = re.sub(k, v, authors)
    poster_data[str(i)] = {
        "index": i,
        "town": 0,
        "townName": "ML4FG poster town",
        "posterImgUrl": "",
        "posterVideo" : link,
        "page": "NA",
        "name": titles[user_id],
        "authors": authors,
        "zoom": "zoom.us"
    } 


import json
with open('data/postersData.json', 'w') as outfile:
    json.dump(poster_data, outfile, indent=4)

# make a playlist of the youtube videos (not sure how to do this for vimeo...)
towatch=[]
for k,v in poster_data.items(): 
    link = v["posterVideo"]
    video = None
    if "youtu.be" in link: 
        video = re.sub("https://youtu.be/", "", link)
    elif "https://www.youtube.com" in link: 
        video = link.split("=")[1].split("&")[0]
    #print(video if video else link)
    if video: 
        towatch.append(video)

print("https://www.youtube.com/watch_videos?video_ids=" + ','.join(towatch))