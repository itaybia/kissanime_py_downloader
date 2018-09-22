# kissanime_py_downloader
Extract all download links for a series from a kissanime.ru series page through RapidVideo.

As the use of RapidVideo on kissanime.ru doesn't require you to enter a captcha, using RapidVideo instead of the other servers on kissanime provides an easy, hassle-free way to get all links for a series.

The extracted links will be written to files for easy use with various downloaders such as IDM, DownThemAll, wget, aria2c, Chrono Download Manager, TabSave.

## How to use
1. Download the ChromeDriver from: http://chromedriver.chromium.org/downloads
2. If on Windows, download the precompiled [executable](https://github.com/itaybia/kissanime_py_downloader/releases/download/1.0.1/url_fetcher.exe). Or use the python script directly as in (3)
3. If you want to use the python 2.7 script directly, then download the "url_fetcher.py" python script and install all the required packages:
    * pip install selenium
    * pip install beautifulsoup4
4. Register a user on kissanime.ru
5. Open the page of the series you want to download and copy its URL
6. In the command line run:
    * For executable: url_fetcher.exe -user < USER NAME > -pass < PASSWORD > -url < SERIES PAGE URL from step 5 > -first < FIRST EPISODE TO DOWNLOAD > -last < LAST EPISODE TO DOWNLOAD > -rename -out < OUTPUT FOLDER >
    * For python: python url_fetcher.py -user < USER NAME > -pass < PASSWORD > -url < SERIES PAGE URL from step 5 > -first < FIRST EPISODE TO DOWNLOAD > -last < LAST EPISODE TO DOWNLOAD > -rename -out < OUTPUT FOLDER >
    * Example: url_fetcher.exe -user some_user -pass 1234 -url http://kissanime.ru/Anime/Wolf-s-Rain -first 5 -last 15 -rename -out C:\Downloads
    * **-last** is not mandatory. If not given, all episodes after first will be downloaded.
    * **-rename** is not mandatory. If given, it changes the links to have the downloaded files have the names as in the series page.
    * **-out** is not mandatory. If given, it will create the files containing the links in the folder given. if not given, they will be created in the same folder as the folder you are running the command from.
7. The script will output the links for the highest possible resolution for an episode (1080p --> 720p --> 480p)
8. Two files will be created in the output folder:
    * download_links.txt - Simple text file containing the RapidVideo links to download.
    * download_links.html - An HTML web page containing the RapidVideo links to download.
9. Download the files through the links by either:
    * Opening the html page in your browser and directly clicking the links to start downloading
    * Loading the files to various downloaders such as IDM, DownThemAll, wget, aria2c, Chrono Download Manager, TabSave ETC.
