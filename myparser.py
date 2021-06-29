import sys

from tag import Tag


# Classe que representa o Parser (Analisador Sintático)

class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proxToken()  # Leitura inicial obrigatoria do primeiro simbolo
        if self.token is None:  # erro no Lexer
            sys.exit(0)

    def sinalizaErroSintatico(self, message):
        print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(
            self.token.getColuna()) + ": ")
        print(message, "\n")

    def advance(self):
        print("[DEBUG] token: ", self.token.toString())
        self.token = self.lexer.proxToken()
        if self.token is None:  # erro no Lexer
            sys.exit(0)

    def skip(self, message):
        self.sinalizaErroSintatico(message)
        self.advance()

    # verifica token esperado t
    def eat(self, t):
        if self.token.getNome() == t:
            self.advance()
            return True
        else:
            return False

    #      1° Bloco - Regras

    # prog → “program” “id” body
    def prog(self):
        if not self.eat(Tag.KW_PROGRAM):
            self.sinalizaErroSintatico("Esperado \"PROGRAM\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

        if not self.eat(Tag.ID):
            self.sinalizaErroSintatico("Esperado \"ID\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

        self.body()
        if self.token.getNome() != Tag.EOF:
            self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

    # body → decl-list “{“ stmt-list “}”
    def body(self):
        self.decl_list()
        if not self.eat(Tag.SMB_OBC):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

        self.stmt_list()

        if not self.eat(Tag.SMB_CBC):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # decl-list → decl “;” decl-list  | ε
    def decl_list(self):
        if self.token.getNome() == Tag.KW_NUM or self.token.getNome() == Tag.KW_CHAR:
            self.decl()
            if self.eat(Tag.SMB_SEM):
                self.decl_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None
        else:
            return

    # decl → type id-list
    def decl(self):
        self.type()
        self.id_list()

    # type → “num” | “char”
    def type(self):
        if self.token.getNome() == Tag.KW_NUM:
            self.eat(Tag.KW_NUM)
        elif self.token.getNome() == Tag.KW_CHAR:
            self.eat(Tag.KW_CHAR)
        else:
            self.sinalizaErroSintatico(
                "Esperado \"NUM\" ou \"CHAR\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # id-list → “id” id_list_linha
    def id_list(self):
        if not self.eat(Tag.ID):
            self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            return None
        self.id_list_linha()

    # id_list_linha → “,” id-list | ε
    def id_list_linha(self):
        if self.token.getNome() == Tag.SMB_COM:
            self.eat(Tag.SMB_COM)
            self.id_list()
        else:
            return

    #  2° Bloco - Regras

    # stmt-list → stmt “;” stmt-list  | ε
    def stmt_list(self):
        if self.token.getNome() == Tag.ID:
            self.assign_stmt()
            if self.eat(Tag.SMB_SEM):
                self.stmt_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None
        elif self.token.getNome() == Tag.KW_IF:
            self.if_stmt()
            if self.eat(Tag.SMB_SEM):
                self.stmt_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None
        elif self.token.getNome() == Tag.KW_WHILE:
            self.while_stmt()
            if self.eat(Tag.SMB_SEM):
                self.stmt_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None
        elif self.token.getNome() == Tag.KW_READ:
            self.read_stmt()
            if self.eat(Tag.SMB_SEM):
                self.stmt_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None
        elif self.token.getNome() == Tag.KW_WRITE:
            self.write_stmt()
            if self.eat(Tag.SMB_SEM):
                self.stmt_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None
        else:
            return

    # stmt → assign-stmt | if-stmt | while-stmt | read-stmt | write-stmt
    def stmt(self):
        if self.eat(Tag.ID) or self.eat(Tag.KW_IF) or self.eat(Tag.KW_WHILE) or self.eat(Tag.KW_READ) or self.eat(
                Tag.KW_WRITE):
            self.advance()

        else:
            self.sinalizaErroSintatico(
                "Esperado \"ID, IF, WHILE, READ ou WRITE\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    #  # assign-stmt → “id” “=” simple_expr
    def assign_stmt(self):
        if self.eat(Tag.ID):
            if not self.eat(Tag.OP_ATRIB):
                self.sinalizaErroSintatico("Esperado \"=\", encontrado " + "\"" + self.token.getLexema() + "\"")
            else:
                self.simple_expr()
                return
        else:
            self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # if-stmt → “if” “(“ expression “)” “{“ stmt-list “}” if-stmt_linha
    def if_stmt(self):
        if self.eat(Tag.KW_IF):
            if not self.eat(Tag.SMB_OPA):
                self.sinalizaErroSintatico("Esperado \"(\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None

            self.expression()

            if not self.eat(Tag.SMB_CPA):
                self.sinalizaErroSintatico("Esperado \")\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None

            if not self.eat(Tag.SMB_OBC):
                self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None

            self.stmt_list()

            if not self.eat(Tag.SMB_CBC):
                self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None

            self.if_stmt_linha()

        else:
            self.sinalizaErroSintatico("Esperado \"IF\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # if-stmt’ → “else” “{“ stmt-list “}” | ε
    def if_stmt_linha(self):
        if self.eat(Tag.KW_ELSE):
            if not self.eat(Tag.SMB_OBC):
                self.sinalizaErroSintatico("Esperado \"{\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                return None

            self.stmt_list()

            if not self.eat(Tag.SMB_CBC):
                self.sinalizaErroSintatico("Esperado \"}\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                return None

        else:
            return

    # while-stmt → stmt-prefix “{“ stmt-list “}”
    def while_stmt(self):
        self.stmt_prefix()

        if not self.eat(Tag.SMB_OBC):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

        self.stmt_list()

        if not self.eat(Tag.SMB_CBC):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # stmt-prefix → “while” “(“ expression “)”
    def stmt_prefix(self):
        if self.eat(Tag.KW_WHILE):
            if not self.eat(Tag.SMB_OPA):
                self.sinalizaErroSintatico("Esperado \"(\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None

            self.expression()

            if not self.eat(Tag.SMB_CPA):
                self.sinalizaErroSintatico("Esperado \")\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None
        else:
            self.sinalizaErroSintatico("Esperado \"WHILE\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # read-stmt → “read” “id”
    def read_stmt(self):
        if self.eat(Tag.KW_READ):
            if not self.eat(Tag.ID):
                self.sinalizaErroSintatico("Esperado \"ID\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None
        else:
            self.sinalizaErroSintatico("Esperado \"READ\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # write-stmt → “write” simple-expr
    def write_stmt(self):
        if self.eat(Tag.KW_WRITE):
            self.simple_expr()
            return
        else:
            self.sinalizaErroSintatico("Esperado \"WRITE\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    #    3° Bloco - Regras

    # expression → simple_expr expression_linha
    def expression(self):
        self.simple_expr()
        self.expression_linha()

    # expression_linha → logop simple_expr expression_linha | ε
    def expression_linha(self):
        if self.eat(Tag.KW_AND) or self.eat(Tag.KW_OR):
            self.simple_expr()
            self.expression_linha()

    # simple_expr → term simple_exp_linha
    def simple_expr(self):
        self.term()
        self.simple_exp_linha()

    # simple_exp_linha → relop term simple_exp_linha | ε
    def simple_exp_linha(self):
        if (self.eat(Tag.OP_EQ) or self.eat(Tag.OP_GT) or self.eat(Tag.OP_GE) or
                self.eat(Tag.OP_LT) or self.eat(Tag.OP_LE) or self.eat(Tag.OP_NE)):
            self.term()
            self.simple_exp_linha()

    # term → factor_b term_linha
    def term(self):
        self.factor_b()
        self.term_linha()

    # term_linha → addop factor_b term_linha | ε
    def term_linha(self):
        if self.eat(Tag.OP_AD) or self.eat(Tag.OP_MIN):
            self.factor_b()
            self.term_linha()

    # factor_b → factor_a factor_b_linha
    def factor_b(self):
        self.factor_a()
        self.factor_b_linha()

    # factor_b_linha → mulop factor_a factor_b_linha | ε
    def factor_b_linha(self):
        if self.eat(Tag.OP_MUL) or self.eat(Tag.OP_DIV):
            self.factor_a()
            self.factor_b_linha()

    # factor_a → factor | not factor
    def factor_a(self):
        if self.eat(Tag.KW_NOT):
            self.factor()
        else:
            self.factor()

    # factor → “id” | constant | “(“ expression “)”
    def factor(self):
        if self.token.getNome() == Tag.ID:
            self.eat(Tag.ID)
        elif self.token.getNome() == Tag.NUM_CONST:
            self.eat(Tag.NUM_CONST)
        elif self.token.getNome() == Tag.CHAR_CONST:
            self.eat(Tag.CHAR_CONST)
        elif self.token.getNome() == Tag.SMB_OPA:
            self.eat(Tag.SMB_OPA)
            self.expression()
            if not self.eat(Tag.SMB_CPA):
                self.sinalizaErroSintatico("Esperado \")\", encontrado " + "\"" + self.token.getLexema() + "\"")
                return None
        else:
            self.sinalizaErroSintatico(
                "Esperado \"ID, NUM_CONST, CHAR_CONST ou (\" encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # 4° Bloco - Regras

    # logop → “or” | “and”
    def logo(self):
        if self.token.getNome() == Tag.KW_OR:
            self.eat(Tag.KW_OR)

        elif self.token.getNome() == Tag.KW_AND:
            self.eat(Tag.KW_AND)

        else:
            self.sinalizaErroSintatico("Esperado \"OR ou AND\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # relop → “==” | “>” | “>=” | “<” | “<=” | “!=”
    def relop(self):
        if self.token.getNome() == Tag.OP_EQ:
            self.eat(Tag.OP_EQ)

        elif self.token.getNome() == Tag.OP_GT:
            self.eat(Tag.OP_GT)

        elif self.token.getNome() == Tag.OP_GE:
            self.eat(Tag.OP_GE)

        elif self.token.getNome() == Tag.OP_LT:
            self.eat(Tag.OP_LT)

        elif self.token.getNome() == Tag.OP_LE:
            self.eat(Tag.OP_LE)

        elif self.token.getNome() == Tag.OP_NE:
            self.eat(Tag.OP_NE)

        else:
            self.sinalizaErroSintatico(
                "Esperado \"==, >, >=, <, <= ou !=\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # addop → “+” | “-”
    def addop(self):
        if self.token.getNome() == Tag.OP_AD:
            self.eat(Tag.OP_AD)
        elif self.token.getNome() == Tag.OP_MIN:
            self.eat(Tag.OP_MIN)
        else:
            self.sinalizaErroSintatico("Esperado \"+ ou -\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # mulop → “*” | “/”
    def mulop(self):
        if self.token.getNome() == Tag.OP_MUL:
            self.eat(Tag.OP_MUL)
        elif self.token.getNome() == Tag.OP_DIV:
            self.eat(Tag.OP_DIV)
        else:
            self.sinalizaErroSintatico("Esperado \"* ou /\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None

    # constant → “num_const” | “char_const”
    def constant(self):
        if self.token.getNome() == Tag.NUM_CONST:
            self.eat(Tag.NUM_CONST)
        elif self.token.getNome() == Tag.CHAR_CONST:
            self.eat(Tag.CHAR_CONST)
        else:
            self.sinalizaErroSintatico(
                "Esperado \"NUM_CONST ou CHAR_CONST\", encontrado " + "\"" + self.token.getLexema() + "\"")
            return None
