__author__ = 'adrian'

import re


def episodenumber(filename):
    """
    Get the episode number from an episode name or full path using regex.
    :param episode: The name of the episode file or the full path to the episode
    :return: The episode number contained in the name
    :rtype: int
    """
    match = re.search(
        r'''(?ix)                 # Ignore case (i), and use verbose regex (x)
        (?:                       # non-grouping pattern
          e|x|episode|^           # e or x or episode or start of a line
          )                       # end non-grouping pattern
        \s*                       # 0-or-more whitespaces
        (\d{2})                   # exactly 2 digits
        ''', filename)
    if match:
        return int(match.group(1))


def seasonnumber(filename):
    """
    Get the season number from an episode name or full path using regex.
    :param filename:  The filename that conains a season number
    :return: The season number contained in the name
    :rtype: int
    """
    match = re.search(r"(?ix)(?:s|season|^)\s*(\d{2})", filename, re.I)
    if match:
        return int(match.group(1))


def main():
    tests = (
        'Series Name s01e01.avi',
        'Series Name 1x01.avi',
        'Series Name episode 01.avi',
        '01 Episode Title.avi',
        'Season 12/Show.S12E23.avi',
        'Season 12'
        )
    for test in tests:
        if seasonnumber(test) is not None:
            season = seasonnumber(test)
        else:
            season = -1
        if episodenumber(test) is not None:
            episode = episodenumber(test)
        else:
            episode = -1
        print "%s -> Season %d, Episode %d" % (test, season, episode)


if __name__ == "__main__":
    main()
