# MRU Function

## Install
1. Install Exuberant Ctags.

        sudo apt-get install exuberant-ctags  
    
2. Install [Pathogen](https://github.com/tpope/vim-pathogen) (Vim Plugin Manager).  
3. Clone MRU-Function repo into your vim bundle directory.  

        cd ~/.vim/bundle  
        git clone git@github.com:sequenceGeek/MRU-Function.git

## Usage 
- Pressing `<F3>` opens the MRU Function Browser.
- Select function/method and press `<Enter>`.

## Todo/Issues
- Check if function exists/was moved.
- Display in a way you can select the file and THEN pick the function/method under the file.
- Custom nearest tag function for python to handle nested functions/methods.
- Add gif to show usage.
- Fix "wrongly logged tag due to file being edited" bug.
