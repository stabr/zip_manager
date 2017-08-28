#!/python
# -*- coding: utf-8 -*-
'''
File manager to archive project files for outsource

author: Dmitry Stabrov
mailto: fx@dimastabrov.com

'''

import os
import re
import json
from time import sleep

from PySide.QtCore import *
from PySide.QtGui import *

import zip_archiver
import setup

prj_root = setup.config('project_root')
print 'prj_root', prj_root

class ZipManager(QWidget):
    """ZipManager"""
    def __init__(self):
        super(ZipManager, self).__init__()
        # ui
        self.resize(609, 288)
        # self.setMinimumSize(QSize(609, 422))
        self.main_lay = QHBoxLayout()
        # self.main_lay.setContentsMargins(40, 20, 40, 20)
        
        # stl = 'QWidget {color: rgb(210,210,190);background-color:rgb(68,68,68);font: bold 12px;}\
        #        QPushButton {color: rgb(160,160,160);background-color:rgb(68,68,68);font: bold 12px;}'
        stl = os.path.join(os.path.dirname(__file__), 'wgt/style.css')
        self.setStyleSheet(stl)

        self.entitys_lay = QVBoxLayout()       
        self.shot_lst = QListWidget()
        self.shot_lst.setMinimumSize(QSize(398, 0))
        self.shot_lst.setSelectionMode(QAbstractItemView.MultiSelection)
        self.shot_lst.setMouseTracking(True)
        self.shot_lst.setToolTip('Entities')

        self.entitys_lay.addWidget(self.shot_lst)
        self.find_le = FindField(self)
        self.entitys_lay.addWidget(self.find_le)

        self.button_lay = QVBoxLayout()
        self.button_lay.setContentsMargins(0, 0, 0, 9)
        # self.select_btn = QPushButton('Select')
        # self.select_btn.setMinimumSize(QSize(0, 50))
        # self.select_btn.setMaximumSize(QSize(100, 50))
        # self.button_lay.addWidget(self.select_btn)
        # self.clear_btn = QPushButton('Clear Selection')
        # self.clear_btn.setMinimumSize(QSize(0, 50))
        # self.clear_btn.setMaximumSize(QSize(100, 50))
        # self.button_lay.addWidget(self.clear_btn)
        self.refresh_btn = QPushButton('Refresh List')
        self.refresh_btn.setMinimumSize(QSize(0, 50))
        self.refresh_btn.setMaximumSize(QSize(100, 50))
        self.button_lay.addWidget(self.refresh_btn)
        # spacerItem = QSpacerItem(20, 60, QSizePolicy.Minimum, QSizePolicy.Expanding )
        # self.button_lay.addItem(spacerItem)
        self.arch_btn = QPushButton('Archive')
        self.arch_btn.setMinimumSize(QSize(100, 60))
        self.arch_btn.setMaximumSize(QSize(100, 60))
        # self.arch_btn.setSizeIncrement(QSize(0, 0))
        self.button_lay.addWidget(self.arch_btn)
        self.log_btn = QPushButton('View Log')
        self.log_btn.setMinimumSize(QSize(0, 25))
        self.log_btn.setMaximumSize(QSize(100, 35))
        self.button_lay.addWidget(self.log_btn)

        self.main_lay.addLayout(self.entitys_lay)
        self.main_lay.addLayout(self.button_lay)
        self.setLayout(self.main_lay)

        # variables
        self.shot_project_folder = ''
        self.season = ''
        self.sequence = ''
        self.ind = -1
        self.thread_log = []
        self.selected = False
        self.thread = QThread(self)
        self.data = self.get_data()

        #act
        # self.find_le.textChanged.connect(self.find_entity)

        self.find_le.returnPressed.connect(self.return_pressed)
        self.find_le.textChanged.connect(self.find_entity)

        # self.select_btn.clicked.connect(self.filter_selection)
        # self.clear_btn.clicked.connect(self.shot_lst.clearSelection)
        # self.refresh_btn.clicked.connect(self.get_shots)
        self.arch_btn.clicked.connect(self.archive)
        # self.log_btn.clicked.connect(lambda:self.thread.exit(0))
        self.log_btn.clicked.connect(self.get_log)


    def get_data(self):
        root = 'C:/Users/Me/Pictures/img'
        data = [file for file in os.listdir(root)]      
        return data

    def _get_data(self):
        # root = '//bstorage/strg01/mnt/projects'
        root = amg_config.conf.get('projects_path')
        data = []
        for prj in os.listdir(root):
            path = os.path.join(root, prj, '.dir_cache')
            if os.path.exists(path):
                with open(path,'r') as cache:
                    fullpath = lambda x: os.path.join(root,prj,unicode(x.strip(), errors='ignore')).replace('\\','/')
                    data += [fullpath(l) for l in cache if l.startswith(self.entity.lower())]
        return data

    def return_pressed(self):
        selected = self.shot_lst.selectedItems()
        if selected:
            itm = selected[0]
        else:
            itm = self.shot_lst.item(0)
        self.path = itm.data(Qt.UserRole).replace('\\','/')
        self.find_le.setText(itm.text())
        # print '>> {}'.format(self.path)

    def find_entity(self):

        find_text = self.find_le.text()
        if len(find_text.strip()) <2:
            return
        fnd = [t.strip() for t in find_text.split(' ') if t.strip()]

        lst = []
        for n in self.data:
            if not False in [p in n for p in fnd]:
                lst.append(n)

        self.shot_lst.clear()
        for i in lst:
            text = '{}'.format(i)
            self.setItem(i)

        items = self.shot_lst.findItems(find_text, 1)
        for i in items:
            if find_text.lower() in i.text().lower():
                self.shot_lst.setCurrentItem(i)
                i.setSelected(True)
                break

    def target_exists(self, src):
        trg = src.replace(self.shot_project_folder, '%s/outsource'%self.shot_project_folder)
        return os.path.exists(trg)

    def setItem(self, entity_path):
        shot = os.path.basename(entity_path)
        itm = QListWidgetItem(shot)
        brush = QBrush(QColor(250, 250, 1, 0))
        # itm.setBackground(brush)
        itm.setForeground(brush)
        itm.setData(Qt.UserRole, entity_path)
        wtm = QWidget()
        hl = QHBoxLayout()
        hl.setContentsMargins(10,0,10,0)
        wtm.setLayout(hl)
        self.name_lb = QLabel(shot.ljust(30,' '))
        self.name_lb.setMinimumSize(190,20)
        self.override_cbx = QCheckBox()
        self.override_lb = QLabel()
        self.override_lb.setText('override')
        self.info_lb = QLabel()
        self.info_lb.setText('archived')
        self.pr_bar = QProgressBar()
        self.pr_bar.setValue(0)
        stl = 'QProgressBar {color: rgb(60,60,60);font: bold 11px; text-align: center;border: 1px solid grey}'\
              'QProgressBar:chunk {background-color: rgb(110,250,210)}'
        self.pr_bar.setStyleSheet(stl)
        if self.target_exists(entity_path):
            self.pr_bar.setValue(100)
        hl.addWidget(self.name_lb)
        hl.addWidget(self.info_lb)
        hl.addWidget(self.pr_bar)
        hl.addWidget(self.override_lb)
        hl.addWidget(self.override_cbx)
        self.shot_lst.addItem(itm)
        self.shot_lst.setItemWidget(itm, wtm)

    def filter_selection(self):
        files = []
        itm_wgt = []
        sel = self.shot_lst.selectedItems()
        for itm in sel:
            files.append(itm.data(32))
            itm_wgt.append(self.shot_lst.itemWidget(itm))
        self.shot_lst.clear()
        for shot in files:
            self.setItem(shot)
        self.selected = True

    def update_progress(self, val):
        if isinstance(val, list):
                        val = val[0]
        if val>100: val = 100
        val = int(float(val))
        self.pr_bar.setValue(val)

    def zip_log(self, msg):
        if msg:
            # print '>> %s'%msg
            red = False
            self.thread_log.append(msg)
            if 'ERROR' in msg:
                stl = 'QProgressBar {color: rgb(60,60,60);font: bold 11px; text-align: center;border: 1px solid grey}'\
                      'QProgressBar:chunk {background-color: rgb(250,70,0)}'
                self.pr_bar.setStyleSheet(stl)
                red = True
            if 'WARNING' in msg:
                if not red: # not to change a color to orange if errors were found
                    stl = 'QProgressBar {color: rgb(60,60,60);font: bold 11px; text-align: center;border: 1px solid grey}'\
                          'QProgressBar:chunk {background-color: rgb(250,170,0)}'
                    self.pr_bar.setStyleSheet(stl)

    def get_log_path(self):
        return os.path.join(os.path.expanduser("~"), 'zip_log.json')

    def get_log(self):
        if len(self.thread_log) > 0:
            info_lst = self.thread_log
        else:
            log_path = self.get_log_path()
            if not os.path.exists(log_path):
                return
            info_lst = json.load(open(log_path))
        log = Logger(info_lst, self)
        log.show()

    def run_next(self):
        self.thread.exit(0)
        sleep(3)
        if self.thread.isFinished():
            self.archive()

    def get_full_path(self, pth):
        if '/assets/' in pth:
            asset_template = '{asset}/{step}/publish/maya/Rig.v001.ma'
            pth = asset_template.format(asset=pth, step=self.ast_step_cbx.currentText())
        else:
            shot_template = '{shot}/{step}/work/maya/{name}.v001.ma'
            name = os.path.basename(pth)
            pth = shot_template.format(shot=pth, step=self.step_cbx.currentText(), name=name)
            dirr = os.path.dirname(pth)
            versioned = sorted([fl for fl in os.listdir(dirr) if name in fl])
            if len(versioned)>0:
                    pth = pth.replace(name, versioned[-1])
        return pth

    def archive(self):
        if not self.selected:
            msg = 'Please choose files from list and press "Filter" button to filter files for zip.'
            QMessageBox.information(None, 'Suggestion', '\n    %s        '%msg)
            return
        # self.info_lb.setText('running')
        self.ind += 1
        if not self.ind < self.shot_lst.count():
            self.ind = -1
            self.thread.exit(0)
            json.dump(self.thread_log, open(self.get_log_path(),'w'), indent=4)
            log = Logger(self.thread_log, self)
            log.show()
            return
        itm = self.shot_lst.item(self.ind)
        sht_wgt = self.shot_lst.itemWidget(itm)
        self.pr_bar = sht_wgt.findChild(QProgressBar)
        self.info_lb = sht_wgt.findChild(QLabel)
        stl = 'QProgressBar {color: rgb(60,60,60);font: bold 11px; text-align: center;border: 1px solid grey}'\
              'QProgressBar:chunk {background-color: rgb(110,250,210)}'
        self.pr_bar.setStyleSheet(stl)

        file = self.get_full_path(itm.data(32))
        override = self.override_cbx.isChecked()
        
        self.thread = QThread(self)
        self.zipper = zip_archiver.ZipArchiver(file, override)
        self.zipper.moveToThread(self.thread)
        self.thread.started.connect(self.zipper.pack_scene)
        self.zipper.message.connect(self.zip_log)
        self.zipper.progres.connect(self.update_progress)
        self.zipper.finished.connect(self.run_next)
        self.thread.start()
        # self.thread.setPriority(QThread.LowPriority)

