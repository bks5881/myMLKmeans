# -*- coding: utf-8 -*-
"""
Created on Tue Oct 25 19:13:05 2016

@author: solan
"""
#Import the dependencies
import csv
import math
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
#The dtastructure which representsa point in 3d plane.Having points X , Y and Z
class Point:
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def get_z(self):
        return self.z
    def set_x(self,x):
        self.x=x
    def set_y(self,y):
        self.y=y  
    def set_z(self,z):
        self.z=z        
#This is the structure for each cluster.Each of them has a the list of points in it, the SSE 
#calculated and centroid value.
class Cluster:
    def get_points(self):
        return self.points
    def set_points(self,points):
        self.points= points
        #self.set_sse_val()
    def set_centroid(self,centroid):
        self.centroid = centroid
    def get_centroid(self):
        return self.centroid
    def get_sse(self):
        return self.sse
    def set_sse(self,sse):
        self.sse = sse
    #this method calculates the SSE based on the current points in the cluster
    def get_sse_val(self):
        sse=0
        points=self.get_points()
        centroid = self.get_centroid()
        for i in range(len(points)):
            sse= sse+math.pow(centroid.get_x()-points[i].get_x(),2)+math.pow(centroid.get_y()-points[i].get_y(),2)+math.pow(centroid.get_z()-points[i].get_z(),2)
        self.set_sse(sse)
        return self.sse
#Reads the data from the file, converts each value into points andd return a list of points
def get_data(name):
    points=[]
    with open(name) as file:
        readFile = csv.reader(file,delimiter=',')
        for row in readFile:
            localPoint = Point()
            localPoint.set_x(float(row[0]))
            localPoint.set_y(float(row[1]))
            localPoint.set_z(float(row[2]))
            points.append(localPoint)

    return points
#calculate the distance between two points.
def getDistance(centroid,point):
    distance = math.sqrt(math.pow(centroid.get_x()-point.get_x(),2)+math.pow(centroid.get_y()-point.get_y(),2)+math.pow(centroid.get_z()-point.get_z(),2))
    return distance
#this is the method assign the new seed points too a cluster
def assignToClusters(points,clusters):
   #alculate the distance between each point and centroid of each cluster, and assign 
    #each point to a cluster closest to the clusters centroid
    for i in range(len(points)):
       
        minDistance =100000
        clusterIndex=-1
        for j in range(len(clusters)):
            #check the distance between two points
            distance= getDistance(clusters[j].get_centroid(),points[i])
            if distance <minDistance:
                minDistance =distance
                clusterIndex=j
       
        someList =clusters[clusterIndex].get_points()
        
        someList.append(points[i])
        clusters[clusterIndex].set_points(someList)
    return clusters
#this is the actualk means algorithm,
def run_k_means(points,k):
    #sampling random points from initial given data set.
    randomPoints = random.sample(points, k)
    
    clusters =[]
    #Creating empty clusters and empty list of points
    for i in range(k):
        newCluster =Cluster()
        listPoints=[]
        newCluster.set_points(listPoints)
        #newCluster.set_points(newCluster.get_points().append(Point()))
        newCluster.set_centroid(randomPoints[i])
        clusters.append(newCluster)
    #Assign the seed points to certein cluster
    clusters = assignToClusters(points,clusters)
#this iteration will continue, till stopping criteria met.
    while True:
        #Storing previous centroid
        oldCentroids=[]
        for i in range(len(clusters)):
            oldCentroids.append(clusters[i].get_centroid())
        #No update the clusters based on the new centroid
        clusters =updateClusters(clusters,points)
        newCentroids =[]
        for i in range(len(clusters)):
            newCentroids.append(clusters[i].get_centroid())   
        check = False
        for i in range(len(newCentroids)):
            if getDistance(newCentroids[i],oldCentroids[i])< 0.01:
                check=True
            else:
                check=False
                break
        if check==True:
            break
    return clusters
#empty the clusters and only keep the centroid and re calculate the distance between each point and centroid
def redoPoints(clusters,points):
    #print("Points"+str(len(clusters)))
    for i in range(len(clusters)):
        temp =[]
        clusters[i].set_points(temp)
    clusters=assignToClusters(points,clusters)
    return clusters 
#Calculate the new Centroid and assign to cluster
def updateClusters(clusters,points):
    for i in range(len(clusters)):
        newCentroid = calculateCentroid(clusters[i].get_points())
        #assign the new centroid to cluster.
        clusters[i].set_centroid(newCentroid)
    clusters =redoPoints(clusters,points)
    return clusters
