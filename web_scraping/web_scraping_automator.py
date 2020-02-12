from guitar_chord_web_scraper import *
import pickle
import os


temp_data = {}
base_link = "https://www.ultimate-guitar.com/explore?type[]=Chords&tonality[]="



keynums = [i for i in range(1,31)]
temp_data = {}

#finds top songs for every key, and returns a dictionary of key with a list of links to chord pages
for key in keynums:
    main_page = f'{base_link}{key}'
    key_links = link_list(main_page)
    print(key)
    try:
        song_list = {}
        for link in key_links[1]:
            chord_tuple = chord_scraper(link)
            title = f'{chord_tuple[0]} by {chord_tuple[1]}'
            print(title)
            song_list[title] = chord_tuple[2]
        temp_data[key_links[0]] = song_list
    except:
        temp_data["blank"] = key_links[1]

#loops through all the links in temp_data
'''
for i in temp_data:
    song_list = {}
    for link in temp_data[i]:
        chord_tuple = chord_scraper(link)
        title = f'{chord_tuple[0]} by {chord_tuple[1]}'
        song_list[title] = chord_tuple[2]
    temp_data[i] = song_list
'''





data_file = open(os.getcwd() + '/web_scraping/chord_data.pkl', 'wb')
pickle.dump(temp_data, data_file)
data_file.close()
