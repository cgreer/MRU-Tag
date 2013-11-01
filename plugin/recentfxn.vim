let g:mruFXNPluginHome = expand("<sfile>:p:h")
let g:mruDisplayMode = "byfile"
let g:mrutaglogFN = g:mruFXNPluginHome . "/../debug.txt"

function! Logger(logString)
   
    let appendList = ["VIMLOG: " . a:logString]
    let currLogInfo = readfile(g:mrutaglogFN)
    call writefile(currLogInfo + appendList, g:mrutaglogFN)

endfunction

function! WriteCurrentBufferToFile()
    " current buffer needs to be saved as a tmp file with correct extension

    let currentExtension = expand("%:e")
    let currModBuffer = g:mruFXNPluginHome . "/../tmp/cBuffers/cBuffer." . currentExtension
    silent execute "write! " . currModBuffer

endfunction

function! LogTagLocationInfo()

    " first, write the current buffer to a tmp file
    " This is needed because buffer contents could be unsaved and tag needs to
    " come from most recent state of code
    call Logger("LOGGING TAG INFO " . " test")  
    call WriteCurrentBufferToFile()

    " get the tags from the temporary file being edited.  Pass the name of the
    " edited file to allow MRUFunction to go to correct file when called on
    let currentExtension = expand("%:e")
    let logcmd = g:mruFXNPluginHome . "/recentfxn.py " . "log " . expand("%:p") . " " . line(".") . " " . col(".") . " " . currentExtension

    let err = system(logcmd)
    call Logger("log tag info err: " . err)

endfunction 

function HandleChoice()

    if g:mruDisplayMode == "fxn"
        call GoToFxnLocation()
    elseif g:mruDisplayMode == "byfile" 
        let currLine = getline('.')
        if currLine =~ '\v^(\+|-)\[.+\]'
            call UpdateExpandMenu(currLine)
        elseif currLine =~ '^\s*\.\.\.'
            call GoToFileLocation()
        else
            call GoToFxnLocation()
        endif
    endif

endfunction

function! UpdateExpandMenu(cLine)
    " get number inside brackets
    let expandNumber = matchstr(a:cLine, '\v(\+|-)\[\zs\d+')
    let logCmd = g:mruFXNPluginHome . '/recentfxn.py expand ' . expandNumber
    let err = system(logCmd)
    call Logger("UpdateExpandError: " . err)
    
    " open up the browser text
    let eFile =  g:mruFXNPluginHome . "/../tmp/windowtext.txt"
    exe "edit " . eFile

    call SetBrowserSettings()

endfunction

function! GoToFileLocation()    
    " Go to the file/function/line/column when you press enter (or enter a
    " number) on the mrufxn window

    let currLine = getline('.')
    let lineInfo = split(currLine, '\t')
    let fN = lineInfo[1]

    " close the mrufxn window
    silent! close

    " edit the file and go to the line IF we aren't there already
    if fnameescape(fN) != fnameescape(expand("%:p"))
        let editCommand = "edit " . fnameescape(fN)
        exe editCommand
    endif

endfunction

function! GoToFxnLocation()    
    " Go to the file/function/line/column when you press enter (or enter a
    " number) on the mrufxn window

    " get the filename, line, column
    " Check if vim supports multiple variable assignment @wtodo @vimscript

    " Remove spaces from string beginning if there
    let currLine = getline('.')
    if currLine =~ '^\s'
        let currLine = currLine[2:]
    endif

    let lineInfo = split(currLine, '\t')
    let fN = lineInfo[5]
    let lineOffset = lineInfo[2]
    let columnPosition = lineInfo[3] - 1
    let tagRegex = lineInfo[4]

    " close the mrufxn window
    silent! close

    " edit the file and go to the line
    if fnameescape(fN) != fnameescape(expand("%:p"))
        let editCommand = "edit " . fnameescape(fN)
        exe editCommand
    endif

    " go to function/method line
    exe "normal! gg" . tagRegex . "\<CR>"

    " go to last cursor position
    let l = line('.') + lineOffset
    let cp = columnPosition
    exe "call cursor(" . l . ", " . cp . ")"

    "log that we went here
    call LogTagLocationInfo()

endfunction

function! MRUFunction()


    " write current buffer contents to tmp file
    " needed to check for new/deleted tags in open files
    call WriteCurrentBufferToFile()

    " create mrufxn list
    let cBufName = fnameescape(expand("%:p"))
    let err = system(g:mruFXNPluginHome . "/recentfxn.py menu " . cBufName . " " . g:mruDisplayMode)
    call Logger("MRUFuncError: " . err) 

    " create new window
    belowright 10new

    " open up the browser text
    let eFile =  g:mruFXNPluginHome . "/../tmp/windowtext.txt"
    exe "edit " . eFile
    
    call SetBrowserSettings()
    
    exe "call cursor(2,1)"
    

endfunction

function SetBrowserSettings()
    exe "set ft=mrutext"
    set nonumber
    set nowrap
    " set nomodifiable
    nnoremap <buffer>q :q<CR>
    nnoremap <buffer><CR> :call HandleChoice()<CR> 
    nmap <buffer><F3> :q<CR> 
endfunction


" open MRUFunction Browser
nnoremap <F3> :call MRUFunction()<CR>

" log current fxn we are editing every time we insert text into a python file

autocmd InsertLeave *.py :call LogTagLocationInfo()
autocmd InsertLeave *.vim :call LogTagLocationInfo()
autocmd InsertLeave *.js :call LogTagLocationInfo()

autocmd InsertLeave *.c :call LogTagLocationInfo()
autocmd InsertLeave *.c++ :call LogTagLocationInfo()
autocmd InsertLeave *.cc :call LogTagLocationInfo()
autocmd InsertLeave *.cs :call LogTagLocationInfo()
autocmd InsertLeave *.cs :call LogTagLocationInfo()
autocmd InsertLeave *.earl :call LogTagLocationInfo()
autocmd InsertLeave *.go :call LogTagLocationInfo()
autocmd InsertLeave *.java :call LogTagLocationInfo()
autocmd InsertLeave *.pl :call LogTagLocationInfo()
autocmd InsertLeave *.pl :call LogTagLocationInfo()
autocmd InsertLeave *.rb :call LogTagLocationInfo()
autocmd InsertLeave *.ruby :call LogTagLocationInfo()
autocmd InsertLeave *.sh :call LogTagLocationInfo()