#this method calculates the new centroidand returns a Point
def calculateCentroid(cluster):
    x=0
    y=0
    z=0
    length = len(cluster)
    for i in range(len(cluster)):
        x= x+cluster[i].get_x()
        y = y+cluster[i].get_y()
        z=z+cluster[i].get_z()
    point =Point()
    point.set_x(x/length)
    point.set_y(y/length)
    point.set_z(z/length)
    return point
#this metho prints the clusters
def printClusters(clusters):
    for i in range(len(clusters)):
        print("Cluster "+str(i+1)+" contains:"+str(len(clusters[i].get_points())))
        #printPoints(clusters[i].get_points())  
#this metho prints the points
def printPoints(points):
    for i in range(len(points)):
        print(str(points[i].get_x())+","+str(points[i].get_y())+","+str(points[i].get_z()))
#this method sorts the clusters based on the number of points in a given cluster.
def sort_clusters(clusters):
    for i in range(len(clusters)):
        for j in range(len(clusters)):
            if len(clusters[j].get_points())>len(clusters[i].get_points()):
                temp = clusters[i]
                clusters[i]=clusters[j]
                clusters[j]=temp
    printClusters(clusters)
#this method plots the 3d scatter plot of differnt clusters.
def plotClusters(clusters):
    x=[]
    y=[]
    z=[]
    fig = plt.figure()
    #ax = fig.add_subplot(111, projection='3d')
    ax = Axes3D(fig)
    #define the colors.
    colors =['g','r','b','y','m','k','0.45','#f4a460','#ffa500','#ffc0cb','c']
    c_color=[]
    m_mark=[]
    markers=['o',  '8','D','v', '^', '<', '>', 's', 'p', '*', 'h', 'H',  'd']
    for i in range(len(clusters)):
        points=clusters[i].get_points()
        color=colors[i]
        mark=markers[i]
        for j in range(len(points)):
            x.append(points[j].get_x())
            y.append(points[j].get_y())
            z.append(points[j].get_z())
            c_color.append(color)
            m_mark.append(mark)

    for i in range(len(x)):
        ax.scatter(x[i],y[i],z[i],s=40,c=c_color[i],marker=m_mark[i])

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    plt.show()
#This method calculates the sum of all SSEs of given list o clusters
def getSumSSE(clusters):
    sumVal=0.0
    #check if the cluster has 0 points
    if len(clusters[0].get_points())==0:
        return 1000000
    for i in range(len(clusters)):
        sumVal=sumVal+clusters[i].get_sse_val()
    return sumVal
#This is the main method
def main():
   points =get_data('data.csv')
   #this is the sse for each cluster
   sse=[]
   #this is value of K
   ks=[]
   #List of final cluster. Each item in this list is bunch of clusters for given i, where i=k
   final_clusters=[]
   #assign empty clusters to final list with infinite sse and empty points
   for i in range(13):
       list2=[]
       cluster =Cluster()
       some=[]
       cluster.set_points(some)
       cluster.set_sse(100000)
       list2.append(cluster)
       final_clusters.append(list2)
   #Iterate N times to rremove the factor of randomness
   for n in range(10):
       #for each value of K from 1 to 12
       for i in range(13):
           #run K means for given set of points and k
           clusters= run_k_means(points,i+1)
           sumSSECurrent=getSumSSE(clusters)
           sumSSEPrevious=getSumSSE(final_clusters[i])
           #compare the sse for given K and get the best cluster , having least SSE for the given K 
           
           if sumSSECurrent<sumSSEPrevious :
               final_clusters[i]=clusters
#this is the final list of clusters for given K
   for i in range(len(final_clusters)):
       print("K="+str(i+1))
       print("#############################")
       clusters=final_clusters[i]
       sort_clusters(clusters)
       sum_sse=0
       for j in range(len(clusters)):
          sum_sse= sum_sse+clusters[j].get_sse_val()
       sse.append(sum_sse)
       ks.append(i+1)
    #plot k vs SSE 
   plt.plot(ks,sse,lw=2)
   plt.xlabel("k")
   plt.ylabel("SSE")
   plt.title("K vs SSE")
   plt.show()
   print("SSE at K =8 is :"+str(getSumSSE(final_clusters[7])))
   #chosen K =8, least inflection point an plot the cluster based on the 
   plotClusters(final_clusters[7])
  

    
main()