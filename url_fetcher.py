import os
import re
import urllib2
from time import sleep

import argparse
from bs4 import BeautifulSoup
from os.path import join
from selenium import webdriver

LOGIN_PAGE = 'http://kissanime.ru/Login'


def get_download_links_for_url(root_url, min_episode, max_episode, username, password, rename_files, chrome_driver_path):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')    # no GUI. performs faster

    driver = webdriver.Chrome(executable_path=chrome_driver_path, chrome_options=options)

    # go to the login page (login is needed otherwise we won't get the download links in the rapidvideo page
    driver.get(LOGIN_PAGE)
    sleep(5)    # Chrome driver needs 5 seconds to start the browser
    user_element = driver.find_element_by_id('username')
    user_element.send_keys(username)
    user_element = driver.find_element_by_id('password')
    user_element.send_keys(password)
    user_element = driver.find_element_by_id('btnSubmit')
    user_element.click()

    # go to the series page to find all the rapidvideo page URLs inside kissanime
    driver.get(root_url)
    links = []
    td_element = driver.find_elements_by_tag_name('td')
    for element in td_element:
        try:
            episode_tag = element.find_element_by_partial_link_text('')
            href = episode_tag.get_attribute('href')
            episode_num_start_index = len(root_url + '/Episode-')
            episode_num_str = href[episode_num_start_index:episode_num_start_index + 3]
            episode_num = int(episode_num_str)
            if episode_num < min_episode or (max_episode and episode_num > max_episode):
                continue
            print 'found link: ' + href
            links.append((href + '&s=rapidvideo', episode_tag.text))
        except Exception as e:
            pass
    links.reverse()
    print links

    # extract the rapidvideo download page from the kissanime page
    rapidvideo_links = []
    for kissanime_rapidvideo_link, episode_text in links:
        try:
            # open the rapidvideo page in kissanime
            driver.get(kissanime_rapidvideo_link)
            element = driver.find_element_by_link_text('CLICK HERE TO DOWNLOAD')
            href = element.get_attribute('href')
            rapidvideo_links.append((href, episode_text))
            print href
        except Exception as e:
            pass

    # find the link to the file with the highest resolution (no need for the login or cookies anymore, so no need for webdriver which is slow)
    download_links = []
    for rapidvideo_link, episode_text in rapidvideo_links:
        try:
            headers = {'User-Agent': 'Mozilla/5.01'}
            req = urllib2.Request(rapidvideo_link, None, headers)
            r = urllib2.urlopen(req).read()
            soup = BeautifulSoup(r, 'html.parser')
            divResult = soup.find_all('div', { "class" : "video" })
            for div in divResult:
                aResult = div.find_all('a')
                highest_res = 0
                highest_href = None
                for a in aResult:
                    text = a.text
                    href = a.attrs.get('href')
                    if 'Download 480p' in text and highest_res < 480:
                        highest_href = href
                        highest_res = 480
                    if 'Download 720p' in text and highest_res < 720:
                        highest_href = href
                        highest_res = 720
                    if 'Download 1080p' in text and highest_res < 1080:
                        highest_href = href
                        highest_res = 1080
                if highest_res:
                    print 'highest res is: ' + str(highest_res) + '. link: ' + highest_href
                    if rename_files:
                        name_index_in_href = highest_href.find('?name=')
                        if name_index_in_href != -1:
                            file_name = episode_text + ' ' + str(highest_res) + 'p.mp4'
                            file_name = re.sub(r'[^A-Za-z0-9-._~()!*:@,; ]', '', file_name).replace(' ', '%20')
                            highest_href = highest_href[:name_index_in_href + 6] + file_name
                    download_links.append((highest_href, episode_text))
                    break
        except Exception as e:
            pass

    driver.close()

    return download_links


def write_to_text_file(links_and_episodes, links_folder):
    with open(join(links_folder, 'download_links.txt'), mode='w') as links_file:
        for link, episode_name in links_and_episodes:
            links_file.write(link + '\n')


def write_to_html_file(links_and_episodes, links_folder):
    with open(join(links_folder, 'download_links.html'), mode='w') as links_file:
        links_file.write('<!DOCTYPE html>\n<html>\n<body link="blue">\n')
        for link, episode_name in links_and_episodes:
            links_file.write('<p><a href=\"' + link + '\">' + episode_name + '</a></p>\n')
        links_file.write('</body>\n</html>\n')


parser = argparse.ArgumentParser()

parser.add_argument("-out", "--output_folder", help="folder to create teh links files in. default is in the executable's folder")
parser.add_argument("-chrome_drv", "--chrome_driver_path", help="absolute path of the chrome driver executable file")
parser.add_argument("-url", "--series_url", help="series URL")
parser.add_argument("-user", "--user_name", help="kissanime site user name")
parser.add_argument("-pass", "--password", help="kissanime site password")
parser.add_argument("-first", "--first_index", help="First Episode to download", type=int)
parser.add_argument("-last", "--last_index", help="Last Episode to download. 0 or no value if no upper limit", type=int)
parser.add_argument("-rename", "--rename_files", help="when given, the downloaded files will be renamed as in the series url page", action='store_true')

args = parser.parse_args()

print( " output_folder {}\n chrome_driver_path {}\n series_url {}\n user_name {}\n password {}\n first_index {}\n last_index {}\n rename_files {}".format(
        args.output_folder,
        args.chrome_driver_path,
        args.series_url,
        args.user_name,
        args.password,
        args.first_index,
        args.last_index,
        args.rename_files
        ))

if args.first_index < 1:
    print "first_index must be a number of an episode to download"
    exit(1)
if args.last_index < 0:
    print "last_index must be a number of an episode to download, or 0 to download all from first_index and up"
    exit(1)
if not args.user_name or not args.password or not args.series_url:
    print "user_name, password, and series_url can't be empty"
    exit(1)
if not os.path.exists(args.chrome_driver_path):
    print "chrome_driver_path must be the path to the existing chrome driver executable file. if not downloaded, please download from http://chromedriver.chromium.org/downloads"
    exit(1)

download_links_and_episodes = get_download_links_for_url(args.series_url, args.first_index, args.last_index, args.user_name, args.password, args.rename_files, args.chrome_driver_path)
print download_links_and_episodes
links_folder_path = os.path.normpath(args.output_folder if args.output_folder else os.getcwd())
if not os.path.exists(links_folder_path):
    os.makedirs(links_folder_path)
write_to_text_file(download_links_and_episodes, links_folder_path)
write_to_html_file(download_links_and_episodes, links_folder_path)

print "download links written to: " + links_folder_path
