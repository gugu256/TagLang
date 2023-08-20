import sys
import os

TT_PRINT =        ["<print>", "<PRINT>"]
TT_ENDPRINT =     ["</print>", "</PRINT>"]
TT_NEWLINE =      ["<nl>", "<br>"]
TT_STRING =       ["<string>", "<STRING>"]
TT_ENDSTRING =    ["</string>", "</STRING>"]
TT_NUM =          ["<num>", "<NUM>"]
TT_ENDNUM =       ["</num>", "</NUM>"]
TT_LET =          ["<let>", "<LET>"]
TT_ENDLET =       ["</let>", "</LET>"]
TT_NAME =         ["<name>", "<NAME>"]
TT_ENDNAME =      ["</name>", "</NAME>"]
TT_VAR =          ["<var>", "<VAR>"]
TT_ENDVAR =       ["</var>", "</VAR>"]
TT_GETVARS =      ["<getvars>", "<GETVARS>"]
TT_CLEAR =        ["<clear>", "<CLEAR>"]
TT_COMMENT =      ["<!--"]
TT_ENDCOMMENT =   ["-->"]
TT_INPUT =        ["<input>", "<INPUT>"]
TT_ENDINPUT =     ["</input>", "</INPUT>"]
TT_NEXT =         ["<next>", "<NEXT>"]
TT_ENDNEXT =      ["</next>", "</NEXT>"]
TT_PREV =         ["<prev>", "<PREV>"]
TT_ENDPREV =      ["</prev>", "</PREV>"]
TT_TONUM =        ["<tonum>", "<TONUM>"]
TT_ENDTONUM =     ["</tonum>", "</TONUM>"]
TT_TOSTRING =     ["<tostring>", "<TOSTRING>"]
TT_ENDTOSTRING =  ["</tostring>", "</TOSTRING>"]
TT_EXPR =         ["<expr>", "<EXPR>", "<cond>", "<COND>"]
TT_ENDEXPR =      ["</expr>", "</EXPR>" "</cond>", "</COND>"]
TT_PY =           ["<py>", "<PY>"]
TT_ENDPY =        ["</py>", "</PY>"]
TT_DEL =          ["<del>", "<DEL>"]
TT_ENDDEL =       ["</del>", "</DEL>"]
TT_EVAL =         ["<eval>", "<EVAL>"]
TT_ENDEVAL =      ["</eval>", "</EVAL>"]
TT_EXE =          ["<exe>", "<EXE>", ]
TT_ENDEXE =       ["</exe>", "</EXE>", "</import>", "</IMPORT>"]
TT_QUIT =         ["<quit>", "<QUIT>", "<end>", "<END>"]
TT_IMPORT =       ["<import>", "<IMPORT>"]
TT_ENDIMPORT =    ["</import>", "</IMPORT>"]
TT_TRUE =         ["<true>", "<TRUE>"]
TT_FALSE =        ["<false>", "<FALSE>"]
TT_SUB =          ["<sub>", "<SUB>"]
TT_ENDSUB =       ["</sub>", "</SUB>"]
TT_GOSUB =        ["<gosub>", "<GOSUB>"]
TT_ENDGOSUB =     ["</gosub>", "</GOSUB>"]

variables = {
    "_VERSION": 0.0
}

subprocesses = {

}

def getvar(var):
    return variables[var]

class Token:
    def __init__(self, type: str, value: any):
        self.type = type
        self.value = value

    def __repr__(self):
        return (self.type + ":" + '"' + self.value.replace("\n", "\\n") + '"') if self.type == "STRING" or self.type == "NEWLINE" else (self.type + ":" + '(' + self.value.replace("\n", "\\n") + ')') if self.type == "EXPR" else (self.type + ":`" + self.value.replace("\n", "\\n").replace("\t", "\\t") + "`") if self.type == "PY" else f"{self.type}:{self.value}"

