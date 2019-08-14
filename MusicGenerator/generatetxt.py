import numpy as np
from mido import Message, MidiFile, MidiTrack, MetaMessage
from random import *
import random

def sample(h, seed_ix, n):
  x = np.zeros((vocab_size, 1))
  x[seed_ix] = 1
  ixes = []
  for t in xrange(n):
    h = np.tanh(np.dot(Wxh, x) + np.dot(Whh, h) + bh)
    y = np.dot(Why, h) + by
    p = np.exp(y) / np.sum(np.exp(y))
    ix = np.random.choice(range(vocab_size), p=p.ravel())
    x = np.zeros((vocab_size, 1))
    x[ix] = 1
    ixes.append(ix)
  return ixes

model_file  =  open('text300000.dat', 'r')
model =  np.load(model_file)

chars= model['chars']
hprev = np.zeros((100,1))
Wxh=model['Wxh']
Whh=model['Whh']
bh=model['bh']
by=model['by']
Why=model['Why']
vocab_size=model['vocab_size'][0]

char_to_ix = { ch:i for i,ch in enumerate(chars) }
ix_to_char = { i:ch for i,ch in enumerate(chars) }
char2note = {
    '1':48,'!':49,'2':50,'@':51,'3':52,'4':53,'$':54,'5':55,'%':56,'6':57,
    '^':58,'7':59,'8':60,'*':61,'9':62,'(':63,'0':64,'q':65,'Q':66,'w':67,
    'W':68,'e':69,'E':70,'r':71,'t':72,'T':73,'y':74,'Y':75,'u':76,'i':77,
    'I':78,'o':79,'O':80,'p':81,'P':82,'a':83,'s':84,'S':85,'d':86,'D':87,
    'f':88,'g':89,'G':90,'h':91,'H':92,'j':93,'J':94,'k':95,'l':96,'L':97,
    'z':98,'Z':99,'x':100,'c':101,'C':102,'v':103,'V':104,'b':105,'B':106,
    'n':107,'m':108, '&':58, '#':51
}

init_char = random.choice(list(char2note))

sample_ix = sample(hprev, char_to_ix[' '], 10000)

txt = ''.join(ix_to_char[ix] for ix in sample_ix)
txt = init_char + txt
txt = txt.replace('\n', ' ')
txt = txt.replace('  ', ' ')

f = open('Shakespeare20.txt', 'w')
f.write(txt)
