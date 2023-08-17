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
TT_COMMENT =      ["<comment>", "<COMMENT>"]
TT_ENDCOMMENT =   ["</comment>", "</COMMENT>"]

variables = {
    "_VERSION": 0.0
}

def getvar(var):
    return variables[var]

class Token:
    def __init__(self, type: str, value: any):
        self.type = type
        self.value = value

    def __repr__(self):
        return (self.type + ":" + '"' + self.value.replace("\n", "\\n") + '"') if self.type == "STRING" or self.type == "NEWLINE" else f"{self.type}:{self.value}"

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

    for char in filecontent:
        tok += char
        print(tok) if show_token == True else print(end="")
        if tok in " \t\n" and instring == False and incomment == False:
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
        elif tok in TT_GETVARS:
            tokens.append(Token("GETVARS", None))
            tok = ""
        elif tok in TT_LET:
            tokens.append(Token("LET", None))
            tok = ""
        elif tok in TT_CLEAR:
            tokens.append(Token("CLEAR", None))
            tok = ""
        elif tok in TT_ENDLET:
            tokens.append(Token("ENDLET", None))
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
                string = string[:-9]
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
            if comment[-10:] in TT_ENDCOMMENT:
                incomment = False
                comment = comment[:-10]
                tokens.append(Token("COMMENT", comment))
                comment = ""
                tok = ""
            else:
                tok = ""

        pos += 1
    
    print(tokens) if show_tokens == True else print(end="")

    return tokens

def interpret(tokens):
    inprint = False
    inlet = False
    current_var = ""
    current_value = None
    for i in range(0, len(tokens)):
        
        if tokens[i].type == "VAR":
            varname = tokens[i].value
            tokens[i].value = getvar(varname)
            del varname
            #i -= 1

        if inprint:
                
            if tokens[i].type == "ENDPRINT":
                inprint = False
            #elif tokens[i].type == "VAR":
            #    print(getvar(tokens[i].value), end="")
            else:
                print(tokens[i].value, end="")
        elif inlet:
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

def run():
    codefile = open(sys.argv[1]).read()
    toks = lex(codefile, show_token=False, show_tokens=True)
    
    interpret(toks)

run()