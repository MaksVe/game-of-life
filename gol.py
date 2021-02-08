import random
import logging

logging.basicConfig(level=logging.ERROR)

seed = 0.5


def randomize(seed):
    random_number = random.random()

    if random_number >= seed:
        cell_state = 0
    else:
        cell_state = 1

    return cell_state


def dead_state(width, height):
    state = []

    for _ in range(width):
        row = []
        for _ in range(height):
            row.append(0)
    
        state.append(row)

    return state


def get_state_width(state):
    return len(state)


def get_state_height(state):
    return len(state[0])


def random_state(width, height):
    state = dead_state(width, height)

    for item in state:
        for index in range(len(item)):
            item[index] = randomize(seed)

    return state


def render_state(state):
    state_height = get_state_height(state)

    fence = '-' * (state_height + 2)
    print(fence)

    for row in state:
        pretty_row = '|'

        for item in row:
            if item == 0:
                symbol = ' '
            else:
                symbol = u"\u2588"
            pretty_row += symbol

        pretty_row += '|'
        
        print(pretty_row)

    print(fence)


def update_cell_status(cell, state):
    state_width  = get_state_width(state)
    state_height = get_state_height(state)

    cell_x      = cell.get('x')
    cell_y      = cell.get('y')
    cell_status = cell.get('status')

    logging.debug(f"cell coords: {cell_x},{cell_y} | status: {cell_status}")

    live_neighbors = 0

    for neighbor_x in range(cell_x - 1, cell_x + 2):
        if neighbor_x >= 0 and neighbor_x < state_width:
            for neighbor_y in range(cell_y - 1, cell_y + 2):
                if neighbor_y >= 0 and neighbor_y < state_height:
                    if neighbor_x == cell_x and neighbor_y == cell_y:
                        continue
                    else:
                        logging.debug(f"neighbor coords: {neighbor_x},{neighbor_y} | status: {state[neighbor_x][neighbor_y]}")
                        if state[neighbor_x][neighbor_y] == 1:
                            live_neighbors += 1

    if cell_status == 1:
        if live_neighbors <= 1:
            logging.debug("live cell dies because of underpopulation")
            cell_status = 0

        if live_neighbors >= 2 and live_neighbors <= 3:
            logging.debug("live cell lives because of right population")
            cell_status = 1

        if live_neighbors > 3:
            logging.debug("live cell dies because of overpopulation")
            cell_status = 0

    else:
        if live_neighbors == 3:
            logging.debug("dead cell alives because of population")
            cell_status = 1

        else:
            logging.debug("dead cell stays dead")
            cell_status = 0

    logging.debug("updating next state:")

    return cell_status


def next_state(state):
    state_width  = get_state_width(state)
    state_height = get_state_height(state)

    next_state = dead_state(state_width, state_height)

    for x in range(0, state_width):
        for y in range(0, state_height):
            cell = {'x':x, 'y':y, 'status':state[x][y]}
            next_state[x][y] = update_cell_status(cell, state)

    return next_state

state = random_state(5, 4)

render_state(state)

render_state(next_state(state))

