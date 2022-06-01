from PyQt5 import QtCore, QtGui, QtWidgets, uic
import sys
from PyQt5.QtCore import Qt
from motion_capture import *
from PyQt5.QtWidgets import QFileDialog
from Database import Base, create_engine, Capture
from sqlalchemy.orm import sessionmaker

def open_db():
    engine = create_engine('sqlite:///animation.sqlite3')
    Session = sessionmaker(bind=engine)
    sess = Session()
    return sess

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("uis/FrontPage.ui", self)
        # click logic for button
        self.Camera_btn.clicked.connect(self.capture_live)
        self.BrouseVideo_btn.clicked.connect(self.Browse_File)
        self.PreviousVideo_btn.clicked.connect(self.show_saved_content)
        self.Setting_btn.clicked.connect(self.setting_view)

    def capture_live(self):
        # print("clicked")
        motion_capture()


    def Browse_File(self):
        fname,ftype = QFileDialog.getOpenFileName(self, 'Select a video', './','Video (*.mp4 *.avi)')
        motion_capture_video(fname)
        
    def show_saved_content(self):
        files = os.listdir('motion_data')
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Saved Videos")
        layout = QtWidgets.QVBoxLayout()
        if len(files)>0:
            for file in files:
                label = QtWidgets.QLabel(f"📽️ {file}")
                btn = QtWidgets.QPushButton(f"View")
                label.setFont(QtGui.QFont("Sanserif", 18))
                label.color = QtGui.QColor(255, 0, 0)
                layout.addWidget(label)
                layout.addWidget(btn)
                btn.clicked.connect(lambda: self.show_saved_content_file(file))

            dialog.setLayout(layout)
        else:
            label = QtWidgets.QLabel("No saved videos")
            label.setFont(QtGui.QFont("Sanserif", 28))
            layout.addWidget(label)
            dialog.setLayout(layout)
        dialog.exec_()

    def show_saved_content_file(self, file):
        path = os.getcwd()
        osCommandString = f"notepad.exe {path}/motion_data/{file}"
        os.system(osCommandString)

    def setting_view(self):
        dialog = QtWidgets.QDialog()
        dialog.setWindowTitle("Settings")
        layout = QtWidgets.QVBoxLayout()
        label = QtWidgets.QLabel("Settings")
        label.setFont(QtGui.QFont("Sanserif", 28))
        db = open_db()
        count = db.query(Capture).count()
        captureList = db.query(Capture).all()
        # print(captureList, count)
        if count > 0:
            for capture in captureList:
                label = QtWidgets.QLabel(f"{capture.filename}")
                label_time = QtWidgets.QLabel(f"{capture.date}")
                btn = QtWidgets.QPushButton(f"Delete")
                label.setFont(QtGui.QFont("Sanserif", 12))
                layout.addWidget(label)
                layout.addWidget(label_time)
                layout.addWidget(btn)
                btn.clicked.connect(lambda: self.delete_motion_data(capture, dialog))
                dialog.setLayout(layout)
                db.close()
        else:
            label = QtWidgets.QLabel("No saved videos")
            label.setFont(QtGui.QFont("Sanserif", 28))
            layout.addWidget(label)
            dialog.setLayout(layout)
        dialog.exec_()

    def delete_motion_data(self, capture, dialog):
        db = open_db()
        db.delete(capture)
        db.commit()
        try:
            os.unlink(f"{capture.filename}")
        except Exception as e:
            print(e)
        dialog.close()
        self.setting_view()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())