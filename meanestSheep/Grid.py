def valueIteration(grid, sheep, bot):
		print("Start Value Iteration")
		prev = estimatedTvalues(grid)
		print("Done loading Estimated values")
		curr = {}

		beta = 0.98
		convergence = False
		smallval = 0.01
		while not convergence:
			count = 1
			max = -100
			for keys in prev.keys():
				print(count, "/", len(prev.keys()))
				s = keys[0]
				sheep.row = s.x
				sheep.col = s.y
				b = keys[1]
				bot.row = b.x
				bot.col = b.y

				if sheep.row == bot.row and sheep.col == bot.col:
					curr[keys] = float('inf')
					continue
				elif sheep.row == 15 and sheep.col == 15 and not (bot.row == 15 and bot.col == 15):
					curr[keys] = 0.0
					continue
				initial = (s, b)
				finalmin = prev[initial]
				getBotNeighbors(grid, bot)
				getSheepNeighbors(grid, sheep)
				if sheep.view.contains(bot):
					modSheepNeighbors(grid, sheep, bot)
				for bot_neighbor in bot.neighbors:
					reward = -1
					val = 0
					sum = 0
					prob = 1 / len(sheep.neighbors)
					for sheep_neighbor in sheep.neighbors:
						p1 = Point(sheep_neighbor.row, sheep_neighbor.col)
						p2 = Point(bot_neighbor.row, bot_neighbor.col)
						entry = (p1, p2)
						sum += prev[entry] * prob
					val = reward + (beta * sum)
					if val < finalmin:
						finalmin = val
						x = bot_neighbor.row
						y = bot_neighbor.col
				curr[initial] = finalmin
				if abs(curr[initial] - prev[initial]) > max:
					max = abs(curr[initial] - prev[initial])
			if max < smallval:
				convergence = True
			prev = curr.copy()
			curr.clear()
		print("End Value Iteration")
		
def modSheepNeighbors(grid, sheep, bot):
		mindist = float('inf')
		for neighbor in sheep.neighbors:
			val = abs(bot.row - neighbor.row) + abs(bot.col - neighbor.col)
			if val < mindist:
				sheep.neighbors.clear()
				sheep.neighbors.add(neighbor)
				mindist = val
			elif val == mindist:
				sheep.neighbors.add(neighbor)
				
def estimatedTvalues(grid):
		prev = {}
		for i in range(31):
			for j in range(31):
				for m in range(31):
					for n in range(31):
						# sheep position
						p1 = (i, j)
						# bot position
						p2 = (m, n)
						key = (p1, p2)
						# goal states
						if (p1 == (15, 15)) and (p2 != (15, 15)):
							prev[key] = 0.0
						elif p1 == p2:  # sheep and bot are at the same positon
							prev[key] = float('inf')
						else:
							estimate = abs(p2[1] - p1[1]) + abs(p2[0] - p1[0]) + abs(p1[0] - 15) + abs(p1[1] - 15) + 2
							prev[key] = estimate
		return prev

import random

# generate the grid
def generate_Grid():
    grid = [[Node(i, j) for j in range(31)] for i in range(31)]
    populate_Grid(grid)
    return grid

# populate the grid with Node objects that contain row and col vals
def populate_Grid(grid):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            grid[i][j] = Node(i, j)
    # Iniitalize blocked nodes to keep simulate the pen of the sheep
    grid[15][14].blocked = True
    grid[15][16].blocked = True
    grid[14][14].blocked = True
    grid[14][16].blocked = True
    grid[16][14].blocked = True
    grid[16][15].blocked = True
    grid[16][16].blocked = True

