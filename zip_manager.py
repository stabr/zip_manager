#!/python
# -*- coding: utf-8 -*-
'''
File manager to archive project files for outsource

author: Dmitry Stabrov
mailto: fx@dimastabrov.com
mailto: syrbor@gmail.com

'''

import os
import sys
import re
import json
from time import sleep

from PySide.QtCore import *
from PySide.QtGui import *

import zip_archiver
import setup

prj_root = setup.config('project_root')

class ZipManager(QWidget):
    """ZipManager"""
    label_styl = 'QLabel {background-color: rgba(110,250,210,0)}'
    # stl = 'QLineEdit {background-color: rgba(110,250,210,0)}'
    stl = '''
        QWidget {color: rgb(90,150,220);font: 12pt;background-color: rgb(45,45,45)}
        QPushButton {font: 10pt;border: 1px solid rgb(84,84,90);}
        QLineEdit {background-color: rgb(60,60,60); border: 0px}
        QLabel {background-color: rgba(110,250,210,0)}
        QListWidget {background-color: rgb(50,50,50)}
    '''

    def __init__(self):
        super(ZipManager, self).__init__()
        # ui
        self.resize(609, 288)
        self.main_lay = QHBoxLayout()
        # self.main_lay.setContentsMargins(40, 20, 40, 20)
        # self.stl = os.path.join(os.path.dirname(__file__), 'wgt/style.css')
        self.setStyleSheet(self.stl)
        # build UI
        self.entitys_lay = QVBoxLayout()       
        self.file_lst = QListWidget()
        self.file_lst.setMinimumSize(QSize(398, 0))
        self.file_lst.setSelectionMode(QAbstractItemView.MultiSelection)
        # self.file_lst.setMouseTracking(True)
        self.file_lst.setToolTip('Entities')

        self.entitys_lay.addWidget(self.file_lst)
        self.find_le = FindField(self)
        self.find_le.setStyleSheet(self.stl)
        self.entitys_lay.addWidget(self.find_le)

        self.button_lay = QVBoxLayout()
        self.button_lay.setContentsMargins(0, 0, 0, 0)
        self.select_btn = QPushButton('Select')
        self.select_btn.setMinimumSize(QSize(0, 50))
        self.button_lay.addWidget(self.select_btn)
        self.clear_btn = QPushButton('Clear\nSelection')
        self.clear_btn.setMinimumSize(QSize(0, 50))
        self.button_lay.addWidget(self.clear_btn)
        spacerItem = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.button_lay.addItem(spacerItem)
        self.arch_btn = QPushButton('Archive')
        self.arch_btn.setMinimumSize(QSize(100, 60))
        # self.arch_btn.setSizeIncrement(QSize(0, 0))
        self.button_lay.addWidget(self.arch_btn)
        self.log_btn = QPushButton('View Log')
        self.log_btn.setMinimumSize(QSize(0, 35))
        self.button_lay.addWidget(self.log_btn)

        self.main_lay.addLayout(self.entitys_lay)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)
        self.find_le.setFocus()
        # variables
        self.file_project_folder = ''
        self.ind = -1
        self.thread_log = []
        self.selected = False
        self.finder = ''
        self.thread = QThread(self)
        self.threads = []
        self.data = self.collect_folders_list()
        #act
        self.select_btn.clicked.connect(self.filter_selection)
        self.clear_btn.clicked.connect(self.find_entity)
        # self.clear_btn.clicked.connect(self.file_lst.clearSelection)
        # self.refresh_btn.clicked.connect(self.get_files)
        self.arch_btn.clicked.connect(self.archive)
        # self.log_btn.clicked.connect(lambda:self.thread.exit(0))
        self.log_btn.clicked.connect(self.get_log)

    def _get_data(self):
        # test method
        # TEST FOLDER
        root = 'C:/Autodesk/Autodesk_Maya_2018_EN_JP_ZH_Win_64bit_dlm/Setup'
        data = [root+'/'+path for path in os.listdir(root)]      
        return data

    def collect_folders_list(self):
        '''
        getting list of folders of the entities
        '''
        data = []
        for prj in os.listdir(prj_root):
            path = os.path.join(prj_root, prj, '.dir_cache')
            if not os.path.exists(path):
                continue
            with open(path, 'r') as cache:
                fpath = lambda x: os.path.join(prj_root, prj, unicode(x.strip(), errors='ignore'))
                data += [fpath(l).replace('\\', '/') for l in cache]
        return data

    def fill_list(self, lst):
        '''
        shows list of finded objects (folders)
        '''
        self.file_lst.clear()
        # print len(lst)
        for path in lst:
            itm = self.setItem(path)
            self.file_lst.addItem(itm)
            # self.file_lst.setItemWidget(itm, itm.wtm)

    def find_entity(self):
        '''
        method to find list of coinsedences in folder names
        '''
        find_text = self.find_le.text()
        if len(find_text.strip()) < 2 or find_text.endswith(' '):
            return
        for process in self.threads:
            if not process.isFinished():
                process.quit()
        # find_text = self.find_le.text()
        self.thread = QThread(self)
        self.threads.append(self.thread)
        self.finder = Finder(find_text, self.data)
        self.finder.moveToThread(self.thread)
        self.thread.started.connect(self.finder.find)
        self.finder.paths.connect(self.fill_list)
        self.finder.finished.connect(self.thread.quit)
        self.thread.start()
        # print '{}... is finding'.format(finder)

    def setItem(self, entity_path, long_name=True):
        '''
        creates listItem with corresponding content
        iether projec/folder_name
        or name/progress_bar/combo_box to override assets for the Shot
        '''
        label = os.path.basename(entity_path)
        if long_name:
            label = entity_path.split('projects/')[-1]
        itm = QListWidgetItem(label)
        # brush = QBrush(QColor(250, 250, 1, 0))
        # itm.setBackground(brush)
        # itm.setForeground(brush)
        itm.setData(Qt.UserRole, entity_path)
        itm.setToolTip(entity_path)
        # itm.wtm = QLabel(entity_path.split('projects/')[-1].ljust(30,' '))
        itm.wtm = QWidget()
        hl = QHBoxLayout()
        hl.setContentsMargins(10, 0, 10, 0)
        # self.name_lb = QLabel(file.ljust(30,' '))
        # self.name_lb.setMinimumSize(190,20)
        # self.name_lb.setStyleSheet(self.stl)
        itm.override_cbx = QCheckBox()
        override_lb = QLabel()
        override_lb.setStyleSheet(self.stl)
        override_lb.setText('override')
        itm.info_lb = QLabel()
        itm.info_lb.setStyleSheet(self.stl)
        itm.info_lb.setText('archived'.rjust(50, ' '))
        itm.pr_bar = QProgressBar()
        itm.pr_bar.setValue(0)
        stl = 'QProgressBar {color: rgb(60,60,60);font: bold 10pt; text-align: center;border:'\
              '1px solid grey;border-radius 8px;}'\
              'QProgressBar:chunk {background-color: rgb(110,250,210)};border-radius 8px;'
        itm.pr_bar.setStyleSheet(stl)
        trg = entity_path.replace(self.file_project_folder, '%s/outsource'%self.file_project_folder)
        if os.path.exists(trg):
            itm.pr_bar.setValue(100)
        # hl.addWidget(self.name_lb)
        hl.addWidget(itm.info_lb)
        hl.addWidget(itm.pr_bar)
        hl.addWidget(override_lb)
        hl.addWidget(itm.override_cbx)
        itm.wtm.setLayout(hl)
        return itm

    def filter_selection(self):
        '''
        shows new list of selected items
        in with activated lits item widgets
        '''
        files = []
        itm_wgt = []
        sel = self.file_lst.selectedItems()
        for itm in sel:
            files.append(itm.data(Qt.UserRole))
            itm_wgt.append(self.file_lst.itemWidget(itm))
        self.file_lst.clear()
        for path in files:
            itm = self.setItem(path, long_name=False)
            self.file_lst.addItem(itm)
            self.file_lst.setItemWidget(itm, itm.wtm)
        self.selected = True

    def update_progress(self, val):
        '''
        updates zip progress bar while zipping
        '''
        if isinstance(val, list):
            val = val[0]
        if val > 100:
            val = 100
        val = int(float(val))
        self.pr_bar.setValue(val)

    def zip_log(self, msg):
        '''
        append msg to log and format it with different color if needed
        '''
        if not msg:
            return
        # print '>> %s'%msg
        red = False
        self.thread_log.append(msg)
        if 'ERROR' in msg:
            stl = 'QProgressBar {color: rgb(60,60,60);font: bold 11px; text-align: center;'\
                  'border: 1px solid grey}'\
                  'QProgressBar:chunk {background-color: rgb(250,70,0)}'
            self.pr_bar.setStyleSheet(stl)
            red = True
        if 'WARNING' in msg:
            if not red: # not to change a color to orange if errors were found
                stl = 'QProgressBar {color: rgb(60,60,60);font: bold 11px; text-align: center;'\
                      'border: 1px solid grey}'\
                      'QProgressBar:chunk {background-color: rgb(250,170,0)}'
                self.pr_bar.setStyleSheet(stl)

    def get_log_path(self):
        '''
        returns path to log, saved in the user home directory
        '''
        return os.path.join(os.path.expanduser("~"), 'zip_log.json')

    def get_log(self):
        '''
        dispalays process log filefrom the memory
        or from the json file, that was saved in the user home directory
        '''
        if self.thread_log:
            info_lst = self.thread_log
        else:
            log_path = self.get_log_path()
            if not os.path.exists(log_path):
                return
            info_lst = json.load(open(log_path))
        log = Logger(info_lst, self)
        log.show()
        # log.text.setFocus()

    def run_next_thread(self):
        '''
        closes the current thread and launches the next one
        '''
        print('run next - {}'.format(self.thread))
        self.thread.quit()
        # wait for the ending of a process
        # sleep(3)
        if self.thread.isFinished():
            self.archive()

    def archive(self):
        '''
        launches zipp process in a separate thread
        '''
        if not self.selected:
            msg = 'Please choose files from list and press "Filter" button to filter files for zip.'
            QMessageBox.information(self, 'Suggestion', '/n    %s        '%msg)
            return
        # self.info_lb.setText('running')
        self.ind += 1
        if not self.ind < self.file_lst.count():
            self.ind = -1
            self.thread.exit(0)
            json.dump(self.thread_log, open(self.get_log_path(), 'w'), indent=4)
            log = Logger(self.thread_log, self)
            log.show()
            return
        itm = self.file_lst.item(self.ind)
        # sht_wgt = self.file_lst.itemWidget(itm)
        # itm.pr_bar = sht_wgt.findChild(QProgressBar)
        # itm.info_lb = sht_wgt.findChild(QLabel)
        stl = 'QProgressBar {color: rgb(60,60,60);font: bold 11px; text-align: center;'\
              'border: 1px solid grey}'\
              'QProgressBar:chunk {background-color: rgb(110,250,210);border-radius 5px}'
        itm.pr_bar.setStyleSheet(stl)
        filepath = itm.data(Qt.UserRole)
        override = itm.override_cbx.isChecked()
        # separate process launch
        self.thread = QThread(self)
        zipper = zip_archiver.ZipArchiver(filepath, override)
        zipper.moveToThread(self.thread)
        self.thread.started.connect(zipper.pack_scene)
        zipper.message.connect(self.zip_log)
        zipper.progres.connect(self.update_progress)
        zipper.finished.connect(self.run_next_thread)
        self.thread.start()

    def closeEvent(self, event):
        '''
        clear threads while destroing
        '''
        if not self.thread.isFinished():
            self.thread.quit()
        return super(ZipManager, self).closeEvent(event)

