#
# File: objecttier.py
# Name: Deep Patel
# CS 341, Fall 2022
# Builds Movie-related objects from data retrieved through
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:

    def __init__(self, theID, theTitle, theReleaseYear):
        self._Movie_ID = theID
        self._Title = theTitle
        self._Release_Year = theReleaseYear

    @property
    def Movie_ID(self):
        return self._Movie_ID

    @property
    def Title(self):
        return self._Title

    @property
    def Release_Year(self):
        return self._Release_Year


##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:

    def __init__(self, theID, theTitle, theReleaseYear, theNumReviews,
                 theAvgRating):
        self._Movie_ID = theID
        self._Title = theTitle
        self._Release_Year = theReleaseYear
        self._Num_Reviews = theNumReviews
        self._Avg_Rating = theAvgRating

    @property
    def Movie_ID(self):
        return self._Movie_ID

    @property
    def Title(self):
        return self._Title

    @property
    def Release_Year(self):
        return self._Release_Year

    @property
    def Num_Reviews(self):
        return self._Num_Reviews

    @property
    def Avg_Rating(self):
        return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:

    def __init__(self, theID, theTitle, theReleaseDate, theRuntime,
                 theOriginalLanguage, theBudget, theRevenue, theNumReviews,
                 theAvgRating, theTagline, theGenres, theProductionCompanies):
        self._Movie_ID = theID
        self._Title = theTitle
        self._Release_Date = theReleaseDate
        self._Runtime = theRuntime
        self._Original_Language = theOriginalLanguage
        self._Budget = theBudget
        self._Revenue = theRevenue
        self._Num_Reviews = theNumReviews
        self._Avg_Rating = theAvgRating
        self._Tagline = theTagline
        self._Genres = theGenres
        self._Production_Companies = theProductionCompanies

    @property
    def Movie_ID(self):
        return self._Movie_ID

    @property
    def Title(self):
        return self._Title

    @property
    def Release_Date(self):
        return self._Release_Date

    @property
    def Runtime(self):
        return self._Runtime

    @property
    def Original_Language(self):
        return self._Original_Language

    @property
    def Budget(self):
        return self._Budget

    @property
    def Revenue(self):
        return self._Revenue

    @property
    def Num_Reviews(self):
        return self._Num_Reviews

    @property
    def Avg_Rating(self):
        return self._Avg_Rating

    @property
    def Tagline(self):
        return self._Tagline

    @property
    def Genres(self):
        return self._Genres

    @property
    def Production_Companies(self):
        return self._Production_Companies


##################################################################
#
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
    # query for counting Movie_ID in Movies to determine # of movies
    sql1 = "Select Count(Movie_ID) from Movies;"
    numMovies = datatier.select_one_row(dbConn, sql1)
    if (numMovies == None):
        return -1
    else:
        return numMovies[0]  # returns the # of movies in the database


##################################################################
#
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
    # query for counting Rating in Ratings to determine # of reviews
    sql1 = "Select Count(Rating) from Ratings"
    numReviews = datatier.select_one_row(dbConn, sql1)
    if (numReviews == None):
        return -1
    else:
        return numReviews[0]  # returns the # of reviews in the database


