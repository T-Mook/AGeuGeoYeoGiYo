from modules.search_result_crawler import search_result_crawler
from modules.handling_excel import excel
from PyQt5.QtWidgets import QVBoxLayout, QMessageBox, QApplication, QSpinBox, QWidget, QDesktopWidget, QPushButton, QHBoxLayout, QLineEdit, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
import sys
import time
import os
import json # ref: https://docs.python.org/ko/3/library/json.html


### ref
# https://wikidocs.net/38024

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):

        # Make Label of text box
        lbl1 = QLabel('검색어:', self)
        lbl2 = QLabel('페이지 수:', self)

        # Make Text COntent
        text_notice_title = "<br />※ 본 프로그램은 단순 조사를 돕기 위해서만 배포 및 업데이트"
        notices = QLabel(text_notice_title, self)

        # notice title set
        notices.setAlignment(Qt.AlignCenter)
        noticies_font = notices.font()
        noticies_font.setPointSize(10)
        noticies_font.setBold(False)

        notices.setFont(noticies_font) # Set
        notices.setStyleSheet(
            "color: black;"
        ) # color or other css set

        # notice content set
        text_notice_content =  \
            "1. 짧은 시간 내 과도한 반복 사용 X (검색 대상 서비스에 과부하 시 법적 문제 가능성)<br />\
            2. 본 프로그램과 결과물의 수익 목적 사용 금지<br /><br />\
            *문의: msp770@gmail.com"
        notice_contents = QLabel(text_notice_content, self)
        # notice_contents.setAlignment(Qt.AlignCenter)
        notice_contents_font = notice_contents.font()
        notice_contents_font.setPointSize(8)
        
        notice_contents.setFont(notice_contents_font) # Set
        notices.setStyleSheet(
            "color: red;"
        ) # color or other css set

        # Make Input text box
        self.te = QLineEdit()
        self.te.setStyleSheet(
            "min-height: 21px;"
            "min-width: 40px;"
            "background-color: white;"
	        "color: rgb(58, 134, 255);" # light blue
            "border: 1px solid rgb(58, 134, 255);" # light blue
	        "border-radius: 5px;"
        )

        # Whenever text in the text editor is modified, the text_changed method is called
        # self.te.textChanged.connect(self.text_changed)

        # Make Push Btn
        pushBtn = QPushButton(self)
        pushBtn.setText('검색')
        pushBtn.setStyleSheet(
            "min-height: 21px;"
            "min-width: 40px;"
            "background-color: white;"
	        "color: rgb(58, 134, 255);" # light blue
            "border: 1px solid rgb(58, 134, 255);" # light blue
	        "border-radius: 5px;"
        )

        # Make Spin box
        self.spinbox = QSpinBox()
        self.spinbox.setMinimum(1)
        self.spinbox.setMaximum(5)

        ### Make Layout
        # Horizon box
        hbox_searchbar = QHBoxLayout()
        hbox_searchbar.addStretch(1)
        hbox_searchbar.addWidget(lbl1)
        hbox_searchbar.addWidget(self.te)
        hbox_searchbar.addWidget(lbl2)
        hbox_searchbar.addWidget(self.spinbox)
        hbox_searchbar.addWidget(pushBtn)
        hbox_searchbar.addStretch(1)

        vbox_notice = QVBoxLayout()
        vbox_notice.addStretch(1)
        vbox_notice.addWidget(notices)
        vbox_notice.addWidget(notice_contents)
        vbox_notice.addStretch(1)

        # Vertical box
        vbox = QVBoxLayout()
        vbox.addLayout(hbox_searchbar)
        vbox.addLayout(vbox_notice)
        
        self.setLayout(vbox)

        # Signal : Push btn
        try:
            pushBtn.clicked.connect(self.activateCrawler)

        except Exception as ex:
            errorTitle = '오류 발생'
            errorMsg = str(ex)

            QMessageBox.critical(self, errorTitle, errorMsg)

        # Basic Window Settings
        self.setWindowTitle('아그거여기요') # 제목
        self.setWindowIcon(QIcon('icon.png'))
        # self.setGeometry(300, 300, 300, 200)
        self.resize(400, 35)
        self.center()
        self.show()


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


    def activateCrawler(self):
        search_question = "[" + str(self.te.text()) + "]로 [" + str(self.spinbox.value()) + "] 페이지" + " 검색할까요?"
        option = QMessageBox.question(self, "알림", search_question,
            QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Yes)
        
        if option == QMessageBox.Yes:
            self.crawler_and_excel()


    def activateAlert(self, text):
        QMessageBox.information(self, "알림", str(text))


    def crawler_and_excel(self):

        # ---------------[ Get Keyword and requesters ] -------------
        keyword = self.te.text()
        pages = self.spinbox.value()
        
        base_dir = os.path.dirname(os.path.realpath(__file__))
        file_basic_name = "keyword_search_results" # file name
        
        ### [ Run : crawling ] ----------------------------------------------
        
        crawler = search_result_crawler(search_keyword= keyword, pages= pages)
        crawler.run_all()
        result = crawler.result
        
        ### [ Set Save dir and file name ] ----------------------------------------------
        
        time_string = str(time.strftime('%Y%m%d%H%M', time.localtime(time.time())))
        file_name = file_basic_name + "_" + keyword + "_" + time_string + ".xlsx"
        xlxs_dir = os.path.join(base_dir, file_name)
        
        
        ### [ Run : To Excel File ] ----------------------------------------------
        
        make_excel = excel() # init
        df_list = make_excel.lists_to_dataframes_list(target_lists= result)
        sheet_names_list = [
                'Naver Total News',
                'Daum Total News',
                'Google Total News',
                'Naver VIEW',
            ] # Each sheet names
        
        make_excel.dataframe_to_excelfile_multisheets(
                df_list= df_list, sheet_names_list= sheet_names_list, xlxs_dir= xlxs_dir
            )

        alertText = '검색 & 저장이 완료되었습니다\n\n' + '위치:\n' + str(xlxs_dir)
        self.activateAlert(text= alertText)



if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = App()
    sys.exit(app.exec_())