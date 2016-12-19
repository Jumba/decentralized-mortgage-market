sudo apt-get install qtdeclarative5-dev qt5-default
wget -O PyQt5_gpl-5.7.tar.gz "http://downloads.sourceforge.net/project/pyqt/PyQt5/PyQt-5.7/PyQt5_gpl-5.7.tar.gz?r=&ts=1482146895&use_mirror=vorboss"
tar zxf PyQt5_gpl-5.7.tar.gz
cd PyQt5_gpl-5.7
python configure.py --qmake /usr/lib/x86_64-linux-gnu/qt5/bin/qmake  --sip-incdir ../sip-4.18.1/siplib
make
sudo make install