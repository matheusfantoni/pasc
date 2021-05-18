import sys

from ts import TS
from tag import Tag
from token import Token


class Lexer():
    '''
    Classe que representa o Lexer (AFD):

    [1] Voce devera se preocupar quando incremetar as linhas e colunas,
    assim como, quando decrementar ou reinicia-las. Lembre-se, ambas 
    comecam em 1.

    '''

    def __init__(self, input_file):
        try:
            self.input_file = open(input_file, 'rb')
            self.lookahead = 0
            self.n_line = 1
            self.n_column = 1
            self.ts = TS()
        except IOError:
            print('Erro de abertura do arquivo. Encerrando.')
            sys.exit(0)

    def closeFile(self):
        try:
            self.input_file.close()
        except IOError:
            print('Erro ao fechar arquivo. Encerrando.')
            sys.exit(0)

    def sinalizaErroLexico(self, message):
        print("[Erro Lexico]: ", message)

    def retornaPonteiro(self):
        if(self.lookahead.decode('ascii') != ''):
            self.input_file.seek(self.input_file.tell()-1)

    def printTS(self):
        self.ts.printTS()

    def proxToken(self):

        # Implementando um AFD.

        estado = 1
        lexema = ""
        c = '\u0000'

        while(True):
            self.lookahead = self.input_file.read(1)
            c = self.lookahead.decode('ascii')

            if(estado == 1):

                if(c == ''):
                    return Token(Tag.EOF, "EOF", self.n_line, self.n_column)
                elif(c == ' ' or c == '\t' or c == '\n' or c == '\r'):

                    if(c == '\n'):
                        self.n_line += 1

                    estado = 1
                elif(c == '='):
                    estado = 2
                elif(c == '!'):
                    lexema += c
                    estado = 5
                elif(c == '<'):
                    estado = 7
                elif(c == '>'):
                    estado = 10
                elif(c == '+'):
                    # Simula estado 13
                    return Token(Tag.OP_AD, "+", self.n_line, self.n_column)
                elif(c == '-'):
                    # Simula estado 14
                    return Token(Tag.OP_MIN, "-", self.n_line, self.n_column)
                elif(c == '*'):
                    # Simula estado 15
                    return Token(Tag.OP_MUL, "*", self.n_line, self.n_column)
                elif(c == '/'):
                    estado = 16
                elif(c == '{'):
                    # Simula estado 22
                    return Token(Tag.SMB_OBC, "{", self.n_line, self.n_column)
                elif(c == '}'):
                    # Simula estado 23
                    return Token(Tag.SMB_CBC, "}", self.n_line, self.n_column)
                elif(c == '('):
                    # Simula estado 24
                    return Token(Tag.SMB_OPA, "(", self.n_line, self.n_column)
                elif(c == ')'):
                    # Simula estado 25
                    return Token(Tag.SMB_CPA, ")", self.n_line, self.n_column)
                elif(c == ','):
                    # Simula estado 26
                    return Token(Tag.SMB_COM, ",", self.n_line, self.n_column)
                elif(c == ';'):
                    # Simula estado 27
                    return Token(Tag.SMB_SEM, ";", self.n_line, self.n_column)
                elif(c.isdigit()):
                    lexema += c
                    estado = 28
                elif(c.isalpha()):
                    lexema += c
                    estado = 31
                elif(c == '"'):
                    lexema += c
                    estado = 33
                else:
                    self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " + str(
                        self.n_line) + " e coluna " + str(self.n_column))
                    estado = 1
            elif(estado == 2):

                if(c == '='):
                    return Token(Tag.OP_EQ, "==", self.n_line, self.n_column)
                else:
                    # Simula estado 3
                    self.retornaPonteiro()
                    return Token(Tag.OP_ATRIB, "=", self.n_line, self.n_column)

            elif(estado == 5):
                if(c == '='):
                    return Token(Tag.OP_NE, "!=", self.n_line, self.n_column)
                else:
                    self.sinalizaErroLexico("Caractere invalido [" + c + "] na linha " + str(
                        self.n_line) + " e coluna " + str(self.n_column))
                    estado = 1

            elif(estado == 7):
                if(c == '='):
                    return Token(Tag.OP_LE, "<=", self.n_line, self.n_column)

                # Simula estado 9
                self.retornaPonteiro()
                return Token(Tag.OP_LT, "<", self.n_line, self.n_column)
            elif(estado == 10):
                if(c == '='):
                    return Token(Tag.OP_GE, ">=", self.n_line, self.n_column)

                # Simula estado 12
                self.retornaPonteiro()
                return Token(Tag.OP_GT, ">", self.n_line, self.n_column)

            elif(estado == 16):
                if(c == '/'):
                    estado = 17

                elif(c == '*'):
                    estado = 19  # Implementar parte do comentário /**/

                else:
                    self.retornaPonteiro()
                    return Token(Tag.OP_DIV, "/", self.n_line, self.n_column)

            elif(estado == 17):

                if(c == '\n'):
                    self.n_line += 1
                    self.n_column = 1
                    estado = 1
                    # Comentários começando por //
                else:
                    estado = 17

            elif(estado == 19):
                if(c == '*'):
                    estado = 20
                    # Comentários começando por /*
                else:
                    estado = 19

            elif(estado == 20):
                if(c == '/'):
                    estado = 1

                else:
                    estado = 20

            elif(estado == 28):
                if(c.isdigit()):
                    lexema += c

                elif(c == '.'):
                    lexema += c
                    estado = 30

                else:
                    # Simula o estado 29
                    self.retornaPonteiro()
                    return Token(Tag.NUM_CONST, lexema, self.n_line, self.n_column)

            elif(estado == 30):
                if(c.isdigit()):
                    lexema += c
                    estado = 36

                else:
                    self.sinalizaErroLexico("Caractere invalido [" + lexema + "] na linha " + str(
                        self.n_line) + " e coluna " + str(self.n_column))
                    return None

            elif(estado == 36):
                if(c.isdigit()):
                    lexema += c

                else:
                    # Simula estado 37
                    self.retornaPonteiro()
                    return Token(Tag.NUM_CONST, lexema, self.n_line, self.n_column)

            elif(estado == 31):
                if(c.isalnum()):
                    lexema += c

                else:
                    # Simula o estado 32
                    self.retornaPonteiro()
                    token = self.ts.getToken(lexema)

                    if(token is not None):
                        token.setLinha(self.n_line)
                        token.setColuna(self.n_column)

                    else:
                        token = Token(Tag.ID, lexema,self.n_line, self.n_column)
                        self.ts.addToken(lexema, token)
                    return token

            elif (estado == 33):
                
                if(c.isascii()):
                    estado = 34
                    
                else:
                    self.sinalizaErroLexico("Caractere invalido [" + lexema + "] na linha " + str(
                        self.n_line) + " e coluna " + str(self.n_column))
                    
                    return None

            elif(estado == 34):
                if(c.isascii()):
                    lexema += c
                                
                else:
                    return Token(Tag.CHAR_CONST, lexema, self.n_line, self.n_column)
                           
            # fim if's de estados
        # fim while
