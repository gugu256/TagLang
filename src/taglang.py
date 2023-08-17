import sys

TT_PRINT = ["<print>", "<PRINT>"]
TT_ENDPRINT = ["</print>", "</PRINT>"]
TT_NEWLINE = ["<nl>", "<br>"]
TT_STRING = ["<string>", "<STRING>"]
TT_ENDSTRING = ["</string>", "</STRING>"]
TT_NUM = ["<num>", "<NUM>"]
TT_ENDNUM = ["</num>", "</NUM>"]
TT_LET = ["<let>", "<LET>"]
TT_ENDLET = ["</let>", "</LET>"]
TT_NAME = ["<name>", "<NAME>"]
TT_ENDNAME = ["</name>", "</NAME>"]
TT_VAR = ["<var>", "<VAR>"]
TT_ENDVAR = ["</var>", "</VAR>"]
TT_GETVARS = ["<getvars>", "<GETVARS>"]

variables = {
    "_VERSION": 0.0
}

class Token:
    def __init__(self, type: str, value: any):
        self.type = type
        self.value = value

    def __repr__(self):
        return (self.type + ":" + '"' + self.value.replace("\n", "\\n") + '"') if self.type == "STRING" or self.type == "NEWLINE" else f"{self.type}:{self.value}"

def lex(filecontent, debug):
    tok = ""
    pos = 0
    tokens = []
    instring = False
    string = ""
    number = ""
    innum = False
    varname = ""
    inname = False

    for char in filecontent:
        tok += char
        print(tok) if debug == True else print(end="")
        if tok in " \t\n" and instring == False and inname == False:
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

        pos += 1

    return tokens

def interpret(tokens):
    inprint = False
    inlet = False
    current_var = ""
    current_value = None
    for i in range(0, len(tokens)):
        

        if inprint:
                
            if tokens[i].type == "ENDPRINT":
                inprint = False
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


def run():
    codefile = open(sys.argv[1]).read()
    toks = lex(codefile, debug=True)
    print(toks)
    interpret(toks)

run()