import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
#from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re
import project_functions as pf
from matplotlib import animation


df = pd.read_csv(r'data/all_songs_data.csv')

df2 = df.copy()

# unique years
years = df2.Year.unique()

## Process Lyrics Column
df2['Lyrics'] = df2['Lyrics'].astype(str)
#bag_of_lyrics = pf.bag_of_words(df2['Lyrics'], True)

yearly_word_dict_titles = {}
for year in years:
    temp = df2[df2['Year']==year]
    word_dict = pf.word_dictionary(temp['Song Title'], True)
    top_20_words = dict(sorted(word_dict.items(), key=lambda item: item[1], reverse=True)[:20])
    yearly_word_dict_titles[int(year)] = top_20_words


def title_word_dictionary(df, max_words):
    yearly_word_dict_titles = {}
    for year in years:
        temp = df[df['Year']==year]
        word_dict = pf.word_dictionary(temp['Song Title'], True)
        top_words = dict(sorted(word_dict.items(), key=lambda item: item[1], reverse=True)[:max_words])
        yearly_word_dict_titles[int(year)] = top_words

    return yearly_word_dict_titles

def filter_words_by_years(yearly_word_dict_titles, min_years=10):
    """
    Filter words based on the minimum number of years they are present in.
    
    Args:
        yearly_word_dict_titles (dict): Dictionary containing word counts for each year.
        min_years (int, optional): Minimum number of years a word should be present in. Defaults to 10.
    
    Returns:
        list: List of words present in at least min_years.
    """
    selected_words = []

    # Iterate over each word
    # Extract all words available
    all_words = set(word for year_dict in yearly_word_dict_titles.values() for word in year_dict.keys())
    
    for word_to_track in all_words:
        # Count the number of years the word appears in
        num_years_present = sum(1 for year_dict in yearly_word_dict_titles.values() if word_to_track in year_dict)

        # Check if the word appears in at least min_years
        if num_years_present >= min_years:
            selected_words.append(word_to_track)

    return selected_words




yearly_word_dict_titles = title_word_dictionary(df2, 20)
selected_words = filter_words_by_years(yearly_word_dict_titles, min_years = 10)

# List to store names of words with counts exceeding 5 in any year
annotated_words = []

def update(frame):
    plt.cla()

    for i, word_to_track in enumerate(selected_words):
        years = list(yearly_word_dict_titles.keys())
        counts = [yearly_word_dict_titles[year].get(word_to_track, 0) for year in years]

        plt.plot(years[:frame+1], counts[:frame+1], marker='o', label=word_to_track, color=colors[i % len(colors)])

        max_count_index = counts.index(max(counts[:frame+1]))

        label_max_word_count = 5
        if counts[max_count_index] >= label_max_word_count:
            annotated_words.append((word_to_track, years[max_count_index], counts[max_count_index]))

    plt.title('Word Choice in the Top 100 Billboard Song Titles Over Years')
    plt.xlabel('Year')
    plt.ylabel('Word Count')
    plt.grid(True)

    plt.xticks(np.arange(years[0], years[-1] + 1, 2), rotation=70)

    plt.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)

    for word_to_annotate, year, count in annotated_words:
        line_color = colors[selected_words.index(word_to_annotate) % len(colors)]
        plt.text(year, count, f'$\\bf{{\\it {word_to_annotate}}}$', fontsize=8, verticalalignment='bottom',
                 color=line_color, bbox=dict(facecolor=line_color, alpha=0.01, edgecolor=line_color))

    plt.tight_layout()

# Set up the figure
fig, ax = plt.subplots(figsize=(10, 6))

# Set up the initial plot
colors = plt.rcParams['axes.prop_cycle'].by_key()['color']
annotated_words = []

# Create the animation
ani = animation.FuncAnimation(fig, update, frames=len(years), repeat=False)
#ani.save('animation.mp4', writer='ffmpeg')
ani.save('animation.gif', writer='pillow')
plt.show()
