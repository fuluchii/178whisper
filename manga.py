#coding:utf-8
import os
import sys
from PySide.QtCore import QObject
from PySide.QtGui import (QApplication,QDesktopWidget,QMessageBox,QFileDialog,QFontDialog,QFont)
from PySide.QtUiTools import QUiLoader
from mangaD import get_downloader
import urllib
import threading

__folder__ = os.path.dirname(os.path.abspath(__file__))

class DownloadThered(threading.Thread):
	def __init__(self,task):
		threading.Thread.__init__(self)
		self.task = task

	def run(self):
		self.task()

class DownLoader:
	def __init__(self):
		self.downloader = get_downloader(5)
		ui_file = os.path.join(__folder__,'manga.ui')
		self.main_window = QUiLoader().load(ui_file)
		for widget in self.main_window.findChildren(QObject):
			name=widget.objectName()
			if name.startswith("my_"):
				setattr(self,name,widget)
		self.init_slots();

	def init_slots(self):
		self.my_file_button.clicked.connect(self.filebutton_click)
		self.my_start_button.clicked.connect(self.startbutton_click)


	def filebutton_click(self):
		root_path= QFileDialog.getExistingDirectory(self.main_window,u'test',os.getcwd())
		self.downloader.set_path(root_path)
		self.my_file_edit.setText(root_path)
		print root_path

		

	def startbutton_click(self):
		url = self.my_url_edit.text()
		if not url.startswith('http://manhua.178.com'):
			self.url_error()
			return
		try:
			urllib.urlopen(url)
		except Exception ,e:
			self.url_error()
			return 
		index = url.rfind("/")
		root_url = url[0:index+1]
		first_url = url[index+1:]
		self.my_url_edit.setText(first_url)
		self.downloader.set_url(root_url,first_url)
		self.downloader.set_count(int(self.my_vol_edit.text()))
		t = DownloadThered(self.downloader.start)
		t.start()


	def url_error(self):
		self.my_url_edit.setText(u'无效的地址')
		



def main():
	app = QApplication(sys.argv)
	d = DownLoader()
	d.main_window.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()