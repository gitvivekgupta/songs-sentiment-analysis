
# coding: utf-8

# Author: Arnav Dubey.
#   Script to scrape lyrics of songs from lyrics.com

import requests as rq
import pandas as pd
from bs4 import BeautifulSoup as bsp, SoupStrainer as ss
import re
import codecs as cd
import lyrics_scraper as lys
from collections import Counter as ctr

# URL to the website that the methods scrape data from
base_url = 'http://www.lyrics.com'
# name of the artist being used
artist_name = 'Adele'
# full address of the url
full_address = base_url + '/artist/' + artist_name

# method to get the BeautifulSoup object given the 
# axcepts artist name as a parameter.
def get_page(artist_name):
    artist_name = artist_name.replace(' ', '%20')
    base_url = 'http://www.lyrics.com'
    full_address = base_url + '/artist/' + artist_name
    page = rq.get(full_address)
    soup = bsp(page.content, 'html.parser')
    return soup

# method to get the container correspnding to the required content
# accepts the BeautifulSoup object as a parameter
def get_container(soup):
    container = soup.find('div', { "id" : "content-main"})
    return container

# method to get the name of the artist, given the corresponding container
# accepts a BeautifulSoup container as a parameter
def get_artist(container):
    artists = container.findAll('p', attrs={'class': 'artist'})
    artists_name = ''
    for artist in artists:
        artist_name = artist.text
    return artist_name

# method to get the album names given a BeautifulSoup container corresponding to a given artist
def get_album_names(container):
    album_tags = container.findAll('h3', attrs = {'class': 'artist-album-label'})
    album_names = []
    for tag in album_tags:
        album_names.append(tag.text)
    return album_names

# method to get a list of tuples containing the data scraped for an individual artist.
# accepts a list of tuples from the parent method, a list of BeautifulSoup objects 
# containing the releant html for each song. The album_name of the songs, the name of the artist.
# returns a list of tuples with each tuple having the album name, artist name, song name, 
# song duration, and song url. (** Used as a helper method within get_songs_data **)
def generate_songs_data(songs_data, songs_tags, album_name, artist_name):
    i = 0
    song_name = ''
    song_duration = ''
    while(i < len(songs_tags) - 1):
            song_name = songs_tags[i].text
            song_duration = songs_tags[i+1].text
            song_url = songs_tags[i].find('a').get('href')
            i += 2
            songs_data.append((album_name, artist_name, song_name, 
                               song_duration, song_url))
    return songs_data

# returns a list of tuples containing data scraped for individual songs.
# accepts a BeautifulSoup container containing the relavant html.
def get_songs_data(container):
    album_blocks = container.findAll('div', attrs = {'class': 'clearfix'})
    songs_data = []
    artist_name = get_artist(container)
    for block in album_blocks:
        album_tags = block.findAll('h3', attrs = {'class': 'artist-album-label'})
        album_name = ''
        for tag in album_tags:
            album_name = tag.text
        songs_tags = block.findAll('td', attrs = {'class': 'tal qx'})
        songs_data = generate_songs_data(songs_data, songs_tags, 
                                         album_name, artist_name)
    return songs_data


# returns a dataframe containing the complete url for each song
# accepts a dataframe containing the URI's for each song.
def generate_full_url(songs_df):
    base_url = 'http://www.lyrics.com'
    songs_df['Full_URL'] = base_url + songs_df['URI']
    return songs_df

# returns a list of strings with each string representing 
# the lyrics for the particular song that corresponds to 
# the list of urls passed to the method. 
# accepts a list of urls corresponding to the songs for
# which the lyrics is to be scraped.
def get_lyrics(url_list):
    list_lyrics = []
    for url in url_list:
        page = rq.get(url)
        soup = bsp(page.content, 'html.parser')
        container = soup.find('div', { "class" : "lyric clearfix"})
        lyric_tags = container.findAll('pre', attrs = {'id': 'lyric-body-text'})
        for tag in lyric_tags:
            lyric = tag.text
            list_lyrics.append(lyric)
    return list_lyrics


def get_max_word(list_lyrics):
    counts = []
    count_list = []
    for lyric in list_lyrics:
        count_list = ctr(lyric.split()).most_common(3)
        counts.append(count_list)
    return counts