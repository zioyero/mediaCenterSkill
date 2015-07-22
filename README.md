# Media Center Skills for Alexa

This is the repository for the Alexa Skill that allows you to control your Mac VLC-based media center using an [Amazon Echo](http://smile.amazon.com/Amazon-SK705DI-Echo/dp/B00X4WHP5E/ref=sr_1_1?ie=UTF8&qid=1437287015&sr=8-1&keywords=echo&pebp=1437287018130&perid=1XFWKH7X88J9PHY3F1G5). 

It allows for interaction such as "Alexa, tell **kickass** to play **Elements by Lindsey Stirling**" which will then query YouTube for [the video](https://www.youtube.com/watch?v=sf6LD2B_kDQ) and tell VLC to play it on your computer.

There is also a skill for querying your own media library if the files are organized well. You can find projects like [Sickbeard]() or [Sonarr]() which can organize your library in a way that this skill will understand.

### Intent Schema and Interaction Model

The intent schema and interaction models found here are the ones that I've been using that work pretty well. There were issues with overloading the same invocation name, so we had to add more in order to handle each request better. The ones that I used were:

|Invocation Name|Interaction Model|Feature|
|---------------|-----------------|-------|
|kickass|"tell **kickass** to play {youtube video query}"|Plays YouTube videos on VLC|
|kickass|"tell **kickass** to shuffle {youtube playlist query}"|Plays a YouTube playlist through VLC|
|the media center|"tell **the media center** to stop", "tell **the media center** to resume"|Controls playback commands. Accepts: stop, pause, resume, next, skip, go back|
|the library|"tell **the library** to shuffle {tv show name}"|Finds a tv show in your local library and plays a random episodes, also queues up others|
|plex|"tell **plex** to play {show} season {n} episode {m}"|Finds a specific episiode of a show in your library and plays it through VLC|



I wrote a blog post about it which you can [find here](https://zioyero.github.io/amazon/echo,/vlc,/home/automation/2015/07/18/mediaCenterRelaySkills.html). If anyone actually uses this code I will improve this readme.