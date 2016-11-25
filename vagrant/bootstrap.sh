sudo add-apt-repository -y ppa:webupd8team/java
wget -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -
echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee -a /etc/apt/sources.list.d/neo4j.list
sudo apt-get update
sudo apt-get -y upgrade
echo debconf shared/accepted-oracle-license-v1-1 select true | sudo debconf-set-selections
echo debconf shared/accepted-oracle-license-v1-1 seen true | sudo debconf-set-selections
sudo apt-get -y install oracle-java8-installer
apt-get install -y apache2
sudo ufw enable
sudo ufw allow 80/tcp
sudo ufw allow 7474/tcp
# python3 is included in ubuntu box
sudo apt -y install python3-pip
sudo pip3 install virtualenv
sudo pip3 install virtualenvwrapper
# add to .profile
# export WORKON_HOME=$HOME/.virtualenvs
# export PROJECT_HOME=$HOME/Devel
# export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3
# source /usr/local/bin/virtualenvwrapper.sh
# neo4j
sudo apt-get install neo4j=3.1.3

# configure vim
mkdir -p ~/.vim/autoload ~/.vim/bundle && \
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim
cd ~/.vim/bundle && \
git clone https://github.com/tpope/vim-sensible.git
# add to .vimrc

git clone https://github.com/scrooloose/nerdtree.git ~/.vim/bundle/nerdtree

git clone git://github.com/altercation/vim-colors-solarized.git ~/.vim/bundle/vim-colors-solarized
