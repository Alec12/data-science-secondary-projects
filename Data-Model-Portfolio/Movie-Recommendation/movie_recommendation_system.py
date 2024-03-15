# import libraries
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import warnings
import time
import math
import os
from utils import create_bins

class MovieRecommendationSystem:
    def __init__(self):
        """Initialize necessary attributes and libraries"""
        self.G = nx.Graph(label='IMDB Movies')
        warnings.filterwarnings("ignore")
        plt.rcParams['figure.figsize'] = [7,7]
        self.load_data()

    def load_data(self):
        """Load and preprocess data"""
        data_folder = 'data'
        data_path = os.path.join(os.getcwd(), data_folder)
        self.movies = pd.read_csv(os.path.join(data_path, 'IMDb movies.csv'))
        self.mov_names = pd.read_csv(os.path.join(data_path, 'IMDb names.csv'))
        self.mov_ratings = pd.read_csv(os.path.join(data_path, 'IMDb ratings.csv'), na_filter=False)
        self.mov_t_principals = pd.read_csv(os.path.join(data_path, 'IMDb title_principals.csv'))
        self.mv_new = self.transform_data()

    def transform_data(self):
        """Data transformation"""
        mr = self.mov_ratings[self.mov_ratings.columns.drop(list(self.mov_ratings.filter(regex='_0age'))).drop(['weighted_average_vote', 'total_votes', 'mean_vote', 'median_vote'])]
        mv = self.movies[['imdb_title_id', 'original_title', 'year', 'genre', 'country', 'avg_vote', 'votes']]
        mv.rename(columns={'original_title': 'title'}, inplace=True)
        
        #include demographic ratings
        mv = mv.merge(mr, on='imdb_title_id', how='left')
        mv = mv.dropna()

        # Filter USA/Canada ratings
        mv = mv[(mv['country'].str.contains('USA'))|(mv['country'].str.contains('Canada'))]

        # Change year
        mv['year'] = mv['year'].astype(str).str.replace('TV Movie ','')


        reit_cols = list(mv.columns[5:]) # + ['year']
        num_bins_created = 4
        for col in reit_cols:
            # Create bins
            mv = create_bins(mv, num_bins_created, col)

            # Make each column a list
            mv[col] = mv[col].apply(lambda x: [] if pd.isna(x) else [i.strip() for i in x.split(",")])

        mv['genre'] = mv.genre.apply(lambda l: [] if pd.isna(l) else [i.strip() for i in l.split(",")])
        mv['country'] = mv.country.apply(lambda x: [] if pd.isna(x) else [i.strip() for i in x.split(",")])

        # Find duplicates
        dup = mv['title'].duplicated(keep=False)
        mv.loc[dup, 'title'] += mv.groupby('title').cumcount().astype(str)
        
        return mv

    def create_graph(self, mv):
        """Create graph representation of data"""
        self.start_time = time.time()
        self.G = nx.Graph(label='IMDB Movies')

        for i, row in mv.iterrows():
            if i % 10000 == 0:
                print(" iter {} -- {} seconds --".format(i, time.time() - self.start_time))
            
            self.G.add_node(row['title'], key=row['imdb_title_id'], label='MOVIE')
            
            for col in mv.columns[2:]:
                for element in row[col]:
                    if col == 'genre':
                        genre_node = element + '_Genre'
                        self.G.add_node(genre_node, label='GENRE')
                        self.G.add_edge(row['title'], genre_node, label='GENRE_IN')
                    else:
                        self.G.add_node(element, label=col.upper())
                        self.G.add_edge(row['title'], element, label=col.upper() + "_IN")
                    
        print(" finish -- {} seconds --".format(time.time() - self.start_time))

    def draw_sub_graph(self, sub_graph):
        """Visualize the subgraph with movie names, year, genre, and country"""
        subgraph = self.G.subgraph(sub_graph)
        colors = []
        font_colors = []

        label_colors_mapping = {
            'MOVIE': (0, 1, 1, 1),  # Cyan
            'YEAR': (1, 0, 0, 1),     # Red
            'GENRE': (0, 1, 0, 1),    # Green
            'COUNTRY': (0, 0, 1, 1),    # Blue
        }

        labels_to_keep = ['MOVIE', 'YEAR', 'GENRE', 'COUNTRY']
        for e in subgraph.nodes():
            label = self.G.nodes[e]['label']
            if label in labels_to_keep:
                color = label_colors_mapping.get(label, (1, 0, 0, 0))  # Default to transparent if label not found
                font_color = (1,0,0,0)
            else:
                color = (1, 1, 1, 0)  # Fully transparent color for nodes not in labels_to_keep
                font_color = (1,0,0,0)
            colors.append(color)
            font_colors.append(font_color)

        nx.draw(subgraph, with_labels=True, font_color=(0, 0, 0, 1), font_weight='bold', node_color=colors)


    def get_all_adj_nodes(self, list_in):
        """Find all adjacent nodes"""
        sub_graph=set()
        for m in list_in:
            sub_graph.add(m)
            for e in self.G.neighbors(m):
                sub_graph.add(e)
        return list(sub_graph)
    
    def get_recommendation(self, root):
        """Get movie recommendations"""
        commons_dict = {}
    
        for e in self.G.neighbors(root):
            for e2 in self.G.neighbors(e):
                if e2 == root:
                    continue
                if self.G.nodes[e2]['label']=='MOVIE':
                    commons = commons_dict.get(e2)
                    if commons==None:
                        commons_dict.update({e2 : [e]})
                    else:
                        commons.append(e)
                        commons_dict.update({e2 : commons})
        
        movies = []
        weight = []
        
        for key, values in commons_dict.items():
            w = 0.0
            for e in values:
                w += 1 / math.log(self.G.degree(e))
            movies.append(key)
            weight.append(w)
        
        result = pd.Series(data=np.array(weight), index=movies)
        result.sort_values(inplace=True, ascending=False)
        
        return result

    def conclude_results(self, title):
        """Display results and recommendations"""
        result = self.get_recommendation(title)
        
        print("*" * 40)
        print(" Recommendation for {} ".format(title))
        print("*" * 40)
        print(result.head(7))
        
        reco = list(result.index[:4].values)
        reco.extend([title])
        sub_graph = self.get_all_adj_nodes(reco)
        self.draw_sub_graph(sub_graph)

    def run_recommendation_system(self, title):
        """Runs recommendation system based on user input"""
        self.create_graph(self.mv_new)
        self.conclude_results(title)
        print("Recommendation system execution time:", time.time() - self.start_time, "seconds")
