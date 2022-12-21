# Name: Deep Patel
# Class: CS 341, 2pm
# Description:  a Python program to implement 5 commands:
# lookup movies by name/pattern,
# lookup details about a specific movie,
# top N movies by average rating,
# insert a review, and
# set a movie’s tagline. 
# Imports sqlite3 and objecttier to call the functions in order to perform 
# particular activity with the database
# References: 
#  learning python: https://www.w3schools.com/python/
#  sqlite programming: https://docs.python.org/3/library/sqlite3.html
#
import sqlite3
import objecttier


def print_stats(dbConn):
    print("General stats:")
    theNumMovies = objecttier.num_movies(dbConn)
    theNumReviews = objecttier.num_reviews(dbConn)
    print("  # of movies:", f"{theNumMovies:,}")
    print("  # of reviews:", f"{theNumReviews:,}\n")

def retreiveMovies(dbConn):
    userEntered = input("\nEnter movie name (wildcards _ and % supported): ")
    theMovies = objecttier.get_movies(dbConn, userEntered)
    if (len(theMovies) == 0 or theMovies is None):
        print("\n# of movies found: 0")
    elif(len(theMovies) >= 101):
        print("\n# of movies found:", len(theMovies))
        print("There are too many movies to display, please narrow your search and try again...")
    else:
        print("\n# of movies found:", len(theMovies))
        print()
        for e in theMovies:
            print(e.Movie_ID, ":", e.Title, f"({e.Release_Year})")

def retreiveDetails(dbConn):
    userEntered = input("\nEnter movie id: ")
    theDetails = objecttier.get_movie_details(dbConn, userEntered)
    if (theDetails is None):
        print("\nNo such movie...")
    else:
        print()
        print(theDetails.Movie_ID, ":", theDetails.Title)
        print("  Release date:", theDetails.Release_Date)
        print("  Runtime:", theDetails.Runtime, "(mins)\n  Orig language:", theDetails.Original_Language)
        print("  Budget:", f"${theDetails.Budget:,}", "(USD)\n  Revenue:", f"${theDetails.Revenue:,}", "(USD)\n  Num reviews:", theDetails.Num_Reviews)
        print("  Avg rating:", f"{theDetails.Avg_Rating:.2f}", "(0..10)\n  Genres: ", end="")
        if(len(theDetails.Genres) == 0):
            print()
        else:
            for e in theDetails.Genres:
                print(e + ", ", end="")
        print("\n  Production companies: ", end="")
        if(len(theDetails.Production_Companies) == 0):
            print()
        else:
            for e in theDetails.Production_Companies:
                print(e + ", ", end="")
        print("\n  Tagline:", theDetails.Tagline)

def retrieveTopN(dbConn):
    userN = int(input("\nN? "))
    if(userN <= 0):
        print("Please enter a positive value for N...\n")
        return
    userReview = int(input("min number of reviews? "))
    if (userReview <= 0):
        print("Please enter a positive value for min number of reviews...\n")
        return
    theTopN = objecttier.get_top_N_movies(dbConn, userN, userReview)
    if (len(theTopN) == 0 or theTopN is None):
        print()
    else:
        print()
        for e in theTopN:
            print(e.Movie_ID, ":", e.Title, f"({e.Release_Year}),", "avg rating =", f"{e.Avg_Rating:.2f}", f"({e.Num_Reviews} reviews)")

def retrieveReview(dbConn):
    userRating = int(input("\nEnter rating (0..10): "))
    if (userRating < 0 or userRating > 10):
        print("Invalid rating...\n")
        return
    userID = input("Enter movie id: ")
    theReview = objecttier.add_review(dbConn, userID,userRating)
    if (theReview == 0):
        print("\nNo such movie...")
    else:
        print("\nReview successfully inserted")

def retrieveTagline(dbConn):
    userTagline = input("\ntagline? ")
    userID = input("movie id? ")
    theTagline = objecttier.set_tagline(dbConn, userID, userTagline)
    if (theTagline == 0):
        print("\nNo such movie...")
    else:
        print("\nTagline successfully set")
    
        

print('** Welcome to the MovieLens app **\n')
dbConn = sqlite3.connect('MovieLens.db')
print_stats(dbConn)
cmd = input("Please enter a command (1-5, x to exit): ")

while cmd != "x":
    if cmd == "1":
        retreiveMovies(dbConn)
    elif cmd == "2":
        retreiveDetails(dbConn)
    elif cmd == "3":
        retrieveTopN(dbConn)
    elif cmd == "4":
        retrieveReview(dbConn)
    elif cmd == "5":
        retrieveTagline(dbConn)
    else:
        print("**Error, unknown command, try again...")

    print()
    cmd = input("Please enter a command (1-5, x to exit): ")