from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import os
import mediautlils

extensionsToCheck = ["mkv", "avi", "mp4", "mpg", "mpeg"]
tvfolders = ["TV", "tv", "Television", "Anime"]
moviefolders = ["Movies", "movies"]


class MediaLibrary:
    """
    Media Library class that can search through a formatted file directory that contains a TV directory with television
    shows formatted like TV/South Park/Season 04/South.Park.S04E03.mkv, for example. It can parse a variety of video
    formats, but expects certain indicators in the file path, such as season and episode specifiers.
    """

    def __init__(self, directories):
        """
        Initialize a media library using a list of directories.
        :param directories: list of directory paths, when querying episode paths, this path will be prepended to the
                            file path.
        :return: MediaLibrary
        :rtype : MediaLibrary
        """
        self.directories = directories

    def list_shows(self):
        """
        Scan the media library's directories for the current shows.
        :return: A list of the names of the available television shows in the library.
        :rtype : list
        """
        ret = []
        for directory in self.directories:
            walk = os.walk(directory)
            try:
                _, notList, files = next(walk)
                for tvfolder in tvfolders:
                    if tvfolder in notList:
                        directory, shows, _ = next(os.walk("%s/%s" % (directory, tvfolder)))
                        ret = ret + shows

            except StopIteration as e:
                pass
                # no op
        return ret

    def list_movies(self):
        """
        Scan the media library's directories for the current movies.
        :return: A list of the names of the available movies in the library
        :rtype: list[str]
        """
        ret = []
        for directory in self.directories:
            walk = os.walk(directory)
            try:
                _, folders, _ = next(walk)
                if "Movies" in folders:
                    dir, movies, _ = next(os.walk(directory + "/Movies"))
                    ret = ret + movies
            except Exception as e:
                pass
        return ret

    def list_movie_paths(self):
        """
        Get the list of the file paths of all of the available movies
        :return: A list of the file paths for all of the currently available movies
        :rtype: list[str]
        """
        ret = []
        for directory in self.directories:
            walk = os.walk(directory)
            try:
                _, folders, _ = next(walk)
                if "Movies" in folders:
                    dir, movies, _ = next(os.walk(directory + "/Movies"))
                    for movie in movies:
                        path, _, files = next(os.walk(dir + "/" + movie))
                        for file in files:
                            if any(ext in file for ext in extensionsToCheck):
                                ret.append(path + "/" + file)
            except Exception as e:
                pass
        return ret

    def find_movie(self, query):
        """
        Find the movie in the library that best matches the given query.
        :param query: Query to search for in the library
        :return: The name of the movie whose title best matches the given query
        :rtype: str
        """
        results = process.extract(query, self.list_movies(), limit=1)
        return results[0][0]

    def movie_path(self, movie):
        """
        Get the file path for a given movie query
        :param movie: The movie being queried
        :return: File path for the movie that best matched the query
        :rtype: str
        """
        movie = self.find_movie(movie)
        movie_paths = self.list_movie_paths()
        for path in movie_paths:
            if movie in path:
                return path
        return None

    def find_movie_path(self, query):
        return self.movie_path(self.find_movie(query))

    def show_path(self, show_name):
        """
        Get the root path of a show by name.
        :rtype : str
        :param show_name: The name of the show whose root directory path is wanted.
        :return: string containing the path to the requested show's directory.
        """
        show_name = self.find_show(show_name)
        for directory in self.directories:
            walk = os.walk(directory)
            try:
                _, dirlist, _ = next(walk)
                if "TV" in dirlist:
                    path, shows, _ = next(os.walk(directory + "/TV"))
                    if show_name in shows:
                        return path + "/" + show_name
            except Exception as e:
                pass
        print "Show %s not found in library" % show_name
        return None

    def list_seasons(self, show_name):
        """
        Get the list of all the seasons available for a given show. Any folder under the show directory is considered a
        season.
        :param show_name: The name of the show
        :return: A list of the seasons available for this show.
        :rtype : list[str]
        """
        show_name = self.find_show(show_name)
        rootpath = self.show_path(show_name)
        walk = os.walk(rootpath)
        try:
            _, seasons, files = next(walk)
            seasons = filter(lambda x:mediautlils.seasonnumber(x) is not None, seasons)
            return seasons
        except Exception, e:
            print "No seasons available for %s" % show_name
            return None

    def list_episodes(self, showname, snum=None):
        """
        Get the list of all of the episodes available for a given show for a given season. If no season is specified,
        it will return all of the episodes for the show.
        :param showname: The name of the show
        :param season: The season whose episodes you want. If not specified, this function will return all of the episodes
                        for the show.
        :return: A list of the episode file names for the requested show.
        :rtype: list[str]
        """
        seasons = self.list_seasons(showname)
        showdirectory = self.show_path(showname)
        ret = []

        if snum is None:
            # Get all the episodes if no season is specified
            for season in seasons:
                walk = os.walk(showdirectory + "/" + season)
                directory, _, episodes = next(walk)
                ret = ret + episodes
        else:
            seasoncandidates = filter(lambda x:mediautlils.seasonnumber(x) == snum, seasons)
            for season in seasoncandidates:
                walk = os.walk(showdirectory + "/" + season)
                directory, _, episodes = next(walk)
                ret = episodes

        # Filter out non-video files
        filtered = []
        for result in ret:
            if any(ext in result for ext in extensionsToCheck):
                filtered.append(result)

        return filtered

    def list_episode_paths(self, showname, season=None):
        """
        Get the list of all of the episode paths available for a given show for a given season. If no season is specified,
        it will return all of the paths for episodes of the show.
        :param showname: The name of the show
        :param season: The season whose episodes you want. If not specified, this function will return all of the episodes
                        for the show.
        :return: A list of the episode file paths for the requested show.
        :rtype: list[str]
        """
        seasons = self.list_seasons(showname)
        showdirectory = self.show_path(showname)
        ret = []

        if season is None:
            for season in seasons:
                walk = os.walk(showdirectory + "/" + season)
                directory, _, episodes = next(walk)
                ret = ret + [directory + "/" + episode for episode in episodes]
        else:
            if season < 10:
                sestr = "0" + str(season)
            else:
                sestr = "" + str(season)
            for season in seasons:
                if sestr in season:
                    walk = os.walk(showdirectory + "/" + season)
                    directory, _, episodes = next(walk)
                    ret = [directory + "/" + episode for episode in episodes]

        # Filter out non-video files
        filtered = []
        for result in ret:
            if any(ext in result for ext in extensionsToCheck):
                filtered.append(result)

        return filtered

    def find_episode(self, showname, season, episodenum):
        """
        Find the file path for the requested episode.
        :param showname: The name of the show
        :param season: The season number of the episode
        :param episodenum: The episode number within the season of the episode
        :return: The file path for the episode requested, or None if the episode was not found
        :rtype: str
        """
        episodes = self.list_episode_paths(showname, season)
        if episodes is None:
            print "Season %d not found for show %s" % (season, showname)
            return None
        candidates = filter(lambda x: mediautlils.episodenumber(x) == episodenum, episodes)
        if len(candidates) > 0:
            return candidates[0]
        return None

    def find_show(self, query):
        """
        Find a show in the library that most closely matches the given query, using a fuzzy string match.
        :param query: The guess for the show name
        :return: The name of the show in the library that most closely matches the given query
        :rtype : str
        """
        results = process.extract(query, self.list_shows(), limit=1)
        return results[0][0]

    def index_search(self, show_name, season_num, episode_num):
        """
        Find a specific episode for a show and its index in the list in all of the episodes for that show.
        :param show_name: The name of the show
        :param season_num: The season number of the episode
        :param episode_num: The episode number within the season of the episode.
        :return: The index of the path for the requested episode int the list of episodes and the list of episodes
        for the show.
        :rtype: (int, list[str])
        """
        episode = self.find_episode(show_name, season_num, episode_num)
        episode_list = self.list_episode_paths(show_name)
        return episode_list.index(episode), episode_list


