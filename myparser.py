import sys
import copy

from tag import Tag
from no import No


# Classe que representa o Parser (Analisador Sintático)

class Parser:

    def __init__(self, lexer):
        self.lexer = lexer
        self.token = lexer.proxToken()  # Leitura inicial obrigatoria do primeiro simbolo
        if self.token is None:  # erro no Lexer
            sys.exit(0)

    def sinalizaErroSemantico(self, message):
        print("[Erro Semantico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
        print(message, "\n")

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

    # 1° Bloco - Regras

    # prog → “program” “id” body
    def prog(self):
        
        # armazena token corrente, uma vez que o ID pode ser consumido
        tempToken = copy.copy(self.token)

        if not self.eat(Tag.KW_PROGRAM):
            self.sinalizaErroSintatico("Esperado \"PROGRAM\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

        if not self.eat(Tag.ID):
            self.sinalizaErroSintatico("Esperado \"ID\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

        self.lexer.ts.removeToken(tempToken.getLexema())
        tempToken.setTipo(Tag.TIPO_VAZIO)
        self.lexer.ts.addToken(tempToken.getLexema(), tempToken)
        
        self.body()
        if self.token.getNome() != Tag.EOF:
            self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

    # body → decl-list “{“ stmt-list “}”
    def body(self):
        self.decl_list()
        if not self.eat(Tag.SMB_OBC):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

        self.stmt_list()

        if not self.eat(Tag.SMB_CBC):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

    # decl-list → decl “;” decl-list  | ε
    def decl_list(self):
        if self.token.getNome() == Tag.KW_NUM or self.token.getNome() == Tag.KW_CHAR:
            self.decl()
            if self.eat(Tag.SMB_SEM):
                self.decl_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)
        else:
            return

    # decl → type id-list
    def decl(self):
        noType = self.type()
        self.id_list(noType)

    # type → “num” | “char”
    def type(self):
        noType = No()

        if self.eat(Tag.KW_NUM):
            noType.tipo = Tag.TIPO_NUMERO
        elif self.eat(Tag.KW_CHAR):
            noType.tipo = Tag.TIPO_CARACTERE
        else:
            self.sinalizaErroSintatico(
                "Esperado \"NUM\" ou \"CHAR\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)
        
        return noType

    # id-list → “id” id_list_linha
    def id_list(self, type):
        noId_list = type

        # armazena token corrente, uma vez que o ID pode ser consumido
        tempToken = copy.copy(self.token)

        if not self.eat(Tag.ID):
            self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)  

        self.lexer.ts.removeToken(tempToken.getLexema())
        tempToken.setTipo(noId_list.tipo)
        self.lexer.ts.addToken(tempToken.getLexema(), tempToken)

        self.id_list_linha(noId_list)

    # id_list_linha → “,” id-list | ε
    def id_list_linha(self, type):
        noId_list_linha = type
        if self.token.getNome() == Tag.SMB_COM:
            self.eat(Tag.SMB_COM)
            self.id_list(noId_list_linha)
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
                sys.exit(0)
        elif self.token.getNome() == Tag.KW_IF:
            self.if_stmt()
            if self.eat(Tag.SMB_SEM):
                self.stmt_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)
        elif self.token.getNome() == Tag.KW_WHILE:
            self.while_stmt()
            if self.eat(Tag.SMB_SEM):
                self.stmt_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)
        elif self.token.getNome() == Tag.KW_READ:
            self.read_stmt()
            if self.eat(Tag.SMB_SEM):
                self.stmt_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)
        elif self.token.getNome() == Tag.KW_WRITE:
            self.write_stmt()
            if self.eat(Tag.SMB_SEM):
                self.stmt_list()
            else:
                self.sinalizaErroSintatico("Esperado \";\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)
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
            sys.exit(0)

    #  # assign-stmt → “id” “=” simple_expr
    def assign_stmt(self):
        # armazena token corrente, uma vez que o ID pode ser consumido
        tempToken = copy.copy(self.token)
        
        if self.eat(Tag.ID):
            if (tempToken.getTipo() == Tag.TIPO_VAZIO):
                self.sinalizaErroSemantico("ID não declarado")
                sys.exit(0)
            if not self.eat(Tag.OP_ATRIB):
                self.sinalizaErroSintatico("Esperado \"=\", encontrado " + "\"" + self.token.getLexema() + "\"")
            else:
                noSimple_expr = self.simple_expr()
                if noSimple_expr.tipo != tempToken.getTipo():
                    self.sinalizaErroSemantico("Atribuição incompatível")
                    sys.exit(0)
                return
        else:
            self.sinalizaErroSintatico("Esperado \"ID\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

    # if-stmt → “if” “(“ expression “)” “{“ stmt-list “}” if-stmt_linha
    def if_stmt(self):
        if self.eat(Tag.KW_IF):
            if not self.eat(Tag.SMB_OPA):
                self.sinalizaErroSintatico("Esperado \"(\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)

            noExpression = self.expression()

            if not self.eat(Tag.SMB_CPA):
                self.sinalizaErroSintatico("Esperado \")\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)

            if noExpression.tipo != Tag.TIPO_LOGICO:
                self.sinalizaErroSemantico("Expressão lógica mal formada")
                sys.exit(0)

            if not self.eat(Tag.SMB_OBC):
                self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)

            self.stmt_list()

            if not self.eat(Tag.SMB_CBC):
                self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)

            self.if_stmt_linha()

        else:
            self.sinalizaErroSintatico("Esperado \"IF\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

    # if-stmt’ → “else” “{“ stmt-list “}” | ε
    def if_stmt_linha(self):
        if self.eat(Tag.KW_ELSE):
            if not self.eat(Tag.SMB_OBC):
                self.sinalizaErroSintatico("Esperado \"{\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)

            self.stmt_list()

            if not self.eat(Tag.SMB_CBC):
                self.sinalizaErroSintatico("Esperado \"}\"; encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)

        else:
            return

    # while-stmt → stmt-prefix “{“ stmt-list “}”
    def while_stmt(self):
        self.stmt_prefix()

        if not self.eat(Tag.SMB_OBC):
            self.sinalizaErroSintatico("Esperado \"{\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

        self.stmt_list()

        if not self.eat(Tag.SMB_CBC):
            self.sinalizaErroSintatico("Esperado \"}\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)


#stmt-prefix → “while” “(“ expression “)”
#{se expression.t != BOOL: sinalizar erro de expressão lógica mal formada}

    # stmt-prefix → “while” “(“ expression “)”
    def stmt_prefix(self):
        if self.eat(Tag.KW_WHILE):
            if not self.eat(Tag.SMB_OPA):
                self.sinalizaErroSintatico("Esperado \"(\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)

            noExpression = self.expression()
            
            if not self.eat(Tag.SMB_CPA):
                self.sinalizaErroSintatico("Esperado \")\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)

            else:
                if noExpression.tipo != Tag.TIPO_LOGICO:
                    self.sinalizaErroSemantico("Expressão lógica mal formada.")
                    sys.exit(0)
        
        else:
            self.sinalizaErroSintatico("Esperado \"WHILE\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)


    # read-stmt → “read” “id”
    def read_stmt(self):
        if self.eat(Tag.KW_READ):
            # armazena token corrente, uma vez que o ID pode ser consumido
            tempToken = copy.copy(self.token)

            if not self.eat(Tag.ID):
                self.sinalizaErroSintatico("Esperado \"ID\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)

            else:
                if tempToken.getTipo() == Tag.TIPO_VAZIO:
                    self.sinalizaErroSemantico("ID não declarado")
                    sys.exit(0)

        else:
            self.sinalizaErroSintatico("Esperado \"READ\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)


    # write-stmt → “write” simple-expr
    def write_stmt(self):
        if self.eat(Tag.KW_WRITE):
            noSimple_expr = self.simple_expr()
            if noSimple_expr.tipo != Tag.TIPO_CARACTERE and noSimple_expr.tipo != Tag.TIPO_NUMERO:
                self.sinalizaErroSemantico("Erro de incompatibilidade para impressão de valores.")
                sys.exit(0)
                
            return 
        else:
            self.sinalizaErroSintatico("Esperado \"WRITE\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

    #    3° Bloco - Regras

    #expression → simple-expr expression_linha
    def expression(self):
        noExpression = No()
        noSimple_expr = self.simple_expr()
        noExpression_linha = self.expression_linha()
        if noExpression_linha.tipo == Tag.TIPO_VAZIO:
            noExpression.tipo = noSimple_expr.tipo
        elif noExpression_linha.tipo == noSimple_expr.tipo and noSimple_expr.tipo == Tag.TIPO_LOGICO:
            noExpression.tipo = Tag.TIPO_LOGICO
        else:
            noExpression.tipo = Tag.TIPO_ERRO
        return noExpression    

    #expression’ → logop simple-expr expression’
    def expression_linha(self):
        noExpression_linha = No()
        if self.eat(Tag.KW_AND) or self.eat(Tag.KW_OR):
            noSimple_expr = self.simple_expr()
            noExpression_linha_filho = self.expression_linha()
            if noExpression_linha_filho.tipo == Tag.TIPO_VAZIO and noSimple_expr.tipo == Tag.TIPO_LOGICO:
                noExpression_linha.tipo = Tag.TIPO_LOGICO

            elif noExpression_linha_filho.tipo == noSimple_expr.tipo and noSimple_expr == Tag.TIPO_LOGICO:
                noExpression_linha.tipo = Tag.TIPO_LOGICO

            else:
                noExpression_linha.tipo = Tag.TIPO_ERRO
            
            return noExpression_linha

        noExpression_linha.tipo = Tag.TIPO_VAZIO
        return noExpression_linha


    # simple_expr → term simple_exp_linha
    def simple_expr(self):
        noSimple_expr = No()
        noTerm = self.term()
        noSimple_expr_linha = self.simple_exp_linha()
        if noSimple_expr_linha.tipo == Tag.TIPO_VAZIO:
            noSimple_expr.tipo = noTerm.tipo
        
        elif noSimple_expr_linha.tipo == noTerm.tipo and noSimple_expr_linha.tipo == Tag.TIPO_NUMERO:
            noSimple_expr.tipo = Tag.TIPO_LOGICO

        else:
            noSimple_expr.tipo = Tag.TIPO_ERRO

        return noSimple_expr

    # simple_exp_linha → relop term simple_exp_linha | ε
    def simple_exp_linha(self):
        noSimple_exp_linha = No()
        if (self.eat(Tag.OP_EQ) or self.eat(Tag.OP_GT) or self.eat(Tag.OP_GE) or self.eat(Tag.OP_LT) or self.eat(Tag.OP_LE) or self.eat(Tag.OP_NE)):
            noTerm = self.term()
            noSimple_exp_linha_filho = self.simple_exp_linha()

            if noSimple_exp_linha_filho.tipo == Tag.TIPO_VAZIO and noTerm.tipo == Tag.TIPO_NUMERO:
                noSimple_exp_linha.tipo = Tag.TIPO_NUMERO
            
            elif noSimple_exp_linha_filho.tipo == noTerm.tipo and noTerm.tipo == Tag.TIPO_NUMERO:
                noSimple_exp_linha.tipo = Tag.TIPO_NUMERO
            
            else:
                noSimple_exp_linha.tipo = Tag.TIPO_ERRO
            return noSimple_exp_linha
        
        noSimple_exp_linha.tipo = Tag.TIPO_VAZIO
        return noSimple_exp_linha
      
    # term → factor_b term_linha
    def term(self):
        noTerm = No()
        noFactor_b = self.factor_b()
        noTerm_linha = self.term_linha()
        
        if noTerm_linha.tipo == Tag.TIPO_VAZIO:
            noTerm.tipo = noFactor_b.tipo
        
        elif noTerm_linha.tipo == noFactor_b.tipo and noTerm_linha.tipo == Tag.TIPO_NUMERO:
            noTerm.tipo = Tag.TIPO_NUMERO
            
        else:
            noTerm.tipo = Tag.TIPO_ERRO

        return noTerm


    # term_linha → addop factor_b term_linha | ε
    def term_linha(self):
        noTerm_linha = No()
        
        if self.eat(Tag.OP_AD) or self.eat(Tag.OP_MIN):
            noFactor_b = self.factor_b()
            noTerm_linha_filho = self.term_linha()

            if noTerm_linha_filho.tipo == Tag.TIPO_VAZIO and noFactor_b.tipo == Tag.TIPO_NUMERO:
                noTerm_linha.tipo = Tag.TIPO_NUMERO
            elif noTerm_linha_filho.tipo == noFactor_b.tipo and noFactor_b.tipo == Tag.TIPO_NUMERO:
                noTerm_linha.tipo = Tag.TIPO_NUMERO
            else:
                noTerm_linha.tipo = Tag.TIPO_ERRO
            
            return noTerm_linha    

        noTerm_linha.tipo = Tag.TIPO_VAZIO
        return noTerm_linha

    # factor_b → factor_a factor_b_linha
    def factor_b(self):
        noFactor_b = No()
        
        noFactor_a = self.factor_a()
        noFactor_b_linha = self.factor_b_linha()
        
        if noFactor_b_linha.tipo == Tag.TIPO_VAZIO:
            noFactor_b.tipo = noFactor_a.tipo
        elif noFactor_b_linha.tipo == noFactor_a.tipo and noFactor_b_linha.tipo == Tag.TIPO_NUMERO:
            noFactor_b.tipo = Tag.TIPO_NUMERO
        else:
            noFactor_b.tipo = Tag.TIPO_ERRO
        
        return noFactor_b

    # factor_b_linha → mulop factor_a factor_b_linha | ε
    def factor_b_linha(self):
        noFactor_b_linha = No()
        if self.eat(Tag.OP_MUL) or self.eat(Tag.OP_DIV):
            noFactor_a = self.factor_a()
            noFactor_b_linha_filho = self.factor_b_linha()

            if noFactor_b_linha_filho.tipo == Tag.TIPO_VAZIO and noFactor_a.tipo == Tag.TIPO_NUMERO:
                noFactor_b_linha.tipo = Tag.TIPO_NUMERO
            elif noFactor_b_linha_filho.tipo == noFactor_a.tipo and noFactor_a.tipo == Tag.TIPO_NUMERO:
                noFactor_b_linha.tipo = Tag.TIPO_NUMERO
            else:
                noFactor_b_linha.tipo = Tag.TIPO_ERRO
            return noFactor_b_linha
        
        noFactor_b_linha.tipo = Tag.TIPO_VAZIO
        return noFactor_b_linha

    # factor_a → factor | not factor
    def factor_a(self):
        noFactor_a = No()
        if self.eat(Tag.KW_NOT):
            noFactor = self.factor()
            if noFactor.tipo != Tag.TIPO_LOGICO:
                noFactor_a.tipo = Tag.TIPO_ERRO
                self.sinalizaErroSemantico("Expressao mal formada.")
                sys.exit(0)
            noFactor_a.tipo = Tag.TIPO_LOGICO
        else:
            noFactor = self.factor()
            noFactor_a.tipo = noFactor.tipo
        return noFactor_a
            

    # factor → “id” | constant | “(“ expression “)”
    def factor(self):
        noFactor = No()

        # armazena token corrente, uma vez que o ID pode ser consumido
        tempToken = copy.copy(self.token)
        
        if self.eat(Tag.ID):
            noFactor.tipo = tempToken.getTipo()
        elif self.eat(Tag.NUM_CONST):
            noFactor.tipo = Tag.TIPO_NUMERO
        elif self.eat(Tag.CHAR_CONST):
            noFactor.tipo = Tag.TIPO_CARACTERE
        elif self.token.getNome() == Tag.SMB_OPA:
            self.eat(Tag.SMB_OPA)
            noExpression = self.expression()
            if not self.eat(Tag.SMB_CPA):
                self.sinalizaErroSintatico("Esperado \")\", encontrado " + "\"" + self.token.getLexema() + "\"")
                sys.exit(0)
            noFactor.tipo = noExpression.tipo
        else:
            self.sinalizaErroSintatico(
                "Esperado \"ID, NUM_CONST, CHAR_CONST ou (\" encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

        return noFactor

    # 4° Bloco - Regras

    # logop → “or” | “and”
    def logo(self):
        if self.token.getNome() == Tag.KW_OR:
            self.eat(Tag.KW_OR)

        elif self.token.getNome() == Tag.KW_AND:
            self.eat(Tag.KW_AND)

        else:
            self.sinalizaErroSintatico("Esperado \"OR ou AND\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

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
            sys.exit(0)

    # addop → “+” | “-”
    def addop(self):
        if self.token.getNome() == Tag.OP_AD:
            self.eat(Tag.OP_AD)
        elif self.token.getNome() == Tag.OP_MIN:
            self.eat(Tag.OP_MIN)
        else:
            self.sinalizaErroSintatico("Esperado \"+ ou -\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

    # mulop → “*” | “/”
    def mulop(self):
        if self.token.getNome() == Tag.OP_MUL:
            self.eat(Tag.OP_MUL)
        elif self.token.getNome() == Tag.OP_DIV:
            self.eat(Tag.OP_DIV)
        else:
            self.sinalizaErroSintatico("Esperado \"* ou /\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)

    # constant → “num_const” | “char_const”
    def constant(self):
        noConstant = No()
        if self.eat(Tag.NUM_CONST):
            noConstant.tipo = Tag.TIPO_NUMERO
        elif self.eat(Tag.CHAR_CONST):
            noConstant.tipo = Tag.TIPO_CARACTERE
        else:
            self.sinalizaErroSintatico(
                "Esperado \"NUM_CONST ou CHAR_CONST\", encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)
