" Disable vi compatible mode
set nocompatible

"filetype indent plugin on

" turn on syntax highlight
syntax on

" Enable Pathogen for loading plugins from the bundle folder
execute pathogen#infect()

" backup to /local/vim/backup
set backup
set backupdir=/local/vim/backup,~/.vim/backup
set backupskip=/tmp/*,/private/tmp/*
" swap files to /local/vim/swap
set directory=/local/vim/swap,~/.vim/swap
set noswapfile
set writebackup

" Allow the user to 'hide' buffers (on the buffer list)
set hidden
set nowrap
set autoindent
set history=1024
set ignorecase
set showmatch
set showmode

" Turn on the Cursor Crosshairs
set cursorline
set cursorcolumn

" Setup the code fold colors
hi Folded guibg=darkmagenta guifg=white

" Setup Horizontal and Vertical Split colors
hi Vertsplit guibg=white guifg=black

" GVIM Code Folding
au BufWritePost,BufLeave,BufWinLeave ?* mkview
au BufWinEnter ?* silent loadview

" Fold and Create folds with F9
inoremap <F9> <C-O>za
nnoremap <F9> za
onoremap <F9> <C-C>za
vnoremap <F9> zf

" Disable Auto-Fold for Markdown
let g:vim_markdown_folding_style_pythonic = 1
let g:vim_markdown_json_frontmatter = 1
let g:vim_markdown_new_list_item_indent = 2

" Turn off all scroll bars, toolbar and menu bar
set guioptions-=T
set guioptions-=m
set guioptions-=r
set guioptions-=L

:set formatoptions+=t
:set formatoptions+=c
:set formatoptions+=q
:set formatoptions+=r
:set formatoptions+=o

" Disable Visual and Audible Bells
set noeb vb t_vb=
au GUIEnter * set vb t_vb=

" Python style guide settings
set tabstop=2
set expandtab
set softtabstop=2
set shiftwidth=2
" Similar to the column highlight down below. Wrap at the column before the highlight.
set textwidth=120
" vim-airline shows which line we are on, so disable the builtin
" VIM line numbers
"set number
" Add gutter space since we are no longer showing line numbers in the
" left column
set foldcolumn=1
set bs=2
set list

" Remap the <Leader> key
let mapleader=","
:map <Tab> >
:map <S-Tab> <

" Enable modelines .... used to tweak files if needed
set modelines=1

" Configure gVim to look pretty good
let hostname = substitute(system('hostname'), '\n', '', '')

" vim-airline configuration
set laststatus=2
let g:airline#extensions#tabline#enabled=1
let g:airline#extensions#hunks#enabled=0
let g:airline#extensions#branch=0
let g:airline#extensions#tabline#fnamemod = ':t'
let g:airline_powerline_fonts=1
let g:airline_theme='base16'
let g:airline_section_b = '%{strftime("%A")}'
let g:airline_section_c = '%{strftime("%H:%M")}'
let g:airline_section_y = '%t'

set bg=dark
" VIM Font
if has('unix')
  if system("uname") == "Darwin\n"
    " MACVIM Has a different font rendering size
    " and font callout than the linux side
    set guifont=Source\ Code\ Pro\ for\ Powerline:h10
  else
    set guifont=Liberation\ Mono\ for\ Powerline\ Medium\ 8.5
  endif
endif
set lines=40 columns=165
" Set the color scheme to something that I can read on a black
colorscheme codeschool

" NERDTree Open on Startup
let NERDTreeShowBookmarks=1
"let g:NERDTreeWinPos="right"
au VimEnter * NERDTree
au VimEnter * wincmd p

" Ignore Certain files (we won't ever open these as they are binaries)
let NERDTreeIgnore=['\.wlf$', '\.ucdb$']

" Auto close NERDTree if the only buffer open
autocmd WinEnter * call s:CloseIfOnlyNerdTreeLeft()
function! s:CloseIfOnlyNerdTreeLeft()
  if exists("t:NERDTreeBufName")
    if bufwinnr(t:NERDTreeBufName) != -1
      if winnr("$") == 1
        q
      endif
    endif
  endif
endfunction

" Easier buffer switching, works with airline
nnoremap <C-Tab>    :bn <CR>
nnoremap <C-S-Tab>  :bp <CR>

" Close current buffer, switch to previous
nmap <leader>bq :bp <BAR> bd #<CR>

" Show list of current buffers
nmap <leader>bl :ls <CR>

" mapping a key to toggle the cursorline and cursorcolumn
" " changed to not conflict with NERDComment
:nnoremap <Leader>/c :set cursorline! cursorcolumn!<CR>

" Turn on the leading white space macro
let g:indent_guides_enable_on_vim_startup = 1
let g:indent_guides_auto_colors = 0
let g:indent_guides_start_level = 2
autocmd VimEnter,Colorscheme * :hi IndentGuidesEven guibg=#273333 ctermbg=7

" Enable incremental searches. VIM begins highlighting matched characters in a
" search string as the user is typing. Nice dynamic search capability
set incsearch
" Highlight Search Terms with an olive green color
set hlsearch
" gui= Options, {attr-list} in help docs
" bold
" underline
" undercurl
" reverse
" inverse
" italic
" standout
" NONE
:hi Search guibg=#848444 gui=bold

" Mapping // to search for the text under a visually-selected block
:vnoremap // y/<C-R>"<CR>

" holy mother of jesus stop suspending my windows!!!!!
:map <C-z> u

" Change the cursor line/column colors
hi CursorLine guibg=#446666
hi CursorColumn guibg=#446666

" Change Color when entering Insert Mode
autocmd InsertEnter * highlight CursorLine guibg=#664444
autocmd InsertEnter * highlight CursorColumn guibg=#664444

" Revert Color to default when leaving Insert Mode
autocmd InsertLeave * highlight CursorLine guibg=#446666
autocmd InsertLeave * highlight CursorColumn guibg=#446666

" Only enable cursorline and cursorcolumn in the current window
augroup cursorline
  au!
  au VimEnter,WinEnter,BufWinEnter * setlocal cursorline
  au WinLeave * setlocal nocursorline
augroup end

augroup cursorcolumn
  au!
  au VimEnter,WinEnter,BufWinEnter * setlocal cursorcolumn
  au WinLeave * setlocal nocursorcolumn
augroup end

" map 'control-n' to 'nohlsearch' or 'noh'
" turns of search highlight
nmap <silent> <C-N> :set hls!<CR>:set hls?<CR>

" Color the 80eth Column for proper code alignment
highlight ColorColumn guibg=#3a2a3a
set cc=121,122

" Color is specific for the colorscheme codeschool in dark mode, change if
" colorscheme is altered.
highlight FoldColumn guibg=#252c31

" Tool F-Keys
" Map the Spelling Errors key
nmap <silent> <F1> :set spell!<CR>:set nospell?<CR>
" Map the NERDTree key
map <F2> :NERDTreeToggle <CR>
" Map the GUndo key
nnoremap <F3> :GundoToggle<CR>

"-------------------------------------------------
"                 MACROS!!!!!!!
" Macros can be recorded with the following sequence:
"   q<macro letter/number>
"   key strokes and command sequences follow.
"   q
"
" The macros can then be invoked by commanding:
"   @<macro letter/number>
"
" from command mode (not insert or visual mode).
"
" Macros already attached to a letter/number can
" be pasted (p) by using the command:
"   "<macro letter/number>p
"-------------------------------------------------
let @a='V:s:input :output:'
let @b='V:s:output:input :'
"let @c='dw?kuyw?kd?klpb??c??b'
" This macro is a little more robust than the example above as
" it works for visual mode to refactor a large group of lines
" beginning with numbers (as in a case statement. Simply highlight
" all line you wish to renumber and use normal @c
let @c='wdwkuywkdklpbýcýb'
"-------------------------------------------------
"           Highlight Verilog Instances
"   This will actually only highlight the ports
" of the instances but will allow the highlighting
" to occur on individual lines rather than requiring
" the entire search match to be present before the
" highlighting occurs. Highlighting an entire
" instance causes the highlight to disappear when
" scrolling down to where the actual instance
" declaration is no longer visible.
"
" The autocommand needs a nested keyword to tell the
" autocommander that the following is a nested
" command and not part of the original autcommand
" syntax.
"-------------------------------------------------
"highlight VerilogInstances guibg=#223344
"au VimEnter,WinEnter,BufWinEnter * nested match VerilogInstances /\.\w\+ *(\p*),\{0,1}/

" Clear previous search
nnoremap <esc> :noh<return><esc>

" ################## Python Development Specific stuff ##################
" Add the Smart Indent function for keywords in Python files
autocmd BufRead *.py set smartindent cinwords=if,elif,else,for,while,try,except,finally,def,class

"Enable code completion
autocmd FileType python set omnifunc=pythoncomplete#Complete

" ------------------- Jazz -----------------------
" This sections adds a new highlighter for the Jazz
" Language.
" au BufRead,BufNewFile *.jzz set filetype=jazz
" au! Syntax jazz source C:/Program\ Files/Vim/vim72/syntax/jazz.vim

"------------------- plist -----------------------
au BufRead,BufNewFile *.plist set filetype=xml
"-------------------- Do -------------------------
au BufRead,BufNewFile *.do set filetype=tcl
"---------- Chipscope Probes File ----------------
au BufRead,BufNewFile *.ltx set filetype=xml
"------------- FPGA Constraints ------------------
au BufRead,BufNewFile *.ucf set filetype=tcl
au BufRead,BufNewFile *.xdc set filetype=tcl
au BufRead,BufNewFile *.sdc set filetype=tcl
au BufRead,BufNewFile *.fdc set filetype=tcl
"-------------------- SV -------------------------
au BufRead,BufNewFile *.sv set filetype=verilog_systemverilog
au BufRead,BufNewFile *.svh set filetype=verilog_systemverilog
au BufRead,BufNewFile *.vh set filetype=verilog_systemverilog
au BufRead,BufNewFile *.v set filetype=verilog_systemverilog
au BufRead,BufNewFile *.vhd set filetype=vhdl
"------------------- Conky -----------------------
au BufNewFile,BufRead *conkyrc set filetype=conkyrc
