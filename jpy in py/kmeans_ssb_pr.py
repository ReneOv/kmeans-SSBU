#!/usr/bin/env python
# coding: utf-8

# In[1]:


import matplotlib.pyplot as plt
import numpy as np
import csv
from sklearn.metrics import pairwise_distances_argmin
from collections import Counter, defaultdict


# In[2]:


# Function to read .csv database and convert to variables.

def read_csv():
    x = []
    y = []
    players = []
    x_label = "Average Placement"
    y_label = "Tournaments Played"
    with open('playerDB.csv', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        header = 0
        for row in reader:
            if header == 0:
                header +=1
            else:
                x.append(float(row[1]) / float(row[2]))
                y.append(float(row[2]))
                players.append(row[0])
    return x, y, x_label, y_label, players


# In[3]:


# Assign values to variables

x, y, x_label, y_label, players = read_csv()


# In[4]:


# Convert our (x,y) to paired array structure

X = np.vstack((x, y)).T


# In[5]:


# Print header of our array

X


# In[6]:


# Draw un-clustered graph

plt.title('SSBU Player Consistency', loc='center')
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.scatter(x, y, color='#76c2b4')
plt.show()


# In[7]:


# Function to find clusters using SciKit-learn K-Means Clustering

def find_clusters(X, n_clusters, rseed=2):
    rng = np.random.RandomState(rseed)
    # Get n amount of random centroids
    i = rng.permutation(X.shape[0])[:n_clusters]
    # Save initial centroids
    centers = X[i]

    print("\nLook for converged centroids:")
    # Loops until centroids are found
    while True:
        # Assign cluster labels based on closest center
        labels = pairwise_distances_argmin(X, centers)

        # Find new centers from means of points from distance
        new_centers = np.array([X[labels == i].mean(0) for i in
        range(n_clusters)])

        # Check for convergence. If old centers == new centers
        # Change to for loop if we want only a set amount of iterations
        if np.all(centers == new_centers):
            break
        centers = new_centers

        # Print iterated centroids
        print(centers)
        print()

    return centers, labels


# In[8]:


# Set number of clusters

clust_num = 8


# In[9]:


# Get clustered data and "print" to graph

centers, labels = find_clusters(X, clust_num)    # Can give random seed, or be defaulted
plt.scatter(X[:, 0], X[:, 1], c=labels, s=50, cmap='plasma')
plt.title('K-Means Clustering of Tiers of Consistent Players')
plt.xlabel(x_label)
plt.ylabel(y_label)
plt.show()


# In[10]:


# Print general information on tiers and their players

print("\nNumber of players in each tier:")
print(Counter(labels))

# Get cluster indices
clusters_indices = defaultdict(list)
for index, c in enumerate(labels):
    clusters_indices[c].append(index)

# Print players in each tier, their stats, and the tier average
x = 0 # Select tier, from 0 to clust_num - 1
print("\nTier " + str(x + 1))
print("----------")
for i in clusters_indices[x]:
    print(players[i])
print("----------")
print("Mean average placement:", centers[x][0])
print("Mean tournaments played:", centers[x][1])


# In[ ]:




