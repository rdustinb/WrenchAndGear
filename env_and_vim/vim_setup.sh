# Make any initial directories...
cd ~
mkdir -p ~/.vim
cd ~/.vim
mkdir autoload bundle plugin

# Clone Pathogen package manager for VIM
cd autoload
git clone https://github.com/tpope/vim-pathogen.git

cd ~

# Install pathogen packages
git clone https://github.com/preservim/nerdtree.git ~/.vim/bundle/nerdtree
git clone https://github.com/godlygeek/tabular.git ~/.vim/bundle/tabular
git clone https://github.com/vim-airline/vim-airline.git ~/.vim/bundle/vim-airline
git clone https://github.com/vim-airline/vim-airline-themes.git ~/.vim/bundle/vim-airline-themes
git clone https://github.com/preservim/vim-indent-guides.git ~/.vim/bundle/vim-indent-guides

# Install Gitgutter (isn't there a Pathogen way?)
mkdir -p ~/.vim/pack/airblade/start
cd ~/.vim/pack/airblade/start
git clone https://github.com/airblade/vim-gitgutter.git
vim -u NONE -c "helptags vim-gitgutter/doc" -c q

cd ~

# Install extra syntax highlighters
git submodule add https://github.com/flazz/vim-colorschemes.git ~/.vim/bundle/colorschemes
cd ~/.vim/bundle
git clone https://github.com/vhda/verilog_systemverilog.vim
cd ~

# Install Visual Incrementer
cd ~/.vim/plugin
wget https://github.com/vim-scripts/visual-increment/tree/master/plugin/visual-increment.vim
cd ~/.vim/doc
wget https://github.com/vim-scripts/visual-increment/tree/master/doc/visual-increment.txt
cd ~
