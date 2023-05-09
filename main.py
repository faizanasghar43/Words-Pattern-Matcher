import string
import sys
import nltk
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QTextEdit, QGridLayout, QVBoxLayout, \
    QPushButton, QSplitter, QScrollArea, QMessageBox, QComboBox, QLineEdit, QHBoxLayout, QListWidget, QSizePolicy
from nltk import word_tokenize
from nltk.corpus import stopwords


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Define the list of keywords
        self.keywords = []
        self.setWindowTitle("Keyword Searcher")
        # Create the widgets
        self.keyword_labels = [QLabel(keyword) for keyword in self.keywords]
        text_edit = QTextEdit()
        find_button = QPushButton("Find Pattern")
        # Create the grid layout for the keywords section
        self.grid_layout = QGridLayout()
        for i, keyword_label in enumerate(self.keyword_labels):
            self.grid_layout.addWidget(keyword_label, i + 1, 0)
        # Create a scroll area widget for the keywords section
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(QWidget())
        scroll_area.widget().setLayout(self.grid_layout)
        # scroll_area.setStyleSheet("QScrollArea { border: none; }")
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
            }
            QScrollBar:horizontal {
                border: none;
                background: black;
                height: 14px;
            }
            QScrollBar::handle:horizontal {
                background: gray;
                min-width: 20px;
            }
            QScrollBar::add-line:horizontal {
                border: none;
                background: none;
            }
            QScrollBar::sub-line:horizontal {
                border: none;
                background: none;
            }
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {
                background: none;
            }
            QScrollBar:vertical {
                border: none;
                background: black;
                width: 14px;
            }
            QScrollBar::handle:vertical {
                background: gray;
                min-height: 20px;
            }
            QScrollBar::add-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::sub-line:vertical {
                border: none;
                background: none;
            }
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
                background: none;
            }
        """)
        # Create a vertical layout for the right pane
        vbox_layout = QVBoxLayout()
        vbox_layout1 = QVBoxLayout()
        vbox_layout.addWidget(find_button)
        vbox_layout.addWidget(text_edit)

        # vbox_layout1.insertWidget(0, label1)
        # vbox_layout1.addLayout(self.grid_layout)
        # Create a splitter widget to divide the window into two panes
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(scroll_area)
        splitter.addWidget(QWidget())
        splitter.setSizes([250, 550])
        splitter.setStyleSheet("QSplitter::handle { background-color: gray }")
        splitter.widget(1).setLayout(vbox_layout)
        splitter.widget(0).setLayout(vbox_layout1)

        # Set the splitter as the main widget
        self.setCentralWidget(splitter)
        self.word_count_combo = QLineEdit()
        self.word_count_combo_label = QLabel('Write No of Words Pattern')
        # add default items to the combo box
        self.word_count_combo.setText("2")
        # Set the window properties for responsiveness
        self.setMinimumWidth(800)
        self.setMinimumHeight(600)
        self.resize(900, 600)
        button_style = """
        QPushButton {
            background-color: #008771;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px;
        }

        QPushButton:hover {
            background-color: black;git switch -c
        }
        """
        find_button.setStyleSheet(button_style)
        find_button.setFixedSize(105, 55)
        # Create a dictionary to keep track of the number of occurrences of each pattern
        self.pattern_counts = {}
        # Connect the find_button widget to the search_for_keywords method
        find_button.clicked.connect(self.func)
        # vbox_layout.addWidget(self.word_count_combo_label)
        # vbox_layout.addWidget(self.word_count_combo)
        # # Store the QTextDocument of the QTextEdit widget
        self.text_document = text_edit.document()
        self.list_widget = QListWidget()
        self.grid_layout.addWidget(self.list_widget, 0, 0)
        self.list_widget.setMaximumHeight(460)
        self.list_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)

    def resizeEvent(self, event):
        # Ensure that the splitter widget is always centered and takes up the maximum space available
        self.centralWidget().setGeometry(self.centralWidget().frameGeometry())
        self.centralWidget().widget(0).setMinimumWidth(250)
        self.centralWidget().widget(1).setMinimumWidth(self.width() - 150)

    def func(self):
        self.patterns(self.text_document.toPlainText(), int(self.word_count_combo.text()))
        message_box = QMessageBox()
        message_box.setText("Successfully accomplished")
        message_box.setWindowTitle("Success")
        message_box.setStyleSheet("""
        QPushButton {
            background-color: #008771;
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px;
        }

        QPushButton:hover {
            background-color: black;
        }
        """)
        message_box.exec_()

    def patterns(self, text, min_length=2, max_length=200, excluded_patterns=(' ', '',)):
        # Clear the list widget
        self.list_widget.clear()
        # Tokenize the text into words
        words = word_tokenize(text)
        # Remove stop words (words that do not contribute to the meaning of the text)
        stop_words = set(stopwords.words('english'))
        filtered_words = [word for word in words if
                          word.lower() not in stop_words and not word.isdigit() and word not in string.punctuation]
        # Generate all n-word combinations from the filtered words, where n ranges from min_length to max_length
        all_combinations = []
        for n in range(min_length, max_length + 1):
            combinations = nltk.ngrams(filtered_words, n)
            all_combinations.extend(combinations)
        # Get the frequency distribution of the n-word combinations
        fdist = nltk.FreqDist(all_combinations)
        # Create a set of excluded patterns to filter out
        excluded_set = set(excluded_patterns)
        # Get the most frequent n-word patterns that are not in the excluded set
        top_patterns = [(pattern, count) for pattern, count in fdist.most_common() if
                        all(word not in excluded_set and (
                                    all(c.isalpha() or c.isdigit() for c in word) and len(word) > 1)
                            for word in pattern) and count > 1]
        # Add the new keyword labels to the list widget
        for i, (pattern, count) in enumerate(top_patterns):
            self.list_widget.addItem(f"{' '.join(pattern)} ({count})")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
