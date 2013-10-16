let g:mruFXNPluginHome = expand("<sfile>:p:h")

function! LogTagLocationInfo()

    " first, write the current buffer to a tmp file
    " This is needed because buffer contents could be unsaved and tag needs to
    " come from most recent state of code
    
    " current buffer needs to be saved as a tmp file with correct extension
    let currentExtension = expand("%:e")

    " change vim to vimL to avoid Pathogen sourcing... Don't want .vim tmp
    " files to be sourced
    if currentExtension == "vim"
        let currentExtension = "vimL"
    endif
    " echom "tmp extension " . currentExtension

    let cbc = g:mruFXNPluginHome . "/tmp/cBuffer." . currentExtension
    execute "write! " . cbc

    " get the tags from the temporary file being edited.  Pass the name of the
    " edited file to allow MRUFunction to go to correct file when called on
    let logcmd = g:mruFXNPluginHome . "/recentfxn.py " . "log " . expand("%:p") . " " . line(".") . " " . col(".") . " " . currentExtension

    " echom "log cmd: " . logcmd
    let err = system(logcmd)
    " echom "err: " . err

endfunction 

function! GoToFxnLocation()    
    " Go to the file/function/line/column when you press enter (or enter a
    " number) on the mrufxn window

    " get the filename, line, column
    " Check if vim supports multiple variable assignment @wtodo @vimscript
    let lineInfo = split(getline('.'), '\t')
    let fN = lineInfo[5]
    let lineOffset = lineInfo[2]
    let columnPosition = lineInfo[3] - 1
    let tagRegex = lineInfo[4]

    " close the mrufxn window
    silent! close

    " edit the file and go to the line
    if fnameescape(fN) != fnameescape(expand("%:p"))
        let editCommand = "edit " . fnameescape(fN)
        " echom editCommand
        exe editCommand
    endif

    " go to function/method line
    exe "normal! gg" . tagRegex . "\<CR>"

    " go to last cursor position
    let l = line('.') + lineOffset
    let cp = columnPosition + 1
    " echom "pos " . l . " " . columnPosition
    exe "call cursor(" . l . ", " . cp . ")"

endfunction

function! MRUFunction()

    " create new window
    belowright 12new

    " create mrufxn list
    call system(g:mruFXNPluginHome . "/recentfxn.py browsertext")

    " open up the browser text
    let eFile =  g:mruFXNPluginHome . "/windowtext.txt"
    exe "edit " . eFile
    
    nnoremap <buffer>q :q<CR>
    nnoremap <buffer><CR> :call GoToFxnLocation()<CR> 

endfunction

" open MRUFunction Browser
nnoremap <F3> :call MRUFunction()<CR>

" log current fxn we are editing every time we insert text into a python file

autocmd InsertLeave *.py :call LogTagLocationInfo()
autocmd InsertLeave *.vim :call LogTagLocationInfo()
