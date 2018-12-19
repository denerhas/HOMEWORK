#!/usr/bin/python

#Hasan Dener

from gurobipy import GRB, Model

# dissimilarity
dissimilarity = [[0,50,21,41,44,18,91,12,90,77,89,31],
				[50,0,81,88,36,70,19,49,67,100,35,74],
				[21,81,0,40,98,79,65,84,60,15,37,60],
				[41,88,40,0,18,49,31,96,78,93,41,38],
				[44,36,98,18,0,36,77,94,70,52,49,31],
				[18,70,79,49,36,0,87,40,15,90,0,46],
				[91,19,65,31,77,87,0,40,31,34,22,60],
				[12,49,84,96,94,40,40,0,15,25,3,87],
				[90,67,60,78,70,15,31,15,0,60,17,100],
				[77,100,15,93,52,90,34,25,60,0,21,83],
				[89,35,37,41,49,0,22,3,17,21,0,15],
				[31,74,60,38,31,46,60,87,100,83,15,0]]

species = range(0,10)

# Model
m = Model("species")

x = m.addVars(species, species, vtype = GRB.BINARY, name="dissimilarity")

y = m.addVars(species, vtype=GRB.BINARY, name="select")

D = m.addVar(name="max_diss", obj = 1)

m.addConstrs(
    (x.sum(i,'*') <= 10 * y[i] for i in species), "group")

m.addConstrs(
    (x.sum('*',j) == 1 for j in species), "assign")

m.addConstr(y.sum() == 1)

m.addConstrs(dissimilarity[i][j] * x[i,j] <= D for i in species for j in species)

# The objective is to minimize the group dissimilarity within group and maximize the group dissimilarity between groups
m.modelSense = GRB.MINIMIZE

# Solve
m.optimize()


# Create an empty directed graph
G = nx.DiGraph()
for i in species:
    for j in species:
        if x[i,j].x > 0:
			G.add_edge(i, j, cost=dissimilarity[i][j])

print('SUB GRAPH NODE LIST: ')
for i in species:
	subNodeList = [];
	maxWeight = 0;
    for j in species:
        if x[i,j].x > 0:
			subNodeList.append(j)		
	
	
	sub_G = nx.subgraph(G,subNodeList)
	
	print("The layout of the sub graph of nodes with edges")
	msT = nx.minimum_spanning_tree(sub_G)		
	pos = nx.spring_layout(msT, scale = 100.)
	nx.draw_networkx_nodes(msT, pos)
	nx.draw_networkx_edges(msT, pos)
	nx.draw_networkx_labels(msT, pos)
	plt.axis('off')
	plt.show()	

	print("Average species dissimilarity between nodes ")
	print(nx.average_node_connectivity(msT))
	
	print("Average shortest path length between all pairs of a cluster")
	print(nx.average_clustering(msT))	
	
	
	mxsT = nx.maximum_spanning_tree(sub_G)
	pos = nx.spring_layout(msT, scale = 100.)
	nx.draw_networkx_nodes(msT, pos)
	nx.draw_networkx_edges(msT, pos)
	nx.draw_networkx_labels(msT, pos)
	plt.axis('off')
	plt.show()
	
	for j in species:
		DSP = nx.dijkstra_path(sub_G, i, j)
		print("Maximum dissimilarity between", i, "and", j)
		print(nx.dijkstra_path_length(sub_G, i, j))
			
# Print solution
print('\MAXIMUM DISSIMILARITY: %g' % m.objVal)
print('SOLUTION:')
for i in species:
    for j in species:
        if x[i,j].x > 0:
            print('Species %g is assigned to species %g' % (j, i))