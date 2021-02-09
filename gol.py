import time
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

    cell_row      = cell.get('row')
    cell_col      = cell.get('col')
    cell_status   = cell.get('status')

    logging.debug(f"cell coords: {cell_row},{cell_col} | status: {cell_status}")

    live_neighbors = 0

    for neighbor_row in range(cell_row - 1, cell_row + 2):
        if neighbor_row >= 0 and neighbor_row < state_width:
            for neighbor_col in range(cell_col - 1, cell_col + 2):
                if neighbor_col >= 0 and neighbor_col < state_height:
                    if neighbor_row == cell_row and neighbor_col == cell_col:
                        continue
                    else:
                        logging.debug(f"neighbor coords: {neighbor_row},{neighbor_col} | status: {state[neighbor_row][neighbor_col]}")
                        if state[neighbor_row][neighbor_col] == 1:
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

    for row in range(0, state_width):
        for col in range(0, state_height):
            cell = {'row':row, 'col':col, 'status':state[row][col]}
            next_state[row][col] = update_cell_status(cell, state)

    return next_state


def run(w, h):
    dead  = dead_state(w, h)
    state = random_state(w, h)
    while True:
        if state == dead:
            render_state(state)
            break
        render_state(state)
        state = next_state(state)
        time.sleep(0.1)

if __name__ == '__main__':
    run(5, 5)

