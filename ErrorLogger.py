from PyQt5 import QtWidgets

class ErrorLogger:

    def WriteError(ErrorText):
        try:
            log_file = open(r"ErrorLogger.txt", "a")
            log_file.write("\n" + ErrorText)
            log_file.close()  
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, 'Exception raised', format(e))    

        # except Exception as e:
        #     ErrorLogger.WriteError('Line 177: ' + str(e))
        #     QtWidgets.QMessageBox.critical(None, 'Exception raised', format(e))                 