##################################################################
#
# get_movies:
#
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name;
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
    # query for getting movies whose names are "like"
    sql1 = "Select Movie_ID, Title, strftime('%Y', Date(Release_Date)) from Movies where Title Like ? Order by Title asc;"
    theRows = datatier.select_n_rows(dbConn, sql1, [pattern])
    theMovies = []
    if (theRows == None):
        return theMovies
    else:
        for e in theRows:
            theMovies.append(Movie(e[0], e[1], e[2]))  # adds all the movies whose name are "like" the pattern
    return theMovies  # returns the list contains movie_id, title, year of all the movies whose name are "like" the pattern


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
    # query for movie details and the tagline condition
    sql1 = "Select Movies.Movie_ID, Title, Date(Release_Date), Runtime, Original_Language, Budget, Revenue, (Case When Tagline is Null Then '' Else Tagline End) From Movies Left Join Movie_Taglines on (Movies.Movie_ID = Movie_Taglines.Movie_ID) where Movies.Movie_ID = ?;"
    # query for count rating and average rating
    sql2 = "Select Count(Rating), (Case When Count(Rating) Is 0 Then 0.0 Else Avg(Rating) End) From Ratings where Movie_ID = ?;"
    # query for genre
    sql3 = "Select Genre_Name From Genres Join Movie_Genres on (Genres.Genre_ID = Movie_Genres.Genre_ID) where Movie_Genres.Movie_ID = ? Order by Genre_Name asc;"
    # query for movie production company
    sql4 = "Select Company_Name From Companies Join Movie_Production_Companies on (Companies.Company_ID = Movie_Production_Companies.Company_ID) where Movie_Production_Companies.Movie_ID = ? Order by Company_Name asc;"

    # acquires the information
    theMovies = datatier.select_one_row(dbConn, sql1, [movie_id])
    theRowRating = datatier.select_one_row(dbConn, sql2, [movie_id])
    theRowGenre = datatier.select_n_rows(dbConn, sql3, [movie_id])
    theRowProduction = datatier.select_n_rows(dbConn, sql4, [movie_id])

    if(theMovies is None or len(theMovies) == 0):
        return None
    else: # if info was fetched
        theGen = []
        theProd = []
        for e in theRowGenre:
            theGen.append(e[0])
        for e in theRowProduction:
            theProd.append(e[0])
    # returns all the data by calling MovieDetails
    return MovieDetails(theMovies[0], theMovies[1], theMovies[2], theMovies[3], theMovies[4], theMovies[5], theMovies[6], theRowRating[0], theRowRating[1], theMovies[7], theGen, theProd)


##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):
    # query for getting top N movies based on their average rating, and movie has to ahve specied # of reviews 
    sql1 = "Select Movies.Movie_ID, Title, strftime('%Y', Date(Release_Date)), Count(Rating), Avg(Rating) from Movies Join Ratings on (Movies.Movie_ID = Ratings.Movie_ID) Group by Movies.Movie_ID Having Count(Rating) >= ? Order By Avg(Rating) desc limit ?;"
    theRows = datatier.select_n_rows(dbConn, sql1, [min_num_reviews, N])
    theMovies = []
    if (theRows == None):
        return theMovies
    else:  # data was fetched and now adds Top N to theMovies list for each movie that has the conditions matched 
        for e in theRows:
            theMovies.append(MovieRating(e[0], e[1], e[2], e[3], e[4]))
    return theMovies
    

##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
    # condition for the rating
    if (rating < 0 or rating > 10):
        return 0
    # query for Movie_ID in Movie is valid
    sql1 = "Select * From Movies where Movie_ID = ?;"
    isMovie = datatier.select_one_row(dbConn, sql1, [movie_id])
    if (isMovie == None or len(isMovie) == 0):
        return 0
    else:
        sql1 = "Insert into Ratings(Movie_ID, Rating) Values(?, ?);"
        # perform_action() to return 1 if change was successfully made
        validated = datatier.perform_action(dbConn, sql1, [movie_id, rating])
        if (validated == 1):
            return validated  # returns 1
        else:
            return 0


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
    sql1 = "Select * From Movies where Movie_ID = ?;"
    isMovie = datatier.select_one_row(dbConn, sql1, [movie_id])
    if (isMovie is None or len(isMovie) == 0):
        return 0
    sql1 = "Select * From Movie_Taglines where Movie_ID = ?"
    isMovieID = datatier.select_one_row(dbConn, sql1, [movie_id])
    if (isMovieID is None or len(isMovieID) == 0):  # does not have one yet, hence inserts the provided one
        sql1 = "Insert into Movie_Taglines(Movie_ID, Tagline) Values(?,?);"
        # perform_action() to return 1 if change was successfully made
        validated = datatier.perform_action(dbConn, sql1, [movie_id, tagline])
    else:  # already has it, updates the taglin to provided one
        sql1 = "Update Movie_Taglines Set Tagline = ? where Movie_ID = ?;"
        # perform_action() to return 1 if change was successfully made
        validated = datatier.perform_action(dbConn, sql1, [tagline, movie_id])
    if (validated == 1):
        return validated  # returns 1
    else:
        return 0