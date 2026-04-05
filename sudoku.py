from sudokus import sudoku1, sudoku2,sudoku3,sudoku4,sudoku5,sudoku6,sudoku7,sudoku8,sudoku9,sudoku10


def find_empty_cell(sudoku ) :
    for i in range (9):
        for j in range (9) :
            if sudoku[i][j] == 0 :
                return (i,j) #position of empty cell 
    return None  # No empty cells left

def conditions (sudoku , row, col, n ) :
    #Chek the row & column 
    for i in range(9) :
        if sudoku[row][i] == n or sudoku[i][col] == n :
            return False 
        
    # Check the 3x3 box
    row_start = (row // 3) * 3
    col_start = (col // 3) * 3
    for i in range(row_start, row_start + 3):
        for j in range(col_start, col_start + 3):
            if sudoku[i][j] == n:
                return False
    return True 


def solve(sudoku) :
    empty = find_empty_cell(sudoku) 

    if not empty :
        return True
    
    row,col = empty 

    for num in range(1, 10):  # Try numbers 1 to 9
        if conditions(sudoku, row, col, num):  # Check if the number is valid
            sudoku[row][col] = num  # Place the number in the empty cell
            if solve(sudoku):  # Recursively solve the next cell
                return True
            sudoku[row][col] = 0  # Backtrack if any solution found
            
    return False  # Trigger backtracking if no valid number is found


# Solve all puzzles and print the result
sudokus = [sudoku1, sudoku2, sudoku3, sudoku4, sudoku5,
           sudoku6, sudoku7, sudoku8, sudoku9,sudoku10]
for i in range(10) :
    if solve(sudokus[i]) :
        print("Sudoku", i+1)
        for row in sudokus[i]:
            print(row)   # Print the solved Sudoku
        print("\n")
    else:
        print("No solution exists")


    
    