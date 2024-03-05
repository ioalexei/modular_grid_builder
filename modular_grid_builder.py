# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ModularGridBuilder
                                 A QGIS plugin
 This plugin creates a modular layout grid for print layouts
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2024-03-04
        git sha              : $Format:%H$
        copyright            : (C) 2024 by Alexei
        email                : modulargrid@fastmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import QgsProject, QgsPrintLayout, QgsLayoutGuideCollection, QgsLayout, QgsLayoutGuide, QgsLayoutMeasurement, QgsPageSizeRegistry
import qgis.core 

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .modular_grid_builder_dialog import ModularGridBuilderDialog
import os.path

# Function to increment values by alternating steps (row/col size + gutter)
# https://stackoverflow.com/questions/39241505/python-simple-way-to-increment-by-alternating-values
from itertools import cycle
def range_alternate_steps(start, stop, steps=(1,)):
    steps = cycle(steps)
    val = start
    while val < stop:
        yield val
        val += next(steps)


class ModularGridBuilder:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'ModularGridBuilder_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Modular Grid')

        # Check if plugin was started the first time in current QGIS session
        # Must be set in initGui() to survive plugin reloads
        self.first_start = None

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('ModularGridBuilder', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/modular_grid_builder/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Modular Grid'),
            callback=self.run,
            parent=self.iface.mainWindow())

        # will be set False in run()
        self.first_start = True


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&Modular Grid'),
                action)
            self.iface.removeToolBarIcon(action)



    def run(self):
        """Run method that performs all the real work"""

        # Create the dialog with elements (after translation) and keep reference
        # Only create GUI ONCE in callback, so that it will only load when the plugin is started
        if self.first_start == True:
            self.first_start = False
            self.dlg = ModularGridBuilderDialog()

        paperSizes = qgis.core.QgsPageSizeRegistry()
        paperSizeList = []
        for paperSize in paperSizes.entries():
            paperSizeList.append(f"{paperSize.name} - {paperSize.size.height()} × {paperSize.size.width()}{paperSize.size.units()}")

        self.dlg.paperSizeSelector.addItems(paperSizeList) 

        # show the dialog
        self.dlg.show()

        # Run the dialog event loop
        result = self.dlg.exec_()

        # See if OK was pressed
        if result:

            selectedPageSize = self.dlg.paperSizeSelector.currentIndex()

            page_width = qgis.core.QgsPageSizeRegistry().entries()[selectedPageSize].size.width()
            page_height = qgis.core.QgsPageSizeRegistry().entries()[selectedPageSize].size.height()


            num_columns = self.dlg.numColumnsInput.value()
            num_rows = self.dlg.numColumnsInput.value()

            gutter = self.dlg.gutterInput.value()

            margin_left = self.dlg.marginLeftInput.value()
            margin_right = self.dlg.marginRightInput.value()
            margin_top = self.dlg.marginTopInput.value()
            margin_bottom = self.dlg.marginBottomInput.value()

            column_width = (page_width - margin_left - margin_right - (gutter * (num_columns - 1))) / num_columns
            row_height = (page_height - margin_top - margin_bottom - (gutter * (num_rows - 1))) / num_rows

            vertical_guides = list(range_alternate_steps(margin_left, (page_width - margin_right), (column_width, gutter)))
            vertical_guides.append(vertical_guides[-1]+column_width)

            print(vertical_guides)

            horizontal_guides = list(range_alternate_steps(margin_top, (page_height - margin_bottom), (row_height, gutter)))
            horizontal_guides.append(horizontal_guides[-1]+row_height)

            print(horizontal_guides)

            # identify current project
            project = QgsProject.instance()

            # initiate layout manager 
            manager = project.layoutManager()

            layout = QgsPrintLayout(project) ## https://qgis.org/pyqgis/master/core/QgsLayout.html#qgis.core.QgsLayout

            layout.initializeDefaults()
            layout.setName("Layout 1")
            manager.addLayout(layout)

            # Set up Layout Guide Collection to hold the guides 
            guidecollection = QgsLayoutGuideCollection(layout=layout, pageCollection=layout.pageCollection())
            #guidecollection.setLayout(layout=layout)
            guidecollection.setVisible(True)
            guidecollection.update()

            # Create guides in loop
            #https://doc.qt.io/qt-6/qt.html#Orientation-enum
            #orientation=1 # Horizontal 
            #orientation=2 # Vertical
            # https://qgis.org/pyqgis/master/core/QgsLayoutMeasurement.html#qgis.core.QgsLayoutMeasurement
            #position=QgsLayoutMeasurement(length=10, units=Qgis.LayoutUnit.Millimeters)

            for i in vertical_guides: 
                guide_vertical = QgsLayoutGuide(orientation=2, position=QgsLayoutMeasurement(length=i, units=qgis.core.Qgis.LayoutUnit.Millimeters), page=layout.pageCollection().pages()[0]) # returns only or first page
                guidecollection.addGuide(guide_vertical)

            for i in horizontal_guides: 
                guide_horizontal = QgsLayoutGuide(orientation=1, position=QgsLayoutMeasurement(length=i, units=qgis.core.Qgis.LayoutUnit.Millimeters), page=layout.pageCollection().pages()[0]) # returns only or first page
                guidecollection.addGuide(guide_horizontal)





            
