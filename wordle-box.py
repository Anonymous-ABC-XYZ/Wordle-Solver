from PySide6.QtCore import Qt, QSize, QRect
from PySide6.QtGui import *
from PySide6.QtWidgets import QApplication, QLabel, QListWidget, QWidget, QListWidgetItem, QPushButton, QHBoxLayout, \
    QVBoxLayout, QMainWindow, QTabWidget, QToolBox, QGridLayout, QLineEdit, QSpacerItem, QSizePolicy
import sys
import time
import random

class Validator(QValidator):
    def validate(self, string, pos):
        return QValidator.Acceptable, string.upper(), pos


class WordleBox(QWidget):
    def __init__(self):
        super().__init__()
        ####--------------------Array Declarations--------------------####
        self.button_list = [] 
        self.completeBoxes = []
        self.completeButtons = []
        self.completeArrays = []
        box_list = []
        button_list = []
        with open("./answers.txt") as w:
            self.universe = w.readlines()
        self.setWindowTitle("Wordle Solver")
 
        width = 500
         
        # setting  the fixed width of window
        self.setFixedWidth(width)
        
        
    ####--------------------QT Declarations--------------------####
        self.layout= QVBoxLayout() 
        self.setLayout(self.layout)
        self.Text = QLabel(text="Guess: GREAT") 
        self.Text.setStyleSheet("background-color: transparent; color: white") 
        self.Text.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.Text.setFont(QFont("Urbanist", 18, -1))
        self.layout.addWidget(self.Text)
        qss_file = open('style.qss').read()
        self.setStyleSheet(qss_file)
        self.checkWord = ""
        self.font = QFont("Arial", 28, -1)
        self.checkButtonList = []


        
        ####--------------------Initial Wordle Box Set-Up--------------------####
        layout2 = QGridLayout()
        for i in range(0, 5):

            # Initialising the Boxes
            box_list.append(QLineEdit())
            currentBox = box_list[i]

            # Box properties
            layout2.addWidget(currentBox, 0, i, Qt.AlignmentFlag.AlignHCenter)
            currentBox.setFixedWidth(50)
            currentBox.setFixedHeight(50)
            currentBox.setMaxLength(1)
            currentBox.setFont(self.font)


            self.validator = Validator(self) # Checking whether they letters entered are uppercase
            currentBox.setValidator(self.validator) #Changing them to uppercase if they aren't
            currentBox.setAlignment(Qt.AlignCenter)

            # Initialising the buttons
            button = [QPushButton(), 0, i] # Array with the 2nd representing the state of the box: green, yellow, black
            button_list.append(button)
            currentButton = button_list[i][0]
            layout2.addWidget(currentButton, 1, i, Qt.AlignmentFlag.AlignHCenter) 
            currentButton.setFixedWidth(20)
            currentButton.setFixedHeight(10)
            currentButton.setStyleSheet("border-width: 0px;background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #7469B6, stop: 1 #AD88C6)")
            

            # The checked, pos is used so that the counter(i) at that time can be captured
            currentButton.clicked.connect(lambda checked, pos= i:self.colorChange(l=pos, j=0)) 

        # Adding a check button to the end of each box
        self.checkButtonList.append(QPushButton(text=f"Get guess 1"))
        self.checkButtonList[0].clicked.connect(lambda e:self.get_words(j=0))

        layout2.addWidget(self.checkButtonList[0], 0, 5)

        Spacer = QLabel('')
        layout2.addWidget(Spacer)
        Spacer.setStyleSheet("background: transparent") 
        Spacer.setFixedHeight(10)
        #Appending this set to the total boxes so that it can be displayed
        self.completeBoxes.append(box_list)
        self.completeArrays.append(layout2)
        self.completeButtons.append(button_list)

        ####--------------------Initializing the rest of the wordle boxes--------------------####        
        for k in range(1,7):
             self.wordleBoxes(k)
             self.layout.addLayout(self.completeArrays[k-1]) # Adding each layout to the parent layout
             

    def wordleBoxes(self, k):
        box_list = []
        layout2 = QGridLayout()
        button_list = []
        for i in range(0, 5):
            # Initialising the Boxes
            box_list.append(QLineEdit())
            currentBox = box_list[i]

            # Box properties
            layout2.addWidget(currentBox, 0, i, Qt.AlignmentFlag.AlignHCenter)
            currentBox.setFixedWidth(50)
            currentBox.setFixedHeight(50)
            currentBox.setMaxLength(1)
            currentBox.setFont(self.font)


            self.validator = Validator(self) # Checking whether they letters entered are uppercase
            currentBox.setValidator(self.validator) #Changing them to uppercase if they aren't
            currentBox.setAlignment(Qt.AlignCenter)

            # Initialising the buttons
            button = [QPushButton(), 0, i] # Array with the 2nd representing the state of the box: green, yellow, black
            button_list.append(button)
            currentButton = button_list[i][0]
            currentButton.setStyleSheet("border-width: 0px;background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #7469B6, stop: 1 #AD88C6)")
            layout2.addWidget(currentButton, 1, i, Qt.AlignmentFlag.AlignHCenter) 
            currentButton.setFixedWidth(20)
            currentButton.setFixedHeight(10)

            # The checked, pos is used so that the counter(i) at that time can be captured
            currentButton.clicked.connect(lambda checked, pos= i:self.colorChange(l=pos, j=k)) 

        # Adding a check button to the end of each box
        checkBox = QPushButton(text=f"Get guess {(k+1)}")
        self.checkButtonList.append(checkBox)
        self.checkButtonList[k].clicked.connect(lambda e:self.get_words(j=k))
        layout2.addWidget(self.checkButtonList[k], 0, 5)

        Spacer = QLabel('')
        layout2.addWidget(Spacer)
        Spacer.setStyleSheet("background-color: transparent")
        Spacer.setFixedHeight(10)


        # Appending this set to the total boxes so that it can be displayed
        self.completeBoxes.append(box_list)
        self.completeArrays.append(layout2)
        self.completeButtons.append(button_list)

        
    def shift_focus(self):  
            for j in range(0,6):
                # Iterating through the boxes to then shift the focus to the next one once text is entered
                self.completeBoxes[j][0].textEdited.connect(self.completeBoxes[j][1].setFocus)
                self.completeBoxes[j][1].textEdited.connect(self.completeBoxes[j][2].setFocus)
                self.completeBoxes[j][2].textEdited.connect(self.completeBoxes[j][3].setFocus)
                self.completeBoxes[j][3].textEdited.connect(self.completeBoxes[j][4].setFocus)

    def get_words(self, j):    
        self.checkWord = ""
        self.btnColor = ""

        for i in range(0,5):
            self.checkWord += self.completeBoxes[j][i].text()
            if self.completeButtons[j][i][1]== 0:
                 self.btnColor += "b"
            elif self.completeButtons[j][i][1] == 1:
                 self.btnColor += "y"
            elif self.completeButtons[j][i][1] == 2:
                 self.btnColor += 'g' 

        self.wordleSolverBackend(f'{self.checkWord} :{self.btnColor}')

    def colorChange(self, l, j):
            # Comparing the states of the button and setting the color of the boxes and buttons accordingly
            if self.completeButtons[j][l][1] == 0: #0 is the default color
                self.completeButtons[j][l][0].setStyleSheet("background-color: #FEC538") # Changing it to yellow once clicked
                self.completeBoxes[j][l].setStyleSheet("background-color: #FEC538")  
                self.completeButtons[j][l][1] += 1
            elif self.completeButtons[j][l][1] == 1:
                self.completeButtons[j][l][0].setStyleSheet("background-color: #3CAEA3") # If the state is 1 (yellow), it will then change to green
                self.completeBoxes[j][l].setStyleSheet("background-color: #3CAEA3")  
                self.completeButtons[j][l][1] += 1  
            elif self.completeButtons[j][l][1] == 2:
                self.completeButtons[j][l][0].setStyleSheet("background-color: #AD88C6") # If green, change to default state
                self.completeBoxes[j][l].setStyleSheet("background-color: qlineargradient(x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #7469B6, stop: 1 #AD88C6);")
                self.completeButtons[j][l][1] = 0

    def wordleSolverBackend(self, guess):
         guess = guess.lower()
         print(guess)
         g1 = guess.split(':', 1)
         arr1 = g1[0].strip()
         arr2 = g1[1].strip()
        # validate the input and ask for guess again if input is wrong
        # Go through input one character at a time
         for i in range(0, len(arr1)):
            guess_char = arr1[i]
            guess_char_color = arr2[i]
 

            position = i

        # If we got a green guess_char
            if guess_char_color == 'g':
                x = 0
                # Go through all possible words
                while x < len(self.universe):
                    if self.universe[x][position] != guess_char:
                        self.universe.pop(x)
                    else:
                        x = x+1

            elif guess_char_color == 'b':
                x = 0
                counter = 1
                for i in range(0, len(self.universe[x])):
                    if self.universe[x][i] == guess_char:
                        counter = counter+1
                while x < len(self.universe):
                    if counter > 1:
                        x = x+1
                    elif guess_char in self.universe[x]:
                        self.universe.pop(x)
                    else:
                        x = x+1

            elif guess_char_color == 'y':
                x = -1
                while x < len(self.universe):
                    word = self.universe[x]
                    if guess_char not in word:
                        # delete word
                        self.universe.pop(x)
                    if guess_char in word and word[position] == guess_char:
                        self.universe.pop(x)
                    x = x+1
         try:
            self.Text.setText(f'Guess: {str(self.universe[random.randint(0, len(self.universe))])}')

         except IndexError:
            self.Text.setText(f'Guess: {str(self.universe[0])}')
            print(self.universe[0])

             



app = QApplication(sys.argv)
wordleboxList = []

wordlebox = WordleBox()
wordlebox.show()
wordlebox.shift_focus()

sys.exit(app.exec())
