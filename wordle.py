import random

def word_list():
    with open('5_letter_words.txt', 'r+') as f:
        words = f.read().strip().split('\n')
        #print(words_list)
        return(words)    
words = word_list()
#print('words: \n', words)

def random_word(words):
    return random.choice(words)
#word = random_word(words)
#print('word: ', word)

def next_guess(words):    
    guess_word = input('Please enter a guess: ').lower()
    if guess_word in words:
            return guess_word
    else:
        guess_word = input('Please enter a guess: ').lower()
        return guess_word
guess = next_guess(words)
#print('guess: ', guess)

def is_real_word(guess, words):
    if guess in words:
        #print(True)
        return True
    else:
        #print(False)
        return False
#guess = next_guess(words)
real_check = is_real_word(guess, words)
#print('real_check: ', real_check)

def check_guess(guess, word):
    word_list = list(word)
    result = ["_"] * len(word)
    # check for exact matches chars
    for i, l in enumerate(guess):
        if l == word_list[i]:
            result[i] = "X"
            word_list[i] = " "
    # check for chars are wrong position
    for i, l in enumerate(guess):
        if l in word_list:
            if result[i] != "X":
                result[i] = "O"
                word_list[word_list.index(l)] = " "
    return "".join(result)
#check = check_guess(guess, word)
#print(result)

def play():
    print(guess)
    print(word)
    print(real_check)
    #is_real_word(guess, words)
    #rword = random_word(words)
    turn = 6
    for i in range(0,turn):
        if check == 'XXXXX':
            return 'You won!'
            break
        else:
            guessed = next_guess(words)
            result = check_guess(guess, word)
            print(result)

    if word != guess:
        return f'You lost!\nThe word was: {word}'

guess = next_guess(words)
word = random_word(words)
check = check_guess(word, guess)
func = play()
print(func)