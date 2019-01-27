import numpy as np
import matplotlib.pyplot as plt
import sys
import copy
import time
import pandas as pd
from matplotlib.colors import ListedColormap 
import networkx as nx
# アニメーション用
import matplotlib.pyplot as plt
import matplotlib.animation as animation


def checkConnectedCells(cells):
    height, width = cells.shape
    ConnectionList = []
    for y in range(height):
        for x in range(width):
            try:
                if cells[y][x]==cells[y+1][x] and cells[y][x]==cells[y+2][x] and cells[y][x] != -1:
                    ConnectionList.append({"coordinate":[(y,x),(y+1,x),(y+2,x)],"value":cells[y,x],"kind":"vert"})
            except:pass #index out of range
            try:
                if cells[y][x]==cells[y][x+1] and cells[y][x]==cells[y][x+2] and cells[y][x] != -1:
                    ConnectionList.append({"coordinate":[(y,x),(y,x+1),(y,x+2)],"value":cells[y,x],"kind":"hori"})
            except:pass #index out of range
    return ConnectionList

def CheckConnection(combo1,combo2):
    """
    2集合の最小マンハッタン距離を調べる
    """
    min_distance = WIDTH_SIZE+HEIGHT_SIZE
    for i in range(len(combo1)):
        y1,x1 = combo1[i]
        for j in range(len(combo2)):
            y2,x2 = combo2[j]
            dist = np.abs(x1-x2)+np.abs(y1-y2)
            if min_distance > dist:
                min_distance = dist
        if min_distance <= 1:
            return True
    return False


def countCombo(connections):
    """
    connectionListから、そのときのコンボ数を計算する。
    xxx
    xoo
    xoo
    みたいなものは、連結しているので1コンボ
    """
    global KIND_NUM
    combocount = 0
    for k in range(KIND_NUM):
        connection_k = [connection["coordinate"] for connection in connections if connection["value"]==k]
        combolist = []
        connection_index = []
        connection_pairs = [] 
        for i in range(len(connection_k)):
            for j in range(i+1,len(connection_k)):
                if CheckConnection(connection_k[i],connection_k[j]):
                   connection_pairs.append([i,j]) 
        # networkxを使って検出
        G = nx.DiGraph()  # 有向グラフ (Directed Graph)  
        G.add_nodes_from([i for i in range(len(connection_k))]) #頂点の追加
        G.add_edges_from(connection_pairs) #ペアの追加
        G = nx.to_undirected(G)
        nx.draw_networkx(G)
        for g in nx.connected_components(G):
            connection_index.append(list(g))
        # print(connection_index)
        combocount += len(connection_index)
    return combocount

def dropCells(cells):
    height, width = cells.shape
    droppedcells = copy.deepcopy(cells)
    while(1): #落とせるdropがなくなるまで
        count = 0
        for x in range(width):
            for y in range(height-1,0,-1):#下から走査
                if cells[y,x]==-1 and cells[y-1,x]!=-1:
                    # 入れ替え
                    temp = droppedcells[y-1,x]
                    droppedcells[y-1,x] = droppedcells[y,x]
                    droppedcells[y,x] = temp
                    count += 1
        # print("result:{}".format(count))#debug
        cells = copy.deepcopy(droppedcells)
        # display(cells) debug
        if count == 0:
            break   
        # time.sleep(0.5)
    return cells

def fillCells(cells):
    # 空きセルを埋める
    global KIND_NUM
    height, width = cells.shape
    for y in range(height):
        for x in range(width):
            if cells[y,x] == -1:
                cells[y,x] = np.random.randint(low=0, high=KIND_NUM)
    return cells

def display(cells):
    global HEIGHT_SIZE
    global WIDTH_SIZE
    for y in range(HEIGHT_SIZE):
        for x in range(WIDTH_SIZE):
            sys.stdout.write("{:3d}".format(cells[y][x]))
            sys.stdout.flush()
        sys.stdout.write("\n")
    sys.stdout.write("\n")

