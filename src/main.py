# coding: utf-8
from __future__ import print_function

import logging

from PySide2.QtCore import QSettings, QCoreApplication
from PySide2.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget

from src import tabs
from src.about import get_about_key
from src.widgets import ErrorDialog, AboutWidget


LOGGER = logging.getLogger('ProfileInspector.main')
LOGGER.info("\n\n=> START APPLICATION")

# HACK: Nuke will load this file directly
try:
    import nukescripts
except ImportError as error:
    LOGGER.warning('%s', error)
else:
    nukescripts.panels.registerWidgetAsPanel(
        'ProfileInspector.src.main.MainWindow', 'ProfileInspector',
        'ProfileInspector.MainWindow')


class MainWindowTabs(QTabWidget):
    def __init__(self):
        QTabWidget.__init__(self)

        self.addTab(tabs.DagInspector(), 'DAG')
        self.addTab(tabs.FileInspectorWidget(), 'XML Report')
        self.addTab(tabs.NukeLauncher(), 'Other')
        self.addTab(AboutWidget(), 'About')


class MainWindowWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self._tabs = MainWindowTabs()

        _layout = QVBoxLayout()
        _layout.addWidget(self._tabs)

        self.setLayout(_layout)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setObjectName('MainWindow')

        QSettings.setDefaultFormat(QSettings.IniFormat)
        QCoreApplication.setOrganizationName('virgilsisoe')
        QCoreApplication.setOrganizationDomain(get_about_key('Github'))
        QCoreApplication.setApplicationName('ProfileInspector')

        try:
            self.main_window = MainWindowWidget()
        except Exception as err:
            ErrorDialog(self, str(err)).show()
            LOGGER.critical(err, exc_info=True)
        else:
            self.setCentralWidget(self.main_window)
