from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap, QPainter, QPen, QMouseEvent, QColor
from PyQt6.QtCore import pyqtSignal, Qt

class ChoiceWidget(QLabel):
    onclick = pyqtSignal()

    def __init__(self, story="Tails", ban=False, **args):
        super().__init__(*args)

        self.story = story
        self.ban = ban

        self.setFixedSize(40, 40)
        self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.setScaledContents(True)
        self.updatePixmap()

    def updatePixmap(self):
        """Loads the base icon and triggers a repaint."""
        self.setPixmap(QPixmap(f'res/{self.story.replace(" ", "").lower()}.png'))
        self.repaint()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.onclick.emit()

    def paintEvent(self, event):
        """Overrides the default paint event to draw the red cross with black outline and a red-bordered frame."""
        super().paintEvent(event)

        if self.ban:
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            # Black outline (thicker than red lines)
            outline_pen = QPen(Qt.GlobalColor.black, 10)
            painter.setPen(outline_pen)

            painter.drawLine(0, 0, self.width(), self.height())
            painter.drawLine(0, self.height(), self.width(), 0)

            painter.drawRect(3, 3, self.width() - 6, self.height() - 6)

            # Red cross
            thickness = 6
            red_pen = QPen(QColor("#d20f39"), thickness)
            painter.setPen(red_pen)
            painter.drawLine(0, 0, self.width(), self.height())
            painter.drawLine(0, self.height(), self.width(), 0)

            # Red border
            painter.drawRect(thickness // 2, thickness // 2, self.width() - thickness, self.height() - thickness)
