set nocompatible
filetype plugin indent on
syntax on

execute pathogen#infect()

" Disable swap files
set noswapfile

" Map a leader key
let mapleader = ","

" Security
set modelines=0

" Remove Menu Bar, Toolbar, Scroll-bars
:set go-=m
:set go-=T
:set go-=r
:set go-=L

" Show file stats
set ruler

" Blink cursor on error instead of beeping (grr)
set visualbell

" Encoding
set encoding=utf-8

" Font
" Linux Variant:
"set guifont=Source\ Code\ Pro\ for\ Powerline\ 10
" macOS Variant:
set guifont=SourceCodeProForPowerline-Regular:h10

" Whitespace
set nowrap
set textwidth=120
set tabstop=2
set formatoptions=tcro
set shiftwidth=2
set softtabstop=2
set expandtab
set noshiftround
set autoindent

" Cursor and Scrolling Stuff
set scrolloff=3
set backspace=indent,eol,start
"set matchpairs+=<:> " use % to jump between pairs
"runtime! macros/matchit.vim
set cursorline
set cursorcolumn

" Move up/down editor lines
nnoremap j gj
nnoremap k gk

" Allow hidden buffers
set hidden

" managing buffers
nnoremap <C-Tab> :bnext<CR>
nnoremap <C-S-Tab> :bprevious<CR>
nmap <leader>bq :b#<bar>bd#<CR>

" Rendering
set ttyfast

" Status bar
set laststatus=2

" Last line
set showmode
set showcmd

" Folding
"set foldmethod=syntax
set foldnestmax=2

" Searching
nnoremap / /\v
vnoremap / /\v
set hlsearch
set incsearch
set ignorecase
set smartcase
set showmatch
nnoremap <silent> <Esc><Esc> <Esc>:nohlsearch<CR><Esc>

" Remap help key.
inoremap <F1> <ESC>:set invfullscreen<CR>a
nnoremap <F1> :set invfullscreen<CR>
vnoremap <F1> :set invfullscreen<CR>

" Formatting
map <leader>q gqip

" Uncomment this to enable by default:
" set list " To enable by default
" Or use your leader key + l to toggle on/off
map <leader>l :set list!<CR> " Toggle tabs and EOL

" Color scheme (terminal)
set t_Co=256
set background=dark
let g:solarized_termcolors=256
let g:solarized_termtrans=1
colorscheme iceberg

" NERDTree
" Toggle mapping
map <F2> :NERDTreeToggle<CR>
" Change Open NERDTree to current file location
map <leader>r :NERDTreeFind<CR>
" Close VIM if NERDTree is the only thing open
autocmd bufenter * if (winnr("$") == 1 && exists("b:NERDTree") && b:NERDTree.isTabTree()) | q | endif
autocmd vimenter * NERDTree
" Enter the file edit pane rather than keeping the cursor in the NERDTree pane
autocmd vimenter * wincmd p

" VIM Airline
let g:airline#extensions#tabline#enabled = 1
let g:airline_powerline_fonts = 1

" VIM Visual Increment
set nrformats=alpha

" VIM-HDL Plugin for VHDL Syntax Checking
" No configs yet....

" Highlight the TODO keyword in all code comments
autocmd Syntax * syntax keyword Todo containedin=.*Comment.* contained TODO

" Set the initial window size
set lines=48 columns=175

" Search Uses no magic which means all special characters act as regular ASCII until escaped
nnoremap / /
vnoremap / /
hi Search guibg=#6699bb guifg=#222222

" Create the FDC keywords
au BufRead,BufNewFile *.fdc set filetype=sdc
" Create the PDC keywords
au BufRead,BufNewFile *.pdc set filetype=pdc
" Create the NDC keywords
au BufRead,BufNewFile *.ndc set filetype=ndc
" Define .do as sdc syntax
au BufRead,BufNewFile *.do set filetype=sdc
" Create the Picoblaze Assembler keywords
au BufRead,BufNewFile *.psm set filetype=psm

" Use my custom PDC keywords
au! Syntax pdc source ~/.vim/syntax/pdc.vim
" Use my custom SDC keywords
au! Syntax sdc source ~/.vim/syntax/sdc.vim
" Use my custom NDC keywords
au! Syntax ndc source ~/.vim/syntax/ndc.vim
" Use my custom PSM keywords
au! Syntax psm source ~/.vim/syntax/psm.vim