def lex(filecontent, show_tokens, show_token):
    tok = ""
    pos = 0
    tokens = []
    instring = False
    string = ""
    innum = False
    number = ""
    inname = False
    varname = ""
    invar = False
    variable = ""
    incomment = False
    comment = ""
    inexpr = False
    expr = ""
    inpy = False
    pythoncode = ""
    inimport = False
    package = ""
    ingosub = False
    subname = ""

    for char in filecontent:
        tok += char
        print(tok) if show_token == True else print(end="")
        if tok in " \t\n" and instring == False and incomment == False and inexpr == False and inpy == False:
            tok = ""

        if tok in TT_PRINT:
            tokens.append(Token("PRINT", None))
            tok = ""
        elif tok in TT_ENDPRINT:
            tokens.append(Token("ENDPRINT", None))
            tok = ""
        elif tok in TT_NEWLINE:
            tokens.append(Token("NEWLINE", "\n"))
            tok = ""
        elif tok in TT_NEXT:
            tokens.append(Token("NEXT", None))
            tok = ""
        elif tok in TT_ENDNEXT:
            tokens.append(Token("ENDNEXT", None))
            tok = ""
        elif tok in TT_PREV:
            tokens.append(Token("PREV", None))
            tok = ""
        elif tok in TT_ENDPREV:
            tokens.append(Token("ENDPREV", None))
            tok = ""
        elif tok in TT_TONUM:
            tokens.append(Token("TONUM", None))
            tok = ""
        elif tok in TT_ENDTONUM:
            tokens.append(Token("ENDTONUM", None))
            tok = ""
        elif tok in TT_TOSTRING:
            tokens.append(Token("TOSTRING", None))
            tok = ""
        elif tok in TT_ENDTOSTRING:
            tokens.append(Token("ENDTOSTRING", None))
            tok = ""
        elif tok in TT_GETVARS:
            tokens.append(Token("GETVARS", None))
            tok = ""
        elif tok in TT_LET:
            tokens.append(Token("LET", None))
            tok = ""
        elif tok in TT_ENDLET:
            tokens.append(Token("ENDLET", None))
            tok = ""
        elif tok in TT_SUB:
            tokens.append(Token("SUB", None))
            tok = ""
        elif tok in TT_ENDSUB:
            tokens.append(Token("ENDSUB", None))
            tok = ""
        elif tok in TT_DEL:
            tokens.append(Token("DEL", None))
            tok = ""
        elif tok in TT_ENDDEL:
            tokens.append(Token("ENDDEL", None))
            tok = ""
        elif tok in TT_EVAL:
            tokens.append(Token("EVAL", None))
            tok = ""
        elif tok in TT_ENDEVAL:
            tokens.append(Token("ENDEVAL", None))
            tok = ""
        elif tok in TT_EXE:
            tokens.append(Token("EXE", None))
            tok = ""
        elif tok in TT_ENDEXE:
            tokens.append(Token("ENDEXE", None))
            tok = ""
        elif tok in TT_CLEAR:
            tokens.append(Token("CLEAR", None))
            tok = ""
        elif tok in TT_QUIT:
            tokens.append(Token("QUIT", None))
            tok = ""
        elif tok in TT_TRUE:
            tokens.append(Token("BOOL", True))
            tok = ""
        elif tok in TT_FALSE:
            tokens.append(Token("BOOL", False))
            tok = ""
        elif tok in TT_INPUT:
            tokens.append(Token("INPUT", None))
            tok = ""
        elif tok in TT_ENDINPUT:
            tokens.append(Token("ENDINPUT", None))
            tok = ""

        elif tok in TT_ENDSTRING:
            tokens.append(Token("STRING", string))
            string = ""
            tok = ""
        elif tok in TT_STRING:
            if instring != True:
                instring = True
                tok = ""
            elif instring:
                string += tok
                tok = ""
        elif instring:
            string += tok
            if string[-9:] in TT_ENDSTRING:
                instring = False
                string = string[:-9].replace("\\n", "\n").replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "\r").replace("\\\\", "\\")
                tokens.append(Token("STRING", string))
                string = ""
                tok = ""
            else:
                tok = ""

        elif tok in TT_NUM:
            if innum != True:
                innum = True
                tok = ""
            elif innum:
                number += tok
                tok = ""
        elif innum:
            number += tok
            if number[-6:] in TT_ENDNUM:
                innum = False
                number = float(number[:-6]) if "." in  number[:-6] else int(number[:-6])
                tokens.append(Token("NUM", number))
                number = ""
                tok = ""
            else:
                tok = ""

        elif tok in TT_ENDNAME:
            tokens.append(Token("VARNAME", varname))
            varname = ""
            tok = ""
        elif tok in TT_NAME:
            if inname != True:
                inname = True
                tok = ""
            elif inname:
                varname += tok
                tok = ""
        elif inname:
            varname += tok
            if varname[-7:] in TT_ENDNAME:
                inname = False
                varname = varname[:-7]
                tokens.append(Token("VARNAME", varname))
                varname = ""
                tok = ""
            else:
                tok = ""
        
        elif tok in TT_ENDVAR:
            tokens.append(Token("VAR", variable))
            variable = ""
            tok = ""
        elif tok in TT_VAR:
            if invar != True:
                invar = True
                tok = ""
            elif invar:
                variable += tok
                tok = ""
        elif invar:
            variable += tok
            if variable[-6:] in TT_ENDVAR:
                invar = False
                variable = variable[:-6]
                tokens.append(Token("VAR", variable))
                variable = ""
                tok = ""
            else:
                tok = ""
        
        elif tok in TT_ENDCOMMENT:
            tokens.append(Token("COMMENT", comment))
            comment = ""
            tok = ""
        elif tok in TT_COMMENT or tok == "<comment>":
            if incomment != True:
                incomment = True
                tok = ""
            elif incomment:
                comment += tok
                tok = ""
        elif incomment:
            comment += tok
            if comment[-3:] in TT_ENDCOMMENT:
                incomment = False
                comment = comment[:-3]
                tokens.append(Token("COMMENT", comment))
                comment = ""
                tok = ""
            else:
                tok = ""
        
        elif tok in TT_ENDEXPR:
            tokens.append(Token("EXPR", expr))
            expr = ""
            tok = ""
        elif tok in TT_EXPR:
            if inexpr != True:
                inexpr = True
                tok = ""
            elif inexpr:
                expr += tok
                tok = ""
        elif inexpr:
            expr += tok
            if expr[-7:] in TT_ENDEXPR:
                inexpr = False
                expr = expr[:-7]
                expr = expr.replace("<var>", 'variables["').replace("</var>", '"]').replace("<VAR>", 'variables["').replace("</VAR>", '"]')
                expr = expr.replace("\"", '\\"')
                expr = expr.replace("<string>", "\"").replace("</string>", "\"").replace("<STRING>", "\"").replace("</STRING>", "\"")
                expr = expr.replace("<num>", "").replace("</num>", "").replace("<NUM>", "").replace("</NUM>", "")
                expr = expr.replace("<in>", "in").replace("<IN>", "in")
                expr = expr.replace("<and>", "and").replace("<AND>", "and")
                expr = expr.replace("<not>", "not").replace("<NOT>", "not")
                expr = expr.replace("<is>", "is").replace("<IS>", "is")
                tokens.append(Token("EXPR", expr))
                expr = ""
                tok = ""
            else:
                tok = ""
        
        elif tok in TT_ENDPY:
            tokens.append(Token("PY", pythoncode))
            pythoncode = ""
            tok = ""
        elif tok in TT_PY:
            if inpy != True:
                inpy = True
                tok = ""
            elif inpy:
                pythoncode += tok
                tok = ""
        elif inpy:
            pythoncode += tok
            if pythoncode[-5:] in TT_ENDPY:
                inpy = False
                pythoncode = pythoncode[:-5]
                pythoncode = pythoncode.replace("\\n", "\n").replace("\\t", "\t").replace("\\n", "\n").replace("\\r", "\r").replace("\\\\", "\\")
                tokens.append(Token("PY", pythoncode))
                pythoncode = ""
                tok = ""
            else:
                tok = ""
        
        elif tok in TT_ENDIMPORT:
            tokens.append(Token("IMPORT", package + ".taglang"))
            package = ""
            tok = ""
        elif tok in TT_IMPORT:
            if inimport != True:
                inimport = True
                tok = ""
            elif inimport:
                package += tok
                tok = ""
        elif inimport:
            package += tok
            if package[-9:] in TT_ENDIMPORT:
                inimport = False
                package = package[:-9].replace(".", "/")
                tokens.append(Token("IMPORT", package + ".taglang"))
                package = ""
                tok = ""
            else:
                tok = ""
        
        elif tok in TT_ENDGOSUB:
            tokens.append(Token("GOSUB", subname))
            subname = ""
            tok = ""
        elif tok in TT_GOSUB:
            if ingosub != True:
                ingosub = True
                tok = ""
            elif ingosub:
                package += tok
                tok = ""
        elif ingosub:
            subname += tok
            if subname[-8:] in TT_ENDGOSUB:
                ingosub = False
                subname = subname[:-8]
                tokens.append(Token("GOSUB", subname))
                subname = ""
                tok = ""
            else:
                tok = ""

        pos += 1
    
    print(tokens) if show_tokens == True else print(end="")

    return tokens

