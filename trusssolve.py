import sys
from node import node
from ele import ele
import turtle
import numpy as np
import math
import copy
import pyautogui
import time
import csv
import os

node_file = sys.argv[1] 
ele_file = sys.argv[2]


class truss:
    node_list = []
    ele_list = []
    dis_list = []
    f_list = []
    GK = []

    def __init__(self):

        with open(node_file) as csvfile1:
            reader = csv.reader(csvfile1)
            for row in reader:
                num = int(row[0])
                pos_x = float(row[1])
                pos_y = float(row[2])
                dis_x = np.nan if row[3] == 'nan' else float(row[3])
                dis_y = np.nan if row[4] == 'nan' else float(row[4])
                f_x = float(row[5])
                f_y = float(row[6])
                temp1 = node(num, pos_x, pos_y, dis_x, dis_y, f_x, f_y)
                self.node_list.append(temp1)

        with open(ele_file) as csvfile2:
            reader = csv.reader(csvfile2)
            for row in reader:
                num = int(row[0])
                length = float(row[1])
                area = float(row[2])
                ym = float(row[3])
                theta = math.pi * float(row[4][3:])
                node_a = self.node_list[int(row[5]) - 1]
                node_b = self.node_list[int(row[6]) - 1]
                temp2 = ele(num, length, area, ym, theta, node_a, node_b)
                self.ele_list.append(temp2)


    def globalstiff(self):
        # dimension of global matrix
        dim = 2 * len(self.node_list)
        eles = self.ele_list
        # generate and store the element-wise stiffness matrices

        GK = np.zeros((dim, dim))

        for e in eles:
            i = 2 * e.node_a.num - 2
            j = 2 * e.node_a.num - 1
            k = 2 * e.node_b.num - 2
            l = 2 * e.node_b.num - 1
            e_stiff = e.stiff()

            index = [i, j, k, l]
            index2d = [(a, b) for a in index for b in index]
            d = {i: 0, j: 1, k: 2, l: 3}
            for p, q in index2d:
                GK[p][q] = GK[p][q] + e_stiff[d[p]][d[q]]
        self.GK = GK

    def solve(self):
        # generate global matrix by calling globalstiff method
        self.globalstiff()

        dis_list = []
        for n in self.node_list:
            dis_list.append(n.dis_x)
            dis_list.append(n.dis_y)

        dis = np.array(dis_list)

        f_list = []
        for n in self.node_list:
            f_list.append(n.f_x)
            f_list.append(n.f_y)

        f = np.array(f_list)

        #check for undetermined values in dis and create linear eqns

        GK_dis =  copy.deepcopy(self.GK)
        f_dis =  copy.deepcopy(f)

        #get a list of rows to remove
        del_row = []

        index_list = list(range(0,2*len(self.node_list)))
        for i in range(0,2*len(self.node_list)):
            if not np.isnan(dis_list[i]):
                del_row.append(i)
                index_list.remove(i)

        #remove the rows that have displacement given
        GK_dis = np.delete(GK_dis,del_row,0)
        f_dis = np.delete(f_dis,del_row,0)

        #before deleting the columns we subratct these from force vector
        for i in del_row:
            f_dis = f_dis - dis_list[i] * GK_dis[:,i]

        #delete the columns that are due to the displacements that are determined
        GK_dis = np.delete(GK_dis,del_row,1)   

        ans_dis = np.linalg.solve(GK_dis, f_dis)

        for i in range(0, len(ans_dis)):
            dis[index_list[i]] = ans_dis[i]
        self.dis_list = dis

        ans_force = np.dot(self.GK, dis)
        self.force_list = ans_force

        k = 0
        for i in self.node_list:
            i.dis_x = self.dis_list[k]
            k = k + 1
            i.dis_y = self.dis_list[k]
            k = k + 1

        #print(self.dis_list)
        #print(self.force_list)

    def visualize(self, height=560, width=1300, grid=12, speed=7, delay=2):
        try:
            width, height = pyautogui.size()
        except:
            None

        turtle.title("Visualization")
        turtle.setup(width, height)
        turtle.bgcolor("black")
        ratio = height / width
        turtle.setworldcoordinates(-2, -2 * ratio, grid, ratio * grid)

        t = turtle.Turtle()
        t.speed(speed)
        t.hideturtle()
        t.pensize(5)
        t.pencolor("blue")

        for ele in self.ele_list:
            t.goto(ele.node_a.pos_x, ele.node_a.pos_y)
            t.pendown()
            t.goto(ele.node_b.pos_x, ele.node_b.pos_y)
            t.penup()

        t.speed(0)
        for node in self.node_list:
            t.penup()
            t.goto(node.pos_x, node.pos_y)
            t.pendown()
            t.dot(15, "red")

        t.penup()
        t.goto((ele.node_a.pos_x + ele.node_a.dis_x), (ele.node_a.pos_y + ele.node_a.dis_y))
        t.pendown()

        # def fun():
        #    return None 
        # turtle.onclick(fun, btn=1, add=None)
        time.sleep(delay)

        t.speed(speed)
        # after solving
        t.pencolor("green")
        for ele in self.ele_list:
            t.goto((ele.node_a.pos_x + ele.node_a.dis_x), (ele.node_a.pos_y + ele.node_a.dis_y))
            t.pendown()
            t.goto((ele.node_b.pos_x + ele.node_b.dis_x), (ele.node_b.pos_y + ele.node_b.dis_y))
            t.penup()

        t.speed(0)
        for node in self.node_list:
            t.penup()
            t.goto((node.pos_x + node.dis_x), (node.pos_y + node.dis_y))
            t.pendown()
            t.dot(15, "yellow")
        turtle.Screen().exitonclick()

    def writeoutput(self):
        with open('./csv_files/output.csv' , 'w') as csvfile3:
            writer = csv.writer(csvfile3)
            writer.writerow(['num','pos_x','pos_y', 'dis_x','dis_y',  'f_x', 'f_y'])
            for node in self.node_list:
                writer.writerow(node.value())
            writer.writerow(['num', 'length' , 'area' , 'ym', 'theta', 'node_a' , 'node_b'])
            for ele in self.ele_list:
                writer.writerow(ele.value())




truss1 = truss()
truss1.solve()
truss1.writeoutput()
truss1.visualize()
