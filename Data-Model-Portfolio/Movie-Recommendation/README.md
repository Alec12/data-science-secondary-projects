# Movie Recommendation System based on Graph Representation of Data

There are numerous movie rating websites like IMDB.com that offer users a wealth of information about movies. Users can search for their favorite actors or actresses and discover the movies they've starred in, along with the overall ratings of those movies. While these platforms facilitate the process of finding movies to watch, the sheer volume of available options can make it challenging to pinpoint ones that align with individual tastes. Websites like rottentomatoes.com have attempted to address this issue by aggregating both critic and audience scores, providing users with a curated selection of movies categorized by genre. However, even with such catalogs, users may still find themselves sifting through numerous pages to identify films that truly resonate with them.

This repository offers a straightforward solution by matching a given movie with the most similar ones, thereby enabling users to efficiently discover movies based solely on ratings and available demographic data. The methodology employed here leverages IMDB data for movies up to the year 2020. Movies are organized within a graph network, with connections established based on their respective quantile rating positions within demographic groups. This approach allows us to identify movies that are most closely aligned with those rated similarly by various demographic segments.

## Example:

### Enter the name of the movie: The Godfather
****************************************
 Recommendation for The Godfather 
****************************************
Wind River1                                  5.025763
Three Billboards Outside Ebbing, Missouri    5.025763
Detroit                                      5.025763
Molly's Game                                 5.025763
Baby Driver                                  5.025763
Shot Caller                                  5.025763
Witness for the Prosecution                  5.025594