class FindField(QLineEdit):
    '''
    overrides default key events to add new functionality
    '''
    def __init__(self, parent):
        super(FindField, self).__init__()
        self.p = parent

    def keyReleaseEvent(self, event):
        '''
        finds entity name against text input
        '''
        if event.key() in range(128):
            self.p.find_entity()
        return super(FindField, self).keyReleaseEvent(event)

    def keyPressEvent(self, event):
        '''
        clears find line and list of foud objects with Escape Key
        redirects arrow navigation to the find result list
        '''
        if event.key() == Qt.Key_Escape:
            if self.text():
                self.clear()
                self.p.file_lst.clear()
        elif event.key() in [
                Qt.Key_Up,
                Qt.Key_Down,
                Qt.Key_PageUp,
                Qt.Key_PageDown
            ]:
            return self.p.file_lst.event(event)
        return super(FindField, self).keyPressEvent(event)

class Logger(QFrame):
    '''
    Logger maintain work whit log messages - 
    collect, format, save, display
    '''
    def __init__(self, lst, parent):
        super(Logger, self).__init__(parent)
        self.setWindowFlags(Qt.ToolTip)
        self.setWindowTitle('Log')
        self.setLineWidth(1)
        self.text = QTextEdit()
        self.ly = QVBoxLayout()
        self.ly.setContentsMargins(0, 0, 0, 0)
        self.ly.addWidget(self.text)
        self.setLayout(self.ly)

        stl = 'QFrame {color: rgb(50,210,50);background-color: rgb(10,40,60);font: 12px;}'
        self.setStyleSheet(stl)

        log = ''
        for line in lst:
            log += '%s/n'%line
        self.text.setText(log)

        self.highlight()
        self.highlight('ERROR', 'red')

        geo = QRect(0, 0, 650, 340)
        # geo.moveCenter(QCursor.pos())
        geo.moveTo(parent.pos().x()+55, parent.pos().y()+70)
        self.setGeometry(geo)

    def highlight(self, pattern='WARNING', color='yellow'):
        '''
        paints error and warning words to red and yellow colors
        '''
        # Setup the text editor
        cursor = self.text.textCursor()
        # Setup the desired format for matches
        formatt = QTextCharFormat()
        if color == 'red':
            formatt.setForeground(QBrush(QColor('white')))
            formatt.setBackground(QBrush(QColor(color)))
        else:
            formatt.setForeground(QBrush(QColor(color)))
        # Setup the regex engine
        regex = QRegExp(pattern)
        # Process the displayed document
        pos = 0
        index = regex.indexIn(self.text.toPlainText(), pos)
        while index != -1:
            # Select the matched text and apply the desired format
            cursor.setPosition(index)
            cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor, 1)
            cursor.mergeCharFormat(formatt)
            # Move to the next match
            pos = index + regex.matchedLength()
            index = regex.indexIn(self.text.toPlainText(), pos)

    def keyPressEvent(self, event):
        '''
        closes log window with Escape Key
        '''
        if event.key() == Qt.Key_Escape:
            self.close()
        return super(Logger, self).keyPressEvent(event)

