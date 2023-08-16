import sys

TT_PRINT = ["<print>", "<PRINT>"]
TT_ENDPRINT = ["</print>", "</PRINT>"]
TT_NEWLINE = ["<nl>", "<br>"]
TT_STRING = ["<string>", "<STRING>"]
TT_ENDSTRING = ["</string>", "</STRING>"]
TT_NUM = ["<num>", "<NUM>"]
TT_ENDNUM = ["</num>", "</NUM>"]


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

    for char in filecontent:
        tok += char
        print(tok) if debug == True else print(end="")
        if tok in " \t\n" and instring == False and innum == False:
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

        pos += 1

    return tokens

def interpret(tokens):
    inprint = False
    for i in range(0, len(tokens)):
        if inprint:
                
            if tokens[i].type == "ENDPRINT":
                inprint = False
            else:
                print(tokens[i].value, end="")
        else:    
            if tokens[i].type == "PRINT":
                inprint = True


def run():
    codefile = open(sys.argv[1]).read()
    toks = lex(codefile, debug=False)
    print(toks)
    interpret(toks)

run()