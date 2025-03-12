import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QFileDialog, QTextEdit, QVBoxLayout, QMessageBox, QFrame
from PyQt6.QtGui import QPixmap, QDragEnterEvent, QDropEvent
from PyQt6.QtCore import Qt
import cv2
import numpy as np
import easyocr
import google.generativeai as genai
from ocr_processor import process_image, analyze_historical_period

# Set up Google AI API Key
genai.configure(api_key="AIzaSyBCuS6N-Rfgleo3WurTfdG35BCb7yRK1O8")

reader = easyocr.Reader(["hi", "en"], gpu=False, model_storage_directory="C:/Users/ameen/.EasyOCR/model/", download_enabled=True)

class OCRApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("AI-Powered OCR for Historical Documents")
        self.setGeometry(100, 100, 600, 500)
        self.setAcceptDrops(True)

        self.label = QLabel("Upload or Drag an Image", self)
        self.label.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(300, 300)
        self.image_label.setFrameShape(QFrame.Shape.Box)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("Extracted text will appear here...")

        self.upload_btn = QPushButton("Upload Image", self)
        self.upload_btn.clicked.connect(self.upload_image)

        self.process_btn = QPushButton("Process OCR", self)
        self.process_btn.clicked.connect(self.process_ocr)
        self.process_btn.setEnabled(False)

        self.save_btn = QPushButton("Save Text", self)
        self.save_btn.clicked.connect(self.save_text)
        self.save_btn.setEnabled(False)

        self.analyze_btn = QPushButton("Analyze Historical Period", self)
        self.analyze_btn.clicked.connect(self.analyze_period)
        self.analyze_btn.setEnabled(False)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.upload_btn)
        layout.addWidget(self.process_btn)
        layout.addWidget(self.text_edit)
        layout.addWidget(self.analyze_btn)
        layout.addWidget(self.save_btn)

        self.setLayout(layout)

    def dragEnterEvent(self, event: QDragEnterEvent):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event: QDropEvent):
        urls = event.mimeData().urls()
        if urls:
            self.image_path = urls[0].toLocalFile()
            self.image_label.setPixmap(QPixmap(self.image_path).scaled(300, 300))
            self.process_btn.setEnabled(True)

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Image", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if file_path:
            self.image_label.setPixmap(QPixmap(file_path).scaled(300, 300))
            self.image_path = file_path
            self.process_btn.setEnabled(True)

    def process_ocr(self):
        if hasattr(self, 'image_path'):
            extracted_text = process_image(self.image_path)
            if extracted_text:
                self.text_edit.setPlainText(extracted_text)
                self.save_btn.setEnabled(True)
                self.analyze_btn.setEnabled(True)
            else:
                QMessageBox.warning(self, "OCR Failed", "No text detected. Try another image.")

    def analyze_period(self):
        text = self.text_edit.toPlainText()
        if text:
            historical_period = analyze_historical_period(text)
            self.text_edit.append(f"\n\n[Historical Analysis]\n{historical_period}")
        else:
            QMessageBox.warning(self, "Analysis Failed", "No text available for analysis.")

    def save_text(self):
        text = self.text_edit.toPlainText()
        if text:
            file_path, _ = QFileDialog.getSaveFileName(self, "Save Text", "", "Text Files (*.txt)")
            if file_path:
                with open(file_path, "w", encoding="utf-8") as file:
                    file.write(text)
                QMessageBox.information(self, "Success", "Text saved successfully.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OCRApp()
    window.show()
    sys.exit(app.exec())