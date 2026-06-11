import sys
import subprocess
import shutil
from pathlib import Path
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget, 
    QMessageBox, QDialog, QPushButton, QHBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon
from converter import convert_skill

class SuccessDialog(QDialog):
    def __init__(self, parent=None, success_count=0, last_dest_dir=None):
        super().__init__(parent)
        self.setWindowTitle("변환 완료 🎉")
        self.setFixedSize(350, 150)
        self.setStyleSheet("""
            QDialog {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            }
            QPushButton {
                background-color: #007aff;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #005bb5;
            }
            QPushButton#closeBtn {
                background-color: #e5e5ea;
                color: #333333;
            }
            QPushButton#closeBtn:hover {
                background-color: #d1d1d6;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        
        msg_label = QLabel(f"성공적으로 {success_count}개의 스킬을 변환했습니다!\n변환된 결과물은 원본 위치에 '_hermes' 이름으로 생성되었습니다.")
        msg_label.setWordWrap(True)
        msg_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(msg_label)

        btn_layout = QHBoxLayout()
        
        close_btn = QPushButton("닫기")
        close_btn.setObjectName("closeBtn")
        close_btn.clicked.connect(self.accept)
        
        download_btn = QPushButton("ZIP 다운로드")
        download_btn.clicked.connect(lambda: self.download_zip(last_dest_dir))
        
        open_btn = QPushButton("결과 폴더 열기")
        open_btn.clicked.connect(lambda: self.open_folder(last_dest_dir))
        
        btn_layout.addStretch()
        btn_layout.addWidget(close_btn)
        btn_layout.addWidget(download_btn)
        btn_layout.addWidget(open_btn)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        
    def download_zip(self, dest_dir):
        if not dest_dir or not dest_dir.exists():
            return
            
        default_name = f"{dest_dir.name}.zip"
        save_path, _ = QFileDialog.getSaveFileName(
            self, 
            "ZIP 파일로 저장", 
            default_name,
            "Zip Files (*.zip)"
        )
        
        if save_path:
            # save_path might include .zip already, make_archive adds .zip if not careful, 
            # so we strip it to pass the base name.
            base_name = save_path
            if base_name.endswith('.zip'):
                base_name = base_name[:-4]
                
            try:
                shutil.make_archive(base_name, 'zip', str(dest_dir))
                QMessageBox.information(self, "다운로드 완료", f"성공적으로 다운로드 되었습니다:\n{save_path}")
            except Exception as e:
                QMessageBox.critical(self, "다운로드 실패", f"압축 중 오류가 발생했습니다:\n{str(e)}")
                
    def open_folder(self, dest_dir):
        if dest_dir and dest_dir.exists():
            subprocess.run(["open", str(dest_dir)])
        self.accept()

class DragDropArea(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setText("📦\n여기로 Openclaw 스킬\n(.skill 파일 또는 폴더)을\n드래그 앤 드롭 하세요")
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.default_style = """
            QLabel {
                border: 2px dashed #c7c7cc;
                border-radius: 12px;
                font-size: 18px;
                font-weight: 500;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                color: #8e8e93;
                background-color: #f2f2f7;
                margin: 20px;
                padding: 40px;
                line-height: 1.5;
            }
            QLabel:hover {
                background-color: #e5e5ea;
                border-color: #aeaeb2;
            }
        """
        self.hover_style = """
            QLabel {
                border: 3px dashed #007aff;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
                color: #007aff;
                background-color: #e5f0ff;
                margin: 20px;
                padding: 40px;
                line-height: 1.5;
            }
        """
        
        self.setStyleSheet(self.default_style)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()
            self.setStyleSheet(self.hover_style)
            self.setText("✨\n이제 마우스를 놓아주세요!")
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet(self.default_style)
        self.setText("📦\n여기로 Openclaw 스킬\n(.skill 파일 또는 폴더)을\n드래그 앤 드롭 하세요")

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if urls:
            event.acceptProposedAction()
            self.dragLeaveEvent(event) # Reset style and text
            
            success_count = 0
            errors = []
            last_dest_dir = None
            
            for url in urls:
                local_path = Path(url.toLocalFile())
                if not local_path.exists():
                    continue
                
                # Auto-generate destination
                name = local_path.stem if local_path.is_file() else local_path.name
                dest_dir = local_path.with_name(f"{name}_hermes")
                
                try:
                    convert_skill(local_path, dest_dir)
                    success_count += 1
                    last_dest_dir = dest_dir
                except Exception as e:
                    errors.append(f"{local_path.name}: {str(e)}")

            if errors:
                error_msg = "다음 파일들을 변환하는 중 오류가 발생했습니다:\n\n" + "\n".join(errors)
                QMessageBox.critical(self, "변환 오류", error_msg)
            elif success_count > 0:
                dialog = SuccessDialog(self, success_count, last_dest_dir)
                dialog.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Openclaw ➔ Hermes 변환기")
        self.setMinimumSize(450, 350)
        self.setStyleSheet("QMainWindow { background-color: #ffffff; }")
        
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        
        self.drop_area = DragDropArea(self)
        layout.addWidget(self.drop_area)
        
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    
    # Optional: try to set a nice app font globally
    font = QFont("-apple-system", 13)
    app.setFont(font)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
