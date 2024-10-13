import sys
from PyQt5.QtWidgets import QProgressBar,QMainWindow, QFileDialog,QInputDialog,  QApplication, QWidget, QPushButton, QToolTip, QAction, qApp, QFileDialog
from PyQt5.QtGui import QIcon
import pyautogui
import time
from pynput import mouse
import PyQt5
from PIL import Image

page = 0   # 찍을 페이지 수  
picture_size = [] #왼쪽 상단 좌표 , 오른쪽 하단 좌표

next_page = []  #다음 페이지의 좌표
msg = "순서대로 진행하세요. 버튼에 마우스를 올리면 설명이 나옵니다."

def get_mouse_point(x, y, button, pressed):
    if pressed and button==mouse.Button.left: 
        print('Location input : ', (x, y))
        picture_size.append(x)
        picture_size.append(y)
    return False







# def png_to_pdf(fname):
#     imglist = []
    
#     # Open the first image and use it as the base for saving the PDF
#     img_0 = Image.open(fname[0]).convert("RGB")
    
#     # Loop through the remaining images starting from the second one
#     for file in fname[1:]:
#         img = Image.open(file).convert("RGB")
#         imglist.append(img)
    
#     # Save the PDF with the first image as the base and append the rest
#     img_0.save('New_pdf.pdf', save_all=True, append_images=imglist)


# def png_to_pdf(fname):
#     imglist = []
#     for idx, file in enumerate(fname):
#         globals()['img_{}'.format(idx)] = (Image.open(file)).convert("RGB")
#         imglist.append(globals()['img_{}'.format(idx)])
#     img_0.save('New_pdf.pdf',save_all=True, append_images=imglist)

def get_next_page(x, y, button, pressed):
    if pressed and button==mouse.Button.left: 
        next_page.append((x, y))
        
    return False
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ebook_To_Pdf')
        self.statusBar().showMessage(msg)
        #--------ProgressBar
        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 300, 200, 40)
        self.pbar.setValue(0)
