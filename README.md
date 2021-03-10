# spotify-downloader

<b>This simple Python Script allows you to download songs or albums from spotify</b>

<h2>Make sure you have FFmpeg on the same folder as the script file if you are on Linux or Mac</h3>
<p>       Get it from FFmpeg's official site (www.ffmpeg.org)
   </p>    
       
<h1>usage</h1>
<h3>open terminal and write this command</h3>
<pre>pip install -r requirements.txt</pre>
<h3>open @BotFather(t.me/BotFather) bot in your telegram and create your new bot and add your token here in main.py
</h3>
<pre>token = 'token bot'</pre>
<h3>Now go to www.docs.genius.com and get your Genius API token and add it to this line to detail.py</h3>
<pre> genius = lyricsgenius.Genius(' genius api token  ') </pre>

<h3>After that go to www.developer.spotify.com and get your CLIENT ID & CLIENT SECRET and add them to this lines in youtube.py </h3>
<pre>spotifyy = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(client_id='client id spotify',
                                                        client_secret='client secret spotify'))</pre>

<b>now run the Script ;)</b>
