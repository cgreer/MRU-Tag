# MRU-Tag
  *Spend less time navigating and more time coding!*

## Introduction
MRU-Tag allows you to quickly jump to your most recently used files and tags(functions/methods/etc).  

![Sample Output](https://github.com/sequenceGeek/MRU-Function/raw/master/sample.gif)

## Install
(Note: MRU-Tag currently requires Python to be installed and has not been tested on Windows machines)

1. Install Exuberant Ctags.

        sudo apt-get install exuberant-ctags  
    
2. Install [Pathogen](https://github.com/tpope/vim-pathogen) (Vim Plugin Manager).  
3. Clone MRU-Function repo into your vim bundle directory.  

        cd ~/.vim/bundle  
        git clone git@github.com:sequenceGeek/MRU-Function.git

## Usage
(Note: start editing code inside functions/methods/etc to populate browser)
- Pressing `<F3>` opens the MRU Tag Browser.
- Select a file and press `<Enter>` to expand the file's MRU tags.
- Select a tag and press `<Enter>` to jump to the tag.