class FindField(QLineEdit):
    def __init__(self, parent):
        super(FindField, self).__init__()
        self.p = parent

    def event(self, event):
            resend = None
            if event.type() in [QEvent.KeyPress, QEvent.KeyRelease, QEvent.ShortcutOverride]:
                if event.key() == Qt.Key_Escape:
                    if self.text():
                        self.clear()
                        self.p.lst.close()
                    return True
                elif event.key() in [
                    Qt.Key_Up,
                    Qt.Key_Down,
                    Qt.Key_PageUp,
                    Qt.Key_PageDown,
                    Qt.Key_Home,
                    Qt.Key_End]:
                    resend = self.p.lst.text
            if resend:
                return resend.event(event)
            return super(QLineEdit, self).event(event)

class Logger(QFrame):
    """docstring for Logger"""
    def __init__(self, lst, parent):
        super(Logger, self).__init__(parent)
        self.setWindowFlags(Qt.ToolTip)
        self.setWindowTitle('Log')
        self.setLineWidth(1)
        self.text = QTextEdit()
        self.ly = QVBoxLayout()
        self.ly.setContentsMargins(0,0,0,0)
        self.ly.addWidget(self.text)
        self.setLayout(self.ly)

        stl = 'QFrame {color: rgb(50,210,50);background-color: rgb(10,40,60);font: 12px;}'
        self.setStyleSheet(stl)

        log = ''
        for line in lst:
            log += '%s\n'%line
        self.text.setText(log)

        geo = QRect(0,0,650,340)
        # geo.moveCenter(QCursor.pos())
        geo.moveTo(parent.pos().x()+55, parent.pos().y()+70)
        self.setGeometry(geo)

if __name__ == '__main__':
    if not os.path.exists(prj_root):
        print 'Can`t find this path - {}'.format(prj_root)
    # else:
    app = QApplication([])
    arc = ZipManager()
    arc.show()
    app.exec_()
