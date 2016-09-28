'''
Author: Dmitry Stabrov
------------------------------
description: UI manager to archive project files for outsource
------------------------------
'''

import os
import re
import json
from time import sleep

from PySide.QtCore import *
from PySide.QtGui import *

import zip_archiver
from wgt import zip_wgt

import setup
prj_root = setup.config('project_root')

class ZipManager(QWidget, zip_wgt.Ui_Form):
    """ZipManager"""
    def __init__(self):
        super(ZipManager, self).__init__()
        self.setupUi(self)
        self.ast_project_folder = ''
        self.shot_project_folder = ''
        self.season = ''
        self.sequence = ''
        self.ind = -1
        self.thread_log = []
        self.selected = False
        self.thread = QThread(self)

        self.shot_lst.setSelectionMode(QAbstractItemView.MultiSelection)
        self.shot_lst.setMouseTracking(True)
        self.shot_lst.setToolTip('Entities')

        stl = 'QWidget {color: rgb(210,210,190);background-color:rgb(210,230,240);font: bold 12px;}'\
              'QPushButton {color: rgb(160,160,160);background-color:rgb(40,40,40);font: bold 12px;}'
        # self.setStyleSheet(stl)
        self.log_btn.setText('Log')

        self.project_cbx.addItem('Select Project')
        self.ast_project_cbx.addItem('Select Project')
        for prj_fld in self.get_projects():
            self.project_cbx.addItem(prj_fld)
            self.ast_project_cbx.addItem(prj_fld)

        #act
        self.ast_project_cbx.currentIndexChanged.connect(self.get_ast_types)
        self.ast_type_cbx.currentIndexChanged.connect(self.get_assets)
        # self.ast_step_cbx.currentIndexChanged.connect(self.get_ast_step)

        self.project_cbx.currentIndexChanged.connect(self.get_seasons)
        self.season_cbx.currentIndexChanged.connect(self.get_sequences)
        self.sequence_cbx.currentIndexChanged.connect(self.get_shots)
        # self.find_le.textChanged.connect(self.find_entity)
        self.find_le.returnPressed.connect(lambda: self.find_entity(self.find_le.text()))
        self.ast_find_le.returnPressed.connect(lambda: self.find_entity(self.ast_find_le.text()))
        self.select_btn.clicked.connect(self.filter_selection)
        self.clear_btn.clicked.connect(self.shot_lst.clearSelection)
        self.refresh_btn.clicked.connect(self.get_shots)
        self.arch_btn.clicked.connect(self.archive)
        # self.log_btn.clicked.connect(lambda:self.thread.exit(0))
        self.log_btn.clicked.connect(self.get_log)

    def get_ast_types(self):
        self.ast_type_cbx.clear()
        self.ast_project_folder = self.ast_project_cbx.currentText()
        project_folder = '/'.join([prj_root, self.ast_project_folder])
        if not self.ast_project_folder == 'Select Project':
            self.ast_step_cbx.clear()
            self.shot_lst.clear()
            types = '/'.join([prj_root, self.ast_project_folder,'assets'])
            self.ast_type_cbx.addItems([typ for typ in os.listdir(types) if os.path.isdir('%s/%s'%(types, typ))])

    def get_assets(self):
        skip = ['def','tex']
        get_step = True
        self.shot_lst.clear()
        self.ast_selected = False
        self.ast_type = self.ast_type_cbx.currentText()
        if not self.ast_type:
            return
        assets = '/'.join([prj_root, self.ast_project_folder,'assets',self.ast_type])
        for ast in os.listdir(assets):
            if not ast[0] == '.':
                aset = '/'.join([assets,ast])
                self.setItem(aset)
                if get_step:
                    get_step = False
                    self.ast_step_cbx.clear()
                    self.ast_step_cbx.addItems([step for step in os.listdir(aset) if step.islower() and not step in skip])

    def get_projects(self):
        if os.path.exists(prj_root):
            return [prj for prj in os.listdir(prj_root) if not prj == 'dev' and not prj.startswith('.')]
        else:
            self.thread_log.append(['ERROR::Can`t find any projects here: %s'%prj_root])
            return []

    def get_seasons(self):
        self.shot_project_folder = self.project_cbx.currentText()
        project_folder = '/'.join([prj_root, self.shot_project_folder])
        if not self.shot_project_folder == 'Select Project':
            self.season_cbx.clear()
            self.sequence_cbx.clear()
            self.shot_lst.clear()
            if 'seasons' in os.listdir(project_folder):
                seqs = '/'.join([prj_root, self.shot_project_folder,'seasons'])
                self.season_cbx.addItems([sq for sq in os.listdir(seqs) if re.findall('(S\d{2})', sq[-3:])])
            else:
                self.get_sequences()

    def get_sequences(self):
        self.shot_project_folder = self.project_cbx.currentText()
        project_folder = '/'.join([prj_root, self.shot_project_folder])
        self.season = self.season_cbx.currentText()
        if not self.shot_project_folder == 'Select Project':
            self.sequence_cbx.clear()
            if 'sequences' in os.listdir(project_folder):
                seqs = '/'.join([prj_root, self.shot_project_folder,'sequences'])
                self.sequence_cbx.addItems([sq for sq in os.listdir(seqs) if sq.startswith('E')])
            elif 'seasons' in os.listdir(project_folder) and self.season:
                seqs = '/'.join([prj_root, self.shot_project_folder,'seasons',self.season,'sequences'])
                self.sequence_cbx.addItems([sq for sq in os.listdir(seqs) if sq.startswith('S')])

    def get_shots(self):
        get_step = True
        skip = ['editorial']
        self.shot_lst.clear()
        self.selected = False
        self.season = self.season_cbx.currentText()
        self.sequence = self.sequence_cbx.currentText()
        if not self.sequence:
            return
        if self.season:
            sq = '/'.join([prj_root, self.shot_project_folder,'seasons',self.season,self.sequence])
        else:
            sq = '/'.join([prj_root, self.shot_project_folder,'sequences',self.sequence])
        for shot in os.listdir(sq):
            if re.findall('(\d{2}-sh-\d{4})',shot[-10:]):
                sht = '/'.join([sq, shot])
                self.setItem(sht)
                # fill step combobox
                if get_step:
                    get_step = False
                    self.step_cbx.clear()
                    self.step_cbx.addItems([step for step in os.listdir(sht) if step.islower() and not step in skip])

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

    def find_entity(self, find_text):
        items = self.shot_lst.findItems(find_text, 1)
        for i in items:
            if find_text.lower() in i.text().lower():
                self.shot_lst.setCurrentItem(i)
                i.setSelected(True)
                break

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

class Logger(QFrame):
    """docstring for Logger"""
    def __init__(self, lst, parent):
        super(Logger, self).__init__(parent)
        self.setWindowFlags(Qt.Tool)
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
        print prj_root
    else:
        app = QApplication([])
        arc = ZipManager()
        arc.show()
        app.exec_()
