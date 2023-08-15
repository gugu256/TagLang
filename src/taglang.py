import sys

TT_PRINT = ["<print>", "<PRINT>"]
TT_ENDPRINT = ["</print>", "</PRINT>"]
TT_STRING = ["<string>", "<STRING>"]
TT_ENDSTRING = ["</string>", "</STRING>"]


class Token:
    def __init__(self, type: str, value: any):
        self.type = type
        self.value = value

    def __repr__(self):
        return f"{self.type}:\"{self.value}\"" if self.type == "STRING" else f"{self.type}:{self.value}"

def lex(filecontent, debug):
    tok = ""
    pos = 0
    tokens = []
    instring = False
    string = ""

    for char in filecontent:
        tok += char
        print(tok) if debug == True else print(end="")
        if tok in " \t\n" and instring == False:
            tok = ""

        if tok in TT_PRINT:
            tokens.append(Token("PRINT", None))
            tok = ""
        elif tok in TT_ENDPRINT:
            tokens.append(Token("ENDPRINT", None))
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

        pos += 1

    return tokens


def run():
    codefile = open(sys.argv[1]).read()
    print(lex(codefile, debug=False))

run()