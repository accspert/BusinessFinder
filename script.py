from modules.yelp_scraper import scrape_yelp
from modules.yell_scraper import scrape_yell
from modules.googleMapsScraper import getDataFromGoogleMaps
from modules.bingMapsScraper import getDataFromBingMaps

from PyQt5 import uic, QtGui, QtCore, QtWidgets
from PyQt5.QtWidgets import *
import sys
import csv
import os 
from pathlib import Path
import Email
import pandas as pd
from ErrorLogger import *
from keyvalidator import *
from crypto import *


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        file = os.path.join(Path(__file__).resolve().parent, "BusinessFinder.ui")
        uic.loadUi(file, self)
        self.all_data = []

        self.pushButtonLoadLeads.clicked.connect(lambda: [self.load_leads(self.lineEditLocation.text(), 
                                                          self.lineEditBusiness.text(),self.lineEditMaxCount.text())])
        self.pushButtonSaveToCSV.clicked.connect(self.save_to_csv)
        self.pushButtonClose.clicked.connect(self.close)
        self.pushButtonDelete.clicked.connect(self.delete)
        self.pushButtonScrapeMail.clicked.connect(self.scrape_mail)
        self.pushButtonRemoveDuplicates.clicked.connect(self.remove_duplicates)
        
    def load_leads(self, places, query, maxCountStr):
        data = []
        try:
            if maxCountStr:
                maxCount = int(maxCountStr)
            else:
                maxCount = 500
            if self.lineEditLocation.text() and self.lineEditBusiness.text():
                if self.comboBox.currentText() == 'Google Maps':
                    data = getDataFromGoogleMaps(places, query,maxCount)
                elif self.comboBox.currentText() == 'Yelp.com':
                    data = scrape_yelp(places, query)
                elif self.comboBox.currentText() == 'Yell.com':
                    data = scrape_yell(places, query)
                elif self.comboBox.currentText() == 'Bing Maps':
                    data = getDataFromBingMaps(places, query,maxCount)
                if data:
                    self.all_data += data
                    self.fillTable(self.all_data)
                else:
                    QtWidgets.QMessageBox.information(None, 'No Data', 'No Data could be scraped ') 
            else:
                QtWidgets.QMessageBox.information(None, 'No Data', 'Enter Keyword and Location') 
        except Exception as e:
                ErrorLogger.WriteError(traceback.format_exc())
                QtWidgets.QMessageBox.critical(None, 'Exception raised', format(e))

    def fillTable(self, all_data) :
            self.tableWidget.setRowCount(0)
            for row, form in enumerate(all_data):
                row_position = self.tableWidget.rowCount()
                self.tableWidget.insertRow(row_position) 
                for column, item in enumerate(form):
                    if item:
                       self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
                      
    def scrape_mail(self):
        # self.all_data = [['','','', 'carpetcleanersyork.com'],
        #           ['','','','enviro-clean.co.uk/' ],
        #           ['','','', 'servicemasterclean.co.uk'],
        #           ['','','','excellencefloorcare.co.uk' ],
        #           ['','','', 'cleananddryofyork.co.uk/'],
        #           ['','','', 'yorkdrycarpetcleaning.co.uk'],
        #           ['','','', 'equipsupplygo.com']
        #           ]

        try:
            if self.all_data:
                self.tableWidget.setRowCount(0)
                for row, form in enumerate(self.all_data):
                    row_position = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(row_position) 
                    for column, item in enumerate(form):
                        if column == 3:
                            if item:
                                url_to_scrape = item.strip()
                                email = Email.email_extract(url_to_scrape)
                                if email:
                                    self.tableWidget.setItem(row, column +1 , QTableWidgetItem(str(email)))
                                    # self.all_data[row][4] = email
                        if column in [0,1,2,3]:
                            if item:
                                self.tableWidget.setItem(row, column, QTableWidgetItem(str(item)))
            else:
                QtWidgets.QMessageBox.information(None, 'No Data', 'No Data could be scraped ') 
        except Exception as e:
                ErrorLogger.WriteError(traceback.format_exc())
                QtWidgets.QMessageBox.critical(None, 'Exception raised', format(e))                            
        
    def delete(self):
        
        rows = self.tableWidget.selectionModel().selectedRows()

        indexes = []
        for row in rows:
            indexes.append(row.row())

        # Reverse sort rows indexes
        indexes = sorted(indexes, reverse=True)

        # Delete rows
        for rowidx in indexes:
            self.tableWidget.removeRow(rowidx)
            self.all_data.pop(rowidx)
            
    def save_to_csv(self):
        
        path = QFileDialog.getSaveFileName(
                self, 'Save File', '', 'CSV(*.csv)')
        if path[0]:
            columnHeaders = []
    
            # create column header list
            for j in range(self.tableWidget.model().columnCount()):
                columnHeaders.append(self.tableWidget.horizontalHeaderItem(j).text())
    
            df = pd.DataFrame(columns=columnHeaders)
    
            # create dataframe object recordset
            for row in range(self.tableWidget.rowCount()):
                for col in range(self.tableWidget.columnCount()):
                    if  self.tableWidget.item(row, col) is not None:
                        df.at[row, columnHeaders[col]] = self.tableWidget.item(row, col).text()
    
            df.to_csv(path[0], index=False)
    
    def remove_duplicates(self):
        temp_list = self.all_data
        self.all_data = []
        self.all_data = [t for t in (set(tuple(i) for i in temp_list))]
     
        self.fillTable(self.all_data)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    make_a_expire_date()
    if os.path.isfile("hanso.txt"):
        if datetime.date(datetime.now()) >= get_expire_date() :
            vef_key, ok = QInputDialog().getText(window, "Expired :-(",
                                              "Your try has expired. Enter your license key:", QLineEdit.Normal)
            if ok and vef_key:
                if not verify_account_key(vef_key):
                    QtWidgets.QMessageBox.critical(None, 'Error','This key is not valid' )
                    sys.exit()
                else:
                    os.remove("hanso.txt")
                    QtWidgets.QMessageBox.information(None, 'Success','Your Software is acitvated, enjoy' )
            else:
                  sys.exit()    
    window.show()
    sys.exit(app.exec())    