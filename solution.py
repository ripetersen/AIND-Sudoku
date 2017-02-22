from functools import reduce


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def update_values(values,new_values):
    """
    Please use this function to update your values dictionary!
    Updates the values map and records the change. 
    """
    values.update(new_values)
    assignments.append(values.copy())
    return values

def naked_twins(values):
    """
    Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

    # Loop over all the boxes that have 2 values
    for box,value in [ (b,v) for b,v in values.items() if len(v)==2]:
        # Loop over each unit that contains the box 
        for unit in units[box]:
            # A twin is a peer that has the same value as the box and insn't the box
            for twin in [peer for peer in unit if peer!=box and values[peer]==value]:
                # If we are in the loop the the twin has been found
                # Create a map of the peer and the value with the two digits removed
                # from the other peers (i.e. not the box or twin)
                new_values={peer:values[peer].replace(value[0],'').replace(value[1],'') 
                    for peer in unit if peer not in [box,twin]}
                # Update the values and record the assignment
                update_values(values,new_values)
    return values

def cross(a, b):
    "Cross product of elements in A and elements in B."
    return [s+t for s in a for t in b]

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    return { k:v if v!='.' else '123456789' for k,v in zip(boxes,grid)}

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
	# Get the solved boxes, the ones with only one value
	for box,value in [ (b,v) for b,v in values.items() if len(v)==1]:
		# Loop over the peers removing the solved value
		for peer in peers[box]:
			assign_value(values,peer,values[peer].replace(value,''))
	return values

def only_choice(values):
    # Loop over all the units
    for unit in unitlist:
        # Check each digit
        for digit in '123456789':
            # record the boxes that contain the checked digit
            dplaces = [box for box in unit if digit in values[box]] 
            # if there is only one box that contains the digit, assign the digit to that box
            if len(dplaces) == 1:
                assign_value(values,dplaces[0],digit)
    return values

def reduce_puzzle(values):
	stalled = False
	while not stalled:
		# Check how many boxes have a determined value
		solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

		# Use the Eliminate Strategy
		eliminate(values)

		# Use the Only Choice Strategy
		only_choice(values)

                # Use the Naked Twins Strategy
		naked_twins(values)

		# Check how many boxes have a determined value, to compare
		solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
		# If no new values were added, stop the loop.
		stalled = solved_values_before == solved_values_after
		# Sanity check, return False if there is a box with zero available values:
		if len([box for box in values.keys() if len(values[box]) == 0]):
			return False
	return values

def search(values):
	#"Using depth-first search and propagation, create a search tree and solve the sudoku."
	# First, reduce the puzzle using the previous function
	values = reduce_puzzle(values)
	if values == False or all([len(v)==1 for v in values.values()]):
		return values

	# Choose one of the unfilled squares with the fewest possibilities
	unsolved=[ (k,v) for k,v in values.items() if len(v)>1 ]
        # Get the box that has the fewest values
	smallest=reduce((lambda b1,b2: b1 if len(b1[1])<=len(b2[1]) else b2),unsolved)

	# Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
	for value in smallest[1]:
		new_values=values.copy()
		assign_value(new_values, smallest[0], value)
		result=search(new_values)
		if result:
			return result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

rows = 'ABCDEFGHI'
cols = '123456789'
boxes = cross(rows, cols)
row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# The additional diagonal units
diag_units = [[ r+c for r,c in zip(rows,cols)],[ r+c for r,c in zip(rows,cols[::-1])]]
unitlist = row_units + column_units + square_units + diag_units
units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
assignments = []

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