def main():
    volumes = ["/Volumes/First", "/Volumes/Second", "/Users/adrian"]
    # volumes = ["testFolderStructure", "/cygdrive/k"]

    library = MediaLibrary(volumes)

    # List all of the shows the library has available
    shows = library.list_shows()
    print "The Library has shows:"
    for show in shows:
        print show

    print "\n"

    # List all of the movies in the library
    movies = library.list_movies()
    print "The Library has movies:"
    for movie in movies:
        print movie

    print "\n"

    # List all of the seasons for every show in the library, and their episodes
    for show in shows:
        seasons = library.list_seasons(show)
        episodes = library.list_episodes(show)
        episode_paths = library.list_episode_paths(show)
        print "%s has seasons:" % show
        for season in seasons:
            print "\t" + season
            snum = mediautlils.seasonnumber(season)
            season_episodes = filter(lambda x: mediautlils.seasonnumber(x) == snum, episodes)
            for episode in season_episodes:
                epnum = mediautlils.episodenumber(episode)
                index = episodes.index(episode)
                print "\t\tEpisode %d, index %d: %s -> %s" % (epnum, index, episode, episode_paths[index])
        print "\n"

    print "\n"

    # # List all of the movie paths in the library
    movie_paths = library.list_movie_paths()
    print "Movies in Library:\n"
    for movie in movies:
        print "%s -> %s" % (movie, library.movie_path(movie))


if __name__ == "__main__":
    main()
