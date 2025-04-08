import sys
from PyQt5.QtWidgets import QApplication
from iqt_pyqt.ui import JSONAppUI

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JSONAppUI()
    ex.show()
    sys.exit(app.exec_())