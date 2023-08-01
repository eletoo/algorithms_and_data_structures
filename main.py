import random

from Matrix import Matrix
import configparser

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.read('parameters.ini')

    SEED = int(config['GENERATION']['SEED'])
    NROWS = int(config['GENERATION']['NROWS'])
    NCOLS = int(config['GENERATION']['NCOLS'])
    NOBSTACLES = int(config['GENERATION']['NOBSTACLES'])
    AGGLOMERATION_FACTOR = float(config['GENERATION']['AGGLOMERATION_FACTOR'])

    # instead of saving the adjacency matrix, I save only the list of non-zero elements of the matrix and check every
    # time I have to make a move if the cell is empty. This way I save a lot of memory, especially for large grids with
    # few non-zero elements.

    grid = Matrix(NROWS, NCOLS)

    n_obstacles = NOBSTACLES
    pending = []
    random.seed(SEED)  # for reproducibility
    while n_obstacles > 0:
        pending.append((random.randint(0, NROWS - 1), random.randint(0, NCOLS - 1)))
        while len(pending) > 0:
            i, j = pending.pop(0)  # last element
            if (i, j) not in grid:
                grid.add(i, j)
                n_obstacles -= 1
                if n_obstacles == 0:
                    break
                for l, k in grid.neighbours(i, j):
                    if random.random() < AGGLOMERATION_FACTOR / 2.5 and (l, k) not in grid:
                        # TODO: 2.5 is a magic number
                        pending.append((l, k))

    print(grid)
    print(grid.calc_agg_fac())

    # Per computare gli ostacoli, ho un fattore di agglomerazione che mi dice quanti ostacoli ci sono (%) in una certa
    # area.
    # Finché il numero di ostacoli è inferiore a quello richiesto:
    # Per ogni cella, calcolo la probabilità che sia osatcolo e - se è un ostacolo - faccio sì che ogni cella
    # adiacente sia un ostacolo con probabilità "fattore di agglomerazione". Una volta che una cella viene impostata
    # come ostacolo, non può più essere modificata. Le celle rimaste libere, anche se già visitate, possono comunque
    # essere trasformate in ostacoli più avanti durante l'esecuzione.

    # se alla fine della generazione degli ostacoli, il numero di ostacoli è inferiore a quello richiesto, allora
    # ricomincio da un'altra cella (vuota) scelta casualmente e ripeto il procedimento.
