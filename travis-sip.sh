wget -O sip-4.18.1.tar.gz https://sourceforge.net/projects/pyqt/files/sip/sip-4.18.1/sip-4.18.1.tar.gz/download
tar zvxf sip-4.18.1.tar.gz
cd sip-4.18.1
python configure.py
make
sudo make install