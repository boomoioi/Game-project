from csv import reader
from os import walk
import pygame

def import_csv_layout(path):
    terrain_map = []
    with open(path) as level_map:
        layout = reader(level_map, delimiter = ',')
        for row in layout:
            terrain_map.append(list(row))
        return terrain_map

def import_folder(path):
    surface_list = []
    for _,__,img_files in walk(path):
        for image in img_files:
            full_path = path + '/' + image
            image_surf = pygame.image.load(full_path).convert_alpha()
            surface_list.append(image_surf)
    return surface_list

def read_file(name):
    file1 = open(f"save/{name}.txt","r")
    upgrade, kill = file1.read().split('\n')
    boss, mon = kill.split()
    boss = int(boss)
    mon = int(mon)
    list = upgrade.split()
    for item in range(len(list)):
        list[item] = int(list[item])
    return list, boss, mon

def write_file(name, mul, boss, mon):
    to_write = ""
    for value in mul:
        to_write += str(int(value)) + ' '
    
    to_write += '\n'
    to_write += str(int(boss)) + ' ' + str(int(mon))
    f = open(f"save/{name}.txt", "w")
    f.write(to_write)
    f.close()

def write_high_score(name, score):
    f = open("high_score.txt", "r")
    read = f.read().split('\n')
    dict = {}
    if read:
        for player in read:
            list = player.split()
            dict.update({list[0]:int(list[1])})

    if name not in dict:
        dict.update({name:score})
    else:
        dict[name] = int(score)
    f.close
    to_write = ''
    f = open("high_score.txt", "w")
    for key, value in dict.items():
        to_write += key + ' ' + str(value) + '\n'
    to_write = to_write[:-1]
    f.write(to_write)
    f.close()

def read_score():
    f = open("high_score.txt", "r")
    read = f.read().split('\n')
    dict = {}
    if read:
        for player in read:
            list = player.split()
            dict.update({list[0]:int(list[1])})

    return dict
