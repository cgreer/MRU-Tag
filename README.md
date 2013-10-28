# MRU-Tag
Spend less time navigating and more time coding!

MRU-Tag allows you to quickly jump to the most recently used files and tags(functions/methods/etc). 
![Sample Output](https::github.com/sequenceGeek/MRU-Function/raw/master/sample.gif)

## Install
(Note: MRU-Tag currently requires Python and is only tested on Linux)
1. Install Exuberant Ctags.

        sudo apt-get install exuberant-ctags  
    
2. Install [Pathogen](https://github.com/tpope/vim-pathogen) (Vim Plugin Manager).  
3. Clone MRU-Function repo into your vim bundle directory.  

        cd ~/.vim/bundle  
        git clone git@github.com:sequenceGeek/MRU-Function.git

## Usage 
(Edit code in a few functions/methods/etc to populate Browser)
- Pressing `<F3>` opens the MRU Function Browser.
- Select file and press `<Enter>` to expand the file's MRU tags.
- Select tag and press `<Enter>` to jump to tag
