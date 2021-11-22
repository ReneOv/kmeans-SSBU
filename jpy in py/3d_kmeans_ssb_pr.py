#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import csv
from collections import Counter, defaultdict
from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import KMeans


# In[2]:


# Function to read .csv database and convert to variables.

def read_csv():
    x = []
    y = []
    z = []
    players = []
    x_label = "Average Placement"
    y_label = "Tournaments Played"
    z_label = "Tournaments Topped"
    with open('3dplayerDBTops.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = 0
        for row in reader:
            if header == 0:
                header +=1
            else:
                x.append(float(row[1]) / float(row[2]))
                y.append(float(row[2]))
                z.append(float(row[3]))
                players.append(row[0])
    return x, y, z, x_label, y_label, z_label, players


# In[3]:


# Assign values to variables

x, y, z, x_label, y_label, z_label, players = read_csv()


# In[4]:


# Convert our (x,y,z) to a triplet array structure

X = np.vstack((x, y, z)).T


# In[5]:


# Print header of our array

X


# In[6]:


# Draw unclustered graph

# Configure plot
fig = plt.figure(1, figsize=(10, 10))
ax = Axes3D(fig, rect=[1, 1, 1, 1], elev=25, azim=135, auto_add_to_figure=False)
fig.add_axes(ax)

# Add information to plot
ax.scatter(X[:, 0], X[:, 1], X[:, 2], edgecolor="k", s=110)
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_zlabel(z_label)
ax.set_title("Player Average Placement vs. Tournaments Played vs. Tournaments Topped")
ax.dist = 10


# In[7]:


# Define amount of clusters (tiers)
est = KMeans(n_clusters=3)

# Configure plot
fig = plt.figure(1, figsize=(10, 10))
ax = Axes3D(fig, rect=[1, 1, 1, 1], elev=25, azim=135, auto_add_to_figure=False)
fig.add_axes(ax)

# Run K-Means Clustering
est.fit(X)
labels = est.labels_

# Add information to plot
ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=labels.astype(float), edgecolor="k", s=110)
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
ax.set_zlabel(z_label)
ax.set_title("SSBU Consistency PR Clusters")
ax.dist = 10


# In[8]:


# Prepare each tier

tiers = {}
n = 0
for item in labels:
    if item in tiers:
        tiers[item].append(players[n])
    else:
        tiers[item] = [players[n]]
    n +=1


# In[14]:


# Print out specific tier

tier = 0
n = 0

print("Tier ", tier)
for i in tiers[tier]:
    print(i, X[n])
    n+=1


# In[ ]:




