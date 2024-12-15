import streamlit as st
import random
import matplotlib.pyplot as plt

# set variables
xset = range(0,360)
yset = [0,1,2,3,4,5,6]
result = [0]*8
gamecount = 0
gametarget = 0 

# run game 10000 times
while(gamecount < 10000):
        gamecount = gamecount + 1
        # create a 2D(8*17) list, all set to 0
        sadari = [[0]*8 for i in xset]
        
        # create paths
        i = 0
        start = []
        while(i < len(xset)):
                x = random.choice(xset)
                y = random.choice(yset)

                if(sadari[x][y] == 0 and sadari[x][y+1] == 0):
                        sadari[x][y] = sadari[x][y+1] = 1
                        start.append([x,y])
                        i = i + 1

        # start game
        target = gametarget
        idx = len(xset)-1
        while(idx>=0):
                if(sadari[idx][target] == 0):
                        idx = idx - 1
                elif(sadari[idx][target] == 1):
                        if([idx,target] in start):
                                target = target + 1
                                idx = idx - 1
                        else:
                                target = target - 1
                                idx = idx - 1
        result[target] = result[target]+1

# print game results 
print(result)
x = [1,2,3,4,5,6,7,8]
plt.bar(x,result)
for a,b in zip(x, result):
    plt.text(a, b, str(b), ha='center')
plt.show()
