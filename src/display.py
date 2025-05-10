from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QMainWindow, QSpacerItem, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, QObject, QRect
from PyQt6.QtGui import QFont, QIcon

from wheel_widget import WheelSpinnerWidget
from choice_widget import ChoiceWidget
from draft import DraftController
from splits import generate_livesplit_file, generate_split_names_txt


class MainWindow(QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller if controller else DraftController()
        self.controller.draft_updated.connect(self.update_ui)

        self.setWindowTitle("SADX Small Stories Ultimate Draft")
        self.setFixedSize(1280, 720)
        self.setContentsMargins(20, 20, 20, 20)
        self.setStyleSheet("background-color: #FF00FF; color: #FFFFFF;")
        self.setWindowIcon(QIcon("res/big.png"))

        self.status_label = QLabel()
        self.status_label.setFont(QFont('ITC Eras', 32, 500))
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFixedHeight(60)

        self.picked_stories = QHBoxLayout()
        self.picked_stories.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.picked_stories.setSpacing(32)
        self.picked_stories.addItem(QSpacerItem(0, 80, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum))

        self.wheel = WheelSpinnerWidget(self.controller.choices, self.controller.colors)
        self.wheel.resultSignal.connect(self.controller.wheel_result)
        self.controller.wheel_spun.connect(self.wheel.spin)

        self.layout = QHBoxLayout()
        self.p1_layout = QVBoxLayout()
        self.center_layout = QVBoxLayout()
        self.p2_layout = QVBoxLayout()

        self.center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.p1_layout.setSpacing(32)
        self.p2_layout.setSpacing(32)

        self.p1_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.p2_layout.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)

        self.p1_label = QLabel("Player 1")
        self.p1_label.setFont(QFont('ITC Eras', 32, 400))
        self.p1_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.p1_layout.addWidget(self.p1_label)

        self.control_layout = QHBoxLayout()

        self.spin_button = QPushButton("Spin")
        self.spin_button.setFixedSize(100, 40)
        self.spin_button.clicked.connect(self.wheel.spin)
        self.control_layout.addWidget(self.spin_button)

        self.reset_button = QPushButton("Reset")
        self.reset_button.setFixedSize(100, 40)
        self.reset_button.clicked.connect(self.controller.reset_draft)
        self.control_layout.addWidget(self.reset_button)

        self.undo_button = QPushButton("Undo")
        self.undo_button.setFixedSize(100, 40)
        self.undo_button.clicked.connect(self.controller.undo_last_action)
        self.control_layout.addWidget(self.undo_button)

        self.center_layout.addWidget(self.status_label)
        self.center_layout.addItem(QSpacerItem(0, 32, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.center_layout.addLayout(self.picked_stories)
        self.center_layout.addItem(QSpacerItem(0, 32, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum))
        self.center_layout.addWidget(self.wheel)
        self.center_layout.addItem(QSpacerItem(0, 32, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        self.center_layout.addLayout(self.control_layout)

        self.choice_buttons = []
        for story in self.controller.choices:
            button = ChoiceWidget(story)
            button.onclick.connect(lambda story=story: self.controller.make_choice(story))
            self.control_layout.addWidget(button)
            self.choice_buttons.append(button)

        self.p2_label = QLabel("Player 2")
        self.p2_label.setFont(QFont('ITC Eras', 32, 400))
        self.p2_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        self.p2_layout.addWidget(self.p2_label)

        self.layout.addLayout(self.p1_layout)
        self.layout.addLayout(self.center_layout)
        self.layout.addLayout(self.p2_layout)

        self.main_widget = QWidget()
        self.main_widget.setLayout(self.layout)
        self.setCentralWidget(self.main_widget)

        self.picked_widgets = []
        self.p1_widgets = []
        self.p2_widgets = []
        self.update_ui()

    def update_ui(self):
        self.status_label.setText(self.controller.draft_phases[self.controller.draft_phase])
        
        for widget in self.p1_widgets:
            self.p1_layout.removeWidget(widget)
            widget.deleteLater()
        
        for widget in self.p2_widgets:
            self.p2_layout.removeWidget(widget)
            widget.deleteLater()

        for widget in self.picked_widgets:
            self.picked_stories.removeWidget(widget)
            widget.deleteLater()
        
        self.p1_widgets.clear()
        self.p2_widgets.clear()
        self.picked_widgets.clear()

        for widget in self.choice_buttons:
            if widget.story not in self.controller.available_choices():
                widget.disable()
            else:
                widget.enable()

        if self.controller.draft_phase == 0:
            self.spin_button.setEnabled(True)
        else:
            self.spin_button.setEnabled(False)

        for story in self.controller.picks:
            choice_widget = ChoiceWidget(story)
            choice_widget.setFixedSize(80, 80)
            self.picked_stories.addWidget(choice_widget, alignment=Qt.AlignmentFlag.AlignCenter)
            self.picked_widgets.append(choice_widget)

        for story, choice_type in self.controller.p1_choices:
            choice_widget = ChoiceWidget(story, choice_type == "ban")
            choice_widget.setFixedSize(80, 80)
            self.p1_layout.addWidget(choice_widget)
            self.p1_widgets.append(choice_widget)

        for story, choice_type in self.controller.p2_choices:
            choice_widget = ChoiceWidget(story, choice_type == "ban")
            choice_widget.setFixedSize(80, 80)
            self.p2_layout.addWidget(choice_widget, alignment=Qt.AlignmentFlag.AlignRight)
            self.p2_widgets.append(choice_widget)
        
        if self.controller.draft_phase >= 5:
            self.output_splits()

    def output_splits(self):
        # generate_livesplit_file(self.controller.picks)
        generate_split_names_txt(self.controller.picks)

        if "Gamma" in self.controller.picks:
            # generate_livesplit_file(self.controller.picks, glitched_gamma=False)
            generate_split_names_txt(self.controller.picks, glitched_gamma=False)
