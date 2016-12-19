wget -O PyQt5_gpl-5.7.tar.gz http://downloads.sourceforge.net/project/pyqt/PyQt5/PyQt-5.7/PyQt5_gpl-5.7.tar.gz?r=https%3A%2F%2Fwww.riverbankcomputing.com%2Fsoftware%2Fpyqt%2Fdownload5&ts=1481884926&use_mirror=kent
tar zxvf PyQt5_gpl-5.7.tar.gz
cd PyQt5_gpl-5.7
python configure.py
make
sudo make install