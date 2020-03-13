from api import get_friee
import igraph
from igraph import Graph, plot
from time import sleep
from api import get_friends
#from stopwords import get_stop_words

def get_friend_ids(user_id):
    for i in range(10):
        try:
            ids = [int(u) for u in get_friends(user_id)['items']]
            return ids
        except Exception as e:
            sleep(0.1 * i)


def get_network(user_id, as_edgelist=True):
    users_ids = get_friend_ids(user_id)
    edges = []
    id=[]
    use = get_friee(user_id)
    for i in range(len(users_ids)):
        friends = get_friend_ids(users_ids[i])
        p=use[i]
        if friends:
            for j in range(len(users_ids)):
                g = use[j]
                if users_ids[j] in friends and not (i, j) in edges and not (j, i) in edges:
                    edges.append((p, g))
                    id.append((i,j))
    print(id)


    # Создание графа
    g = Graph(vertex_attrs={"label": use},
              edges=id, directed=False)

    # Задаем стиль отображения графа
    N = len(use)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=100000,
        area=N ** 3,
        repulserad=N ** 3)
    visual_style["bbox"] = (1200, 1200)
    visual_style["edge_color"] = '#CDCDCD'

    g.simplify(multiple=True, loops=True)
    communities = g.community_fastgreedy()
    clusters = communities.as_clustering()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    plot(g, **visual_style)
