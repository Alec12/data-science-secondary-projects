import numpy as np 
from string import punctuation, digits

def extract_words(text):
    """
    Helper function for `bag_of_words(...)`.
    Args:
        a string `text`.
    Returns:
        a list of lowercased words in the string, where punctuation and digits are removed.
    """
    for c in punctuation.replace("'", "")  + digits:
        text = text.replace(c, ' ')
    return text.lower().split()

def word_dictionary(texts, remove_stopword=False):
    """
    Args:
        `texts` - a list of natural language strings.
    Returns:
        a dictionary with count of each word.
    """
    if remove_stopword == True:
        with open('data/stopwords.txt') as f:
            lines = f.readlines()
        stopword = [sub.replace('\n', '') for sub in lines] 
    else:
        stopword = [] 
    #raise NotImplementedError

    indices_by_word = {}  # maps word to unique index
    for text in texts:
        word_list = extract_words(text)
        for word in word_list:
            if word in stopword: continue
            elif word in indices_by_word: 
                indices_by_word[word] += 1
            else:
                indices_by_word[word] = 1

    return indices_by_word


def bag_of_words(texts, remove_stopword=False):
    """
    Args:
        `texts` - a list of natural language strings.
    Returns:
        a dictionary that maps each word appearing in `texts` to a unique
        integer `index`.
    """
    if remove_stopword == True:
        with open('data/stopwords.txt') as f:
            lines = f.readlines()
        stopword = [sub.replace('\n', '') for sub in lines] 
    else:
        stopword = [] 
    #raise NotImplementedError

    indices_by_word = {}  # maps word to unique index
    for text in texts:
        word_list = extract_words(text)
        for word in word_list:
            if word in indices_by_word: continue
            if word in stopword: continue
            indices_by_word[word] = len(indices_by_word)

    return indices_by_word

def title_word_dictionary(df, max_words):
    # unique years in dataframe
    years = df.Year.unique()

    yearly_word_dict_titles = {}
    for year in years:
        temp = df[df['Year']==year]
        word_dict = word_dictionary(temp['Song Title'], True)
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