# 앞의 두 매개변수는 창의 x, y 위치를 결정하고, 뒤의 두 매개변수는 각각 창의 너비와 높이를 결정합니다.
        openFile = QAction('Open', self)
        openFile.setShortcut('Ctrl+O')
        openFile.setStatusTip("open new file")
        openFile.triggered.connect(self.show_file)

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        filemenu = menubar.addMenu('&★Convert to PDF')
        filemenu.addAction(openFile)
        page_btn = QPushButton('1.Pages that will get captured', self)
        page_btn.resize(page_btn.sizeHint())
        page_btn.move(30, 50)
        page_btn.clicked.connect(self.page_input)

        btn_start_point = QPushButton('2.Save top left corner location', self)
        btn_start_point.setToolTip('Click after locating the mouse over the top left corner of the image ')
        btn_start_point.move(30,100)
        btn_start_point.resize(btn_start_point.sizeHint())
        btn_start_point.clicked.connect(self.Event_start_point)
        
        btn_end_point = QPushButton('3.Save bottom right corner location', self)
        btn_end_point.setToolTip('Click after locating the mouse over the bottom right corner of the image')
        btn_end_point.move(30,150)
        btn_end_point.resize(btn_end_point.sizeHint())
        btn_end_point.clicked.connect(self.Event_end_point)

        btn_next_page = QPushButton('4.Save next page button location', self)
        btn_next_page.setToolTip('Click after locating the mouse over the button to move to the next page.')
        btn_next_page.move(30,200)
        btn_next_page.resize(btn_next_page.sizeHint()) 
        btn_next_page.clicked.connect(self.Event_next_page)

        btn_run = QPushButton('5.Run', self)
        btn_run.setToolTip('It is captured as is on the screen. Please make sure no other programs are hiding the image.')
        btn_run.move(30, 250)
        btn_run.resize(btn_run.sizeHint()) 
        btn_run.clicked.connect(self.get_picture)
        self.setGeometry(400,400,500,500)
        self.show()
    def page_input(self):
        global page , picture_size
        picture_size = []
        page, ok = QInputDialog.getText(self, 'Input Dialog', '찍을 페이지 수:')
        if ok:
            page = int(page)
            msg = "찍을 페이지 수 : %d, 예상 소요시간 : %f초"%(page, page*0.8)
            self.status(msg)
            self.pbar.setValue(15)






    def png_to_pdf(self, fname):
        imglist = []

        # Open the first image and use it as the base for saving the PDF
        img_0 = Image.open(fname[0]).convert("RGB")
        
        total_files = len(fname)  # Total number of images to process
        progress_step = 100 // total_files  # Step for each image to increase progress bar

        # Loop through the remaining images starting from the second one
        for idx, file in enumerate(fname[1:], start=1):
            img = Image.open(file).convert("RGB")
            imglist.append(img)

            # Update the progress bar after processing each file
            self.pbar.setValue(progress_step * idx)
            QApplication.processEvents()  # Process UI events to refresh the progress bar

        # Save the PDF with the first image as the base and append the rest
        img_0.save('New_pdf.pdf', save_all=True, append_images=imglist)

        # Set progress bar to 100 when done
        self.pbar.setValue(100)

        # Display "Complete" in the status bar
        self.statusBar().showMessage("PDF creation complete!")

    def show_file(self):
        fname = QFileDialog.getOpenFileNames(self, 'Open file', './')
        
        if fname[0]:
            # Sort files numerically
            fname[0].sort(key=self.natural_sort_key)

            # Pass 'self' to the function to update progress bar and status
            self.png_to_pdf(fname[0])





    def natural_sort_key(self, file_name):
        import re
        # Extract numeric part of the file name
        return [int(text) if text.isdigit() else text for text in re.split(r'(\d+)', file_name)]

    # def show_file(self):
    #     fname = QFileDialog.getOpenFileNames(self, 'Open file' , './')
    #     # Sort files based on numeric order in the file names
    #     if fname[0]:
    #         fname[0].sort(key=self.natural_sort_key)
    #         png_to_pdf(fname[0])

    # def show_file(self):
    #     fname = QFileDialog.getOpenFileNames(self, 'Open file' , './')
    #     fname[0].sort()
    #     if fname[0]:
    #         png_to_pdf(fname[0])

    def status(self,msg):
        self.statusBar().showMessage(msg)

    def Event_start_point(self):
        with mouse.Listener(on_click=get_mouse_point) as listener:
            listener.join()
            msg = "좌측 상단 좌표 : (%s, %s)"%(picture_size[0],picture_size[1])
            self.status(msg)
            self.pbar.setValue(30)

    def Event_end_point(self):
        with mouse.Listener(on_click=get_mouse_point) as listener:
            listener.join()
            msg = "우측 하단 좌표 : (%s, %s)"%(picture_size[0],picture_size[1])
            self.status(msg)
            self.pbar.setValue(45)
    def Event_next_page(self):
        with mouse.Listener(on_click=get_next_page) as listener:
            listener.join()
            msg = "'다음페이지'버튼 좌표 : %s"%next_page
            self.status(msg)
            self.pbar.setValue(60)
            
    def get_picture(self):
        rest_of_percent = 40//page
        for i in range(page):
            if len(picture_size) >= 4:
                pyautogui.screenshot("%s.png" % i, region=(picture_size[0], picture_size[1],
                picture_size[2]-picture_size[0],picture_size[3]-picture_size[1]))
            pyautogui.click(*next_page)
            rest_of_percent += 40//page
            self.pbar.setValue(60+rest_of_percent)
            
            # wait before screenshot
            time.sleep(0.8)
            # time.sleep(0.5)
        self.pbar.setValue(100)
        msg = "Image Capture Complte. Convert to PDF file as cliking a button of Convert to PDF!"
        self.status(msg)
if __name__ == '__main__':
   app = QApplication(sys.argv)
   ex = MyApp()
   sys.exit(app.exec_())
