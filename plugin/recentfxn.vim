let g:pluginHome = expand("<sfile>:p:h")


function! StoreTraversedFunctionInfo()
    
    " note the expand for a filename @i @priming @example
    " let currentFN = expand("%:p")

    " execute commands in functions @i
    " set mark to go back to after parsing function name
    execute "normal! mu" 

    " search for nearest fxn name
    " Note that you have to put the \<cr> to make sure it executes search
    execute "normal! ?def .*(.*):\<cr>"
    
    " get the name of the function
    let fxnName = matchstr(getline('.'), 'def .*(.*):')

    " go back to mark
    execute "normal! `u" 
   
    " compose contents to write to file
    " join in vim, getting current filename @i
    " concatenate in vimscript @i
    let appendList = [join([fxnName, expand("%:p"), line('.'), col('.')], "\t")]
    let inFxnFN = g:pluginHome . "/.mrufxndata"

    " append info to file @example @append @vim
    call writefile(readfile(inFxnFN) + appendList, inFxnFN)
    
endfunction 

function! GoToFxnLocation()
    
    " Go to the file/function/line/column when you press enter (or enter a
    " number) on the mrufxn window

    " assume enter was pressed

    " get the filename, line, column
    " Check if vim supports multiple variable assignment @wtodo @vimscript
    let lineInfo = split(getline('.'), '\t')
    let fN = lineInfo[1]
    let lineNumber = lineInfo[2]
    let columnPosition = lineInfo[3] - 1

    " close the mrufxn window
    silent! close

    " edit the file and go to the line
    let editCommand = "edit " . fnameescape(fN)
    echom editCommand
    exe editCommand 
    exe "call cursor(" . lineNumber . ", " . columnPosition . ")"

endfunction

function! MRUFunction()

    " create new window
    belowright 12new

    " create mrufxn list
    call system(g:pluginHome . "/recentfxn.py")
    let eFile = g:pluginHome . "/.mrufxns"
    exe "edit " . eFile
    
    nnoremap <buffer>q :q<CR>
    nnoremap <buffer><CR> :call GoToFxnLocation()<CR> 

endfunction

" map leader <F3> to open the mrufxn window
nnoremap <F3> :call MRUFunction()<CR>

" log current fxn we are editing every time we insert text into a python file
autocmd InsertLeave *.py :call StoreTraversedFunctionInfo()