def trapSheep(grid, sheep, bot):
    print("Loading Policy... ")
    # Load the Policy for the bot
    policy = loadPolicy(grid)
    # generate random sheep and bot positions
    generateSheepPosition(grid, sheep)
    generateSheepdogPosition(grid, bot)
    startbotrow = bot.row
    startbotcol = bot.col
    startsheeprow = sheep.row
    startsheepcol = sheep.col

    # keeps track of the number of steps
    steps = 1
    # while true run until the sheep is captured at location (15, 15) or the sheep
    # crushes the bot
    while True:
        p1 = Point(sheep.row, sheep.col)
        p2 = Point(bot.row, bot.col)
        # create the current state
        key = Key(p1, p2)
        # based on the state retrieve the policy for the next postion of bot
        next = policy.get(key)
        bot.row = next.row
        bot.col = next.col
        sheepMove(grid, sheep, bot)
        print(
            "step: " +
            str(steps) +
            " botrow: " +
            str(bot.row) +
            " botcol: " +
            str(bot.col) +
            " sheeprow: " +
            str(sheep.row) +
            " sheepcol " +
            str(sheep.col)
        )
        # if sheeplocation == botlocation the bot is considered crushed
        if sheep.row == bot.row and sheep.col == bot.col:
            print("Robot Crushed!")
            print(
                "startbotrow: " +
                str(startbotrow) +
                " startcolrow: " +
                str(startbotcol) +
                " startsheeprow: " +
                str(startsheeprow) +
                " startsheepcol " +
                str(startsheepcol)
            )
            return
        # if the sheep row and col is at pos(15, 15) we have successfully trapped the
        # sheep
        if sheep.row == 15 and sheep.col == 15:
            print("Successfully trapped sheep!")
            print(
                "startbotrow: " +
                str(startbotrow) +
                " startcolrow: " +
                str(startbotcol) +
                " startsheeprow: " +
                str(startsheeprow) +
                " startsheepcol " +
                str(startsheepcol)
            )
            
def generateSheepPosition(grid, sheep):
		rand = random.Random()
		row = rand.randint(0, 30)
		col = rand.randint(0, 30)
		while grid[row][col].blocked:
			row = rand.randint(0, 30)
			col = rand.randint(0, 30)
		sheep.row = row
		sheep.col = col
		grid[row][col] = sheep
		
def generateSheepdogPosition(grid, bot):
		rand = random.Random()
		row = rand.randint(0, 30)
		col = rand.randint(0, 30)
		while grid[row][col].blocked or isinstance(grid[row][col], AngrySheep):
			row = rand.randint(0, 30)
			col = rand.randint(0, 30)
		bot.row = row
		bot.col = col
		grid[row][col] = bot

def getSheepNeighbors(grid, sheep):
    if sheep.neighbors:
        sheep.neighbors.clear()
    row = sheep.row
    col = sheep.col

    sheep.neighbors.append(sheep)

    if row - 1 >= 0:
        sheep.neighbors.append(grid[row - 1][col])
    if row + 1 <= 30:
        sheep.neighbors.append(grid[row + 1][col])
    if col - 1 >= 0:
        sheep.neighbors.append(grid[row][col - 1])
    if col + 1 <= 30:
        sheep.neighbors.append(grid[row][col + 1])

def generateSheepView(grid, sheep):
    vrow = sheep.row - 2
    vcol = sheep.col - 2
    vrowend = vrow + 5
    vcolend = vcol + 5
    if sheep.view:
        sheep.view.clear()

    while vrow < vrowend:
        while vcol < vcolend:
            if vrow < 0 or vcol < 0 or vrow > 30 or vcol > 30:
                vcol += 1
                continue
            if sheep.row == vrow and sheep.col == vcol:
                vcol += 1
                continue
            sheep.view.append(grid[vrow][vcol])
            vcol += 1
        vcol = sheep.col - 2
        vrow += 1
	
