sudo apt-get update -qq
sudo apt-get install -qq libav-tools libjs-excanvas libjs-mootools libsodium13 libx11-6 python-apsw python-cherrypy3 python-crypto python-cryptography python-feedparser python-leveldb python-libtorrent python-m2crypto python-netifaces python-pil python-pyasn1 python-requests python-twisted python-wxgtk2.8 python2.7 vlc python-pip python-pyqt5
pip install decorator
pip install cryptography
pip install faker
pip install twisted
pip install m2crypto
# install libsodium
wget ftp.us.debian.org/debian/pool/main/libs/libsodium/libsodium13_1.0.0-1_amd64.deb
sudo dpkg -i libsodium13_1.0.0-1_amd64.deb