import networkx as nx

def modelling(clean_data):
    my_graph = nx.from_pandas_edgelist(clean_data, source='x', target='y')
    most_influental = nx.degree_centrality(my_graph)
    buzzer_account = []
    for w in sorted(most_influental, key=most_influental.get, reverse=True):
        buzzer = {
            'account_name': w,
            'measure': round(most_influental[w],2)
        }
        buzzer_account.append(buzzer)
    return buzzer_account        