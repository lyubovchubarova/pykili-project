WIDTH = 1200
HEIGHT = 700
CORN_POS = (250, 50)
SIDE = 600

BLACK = (0, 0, 0)
GREEN = (34, 139, 34)
YELLOW = (255, 215, 0)
RED = (178, 34, 34)
BLUE = (70, 130, 180)

GREEN_CELLS = set([(3, 0), (11, 0), (6, 2), (8, 2), (7, 3), (0, 3), (14, 3), (2, 6), (2, 8),
(3, 7), (0, 11), (14, 11), (12, 6), (12, 8), (11, 7), (3, 14), (11, 14), (6, 12),
(8, 12), (7, 11), (6, 6), (8, 8), (6, 8), (8, 6)])

RED_CELLS = set([(0, 0), (7, 0), (14, 0), (0, 7),
(0, 14), (7, 14), (14, 7), (14, 14)])

BLUE_CELLS = set([(1, 1), (2, 2), (3, 3), (4, 4), (10, 10), (11, 11), (12, 12),
(13, 13), (1, 13), (2, 12), (3, 11), (4, 10),
(10, 4), (11, 3), (12, 2), (13, 1)])

YELLOW_CELLS = set([(5, 1), (9, 1), (1, 5), (1, 9), (13, 5), (13, 9), (5, 13), (9, 13)])

LETTERS = ['а','а','а','а','а','а','а','а','а','а','б','б','б','в','в','в','в','в','г','г','г',
           'д','д','д','д','д','е','е','е','е','е','е','е','е','е','ж','ж','з','з','и','и','и','и','и',
           'и','и','и','й','й','й','й','к','к','к','к','к','к','л','л','л','л','м','м','м','м','м','н','н','н','н','н',
           'н','н','н','о','о','о','о','о','о','о','о','о','о','п','п','п','п','п','п','р','р','р','р','р','р','с','с',
           'с','с','с','с','т','т','т','т','т','у','у','у','ф','х','х','ц','ч','ч','ш','щ','ъ','ы','ы','ь','ь','э','ю',
           'я','я','я','*','*','*']

WEIGHT_OF_LETTERS = {'а': 1,'б': 3, 'в': 2,'г': 3,'д': 2,'е': 1,'ж': 5,'з': 5,'и': 1,'й': 2,'к': 2,'л': 2,'м': 2,'н': 1,
                     'о': 1,'п': 2,'р': 2,'с': 2,'т': 2,'т': 2,'у': 3,'ф': 10,'х': 5,'ц': 10,'ч': 5,'ш': 10,'щ': 10,'ъ': 10,
                     'ы': 5,'ь': 5,'э': 10,'ю': 10,'я': 3, '*': '-'}

STOPPER = 30