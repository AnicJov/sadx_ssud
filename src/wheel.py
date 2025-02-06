from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt, QTimer, QPointF, QRectF, QSize
from PyQt6.QtGui import QPainter, QColor, QFont, QConicalGradient
from PyQt6 import QtCore
import math
import random


class WheelSpinnerWidget(QWidget):
    resultSignal = QtCore.pyqtSignal(str)

    def __init__(self, choices, choice_colors=None, parent=None):
        super().__init__(parent)
        self.choices = choices
        self.choice_colors = choice_colors
        self.angle = 0
        self.is_spinning = False
        self.spin_timer = QTimer()
        self.spin_timer.timeout.connect(self.update_spin)
        self.current_speed = 0
        self.final_angle = 0
        self.result = None
        self.init_ui()

    def init_ui(self):
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Wheel Spinner")

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        rect = self.rect()
        center = QPointF(rect.center())
        radius = min(rect.width(), rect.height()) // 2 - 20

        # Draw the wheel
        slice_angle = 360 / len(self.choices)
        for i, choice in enumerate(self.choices):
            start_angle = self.angle + i * slice_angle

            gradient = QConicalGradient(center, -start_angle)

            if self.choice_colors:
                gradient.setColorAt(0.0, QColor.fromString(self.choice_colors[i]))
                gradient.setColorAt(1.0, QColor.fromString(self.choice_colors[i]))
            else:
                gradient.setColorAt(0.0, QColor.fromHsv((i * 50) % 360, 200, 255))
                gradient.setColorAt(1.0, QColor.fromHsv(((i + 1) * 50) % 360, 200, 255))

            painter.setBrush(gradient)
            painter.setPen(Qt.PenStyle.NoPen)

            # Draw the slice
            painter.drawPie(
                int(center.x() - radius), int(center.y() - radius),
                int(2 * radius), int(2 * radius),
                int(-start_angle * 16), int(-slice_angle * 16)
            )

        # Draw text labels
        painter.setFont(QFont("Arial", 12))
        for i, choice in enumerate(self.choices):
            text_angle = math.radians(self.angle + (i + 2) * slice_angle)
            x = int(center.x() + math.sin(text_angle) * (radius * 0.7))
            y = int(center.y() - math.cos(text_angle) * (radius * 0.7))
            painter.setPen(Qt.GlobalColor.black)
            painter.drawText(QRectF(x - 45, y - 10, 90, 20), Qt.AlignmentFlag.AlignCenter, choice)

        # Draw the pointer
        pointer_size = 20
        painter.setBrush(Qt.GlobalColor.black)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawPolygon(
            QPointF(center.x(), center.y() - radius),
            QPointF(center.x() - pointer_size, center.y() - radius + pointer_size),
            QPointF(center.x() + pointer_size, center.y() - radius + pointer_size)
        )

    def spin(self):
        if self.is_spinning:
            return

        self.is_spinning = True
        self.current_speed = random.uniform(10, 25)  # Initial speed
        self.result = None
        self.spin_timer.start(16)  # ~60 FPS

    def update_spin(self):
        if self.current_speed > 0:
            self.angle = (self.angle + self.current_speed) % 360
            self.current_speed -= 0.05  # Slow down gradually
        else:
            self.is_spinning = False
            self.spin_timer.stop()
            result = int((270 - self.angle) % 360 / (360 / len(self.choices)))
            self.resultSignal.emit(self.choices[result])


        self.update()
