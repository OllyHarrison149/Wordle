import pyautogui

class Wordle:

    chars_remaining = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']

    def __init__(self,possible_words):

        self.possible_words = possible_words

    def guess(self):
        
        char_freq = {}

        for char in self.chars_remaining:
            
            char_freq[char] = 0
        
        for word in self.possible_words:
            
            for char in word:

                char_freq[char] += 1

        best_value = 0
        
        for word in self.possible_words:
            
            word_value = sum(char_freq[char] for char in list(set(word)))

            if word_value >= best_value:

                best_value = word_value

                best_word = word

        return best_word

    def feedback(self,word):

        boxes = pyautogui.locateOnScreen('wordBoxes.png')

        pyautogui.moveTo(boxes[0],boxes[1])
        pyautogui.click()

        pyautogui.typewrite(word)
        pyautogui.typewrite('\n',interval = 2)

        cur_x = boxes[0]
        pad_x = 10
        cur_y = boxes[1] + boxes[3]/9

        box_col = []

        for box in range(5):

            color = pyautogui.screenshot().getpixel((cur_x+pad_x,cur_y))

            if color == (120,124,126):
                
                box_col.append('W')
                
            elif color == (201,180,88):
                
                box_col.append('O')
                
            elif color == (106,170,100):
                
                box_col.append('G')
            
            pad_x += 100

        for pos in range(5):

            if box_col[pos] == 'G':

                self.green(word[pos],pos)

            elif box_col[pos] == 'O':

                self.orange(word[pos],pos)

            else:

                self.white(word[pos])

    def green(self,char,pos):

        new_words = []

        for word in self.possible_words:

            if word[pos] == char:

                new_words.append(word)

        self.possible_words = new_words

    def orange(self,char,pos):

        new_words = []

        for word in self.possible_words:

            if char in word and word[pos] != char:

                new_words.append(word)

        self.possible_words = new_words

    def white(self,char):

        new_words = []

        self.chars_remaining.remove(char)

        for word in self.possible_words:

            if all(char in self.chars_remaining for char in word):
                
                new_words.append(word)

        self.possible_words = new_words

def load_words():
    
    with open('words_alpha.txt') as word_file:
        
        words = word_file.read().split()

    valid_words = []
    
    for word in words:
        
        if len(word) == 5:
            
            valid_words.append(word.upper())

    return valid_words


if __name__ == '__main__':
    
    possible_words = load_words()
    
    new_wordle = Wordle(possible_words)

    for guess in range(6):

        word = new_wordle.guess()
        new_wordle.feedback(word)
