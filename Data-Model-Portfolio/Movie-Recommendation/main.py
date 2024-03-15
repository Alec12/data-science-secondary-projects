# Importing necessary libraries
import time
import matplotlib.pyplot as plt
from movie_recommendation_system import MovieRecommendationSystem

def main():
    start_time = time.time()
    print("Initializing recommendation system...")
    recommendation_system = MovieRecommendationSystem()
    title = input("Enter the name of the movie: ")
    recommendation_system.run_recommendation_system(str(title))
    print("Recommendation system execution time:", time.time() - start_time, "seconds")
    plt.show()

if __name__ == "__main__":
    main()
