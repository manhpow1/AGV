# -*- coding: utf-8 -*-
class utility:
    def __init__(self):
        x = {}
        max_value = 0
        with open('map.txt', 'r') as f:
            for line in f:
                parts = line.split()
                if parts[0] == 'a':
                    max_value = max(max_value, int(parts[1]), int(parts[2]))
                    i, j, c_i_j = int(parts[1]), int(parts[2]), int(parts[5])
                    x[i,j] = c_i_j
        self.matrix = x
        self.M = max_value
        self.H = 3600

    def getid(self,pos):
        if pos % self.M != 0:
            return pos%23 
        else: 
            return self.M
    
    def findid(self, pos):
        my_list = set()  # Tạo một set mới
        i = self.getid(pos)
        for j in range(1, 24):
            if (i,j) in self.matrix:
                id1 = self.M * (int(pos / self.M) + self.matrix[i, j]) + j
                id2 = self.M * 10 + pos 
                my_list.add(id1)
                my_list.add(id2)
        return my_list

    
