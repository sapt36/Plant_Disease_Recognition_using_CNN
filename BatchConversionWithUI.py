import os
import sys
import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QFileDialog, QScrollArea,
                             QSizePolicy, QDialog, QLineEdit, QFormLayout, QDialogButtonBox, QMessageBox,
                             QProgressDialog)


def convert_cv_to_pixmap(cv_img):
    qformat = QImage.Format_RGB888 if len(cv_img.shape) == 3 else QImage.Format_Grayscale8
    h, w = cv_img.shape[:2]
    img = QImage(cv_img.data, w, h, cv_img.strides[0], qformat)
    if len(cv_img.shape) == 3:  # 如果是彩色圖像，進行 RGB 轉換
        img = img.rgbSwapped()
    pixmap = QPixmap.fromImage(img)
    return pixmap


class ImageProcessingApp(QWidget):

    # 主視窗UI啟動
    def __init__(self):
        super().__init__()
        self.setWindowTitle('圖像處理軟體')
        self.image = None
        self.initUI()
        self.setGeometry(100, 100, 1500, 900)  # 設置視窗尺寸

    # 主視窗UI設置
    def initUI(self):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)  # 置中所有 UI 元素

        # 設置字體
        self.setFont(QFont('微軟正黑體', 12, QFont.Bold))

        # 創建滾動視窗區域
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        # 創建一個容器 widget 放入滾動區域
        container_widget = QWidget(self.scroll_area)
        self.scroll_area.setWidget(container_widget)

        # 創建佈局來居中顯示圖片
        container_layout = QVBoxLayout(container_widget)
        container_layout.setAlignment(Qt.AlignCenter)

        # 顯示圖片的 QLabel
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)  # 置中顯示圖片
        self.image_label.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.image_label.setScaledContents(False)

        # 將 QLabel 添加到容器佈局中
        container_layout.addWidget(self.image_label)

        # 檔名 Label
        self.filename_label = QLabel('圖片預覽：', self)
        self.filename_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.filename_label)

        layout.addWidget(self.scroll_area)


        # 批量調整空間解析度按鈕
        batch_resize_button = QPushButton('批量調整空間解析度', self)
        batch_resize_button.clicked.connect(self.batch_adjust_resolution)
        layout.addWidget(batch_resize_button)

        # 批量轉換為灰階按鈕
        batch_grayscale_button = QPushButton('批量轉換為灰階', self)
        batch_grayscale_button.clicked.connect(self.batch_convert_to_grayscale)
        layout.addWidget(batch_grayscale_button)

        self.setLayout(layout)

    # 將 OpenCV 圖片轉換為 QImage 並顯示，保持原始大小
    def display_image(self, img):
        qformat = QImage.Format_RGB888 if len(img.shape) == 3 else QImage.Format_Grayscale8
        h, w = img.shape[:2]
        img = QImage(img.data, w, h, img.strides[0], qformat)
        img = img.rgbSwapped()  # OpenCV 使用 BGR，因此我們要轉換成 RGB

        # 將圖片轉換為 QPixmap 並顯示，保持圖片原尺寸
        pixmap = QPixmap.fromImage(img)
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedSize(pixmap.size())  # 調整 QLabel 大小以適應圖片原始尺寸

    # 批量調整空間解析度
    def batch_adjust_resolution(self):
        input_folder = QFileDialog.getExistingDirectory(self, '選擇輸入文件夾')
        if not input_folder:
            return

        output_folder = QFileDialog.getExistingDirectory(self, '選擇輸出文件夾')
        if not output_folder:
            return

        dialog = ResolutionDialog(self)
        if dialog.exec_() == QDialog.Accepted:
            scale_factor = dialog.get_value()
            if scale_factor is None:
                return

            # 獲取圖片文件清單
            file_list = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.bmp'))]
            total_files = len(file_list)

            if total_files == 0:
                QMessageBox.warning(self, '無圖片', '選擇的資料夾中沒有可處理的圖片文件。')
                return

            progress_dialog = QProgressDialog('正在調整空間解析度...', '取消', 0, total_files, self)
            progress_dialog.setWindowTitle('處理進度')
            progress_dialog.setWindowModality(Qt.WindowModal)
            progress_dialog.setValue(0)

            first_image = None
            first_image_name = None

            for idx, filename in enumerate(file_list):
                if progress_dialog.wasCanceled():
                    QMessageBox.information(self, '取消', '處理已取消。')
                    return

                input_path = os.path.join(input_folder, filename)
                output_path = os.path.join(output_folder, filename)

                # 讀取並處理圖片
                img = cv2.imread(input_path)
                if img is not None:
                    h, w = img.shape[:2]
                    new_h, new_w = int(h * scale_factor), int(w * scale_factor)
                    resized_img = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_NEAREST)
                    cv2.imwrite(output_path, resized_img)

                    # 記錄第一張處理後的圖片
                    if idx == 0:
                        first_image = resized_img
                        first_image_name = filename

                progress_dialog.setValue(idx + 1)

            if first_image is not None:
                self.display_image(first_image)  # 在 UI 上顯示第一張處理後的圖片
                self.filename_label.setText(f"檔名：{first_image_name}")

            QMessageBox.information(self, '完成', f'圖片已成功調整空間解析度並保存到：{output_folder}')

    # 批量轉換為灰階
    def batch_convert_to_grayscale(self):
        input_folder = QFileDialog.getExistingDirectory(self, '選擇輸入文件夾')
        if not input_folder:
            return

        output_folder = QFileDialog.getExistingDirectory(self, '選擇輸出文件夾')
        if not output_folder:
            return

        file_list = [f for f in os.listdir(input_folder) if f.lower().endswith(('.jpg', '.jpeg', '.bmp'))]
        total_files = len(file_list)

        if total_files == 0:
            QMessageBox.warning(self, '無圖片', '選擇的資料夾中沒有可處理的圖片文件。')
            return

        progress_dialog = QProgressDialog('正在轉換為灰階...', '取消', 0, total_files, self)
        progress_dialog.setWindowTitle('處理進度')
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setValue(0)

        first_image = None
        first_image_name = None

        for idx, filename in enumerate(file_list):
            if progress_dialog.wasCanceled():
                QMessageBox.information(self, '取消', '處理已取消。')
                return

            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 讀取並處理圖片
            img = cv2.imread(input_path)
            if img is not None:
                gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                cv2.imwrite(output_path, gray_img)

                # 記錄第一張處理後的圖片
                if idx == 0:
                    first_image = gray_img
                    first_image_name = filename

            progress_dialog.setValue(idx + 1)

        if first_image is not None:
            self.display_image(first_image)  # 在 UI 上顯示第一張處理後的灰階圖片
            self.filename_label.setText(f"檔名：{first_image_name}")

        QMessageBox.information(self, '完成', f'圖片已成功轉換為灰階並保存到：{output_folder}')


# 創建一個對話框，可輸入參數調整放大或縮小倍數 (0.1 - 5.0)
class ResolutionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('調整圖片大小')
        self.scale_input = QLineEdit(self)
        self.scale_input.setPlaceholderText('倍數 (0.1 - 5.0)')

        form_layout = QFormLayout()
        form_layout.addRow('圖片大小倍數:', self.scale_input)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addWidget(buttons)
        self.setLayout(layout)

    def get_value(self):
        try:
            scale_factor = float(self.scale_input.text())
            if not (0.1 <= scale_factor <= 5.0):
                raise ValueError("倍數必須在 0.1 到 5.0 之間")
            return scale_factor
        except ValueError as e:
            QMessageBox.warning(self, '輸入錯誤', str(e))
            return None


# Main Execution
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ImageProcessingApp()
    window.show()
    sys.exit(app.exec_())