def PazzleSimulator(anime=False,disp=True):
    """
    初期値でどのくらいコンボする？
    """
    #black pink green blue red yellow purple
    colorList = ["#444444",
             "#fd79a8","#44bd32","#3742fa","#e84118","yellow","purple",
             "#ecf0f1"]
    # セルの初期化
    cells = np.random.randint(0,KIND_NUM,size=(HEIGHT_SIZE,WIDTH_SIZE))
    # cells = np.array([
    #             [  2,  0,  0,  0,  0,  1,  2],
    #             [  1,  2,  2,  1,  0,  1,  0],
    #             [  2,  2,  1,  1,  2,  1,  1],
    #             [  1,  2,  1,  0,  2,  2,  1],
    #             [  1,  0,  1,  0,  0,  2,  1],
    #             [  1,  1,  1,  0,  2,  2,  0]
    #             ])
    img_count = 0
    if anime:
        fig = plt.figure(figsize=(WIDTH_SIZE, HEIGHT_SIZE))
        a = cells.max()
        b = cells.min()
        plt.pcolor(cells,cmap=ListedColormap(colorList[b+1:a+2]))
        plt.gca().invert_yaxis()
        plt.title("COMBO")
        plt.savefig("pazfigure/{}.png".format(img_count))
        img_count += 1
        
    combo = 0
    while True:     # 落ちコンの考慮
        cells = fillCells(cells)
        if disp:
            print("-------FILLING--------")
            display(cells)
        if anime:
            a = cells.max()
            b = cells.min()
            fig = plt.figure(figsize=(WIDTH_SIZE, HEIGHT_SIZE))
            plt.pcolor(cells, cmap=ListedColormap(colorList[b+1:a+2]))
            plt.gca().invert_yaxis()
            plt.title("{} COMBO".format(combo))
            plt.savefig("pazfigure/{}.png".format(img_count))
            img_count += 1
        connections = checkConnectedCells(cells)
        if len(connections) == 0:
            # sys.stdout.write("{:4d}".format(combo))
            # sys.stdout.flush()
            break    
        while True: # 落としの考慮
            connections = checkConnectedCells(cells)
            if len(connections) == 0:
                break
            combo += countCombo(connections)
            # ドロップの削除
            for connection in connections:
                for y,x in connection["coordinate"]:
                    cells[y,x] = -1
            if disp:
                print("-------DELETE--------")
                display(cells)
            if anime:
                a = cells.max()
                b = cells.min()
                fig = plt.figure(figsize=(WIDTH_SIZE, HEIGHT_SIZE))
                plt.pcolor(cells,cmap=ListedColormap(colorList[b+1:a+2]))
                plt.gca().invert_yaxis()
                plt.title("{} COMBO".format(combo))
                plt.savefig("pazfigure/{}.png".format(img_count))
                img_count += 1


            # ドロップを落とす
            cells = dropCells(cells)
            if disp:
                print("-------DROP--------")
                display(cells)
            if anime:
                a = cells.max()
                b = cells.min()
                fig = plt.figure(figsize=(WIDTH_SIZE, HEIGHT_SIZE))
                plt.pcolor(cells, cmap=ListedColormap(colorList[b+1:a+2]))
                plt.gca().invert_yaxis()
                plt.title("{} COMBO".format(combo))
                plt.savefig("pazfigure/{}.png".format(img_count))
                img_count += 1
    #------ここまで while--------------#
    if disp:
        print("-------RESULT--------")
        display(cells)
        print("COMBO : {}".format(combo))
    if anime:
        a = cells.max()
        b = cells.min()
        fig = plt.figure(figsize=(WIDTH_SIZE, HEIGHT_SIZE))
        plt.pcolor(cells, cmap=ListedColormap(colorList[b+1:a+2]))
        plt.gca().invert_yaxis()
        plt.title("{} COMBO".format(combo))
        plt.savefig("pazfigure/{}.png".format(img_count))
        img_count += 1
    sys.stdout.write("{:4d}".format(combo))
    sys.stdout.flush()
    return combo
    

if __name__ == "__main__":
    HEIGHT_SIZE = 6
    WIDTH_SIZE = 7
    KIND_NUM = 6
    combo = PazzleSimulator(anime=True, disp=True)
    """
    流れ
    1. checkConnectionCellsで、盤面上に3つ連結しているやつらを抜き出す
    2. 3つ連結しているセルで、最小のマンハッタン距離が0(結合) or 1(隣接)になる組み合わせのインデックスを貼る
    3. indexから、グラフ構造を抽出(networkxにて)し、マージする
    """