class Finder(QObject):
    ''' finds and returns a list of items (pathes to files or foldres)
        signal "paths" - returns needed value
    '''
    paths = Signal(list) 
    finished = Signal()
    def __init__(self, text_to_find, data):
        super(Finder, self).__init__()
        self.text = text_to_find
        self.data = data

    def find(self):
        '''
        finds corresponding names in the list of folders
        returns a filtered folder list
        '''
        lst = []
        parts = []
        tire = '[{}{}]'.format(
            '' if '-' in self.text else '\-',
            '' if '_' in self.text else '_')
        fnd = [t.strip() for t in self.text.split(' ') if t.strip()]
        for n in self.data:
            n = n.replace('\\', '/')
            if sys.platform == 'win32' and not n[:2] == '//':
                n = '/'+n
            name = n.rsplit('/', 1)[-1]
            if re.findall(r'{f}sh{f}[0-9]{{3,4}}'.format(f=tire), name):
                parts = [p for p in re.split(r'[\-_]sh[\-_]', name) if p]
            elif re.findall(r'{}'.format(tire), name):
                parts = [p for p in re.split(r'[\-_]', name) if p]
            else:
                parts = [name]
            if len(parts) >= len(fnd):
                if not False in [p in parts[i] for i, p in enumerate(fnd) if i < len(parts)]:
                    lst.append(n)
        self.paths.emit(lst)
        self.finished.emit()

if __name__ == '__main__':

    if not os.path.exists(prj_root):
        print 'Can`t find this path - {}'.format(prj_root)
    # else:
    print 'prj_root', prj_root
    app = QApplication([])
    arc = ZipManager()
    arc.show()
    sys.exit(app.exec_())
