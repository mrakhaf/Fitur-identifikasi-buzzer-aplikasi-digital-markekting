import networkx as nx
from sklearn import preprocessing
import pandas as pd

def modelling(clean_data):
    my_graph = nx.from_pandas_edgelist(clean_data, source='source', target='target', edge_attr='weight')

    #degree centrality
    DC = nx.degree_centrality(my_graph)
    result_DC = []
    for w in sorted(DC, key=DC.get, reverse=True):
        buzzer = {
            'account_name': w,
            'DC': DC[w]
        }
        result_DC.append(buzzer)
    df_result_DC = pd.DataFrame(result_DC)

    #betweenness centrality
    BC = nx.betweenness_centrality(my_graph, normalized=False)
    result_BC = []
    for w in sorted(BC, key=BC.get, reverse=True):
        buzzer = {
            'account_name': w,
            'BC': BC[w]
        }
        result_BC.append(buzzer)
    df_result_BC = pd.DataFrame(result_BC)

    #closeness centrality
    CC = nx.closeness_centrality(my_graph)
    result_CC = []
    for w in sorted(CC, key=CC.get, reverse=True):
        buzzer = {
            'account_name': w,
            'CC': CC[w]
        }
        result_CC.append(buzzer)
    df_result_CC = pd.DataFrame(result_CC)

    #eigenvector centrality
    EVC = nx.eigenvector_centrality_numpy(my_graph, weight='weight')
    result_EVC = []
    for w in sorted(EVC, key=EVC.get, reverse=True):
        buzzer = {
            'account_name': w,
            'EVC': EVC[w]
        }
        result_EVC.append(buzzer)
    df_result_EVC = pd.DataFrame(result_EVC)

    #merge
    all_measure = pd.merge(df_result_DC, df_result_BC, on='account_name', how='left')
    all_measure = pd.merge(all_measure, df_result_CC, on='account_name', how='left')
    all_measure = pd.merge(all_measure, df_result_EVC, on='account_name', how='left')

    cols = ['DC', 'BC', 'CC', 'EVC']
    scaller = preprocessing.MinMaxScaler()
    all_measure[['DC_Norm', 'BC_Norm', 'CC_Norm', 'EVC_Norm',]] = scaller.fit_transform(all_measure[cols])
    all_measure['final_measure'] = (all_measure.BC_Norm + all_measure.DC_Norm + all_measure.CC_Norm + all_measure.EVC_Norm)/4
    all_measure = all_measure.sort_values(by='final_measure', ascending=False)

    final_result = []
    for account_name, dc, bc, cc, evc in zip(all_measure['account_name'], all_measure.DC, all_measure.BC, all_measure.CC, all_measure.EVC):
        buzzer = {
            'account_name': account_name,
            'degree_centrality': dc,
            'betweenness_centrality': bc,
            'closeness_centrality': cc,
            'eigenvector_centrality': evc
        }
        final_result.append(buzzer)

    return final_result        