from splinter import Browser
from bs4 import BeautifulSoup
from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.firefox.options import Options
import os
import numpy as np 


def init_browser():
    opts = Options()
    opts.set_headless()
    assert opts.headless
    browser = Firefox(executable_path = "C:/Users/Naveen/Desktop/music_making AI/geckodriver.exe", options = opts)
    return(browser)


#returns a tuple consisting of links to guitar chord pages, and a list of every link on the page. Second tuple element is just for debugging purposes
def link_list(chord_page):
    browser = init_browser()
    #link to page on ultimate-guitar.com which contains links to guitar chord pages
    browser.get(chord_page)

    # html.parser has almost the same speed as xlm, and is almost as accurate as html5lib, so its a good middle ground
    html = browser.page_source
    soup_parsed = BeautifulSoup(html, 'html.parser')

    body = soup_parsed.find("body").find('main').find_all('section')
    raw_links = body[2].find_all('a')
    links = []
    for link in raw_links:
        links.append(link.attrs['href'])

    ###########    This will most likely need to be regularly updated. It is a list of key words that links to chords do not have
    bad_words = ["explore?type[]", 'artist']
    ###############

    good_links = [link for link in links if not any(bad_word in link for bad_word in bad_words)]
    try:
        filters = body[0].find('article').find('nav').find_all('a')
        key = filters[1].text
        browser.quit()       
        return(key, good_links)
    except:
        print("Could not find keys")
        browser.close()
        return(good_links)


#implicitly assumes firefox geko is in the same directory as the function. Returns a Browser object

#should return a tuple consisting of the artist, the song name, and the chords
def chord_scraper(link):
    browser = init_browser()
    try:
        browser.get(link)
    except:
        print("error: link, {link},  not initializing properly")

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    try:
        body = soup.find('body').find('main').find('pre')
    except:
        print("html error: cannot return body with current configurations")
    try:
        chords = [i.text for i in body.find_all('span')]
        just_chords = [i for i in chords if len(i) < 8 and '\r\n' not in i]
    except:
        print("chords not being pinpointed properly")

    header = soup.find('body').find('main').find_all('header')
    artist = header[2].find('a').text
    title = header[2].find('h1').text

    values = (title, artist, just_chords)

    browser.close()

    return(values)



#to be written in separate file


