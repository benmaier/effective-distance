import networkx as nx
from numpy import *
import sys

def get_effdist_tree(G,source,cutoff=None,create_using=nx.DiGraph,weight='weight',effdist_key='effdist'):

    T = create_using()
    T.graph['root'] = source
    T.add_node(source)
    
    length,path = nx.single_source_dijkstra(G,source,cutoff=cutoff,weight=weight)

    for n in path.keys():
        T.add_path(path[n])
        T.node[n][effdist_key] = length[n]

    return T

def get_mean_effdist(G,with_error=False,weight='weight',get_all=False):
    length = nx.all_pairs_dijkstra_path_length(G)
    res = [ length[n][n2] for n in length.keys() for n2 in length[n].keys() ]

    if get_all:
        return array(res)
    elif with_error:
        return mean(res), std(res)/sqrt(len(res)-1)
    else:
        return mean(res)

def get_probability_graph(G_,weight=None,for_effdist=False):
    G = nx.DiGraph(G_)
    k_out = G.out_degree(weight=weight)

    if weight is None:
        key = 'weight'
    else:
        key = weight

    for e in G.edges(data=True):
        if weight in e[2]:
            dat = float(e[2][weight])
        else:
            dat = 1.

        if for_effdist:
            G[e[0]][e[1]][key] = 1. - log(dat/k_out[e[0]])
        else:
            G[e[0]][e[1]][key] = dat/k_out[e[0]]

    return G

def modify_to_effdist_graph(probability_graph,weight='weight'):

    for e in probability_graph.edges(data=True):
        if weight in e[2]:
            dat = float(e[2][weight])
        else:
            print "modify_to_effdist_graph: wrong key (", weight,")"
            sys.exit(1)

        probability_graph[e[0]][e[1]][weight] = 1. - log(dat)



if __name__=="__main__":

    from radial_distance_layout import *
    import pylab as pl
    fig,(ax1,ax2) = pl.subplots(1,2,figsize=(20,10))

    G = nx.fast_gnp_random_graph(100,0.3,directed=True)

    for e in G.edges(data=True):
        G[e[0]][e[1]]['weight'] = random.rand()

    G = get_probability_graph(G,weight='weight',for_effdist=True)
    T = get_effdist_tree(G,0)


    pos = nx.graphviz_layout(G,prog='neato')
    nx.draw_networkx(G,pos,ax=ax1)
    nx.draw_networkx_edge_labels(G,pos,ax=ax1)


    pos = radial_distance_layout(T,dist_key='effdist')
    #pos = nx.graphviz_layout(G,prog='neato')
    nx.draw_networkx(T,pos,ax=ax2)
    #nx.draw_networkx_edge_labels(G,pos)

    e = G.edges(data=True)[0]
    print get_mean_effdist(G)


    pl.show()
    
