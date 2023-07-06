# Make any initial directories...
cd ~
mkdir -p ~/.vim
cd ~/.vim
mkdir autoload bundle plugin doc

# Clone Pathogen package manager for VIM
echo -e "\nPathogen"
curl -LSso ~/.vim/autoload/pathogen.vim https://tpo.pe/pathogen.vim

cd ~

# Install pathogen packages
echo -e "\nNERDTree"
git clone https://github.com/preservim/nerdtree.git ~/.vim/pack/vendor/start/nerdtree
vim -u NONE -c "helptags ~/.vim/pack/vendor/start/nerdtree/doc" -c q
echo -e "\nTabular"
git clone https://github.com/godlygeek/tabular.git ~/.vim/bundle/tabular
echo -e "\nAirline"
git clone https://github.com/vim-airline/vim-airline.git ~/.vim/bundle/vim-airline
echo -e "\nAirline-Themes"
git clone https://github.com/vim-airline/vim-airline-themes.git ~/.vim/bundle/vim-airline-themes
echo -e "\nIndent Guides"
git clone https://github.com/preservim/vim-indent-guides.git ~/.vim/bundle/vim-indent-guides

# Install Gitgutter (isn't there a Pathogen way?)
echo -e "\nGit Gutter"
mkdir -p ~/.vim/pack/airblade/start
cd ~/.vim/pack/airblade/start
git clone https://github.com/airblade/vim-gitgutter.git
vim -u NONE -c "helptags vim-gitgutter/doc" -c q

cd ~

# Install extra syntax highlighters
echo -e "\nColorschemes"
cd ~/.vim
git clone https://github.com/flazz/vim-colorschemes.git
rsync -av ~/.vim/vim-colorschemes/colors ~/.vim/
rsync -av ~/.vim/vim-colorschemes/scripts ~/.vim/
rm -fr ~/.vim/vim-colorscheme
echo -e "\nVerilog/SystemVerilog Syntax highlighter"
cd ~/.vim/bundle
git clone https://github.com/vhda/verilog_systemverilog.vim
cd ~

# Install Visual Incrementer
echo -e "\nVisual Incrementer"
cd ~/.vim/plugin
wget https://raw.githubusercontent.com/triglav/vim-visual-increment/master/plugin/visual-increment.vim
cd ~/.vim/doc
wget https://raw.githubusercontent.com/triglav/vim-visual-increment/master/doc/visual-increment.txt
cd ~

# Pull the latest .vimrc
echo -e "\nMy .vimrc"
wget https://raw.githubusercontent.com/rdustinb/WrenchAndGear/master/env_and_vim/.vimrc ~/ 
dos2unix ~/.vimrc
