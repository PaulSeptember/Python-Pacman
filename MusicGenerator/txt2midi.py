import numpy as np
from mido import Message, MidiFile, MidiTrack, MetaMessage
from random import *
import random

char2note = {
    '1':48,'!':49,'2':50,'@':51,'3':52,'4':53,'$':54,'5':55,'%':56,'6':57,
    '^':58,'7':59,'8':60,'*':61,'9':62,'(':63,'0':64,'q':65,'Q':66,'w':67,
    'W':68,'e':69,'E':70,'r':71,'t':72,'T':73,'y':74,'Y':75,'u':76,'i':77,
    'I':78,'o':79,'O':80,'p':81,'P':82,'a':83,'s':84,'S':85,'d':86,'D':87,
    'f':88,'g':89,'G':90,'h':91,'H':92,'j':93,'J':94,'k':95,'l':96,'L':97,
    'z':98,'Z':99,'x':100,'c':101,'C':102,'v':103,'V':104,'b':105,'B':106,
    'n':107,'m':108, '&':58, '#':51
}

def txt2notes(txt):
    txt = txt.replace(' [', '\n \n[')
    txt = txt.replace('] ', ']\n \n')
    txt_list = txt.split('\n')
    txt_final = list()
    for i in range(len(txt_list)):
        #print txt_list[i]
        if txt_list[i] == ' ':
            txt_final.append(txt_list[i])
        elif " " in txt_list[i] and  "]" in txt_list[i] and "[" in txt_list[i]:
            txt_cord = txt_list[i].replace('[', '\n[')
            txt_cord = txt_cord.replace(']', ']\n')
            txt_cor_list = txt_cord.split('\n')
            for i in range(len(txt_cor_list)):
                if " " in txt_cor_list[i] and  "]" not in txt_cor_list[i] and "[" not in txt_cor_list[i]:
                    in_cord = txt_cor_list[i].split(' ')
                    for i in range(len(in_cord)):
                        txt_final.append(in_cord[i])
                else:
                    txt_final.append(txt_cor_list[i])
        else:
            txt_final.append(txt_list[i])
    return txt_final


mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)
program = randint(0, 79)
time = randint(40, 100)
track.append(Message('program_change', program=program))

f = open('text6.txt', 'r')
txt = f.read()

txt_list = txt.replace('\n', ' ')
txt_list = txt2notes(txt)
for i in range(len(txt_list)):
    if  len(txt_list[i]) > 1:
        cord = txt_list[i]
        if cord.startswith('[') and cord.endswith(']') and " " not in cord:
            cord = cord.replace('[', '')
            cord = cord.replace(']', '')
            for k in range(0, len(cord)):
                track.append(Message('note_on', note=char2note[cord[k]], velocity=62))
            for k in range(0, len(cord)):
                track.append(Message('note_off', note=char2note[cord[k]], velocity=0, time=time*2))
        elif cord.startswith('[') and cord.endswith(']') and " " in cord:
            cord = cord.replace('[', '')
            cord = cord.replace(']', '')
            cord = cord.replace(' ', '')
            for k in range(0, len(cord)):
                track.append(Message('note_on', note=char2note[cord[k]], velocity=100, time=time/4))
                track.append(Message('note_off', note=char2note[cord[k]], velocity=0, time=time))
        else:
            for k in range(0, len(cord)):
                if cord[k] in char2note:
                    track.append(Message('note_on', note=char2note[cord[k]], velocity=100, time=time*2))
                    track.append(Message('note_off', note=char2note[cord[k]], velocity=0, time=time*2))
                elif cord[k] == ' ':
                    track.append(Message('note_on', note=0, velocity=0, time=time))
                elif cord[k] == '|':
                    track.append(Message('note_on', note=0, velocity=0, time=time*2))
    else:
            if txt_list[i] == '|':
                track.append(Message('note_on', note=0, velocity=0, time=time*2))
            elif txt_list[i] == ' ':
                track.append(Message('note_on', note=0, velocity=0, time=time))
            elif txt_list[i] in char2note:
                track.append(Message('note_on', note=char2note[txt_list[i]], velocity=100, time=time))
                track.append(Message('note_off', note=char2note[txt_list[i]], velocity=0, time=time))
mid.save('song6.mid')
