import config
import requests
from api import get_friends
import igraph
from igraph import Graph, plot
from time import sleep
from messages import get_name



def get_friend_ids(user_id):
    for i in range(5):
        try:
            ids = [int(u) for u in get_friends(user_id)['items']]
            return ids
        except:
            sleep(0.1 * (i + 1))


def get_network(user_id, as_edgelist=True):
    users_ids = get_friend_ids(user_id)
    edges = []
    for i in range(len(users_ids)):
        friends = get_friend_ids(users_ids[i])
        if friends:
            for j in range(len(users_ids)):
                if users_ids[j] in friends and not (i, j) in edges and not (j, i) in edges:
                    edges.append(( get_name(users_ids[i]['last_name']),  get_name(users_ids[j]['last_name'])))

    # Создание графа
    g = Graph(vertex_attrs={"label": users_ids},
              edges=edges, directed=False)

    # Задаем стиль отображения графа
    N = len(users_ids)
    visual_style = {}
    visual_style["layout"] = g.layout_fruchterman_reingold(
        maxiter=100000,
        area=N ** 3,
        repulserad=N ** 3)
    visual_style["bbox"] = (1200, 1200)

    g.simplify(multiple=True, loops=True)
    communities = g.community_fastgreedy()
    # communities = g.community_edge_betweenness(directed=False)
    clusters = communities.as_clustering()
    pal = igraph.drawing.colors.ClusterColoringPalette(len(clusters))
    g.vs['color'] = pal.get_many(clusters.membership)

    # Отрисовываем граф
    plot(g, **visual_style)
