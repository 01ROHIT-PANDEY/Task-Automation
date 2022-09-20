import sys, os
from nltk import sent_tokenize
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Image_To_Text import imgToText
from google_trans_new import google_translator 
import Extractive_Summarizer
import pickle
from langdetect import detect
import Abstractive
from gtts import gTTS


class Window(QMainWindow, QWidget):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(450, 450, 800, 520)
        self.setWindowTitle('Automation')
        self.setStyleSheet("background-color: #669999;")
        self.setWindowIcon(QIcon('summarize.png'))
        self.wid = QWidget(self)
        self.setCentralWidget(self.wid)
        self.language='en'
        self.exit_text = 'Exited Application'
        self.file_open_button = None
        self.quit_button = None
        self.textbox_input = None
        self.textbox_output = None
        self.output_label = None
        self.input_label = None
        self.file_text = None
        self.select_Lang=None
        self.my_output = None
        self.image_text=None
        self.my_text = None
        self.summarize_button = None
        self.audio_button=None
        self.n = None
        self.num_lines = None
        self.line_num_input = None
        self.sent_num = None
        self.warning_text_1 = 'You have chosen summarization length more than the actual text length!\n' + \
                              'Please enter a valid number less than the length of actual text'

        self.init_ui()

    # main function containing all the buttons and other elements to display
    def init_ui(self):
        
        # The exit button on the right bottom corner
        self.quit_button = QPushButton('Close', self)
        self.quit_button.setStyleSheet("background-color: #ff3333;")
        self.quit_button.clicked.connect(self.exit_application)
        self.quit_button.resize(self.quit_button.minimumSizeHint())

        # The File Open button on the left bottom corner
        self.file_open_button = QPushButton('Open File', self)
        self.file_open_button.clicked.connect(self.file_open)
        self.file_open_button.setStyleSheet("background-color: #2eb82e;")
        self.file_open_button.resize(self.file_open_button.minimumSizeHint())
        
        
        # The File Image Open button on the left bottom corner
        self.file_Image = QPushButton('Choose Image', self)
        self.file_Image.setStyleSheet("background-color: #2eb82e;")
        self.file_Image.clicked.connect(self.Image_Open)
        self.file_Image.resize(self.file_open_button.minimumSizeHint())
        
        self.select_Lang = QPushButton('Translate', self)
        self.select_Lang.setStyleSheet("background-color: #4dffff;")
        self.select_Lang.clicked.connect(self.Lang_Select)
        self.select_Lang.resize(self.file_open_button.minimumSizeHint())
       
        
        self.method = QComboBox(self)
        self.method.setStyleSheet("background-color: #80b3ff;")
        self.method.addItems(["Extractive", "Abstractive"])
        
        self.cb = QComboBox(self)
        self.cb.setStyleSheet("background-color: #80b3ff;")
        self.cb.addItems(["Hindi", "Marathi", "Tamil"])
        # The Summarize button on the left bottom corner
        self.summarize_button = QPushButton('Summarize', self)
        self.summarize_button.setStyleSheet("background-color: #4dffff;")
        self.summarize_button.clicked.connect(self.summarize)
        self.summarize_button.resize(self.summarize_button.sizeHint())
        
        self.audio_button = QPushButton(self)
        self.audio_button.clicked.connect(self.convert)
      #  self.audio_button.setGeometry(200,150,10,20)
        self.audio_button.setIcon(QIcon('Audio.jpg'))
        self.audio_button.resize(self.audio_button.sizeHint())

        # Left Textbox element used to input the text to be summarized --- Editable
        self.textbox_input = QPlainTextEdit(self)
        self.textbox_input.setStyleSheet("background-color: white;")
        # Right Textbox element used to display the output of the summarized text --- Not Editable (incomplete)
        self.textbox_output = QTextEdit(self)
        self.textbox_output.setStyleSheet("background-color: white;")
        self.textbox_output.setReadOnly(True)

        # Textbox for the Number of lines to summarize to
        self.line_num_input = QLineEdit(self)

        # Left Textbox heading label
        self.input_label = QLabel(self, text='Please Enter Text')
        new_font = QFont("Arial", 18, QFont.Bold)
        self.input_label.setFont(new_font)
        self.input_label.adjustSize()
        self.input_label.setAlignment(Qt.AlignCenter)

        # Right Textbox heading label
        self.output_label = QLabel(self, text='Final Result')
        new_font = QFont("Arial", 18, QFont.Bold)
        self.output_label.setFont(new_font)
        self.output_label.adjustSize()
        self.output_label.setAlignment(Qt.AlignCenter)


        # Setting the logo or picture in the middle
        pixmap = QPixmap(os.getcwd() + "/summarize.png").scaled(180, 180, Qt.KeepAspectRatio)
        pic = QLabel(self)
        # pic.setGeometry(310, 55, 180, 288)
        pic.setPixmap(pixmap)
        pic.setAlignment(Qt.AlignCenter)

        # The layout for proper padding of the button
        summarize_pad_layout = QHBoxLayout()
        summarize_pad_layout.addStretch()
        summarize_pad_layout.addWidget(self.summarize_button)
        summarize_pad_layout.addWidget(self.method)
        summarize_pad_layout.addWidget(self.cb)
        summarize_pad_layout.addStretch()
        summarize_pad_layout.addWidget(self.select_Lang)
        summarize_pad_layout.addStretch()
        


        # Middle layout of the grid
        middle_layout = QVBoxLayout()
        middle_layout.addWidget(pic)
        middle_layout.addLayout(summarize_pad_layout)
        

        # The main Grid Layout
        main_grid_layout = QGridLayout()
        main_grid_layout.addWidget(self.input_label, 0, 0)
        
        main_grid_layout.addWidget(self.output_label, 0, 2)
        main_grid_layout.addLayout(middle_layout, 1, 1)
        main_grid_layout.addWidget(self.textbox_input, 1, 0)
        main_grid_layout.addWidget(self.textbox_output, 1, 2)
        main_grid_layout.addWidget(self.file_open_button, 2, 0, alignment=Qt.AlignLeft)
        main_grid_layout.addWidget(self.file_Image, 2, 1, alignment=Qt.AlignLeft)
        main_grid_layout.addWidget(self.audio_button, 2, 1, alignment=Qt.AlignRight)
        main_grid_layout.addWidget(self.quit_button, 2, 2, alignment=Qt.AlignRight)

        # Menu bar Commands start
        # Open file menu
        menu_open_file = QAction("&Open File", self)
        menu_open_file.setShortcut("Ctrl+O")
        menu_open_file.setStatusTip('Open from text file')
        menu_open_file.triggered.connect(self.file_open)

       

        # Exit menu
        menu_exit = QAction("&Exit", self)
        menu_exit.setShortcut("Ctrl+Q")
        menu_exit.setStatusTip('Exit the program')
        menu_exit.triggered.connect(self.exit_application)

        # Font Choice for input textbox
        font_choice_input = QAction('&Input Font', self)
        font_choice_input.triggered.connect(self.input_font_choice)

        # Font Choice for output textbox
        font_choice_output = QAction('&Output Font', self)
        font_choice_output.triggered.connect(self.output_font_choice)

        self.statusBar()

        # The File menu option
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&File')
        file_menu.addAction(menu_open_file)
        file_menu.addAction(menu_exit)

        # The Edit menu option
        main_menu = self.menuBar()
        file_menu = main_menu.addMenu('&Edit')
        file_menu.addAction(font_choice_input)
        file_menu.addAction(font_choice_output)

        self.wid.setLayout(main_grid_layout)
        self.show()

    # Open file Function
    # Opens Dialog Box to open the file and select text
    # If file is of valid readable format, displays the contents on the left text box
    # Else throws a warning dialog box and prompts to either chose again else cancel
    def file_open(self):
        # noinspection PyBroadException
        try:
            path = QFileDialog.getOpenFileName(self, 'Open File')
            
            file = open(path[0], 'r')
            self.file_text = file.read()
            self.textbox_input.setPlainText(self.file_text)

            return self.file_text
        except Exception as e:
            print('Error Reported:', e)
            message_box = QMessageBox.warning(self, 'Error!', 'File Open Error! Please Choose Valid File!',
                                              QMessageBox.Ok | QMessageBox.Cancel)
            if message_box == QMessageBox.Ok:
                self.file_open()
            else:
                pass
            
    def Image_Open(self):
        name = QFileDialog.getOpenFileName(self,("Open Image"),"",("Image Files (*.png *.jpg *jpeg *.bmp)"))
        if name != ('', ''):
            image_text=imgToText.Eval(name[0])
            print(image_text)
            self.textbox_input.setPlainText(image_text)

            
    def convert(self):
        
        if(self.my_output!=""):
            
            print(self.language)
            myobj = gTTS(text=self.my_output, lang=self.language,slow=False)
            text, ok = QInputDialog.getText(self, 'Text Input Dialog', 'Enter File Name To Save:')
            if ok:
                myobj.save(str(text)+".mp3")
        else:
            print("No Text Found")
     #  os.system("mpg321 project2.mp3").


    # Takes the input from the left textbox, summarize that and display on the right text box
    def summarize(self):
        self.my_text = self.textbox_input.toPlainText()
        if(self.my_text==''):
                QMessageBox.warning(self, 'Error!', "Please Input Text!",
                                QMessageBox.Ok)
       
        if(self.method.currentText()=="Extractive"):
            self.n, ok = QInputDialog.getInt(self, 'Input', 'Enter Expected Sentence You Want:')
            if(self.n<=0):
                QMessageBox.warning(self, 'Error!', "Wrong Input!",
                                QMessageBox.Ok)
            if ok:
                self.my_output=Extractive_Summarizer.summary_text(test_text=self.my_text,n=self.n)
                self.textbox_output.setPlainText(self.my_output) 
           
        if(self.method.currentText()=="Abstractive"):
            self.my_output=Abstractive.abstractive(self.my_text)
            self.textbox_output.setPlainText(self.my_output) 
   
    def Lang_Select(self):
        self.language=self.cb.currentText()
        if(self.language=='Hindi'):
            self.language='hi';
        if(self.language=='Marathi'):
            self.language='mr'
        if(self.language=='Tamil'):
            self.language='ta'
        text=self.my_output
        translator=google_translator()
        result = translator.translate(text,lang_tgt=self.language)
        print(result)
        self.textbox_output.setPlainText(result) 
        
            
      
    # Exit Definition. Runs when the app is Quit using the 'Quit' button
    def exit_application(self):
        print(self.exit_text)
        sys.exit()

    # Reserve function for the selection box to have option to chose number of lines (unused)
    def selection_box(self):
        print('Inside selection_box')
        combo_box = QComboBox(self)
        for i in range(self.sent_num):
            item_text = str(i + 1) + ' Lines'
            combo_box.addItem(item_text)
        combo_box.move(365, 300)
        qApp.processEvents()

    # Font Selection for the input textbox
    def input_font_choice(self):
        font, ok = QFontDialog.getFont(self.textbox_input.font(), self)
        if ok:
            # QApplication.setFont(font)
            self.textbox_input.setFont(font)
            print("Display Fonts", font)

    # Font Selection for the output textbox
    def output_font_choice(self):
        font, ok = QFontDialog.getFont(self.textbox_output.font(), self)
        if ok:
            # QApplication.setFont(font)
            self.textbox_output.setFont(font)
            print("Display Fonts", font)

  


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Window()
    # GUI.show()
    sys.exit(app.exec_())


