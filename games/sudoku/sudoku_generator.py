import random
import math

class Sudoku:
    def __init__(self, N, K):
        self.N = N
        self.K = K

        self.mat = [[0 for i in range(self.N)] for j in range(self.N)]
        self.SRNd = int(math.sqrt(self.N))
        self.originMat = [[0 for i in range(self.N)] for j in range(self.N)]

    def fillValues(self):
        # Fill the diagonal of SRNd x SRNd matrices
        self.fillDiagonal()

        # Fill remaining blocks
        self.fillRemaining(0, self.SRNd)

        # Remove K digits
        self.removeKDigits()
    
    def fillDiagonal(self):
        # Fill diagonal SRNd x SRNd matrices
        for i in range(0, self.N, self.SRNd):
            self.fillBox(i, i)
    
    def unUsedInBox(self, rowStart, colStart, num):
        # Check if num is already present in the box
        for i in range(self.SRNd):
            for j in range(self.SRNd):
                if self.mat[rowStart + i][colStart + j] == num:
                    return False
        return True
    
    def fillBox(self, row, col):
        # Fill SRNd x SRNd matrix
        for i in range(self.SRNd):
            for j in range(self.SRNd):
                while True:
                    num = random.randint(1, self.N)
                    if self.unUsedInBox(row, col, num):
                        self.mat[row + i][col + j] = num
                        break
                self.mat[row + i][col + j] = num
    
    def checkIfSafe(self, i, j, num):
        # Check if num is already present in the row, col, or box
        return (self.unUsedInRow(i, num) and self.unUsedInCol(j, num) and self.unUsedInBox(i - i % self.SRNd, j - j % self.SRNd, num))
    
    def unUsedInRow(self, i, num):
        # Check if num is already present in the row
        for j in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True
    
    def unUsedInCol(self, j, num):
        # Check if num is already present in the col
        for i in range(self.N):
            if self.mat[i][j] == num:
                return False
        return True
    
    def fillRemaining(self, i, j):
        # End of matrix
        if i == self.N - 1 and j == self.N:
            return True
        
        # Next row
        if j == self.N:
            i += 1
            j = 0
        
        # Skip if already filled
        if self.mat[i][j] != 0:
            return self.fillRemaining(i, j + 1)
        
        # Try all numbers
        for num in range(1, self.N + 1):
            if self.checkIfSafe(i, j, num):
                self.mat[i][j] = num
                if self.fillRemaining(i, j + 1):
                    return True
                self.mat[i][j] = 0
        
        # No solution found
        return False
    
    def removeKDigits(self):
        # We copy the elemnts from mat to originMat
        for i in range(self.N):
            for j in range(self.N):
                self.originMat[i][j] = self.mat[i][j]

        count = self.K
        while count != 0:
            i = random.randint(0, self.N - 1)
            j = random.randint(0, self.N - 1)

            
            if self.mat[i][j] != 0:
                count -= 1
                self.mat[i][j] = 0

    def printSudoku(self):
        # print mat
        print("Sudoku: ")
        for i in range(self.N):
            for j in range(self.N):
                print(self.mat[i][j], end=" ")
            print()

        # print originMat
        print("Origin: ")
        for i in range(self.N):
            for j in range(self.N):
                print(self.originMat[i][j], end=" ")
            print()

def puzzle_generator(string):
    N = 9
    if string == "beginner":
        K = 30
    elif string == "intermediate":
        K = 40
    elif string == "advanced":
        K = 50
    sudoku = Sudoku(N, K)
    sudoku.fillValues()
    return sudoku.mat, sudoku.originMat

if __name__ == "__main__":
    N = 9
    K = 50 # beginner = 30, intermediate = 40, advanced = 50

    sudoku = Sudoku(N, K)
    sudoku.fillValues()
    sudoku.printSudoku()
        