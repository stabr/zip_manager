# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\sbr\Dropbox\python\tools\zip_manager\wgt\zip_wgt.ui'
#
# Created: Fri Oct 14 18:31:26 2016
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(609, 488)
        Form.setMinimumSize(QtCore.QSize(609, 422))
        self.verticalLayout_2 = QtGui.QVBoxLayout(Form)
        self.verticalLayout_2.setContentsMargins(40, 20, 40, 20)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.entity_tab = QtGui.QTabWidget(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.entity_tab.sizePolicy().hasHeightForWidth())
        self.entity_tab.setSizePolicy(sizePolicy)
        self.entity_tab.setMinimumSize(QtCore.QSize(0, 169))
        self.entity_tab.setMaximumSize(QtCore.QSize(16777215, 169))
        self.entity_tab.setTabShape(QtGui.QTabWidget.Rounded)
        self.entity_tab.setElideMode(QtCore.Qt.ElideNone)
        self.entity_tab.setUsesScrollButtons(False)
        self.entity_tab.setObjectName("entity_tab")
        self.asset_tab = QtGui.QWidget()
        self.asset_tab.setObjectName("asset_tab")
        self.gridLayout = QtGui.QGridLayout(self.asset_tab)
        self.gridLayout.setObjectName("gridLayout")
        self.ast_project_lbl = QtGui.QLabel(self.asset_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ast_project_lbl.sizePolicy().hasHeightForWidth())
        self.ast_project_lbl.setSizePolicy(sizePolicy)
        self.ast_project_lbl.setMinimumSize(QtCore.QSize(70, 0))
        self.ast_project_lbl.setMaximumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.ast_project_lbl.setFont(font)
        self.ast_project_lbl.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.ast_project_lbl.setObjectName("ast_project_lbl")
        self.gridLayout.addWidget(self.ast_project_lbl, 0, 0, 1, 1)
        self.ast_project_cbx = QtGui.QComboBox(self.asset_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ast_project_cbx.sizePolicy().hasHeightForWidth())
        self.ast_project_cbx.setSizePolicy(sizePolicy)
        self.ast_project_cbx.setMinimumSize(QtCore.QSize(200, 0))
        self.ast_project_cbx.setObjectName("ast_project_cbx")
        self.gridLayout.addWidget(self.ast_project_cbx, 0, 1, 1, 1)
        self.ast_type_cbx = QtGui.QComboBox(self.asset_tab)
        self.ast_type_cbx.setMinimumSize(QtCore.QSize(100, 0))
        self.ast_type_cbx.setObjectName("ast_type_cbx")
        self.gridLayout.addWidget(self.ast_type_cbx, 1, 1, 1, 1)
        self.ast_step_cbx = QtGui.QComboBox(self.asset_tab)
        self.ast_step_cbx.setMinimumSize(QtCore.QSize(100, 0))
        self.ast_step_cbx.setObjectName("ast_step_cbx")
        self.gridLayout.addWidget(self.ast_step_cbx, 2, 1, 1, 1)
        self.ast_find_lbl = QtGui.QLabel(self.asset_tab)
        self.ast_find_lbl.setMinimumSize(QtCore.QSize(70, 0))
        self.ast_find_lbl.setMaximumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.ast_find_lbl.setFont(font)
        self.ast_find_lbl.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.ast_find_lbl.setObjectName("ast_find_lbl")
        self.gridLayout.addWidget(self.ast_find_lbl, 3, 0, 1, 1)
        self.ast_type_lb = QtGui.QLabel(self.asset_tab)
        self.ast_type_lb.setMinimumSize(QtCore.QSize(70, 0))
        self.ast_type_lb.setMaximumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.ast_type_lb.setFont(font)
        self.ast_type_lb.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.ast_type_lb.setObjectName("ast_type_lb")
        self.gridLayout.addWidget(self.ast_type_lb, 1, 0, 1, 1)
        self.ast_step_lbl = QtGui.QLabel(self.asset_tab)
        self.ast_step_lbl.setMinimumSize(QtCore.QSize(70, 0))
        self.ast_step_lbl.setMaximumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.ast_step_lbl.setFont(font)
        self.ast_step_lbl.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.ast_step_lbl.setObjectName("ast_step_lbl")
        self.gridLayout.addWidget(self.ast_step_lbl, 2, 0, 1, 1)
        self.ast_find_le = QtGui.QLineEdit(self.asset_tab)
        self.ast_find_le.setObjectName("ast_find_le")
        self.gridLayout.addWidget(self.ast_find_le, 3, 1, 1, 1)
        self.entity_tab.addTab(self.asset_tab, "")
        self.shot_tab = QtGui.QWidget()
        self.shot_tab.setObjectName("shot_tab")
        self.gridLayout_2 = QtGui.QGridLayout(self.shot_tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.find_lbl = QtGui.QLabel(self.shot_tab)
        self.find_lbl.setMinimumSize(QtCore.QSize(70, 0))
        self.find_lbl.setMaximumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.find_lbl.setFont(font)
        self.find_lbl.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.find_lbl.setObjectName("find_lbl")
        self.gridLayout_2.addWidget(self.find_lbl, 5, 0, 1, 1)
        self.season_lb = QtGui.QLabel(self.shot_tab)
        self.season_lb.setMinimumSize(QtCore.QSize(70, 0))
        self.season_lb.setMaximumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.season_lb.setFont(font)
        self.season_lb.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.season_lb.setObjectName("season_lb")
        self.gridLayout_2.addWidget(self.season_lb, 3, 0, 1, 1)
        self.find_le = QtGui.QLineEdit(self.shot_tab)
        self.find_le.setObjectName("find_le")
        self.gridLayout_2.addWidget(self.find_le, 5, 2, 1, 1)
        self.sequence_cbx = QtGui.QComboBox(self.shot_tab)
        self.sequence_cbx.setObjectName("sequence_cbx")
        self.gridLayout_2.addWidget(self.sequence_cbx, 4, 2, 1, 1)
        self.season_cbx = QtGui.QComboBox(self.shot_tab)
        self.season_cbx.setObjectName("season_cbx")
        self.gridLayout_2.addWidget(self.season_cbx, 3, 2, 1, 1)
        self.step_lbl = QtGui.QLabel(self.shot_tab)
        self.step_lbl.setMinimumSize(QtCore.QSize(70, 0))
        self.step_lbl.setMaximumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.step_lbl.setFont(font)
        self.step_lbl.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.step_lbl.setObjectName("step_lbl")
        self.gridLayout_2.addWidget(self.step_lbl, 4, 0, 1, 1)
        self.step_cbx = QtGui.QComboBox(self.shot_tab)
        self.step_cbx.setObjectName("step_cbx")
        self.gridLayout_2.addWidget(self.step_cbx, 2, 2, 1, 1)
        self.project_cbx = QtGui.QComboBox(self.shot_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.project_cbx.sizePolicy().hasHeightForWidth())
        self.project_cbx.setSizePolicy(sizePolicy)
        self.project_cbx.setMinimumSize(QtCore.QSize(200, 0))
        self.project_cbx.setObjectName("project_cbx")
        self.gridLayout_2.addWidget(self.project_cbx, 1, 2, 1, 1)
        self.sequence_lbl = QtGui.QLabel(self.shot_tab)
        self.sequence_lbl.setMinimumSize(QtCore.QSize(70, 0))
        self.sequence_lbl.setMaximumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.sequence_lbl.setFont(font)
        self.sequence_lbl.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.sequence_lbl.setObjectName("sequence_lbl")
        self.gridLayout_2.addWidget(self.sequence_lbl, 2, 0, 1, 1)
        self.project_lbl = QtGui.QLabel(self.shot_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.project_lbl.sizePolicy().hasHeightForWidth())
        self.project_lbl.setSizePolicy(sizePolicy)
        self.project_lbl.setMinimumSize(QtCore.QSize(70, 0))
        self.project_lbl.setMaximumSize(QtCore.QSize(0, 15))
        font = QtGui.QFont()
        font.setWeight(50)
        font.setBold(False)
        self.project_lbl.setFont(font)
        self.project_lbl.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
        self.project_lbl.setObjectName("project_lbl")
        self.gridLayout_2.addWidget(self.project_lbl, 1, 0, 1, 1)
        self.entity_tab.addTab(self.shot_tab, "")
        self.gridLayout_3.addWidget(self.entity_tab, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(-1, -1, 5, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.select_btn = QtGui.QPushButton(self.groupBox)
        self.select_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.select_btn.setMaximumSize(QtCore.QSize(100, 30))
        self.select_btn.setFlat(False)
        self.select_btn.setObjectName("select_btn")
        self.horizontalLayout.addWidget(self.select_btn)
        self.clear_btn = QtGui.QPushButton(self.groupBox)
        self.clear_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.clear_btn.setMaximumSize(QtCore.QSize(100, 30))
        self.clear_btn.setFlat(False)
        self.clear_btn.setObjectName("clear_btn")
        self.horizontalLayout.addWidget(self.clear_btn)
        self.refresh_btn = QtGui.QPushButton(self.groupBox)
        self.refresh_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.refresh_btn.setMaximumSize(QtCore.QSize(100, 30))
        self.refresh_btn.setFlat(False)
        self.refresh_btn.setObjectName("refresh_btn")
        self.horizontalLayout.addWidget(self.refresh_btn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.arch_btn = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.arch_btn.sizePolicy().hasHeightForWidth())
        self.arch_btn.setSizePolicy(sizePolicy)
        self.arch_btn.setMinimumSize(QtCore.QSize(100, 50))
        self.arch_btn.setMaximumSize(QtCore.QSize(100, 30))
        self.arch_btn.setSizeIncrement(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.arch_btn.setFont(font)
        self.arch_btn.setObjectName("arch_btn")
        self.horizontalLayout.addWidget(self.arch_btn)
        self.log_btn = QtGui.QPushButton(self.groupBox)
        self.log_btn.setMinimumSize(QtCore.QSize(0, 50))
        self.log_btn.setMaximumSize(QtCore.QSize(100, 30))
        self.log_btn.setObjectName("log_btn")
        self.horizontalLayout.addWidget(self.log_btn)
        self.gridLayout_3.addLayout(self.horizontalLayout, 2, 0, 1, 2)
        self.shot_lst = QtGui.QListWidget(self.groupBox)
        self.shot_lst.setMinimumSize(QtCore.QSize(398, 0))
        self.shot_lst.setObjectName("shot_lst")
        self.gridLayout_3.addWidget(self.shot_lst, 1, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.groupBox)

        self.retranslateUi(Form)
        self.entity_tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Archive", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Entities", None, QtGui.QApplication.UnicodeUTF8))
        self.ast_project_lbl.setText(QtGui.QApplication.translate("Form", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.ast_find_lbl.setText(QtGui.QApplication.translate("Form", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.ast_type_lb.setText(QtGui.QApplication.translate("Form", "Type", None, QtGui.QApplication.UnicodeUTF8))
        self.ast_step_lbl.setText(QtGui.QApplication.translate("Form", "Step", None, QtGui.QApplication.UnicodeUTF8))
        self.entity_tab.setTabText(self.entity_tab.indexOf(self.asset_tab), QtGui.QApplication.translate("Form", "Assets", None, QtGui.QApplication.UnicodeUTF8))
        self.find_lbl.setText(QtGui.QApplication.translate("Form", "Find", None, QtGui.QApplication.UnicodeUTF8))
        self.season_lb.setText(QtGui.QApplication.translate("Form", "Season", None, QtGui.QApplication.UnicodeUTF8))
        self.step_lbl.setText(QtGui.QApplication.translate("Form", "Step", None, QtGui.QApplication.UnicodeUTF8))
        self.sequence_lbl.setText(QtGui.QApplication.translate("Form", "Sequence", None, QtGui.QApplication.UnicodeUTF8))
        self.project_lbl.setText(QtGui.QApplication.translate("Form", "Project", None, QtGui.QApplication.UnicodeUTF8))
        self.entity_tab.setTabText(self.entity_tab.indexOf(self.shot_tab), QtGui.QApplication.translate("Form", "Shots", None, QtGui.QApplication.UnicodeUTF8))
        self.select_btn.setText(QtGui.QApplication.translate("Form", "Filter", None, QtGui.QApplication.UnicodeUTF8))
        self.clear_btn.setText(QtGui.QApplication.translate("Form", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.refresh_btn.setText(QtGui.QApplication.translate("Form", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.arch_btn.setText(QtGui.QApplication.translate("Form", "Archive", None, QtGui.QApplication.UnicodeUTF8))
        self.log_btn.setText(QtGui.QApplication.translate("Form", "Log", None, QtGui.QApplication.UnicodeUTF8))

