sudo mkdir -p /builds && sudo chmod a+rw /builds
sudo mkdir -p /downloads && sudo chmod a+rw /downloads
curl -L -o /downloads/sip.tar.gz https://sourceforge.net/projects/pyqt/files/sip/sip-4.18.1/sip-4.18.1.tar.gz
tar xzf /downloads/sip.tar.gz -C /builds --keep-newer-files
cd /builds/sip-4.18.1 && python configure.py && sudo make && sudo make install