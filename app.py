import pygame
from settings import *
from random import randint, shuffle


class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Эрудит')
        self.running = True
        self.font = pygame.font.SysFont('arial', 16)
        self.word_now = ''
        self.list_of_letters = [[],[]]
        self.turn = 0
        self.score =[0, 0]
        self.all_words = [('ВЫШКА',(7, 5), (0, 1))]
        self.matrix = [[' ' for x in range(15)] for x in range(15)]
        self.set_dict = set()
        self.correct_word = True
        self.right_pos = False
        self.ready = False
        self.redact = True
        self.wait_enter = False
        self.pos_now = (0, 0)
        self.dir_now = (0, 1)
        self.need_letter = []
        self.comp_word = ''
        self.comp_pos = (0, 0)
        self.comp_dir = (0, 1)
        self.skip_turn = False
        self.letters = []
        self.winner = 0
        self.comp_dict = {3:[], 4:[], 5:[], 6:[], 7:[], 8:[]}

        for letter in LETTERS:
            self.letters.append(letter)

        self.letter_pack(0)
        self.letter_pack(1)
        
        with open('dict.txt', encoding='utf-8') as f:
            for line in f:
                self.set_dict.add(line[0:-1])
                if len(line[0:-1]) > 2 and len(line[0:-1]) < 9:
                    self.comp_dict[len(line[0:-1])].append(line[0:-1])
        
        
    def run(self):
        while self.running:
            if self.turn == 0:
                if self.redact == True:
                    self.events_type()
                    if self.skip_turn == True:
                        self.update()
                if self.correct_word == True:
                    self.events_place()
                    if self.right_pos == True:
                        self.update()
            else:
                self.comp_turn()
            self.draw()
        pygame.quit()
        
    def events_type(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.wait_enter ==  True:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.wait_enter = False
                    self.ready = False
            else:   
                if event.type == pygame.KEYDOWN and event.unicode.isalpha() and self.correct_word == True:
                    self.word_now += event.unicode
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE and self.correct_word == True:
                    self.word_now = self.word_now[0:-1]
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.correct_word == True:
                    if self.word_now.lower() in self.set_dict:
                        self.correct_word = True
                        self.redact = False
                        break
                    else:
                        self.correct_word = False
                elif event.type == pygame.KEYDOWN and (event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL):
                    self.skip_turn = True
                    break
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and self.correct_word == False:
                    self.correct_word = True
                
                
    def events_place(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                i, j = (y - CORN_POS[1])//40, (x - CORN_POS[0])//40
                if i < 0 or j < 0 or i > 14 or j > 14:
                    continue
                else:
                    self.pos_now = (i, j)
                    for k in range(100):
                        self.draw_grid()
                        if self.dir_now == (0, 1):
                            pygame.draw.rect(self.screen, (255, 255, 0), (CORN_POS[0] + j * 40, CORN_POS[1] + i * 40, min(len(self.word_now) * 40, (15 - j) * 40), 40), 4)
                        else:
                            pygame.draw.rect(self.screen, (255, 255, 0), (CORN_POS[0] + j * 40, CORN_POS[1] + i * 40, 40, min(len(self.word_now) * 40, (15 - i) * 40)), 4)
                        pygame.display.update()
                    
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                self.dir_now = (1, 0)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                self.dir_now = (0, 1)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:

                if not self.check_pos():
                    self.right_pos = False
                    self.ready = True
                    self.redact = True
                    self.wait_enter = True
                else:
                    self.right_pos = True
                    self.ready = True
                break
        
                
                
    def update(self):
        self.correct_word = True
        self.right_pos = False
        self.ready = False
        self.redact = True
        self.wait_enter = False
        if self.turn == 0 and self.skip_turn == False:
            self.all_words.append((self.word_now.upper(), self.pos_now, self.dir_now))
            self.set_dict.remove(self.word_now)
            self.score_counter()
            self.word_now = ''
        elif self.skip_turn == False: 
            self.set_dict.remove(self.comp_word)
            self.score_counter()
            self.comp_word = ''
        for letter in self.need_letter:
            if letter in self.list_of_letters[self.turn]:
                self.list_of_letters[self.turn].remove(letter)
            else:
                self.list_of_letters[self.turn].remove('*')
        self.letter_pack(self.turn)
        self.need_letter = []
        self.turn = 1 - self.turn
        self.skip_turn = False
        pass
    
    def draw(self):
        self.draw_grid()
        if self.correct_word == False:
            self.draw_words('Вы не можете ввести такое слово!', 120, 130)
        if self.right_pos == False and self.ready == True:
            self.draw_words('Невозможное расположение!', 120, 130)
            
        pygame.display.update()

        
        
    def draw_words(self, word, x, y):
        text = self.font.render(word, True, BLACK)
        text_rect = text.get_rect()
        text_rect.centerx, text_rect.centery = x, y
        self.screen.blit(text, text_rect)
        
    def letter_pack(self, turn):
        if self.skip_turn == True:
            for letter in self.list_of_letters[turn]:
                self.letters.append(letter)
            self.list_of_letters[turn] = []
        for i in range(7 - len(self.list_of_letters[turn])):
            n = randint(0, len(self.letters)-1)
            self.list_of_letters[turn].append(self.letters[n])
            self.letters[n], self.letters[-1] = self.letters[-1], self.letters[n]
            self.letters.pop()
        self.list_of_letters[turn].sort()

    def check_pos(self):
        cur_word = ''
        i, j = 0, 0
        direct = (0, 0)
        if self.turn == 0:
            cur_word = self.word_now
            i, j = self.pos_now
            direct = self.dir_now
        else:
            cur_word = self.comp_word
            i, j = self.comp_pos
            direct = self.comp_dir
        intersection = False

        if (self.turn == 0):
            print('пытаюсь поставить ваше слово ' + cur_word)

            
        if direct == (0, 1):
            a = j
            b = j + len(cur_word) - 1
            if (a - 1 >= 0 and self.matrix[i][a-1] != ' ') or (b + 1 <= 14 and self.matrix[i][b+1] != ' '):
                if self.turn == 0:
                    print('По бокам что то есть') 
                return False
            for word in self.all_words:
                if word[2] == (0, 1) and (word[1][0] == i - 1 or word[1][0] == i + 1) and not(word[1][1] + len(word[0]) - 1 < a or word[1][1] > b):
                    if self.turn == 0:
                        print(word[0] + 'касается введенного слова')
                    return False
                if word[2] == (1, 0) and word[1][0] == i + 1 and word[1][1] >= a  and word[1][1] <= b:
                    if self.turn == 0:
                        print(word[0] + ' начинается рядом с вашим словом')
                    return False
                if word[2] == (1, 0) and word[1][0] + len(word[0]) - 1 == i - 1\
                   and word[1][1] >= a  and word[1][1] <= b:
                    if self.turn == 0:
                        print(word[0] + ' заканчивается рядом с вашим словом')
                    return False
        else:
            a = i
            b = i + len(cur_word) - 1
            if (a - 1 >= 0 and self.matrix[a-1][j] != ' ') or (b + 1 <= 14 and self.matrix[b+1][j] != ' '):
                if self.turn == 0:
                    print('По бокам что то есть')    
                return False
            for word in self.all_words:
                if word[2] == (1, 0) and (word[1][1] == j - 1 or word[1][1] == j + 1) and not(word[1][0] + len(word[0]) - 1 < a or word[1][0] > b):
                    if self.turn == 0:
                        print(word[0] + 'касается введенного слова')
                    return False
                if word[2] == (0, 1) and word[1][1] == j + 1 and word[1][0] >= a and word[1][0] <=b:
                    if self.turn == 0:
                        print(word[0] + ' начинается рядом с вашим словом')
                    return False
                if word[2] == (0, 1) and word[1][1] + len(word[0]) - 1 == j - 1\
                   and word[1][0] >= a and word[1][0] <=b:
                    if self.turn == 0:
                        print(word[0] + ' заканчивается рядом с вашим словом')
                    return False
        if self.turn == 0:
            print('закончена проверка на прилегающие слова')

        self.need_letter = []
                
        for letter in cur_word:
            if i >=0 and i <= 14 and j >=0 and j <= 14 and (self.matrix[i][j] == ' ' or self.matrix[i][j] == letter.upper()):
                if self.matrix[i][j] != letter.upper():
                    self.need_letter.append(letter)
                i += direct[0]
                j += direct[1]
            else:
                return False
        if self.turn ==0:
            print('закончена проверка на пересечение с корректными буквами')
          
        letters_now = []
        for letter in self.list_of_letters[self.turn]:
            letters_now.append(letter)


        for letter in self.need_letter:
            if letter in letters_now:
                letters_now.remove(letter)
            elif '*' in letters_now:
                letters_now.remove('*')
            else:
                return False
        if self.turn == 0:
            print('закончена проверка на нехватку букв')
        
        return (len(self.need_letter) != len(cur_word))
     
            
    
    def draw_grid(self):
        self.screen.fill((255, 255, 255))
        pygame.draw.rect(self.screen, BLACK, (CORN_POS[0], CORN_POS[1], SIDE, SIDE), 2)
        for i in range(15):
            pygame.draw.line(self.screen, BLACK, (CORN_POS[0] + i * 40, CORN_POS[1]), (CORN_POS[0] + i * 40, CORN_POS[1] + SIDE), 2)
            pygame.draw.line(self.screen, BLACK, (CORN_POS[0], CORN_POS[1] + i * 40), (CORN_POS[0] + SIDE, CORN_POS[1] + i * 40), 2)
        for cell in GREEN_CELLS:
            pygame.draw.rect(self.screen, GREEN, (CORN_POS[0] + cell[1] * 40 + 2, CORN_POS[1] + cell[0] * 40 + 2, 38, 38))
        for cell in RED_CELLS:
            pygame.draw.rect(self.screen, RED, (CORN_POS[0] + cell[1] * 40 + 2, CORN_POS[1] + cell[0] * 40 + 2, 38, 38))
        for cell in YELLOW_CELLS:
            pygame.draw.rect(self.screen, YELLOW, (CORN_POS[0] + cell[1] * 40 + 2, CORN_POS[1] + cell[0] * 40 + 2, 38, 38))
        for cell in BLUE_CELLS:
            pygame.draw.rect(self.screen, BLUE, (CORN_POS[0] + cell[1] * 40 + 2, CORN_POS[1] + cell[0] * 40 + 2, 38, 38))
            
        pygame.draw.rect(self.screen, BLACK, (50, 50, 100, 40), 2)
        
        self.draw_words('Введите слово:', 100, 30)
        self.draw_words('Ваши буквы', 1000, 30)
        self.draw_words('Цена буквы', 1100, 30)
        self.draw_words('Ваш результат', 950, 550)
        self.draw_words('Результат компьютера', 1100, 550)
        self.draw_words(self.word_now, 100, 70)
        
        
        for i in range(len(self.list_of_letters[0])):
            self.draw_words(self.list_of_letters[0][i].upper(), 1000, 60 + 20 * i)  
            self.draw_words(str(WEIGHT_OF_LETTERS[self.list_of_letters[0][i]]), 1100, 60 + 20 * i)
        self.draw_words(str(self.score[0]), 950, 600)
        self.draw_words(str(self.score[1]), 1100, 600)

        for word in self.all_words:
            i, j = word[1]
            for let in word[0]:
                self.matrix[i][j] = let
                self.draw_words(let, CORN_POS[0] + j * 40 + 20, CORN_POS[1] + i * 40 + 20)
                i += word[2][0]
                j += word[2][1]
                
    def score_counter(self):
        if self.comp_word != '':
            print('Компьютер ввел слово '+ self.comp_word)
        local_score = 0
        bonus = 1
        i, j = 0, 0
        cur_word = ''
        direct = (0, 1)
        if self.turn == 0:
            cur_word = self.word_now
            i, j = self.pos_now
            direct = self.dir_now
        else:
            cur_word = self.comp_word
            i, j = self.comp_pos
            direct = self.comp_dir
        for letter in cur_word:
            if self.matrix[i][j] != ' ':
                local_score += WEIGHT_OF_LETTERS[letter]
            else:
                if (i, j) in GREEN_CELLS:
                    local_score += 2 * WEIGHT_OF_LETTERS[letter]
                elif (i, j) in YELLOW_CELLS:
                    local_score += 3 * WEIGHT_OF_LETTERS[letter]
                elif (i, j) in BLUE_CELLS:
                    bonus *= 2
                    local_score += WEIGHT_OF_LETTERS[letter]
                elif (i, j) in RED_CELLS:
                    bonus *= 3
                    local_score += WEIGHT_OF_LETTERS[letter]
                else:
                    local_score += WEIGHT_OF_LETTERS[letter]
            i += direct[0]
            j += direct[1]
        self.score[self.turn] += local_score * bonus

    def comp_turn(self):
        self.turn = 0

    

                        
                
                        

 

    

    
        
        
        
        
        
    
        
