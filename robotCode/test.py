from typing import NamedTuple

'''
Given a keyboard represented as a matrix and a word, return the shortest path that would spell out the word starting from the top left corner of the matrix.

Example:
Keyboard:
A B C D E F G
H I J K L M N
O P Q R S T U
V W X Y Z * *

Word: DART

Returns:
[
    (V: 0, H: 3),
    (V: 0, H: -3),
    (V: 2, H: 3),
    (V: 0, H: 2),
]
'''


keyboard = [
    ["A", "B", "C", "D", "E", "F", "G"],
    ["H", "I", "J", "K", "L", "M", "N"],
    ["O", "P", "Q", "R", "S", "T", "U"],
    ["V", "W", "X", "Y", "Z", "", ""],
]

# A: 0, 0
# runtime complexity: 0(w+r*c)
# space complexity: 0(w+rc)
class Path(NamedTuple):
    V: int # vertical change... UP: V < 0; Down: V >= 0
    H: int # horizontal change... Left: H < 0; Right: H >= 0

def get_word_journey(keyboard, word):
    dict = {}
    retList = []
    for i in range(len(keyboard)):
        for j in range(len(keyboard[0])):
            dict[keyboard[i][j]] = (i,j)

    currIndex = [0,0]

    for i in range(len(word)):

        nextIndex = dict[word[i]]
        diff = (currIndex[0]-nextIndex[0],currIndex[1]-nextIndex[1])
        currIndex = dict[word[i]]
        toAdd = Path(diff[0],diff[1])
        retList.append(toAdd)
    return retList


## Everything below this line is a test function
def test_function():
    words = {
        "DART": Path(13, 13),
        "FIG": Path(16, 9),
    }
    wrapped = False
    def get_wrapped_idx(idx, length):
        if idx < 0:
            return length + idx
        if idx > length:
            return idx % length
        return idx
    
    for word in words:
        expected_path_len = words[word]
        print(f'Testing word: {word}\n')
        journey = get_word_journey(keyboard, word)
        current = Path(0, 0)
        spelled_word = ""
        path_len = 0
        for path in journey:
            row = current.V + path.V
            col = current.H + path.H
            if wrapped:
                # get letter from wrapped
                row = get_wrapped_idx(row, len(keyboard))
                col = get_wrapped_idx(col, len(keyboard[0]))
            spelled_word += keyboard[row][col]
            current = Path(row, col)
            path_len += abs(path.V)
            path_len += abs(path.H)
        p1 = expected_path_len[0]
        if wrapped:
            p1 = expected_path_len[1]
        if spelled_word == word and path_len <= p1:
            print(f'SUCCESS: word -> {spelled_word}; length -> {path_len}\n')
        else:
            print(f'FAILED: word -> {spelled_word}; length -> {path_len}\n')
            
test_function()  