def getBotNeighbors(grid, bot):
    if not bot.neighbors:
        bot.neighbors.clear()
    row = bot.row
    col = bot.col

    bot.neighbors.append(bot)

    if row - 1 >= 0 and not grid[row - 1][col].blocked:
        bot.neighbors.append(grid[row - 1][col])
    if row + 1 <= 30 and not grid[row + 1][col].blocked:
        bot.neighbors.append(grid[row + 1][col])
    if col - 1 >= 0 and not grid[row][col - 1].blocked:
        bot.neighbors.append(grid[row][col - 1])
    if col + 1 <= 30 and not grid[row][col + 1].blocked:
        bot.neighbors.append(grid[row][col + 1])
    if row - 1 >= 0 and col - 1 >= 0 and not grid[row - 1][col - 1].blocked:
        bot.neighbors.append(grid[row - 1][col - 1])
    if row - 1 >= 0 and col + 1 <= 30 and not grid[row - 1][col + 1].blocked:
        bot.neighbors.append(grid[row - 1][col + 1])
    if row + 1 <= 30 and col + 1 <= 30 and not grid[row + 1][col + 1].blocked:
        bot.neighbors.append(grid[row + 1][col + 1])
    if row + 1 <= 30 and col - 1 >= 0 and not grid[row + 1][col - 1].blocked:
        bot.neighbors.append(grid[row + 1][col - 1])

def sheepMove(grid, sheep, bot):
    move = None
    attack = []
    index = 0
    getSheepNeighbors(grid, sheep)
    generateSheepView(grid, sheep)
    rand = random.Random()
    # if the bot is in the sheep's view the sheep will take the move to reduce its
    # distance to the bot
    if bot in sheep.view:
        mindist = float('inf')
        for neighbor in sheep.neighbors:
            val = abs(bot.row - neighbor.row) + abs(bot.col - neighbor.col)
            if val < mindist:
                attack.clear()
                attack.append(neighbor)
            elif val == mindist:
                attack.append(neighbor)
        index = rand.randint(0, len(attack) - 1)
        move = attack[index]
        if not grid[move.row][move.col].blocked:
            sheep.row = move.row
            sheep.col = move.col
    # else the sheep moves randomly amongst its neighbors
    else:
        index = rand.randint(0, len(sheep.neighbors) - 1)
        move = sheep.neighbors[index]
        if not grid[move.row][move.col].blocked:
            sheep.row = move.row
            sheep.col = move.col

import os

def method1(map):
    try:
        with open("initial.txt", "w") as fileTwo:
            for key, value in map.items():
                x1, y1 = key.key1.x, key.key1.y
                x2, y2 = key.key2.x, key.key2.y
                fileTwo.write(f"{x1} {y1} {x2} {y2} {value}\n")
    except Exception as e:
        pass

def write_policy(map):
    try:
        with open("policy.txt", "w") as f:
            for key, value in map.items():
                x1, y1 = key.key1.x, key.key1.y
                x2, y2 = key.key2.x, key.key2.y
                bot_row, bot_col = value.row, value.col
                f.write(f"{x1} {y1} {x2} {y2} {bot_row} {bot_col}\n")
    except Exception as e:
        pass
                
def loadinitialestimates():
    try:
        toRead = open("initial.txt", "r")
        mapInFile = {}

        for currentLine in toRead:
            # now tokenize the currentLine:
            tokens = currentLine.split(" ")
            x1 = int(tokens[0])
            y1 = int(tokens[1])
            x2 = int(tokens[2])
            y2 = int(tokens[3])
            val = float(tokens[4])
            key = (Point(x1, y1), Point(x2, y2))
            # put tokens on currentLine in map
            mapInFile[key] = val

        toRead.close()
        return mapInFile
    except Exception as e:
        pass
    return None

def loadPolicy(grid):
    try:
        toRead = open("policy.txt", "r")
        mapInFile = {}

        for currentLine in toRead:
            # now tokenize the currentLine:
            tokens = currentLine.split(" ")
            x1 = int(tokens[0])
            y1 = int(tokens[1])
            x2 = int(tokens[2])
            y2 = int(tokens[3])
            bot_row = int(tokens[4])
            bot_col = int(tokens[5])
            key = (Point(x1, y1), Point(x2, y2))
            # put tokens on currentLine in map
            mapInFile[key] = grid[bot_row][bot_col]

        toRead.close()
        return mapInFile
    except Exception as e:
        pass
    return None