def interpret(tokens):          # The place where tokens are interpreted
    inprint = False             # Indicates if we are printing stuff 
    inlet = False               # Indicates if we are defining variables 
    current_var = ""            # The name of the variable we're defining
    current_value = None        # The value of the variable we're defining
    pos = 0                     # The position in an input statment (var name or arguments)
    ininp = False               # Indicates if we are asking ofr input
    innext = False              # Indicates if we are incrementing a value
    inprev = False              # Indicates if we are decrementing a value
    innumconversion = False     # Indicates if we are converting somehting to a NUM
    instringconversion = False  # Indictaes iof we are converting something to a STRING
    target_var = ""             # The var the conversion will be stored in 
    indel = False               # Indicates if we are deleting a variable
    ineval = False              # Indicates if we are running TagLang code
    inexe = False               # Indicates if we are running TagLang code from a file
    insub = False               # Indicates if we are defining a subprocess
    subname = ""                # The name of the subprocess we're defining

    # The Normal Vars array makes sure we don't add useless variables in the variables dictionary (see how the PY token is interepreted to understand why this is useful)
    normal_vars = ["subname", "insub", "inexe", "ineval", "indel", "normal_vars", "i", "pos", "tokens", "inprint", "inlet", "current_var", "current_value", "pos", "ininp", "innext", "inprev", "innumconversion", "instringconversion", "target_var"]

    for i in range(0, len(tokens)):

        # Little explanation for the two next lines, 
        # The first line makes sure that a variable is not replaced by its value in functions that have the first arg as a variable (example : In INPUT, the first argument has to be a variable, but the next arguments for the prompt might be variables' values)
        # The second line makes sure that a variable is not replaced by its value in functions where every variable is an arg (example: in TONUM, every variiable is an argument, and none of their values are used)
                                  
        if tokens[i].type == "VAR" and tokens[i-1].type != "INPUT" and tokens[i-1].type != "NEXT" and tokens[i-1].type != "PREV" and tokens[i-1].type != "TONUM" and tokens[i-1].type != "TOSTRING" and tokens[i].type != "DEL" : # Replaces variable tokens by their value
            if not innumconversion and not instringconversion and not indel:
                varname = tokens[i].value
                tokens[i].value = getvar(varname)
                del varname
        
        if tokens[i].type == "EXPR":
            expr = tokens[i].value
            tokens[i].value = eval(expr)
            del expr

        if inprint: # Printing
                
            if tokens[i].type == "ENDPRINT":
                inprint = False
            else:
                print(tokens[i].value, end="") if tokens[i].type != "COMMENT" else print(end="")

        elif inlet: # Defining variables
            if tokens[i].type == "ENDLET":
                variables[current_var] = current_value
                current_var = ""
                current_value = 0
                inlet = False
            elif tokens[i].type == "VARNAME":
                if current_value != None:
                    variables[current_var] = current_value
                    current_value = None
                current_var = tokens[i].value
            else:
                current_value = tokens[i].value
        
        elif ininp: # Inputting
            if tokens[i].type == "ENDINPUT":
                variables[current_var] = input("")
                pos = 0
                ininp = False
                current_var = ""
            elif tokens[i].type == "VARNAME" and pos == 0 or tokens[i].type == "VAR" and pos == 0:
                current_var = tokens[i].value
                pos += 1
            else:
                print(tokens[i].value, end="")
                pos += 1
        
        elif innext: # Incrementing by 1
            if tokens[i].type == "ENDNEXT":
                variables[current_var] += 1
                current_var = ""
                innext = False
            else:
                current_var = tokens[i].value
        
        elif inprev: # Decrementing by 2
            if tokens[i].type == "ENDPREV":
                variables[current_var] -= 1
                current_var = ""
                inprev = False
            else:
                current_var = tokens[i].value

        elif innumconversion: # Convert to NUM
            if tokens[i].type == "ENDTONUM":
                variables[target_var] = float(variables[current_var]) if "." in str(current_var) else int(variables[current_var])
                pos = 0
                current_var = ""
                target_var = ""
                innumconversion = False
            else:
                if pos == 0:
                    current_var = tokens[i].value
                else:
                    target_var = tokens[i].value
                pos += 1
        
        elif instringconversion: # Convert to STRING
            if tokens[i].type == "ENDTOSTRING":
                variables[target_var] = str(variables[current_var])
                pos = 0
                current_var = ""
                target_var = ""
                instringconversion = False
            else:
                if pos == 0:
                    current_var = tokens[i].value
                else:
                    target_var = tokens[i].value
                pos += 1
        
        elif indel: # Delete variables:
            if tokens[i].type == "ENDDEL":
                indel = False
            else:
                del variables[tokens[i].value]
        
        elif ineval: # Run TagLang code
            if tokens[i].type == "ENDEVAL":
                ineval = False
            else:
                interpret(lex(tokens[i].value, False, False))
        
        elif inexe: # Run TagLang code from a file
            if tokens[i].type == "ENDEXE":
                inexe = False
            else:
                interpret(lex(open(tokens[i].value, "r").read(), False, False))
        
        elif insub: # Define a subprocess
            if tokens[i].type == "ENDSUB":
                insub = False
                subname = ""
            elif tokens[i].type == "VARNAME":
                subname = tokens[i].value
            else:
                try:
                    subprocesses[subname].append(tokens[i])
                except KeyError:
                    subprocesses[subname] = []
                    subprocesses[subname].append(tokens[i])

        else:    
            if tokens[i].type == "PRINT":
                inprint = True
            elif tokens[i].type == "LET":
                inlet = True
            elif tokens[i].type == "GETVARS":
                print(variables)
            elif tokens[i].type == "CLEAR":
                os.system("cls" if os.name == 'nt' else "clear")
            elif tokens[i].type == "COMMENT":
                pass
            elif tokens[i].type == "INPUT":
                ininp = True
            elif tokens[i].type == "NEXT":
                innext = True
            elif tokens[i].type == "PREV":
                inprev = True
            elif tokens[i].type == "TONUM":
                innumconversion = True
            elif tokens[i].type == "TOSTRING":
                instringconversion = True
            elif tokens[i].type == "PY":
                for key in variables:
                    locals()[key] = variables[key]
                del key
                
                exec(tokens[i].value)
                
                for key in variables:
                    exec(f"del {key}")
                del key
                varz = locals()
                for key in varz:
                    if key not in normal_vars:
                        variables[key] = varz[key]
                del key
            elif tokens[i].type == "DEL":
                indel = True
            elif tokens[i].type == "EVAL":
                ineval = True
            elif tokens[i].type == "EXE":
                inexe = True
            elif tokens[i].type == "QUIT":
                quit()
            elif tokens[i].type == "IMPORT":
                interpret(lex(open(tokens[i].value, "r").read(), False, False))
            elif tokens[i].type == "SUB":
                insub = True
            elif tokens[i].type == "GOSUB":
                interpret(subprocesses[tokens[i].value])

def run():
    codefile = open(sys.argv[1]).read()
    toks = lex(codefile, show_token=False, show_tokens=True)
    
    interpret(toks)

run()