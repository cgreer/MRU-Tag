" highlight Normal ctermbg=darkgrey
syntax clear

" braces for expandsion menus
syntax match digitBracketText "\v(\+|-)\["
syntax match digitBracketText "\v]"
syntax match digitBracketText "\v]"
highlight link digitBracketText HBrack 

" syntax for classes and prototypes
syntax match prototypeTag "\v^\s\s\S*\(\zs.*\ze\)\t"
highlight link prototypeTag HPTAG 

" Everything else make dark gray
syntax match extraInfo "\v\t\zs.*$"
highlight link extraInfo HBack 

" syntax match everyLine "\v^.*$"
" highlight link everyLine HBack 

highlight HDGray ctermfg=darkgray guifg=darkgray
highlight HBrack ctermfg=darkgray guifg=darkgray
highlight HPTAG ctermfg=darkgreen guifg=darkgreen
highlight HBack ctermfg=darkgray guifg=background
