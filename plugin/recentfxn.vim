
let g:pluginHome = expand("<sfile>:p:h")

function! LogTagLocationInfo()

    " test
    let logcmd = g:pluginHome . "/recentfxn.py " . "log " . expand("%:p") . " " . line(".") . " " . col(".")
    echom logcmd
    let err = system(logcmd)
    echom "err" . err

endfunction 

function! GoToFxnLocation()
    
    " Go to the file/function/line/column when you press enter (or enter a
    " number) on the mrufxn window

    " assume enter was pressed

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
    let editCommand = "edit " . fnameescape(fN)
    echom editCommand
    exe editCommand

    " go to function/method line
    exe "normal! gg" . tagRegex . "\<CR>"

    " go to last cursor position
    let l = line('.') + lineOffset
    let cp = columnPosition + 1
    echom "pos " . l . " " . columnPosition
    exe "call cursor(" . l . ", " . cp . ")"

endfunction

function! MRUFunction()

    " create new window
    belowright 12new

    " create mrufxn list
    call system(g:pluginHome . "/recentfxn.py browsertext")
    let eFile = g:pluginHome . "/windowtext.txt"
    exe "edit " . eFile
    
    nnoremap <buffer>q :q<CR>
    nnoremap <buffer><CR> :call GoToFxnLocation()<CR> 

endfunction

" map leader <F3> to open the mrufxn window
nnoremap <F3> :call MRUFunction()<CR>

" log current fxn we are editing every time we insert text into a python file

autocmd InsertLeave *.py :call LogTagLocationInfo()
autocmd InsertLeave *.vim :call LogTagLocationInfo()
