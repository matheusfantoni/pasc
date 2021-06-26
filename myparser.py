import sys
import copy

from tag import Tag
from token import Token
from lexer import Lexer
#from no import No


# Classe que representa o Parser (Analisador Sintático)

class Parser():

   def __init__(self, lexer):
      self.lexer = lexer
      self.token = lexer.proxToken() # Leitura inicial obrigatoria do primeiro simbolo
      if self.token is None: # erro no Lexer
        sys.exit(0)

   #def sinalizaErroSemantico(self, message):
    #  print("[Erro Semantico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
     # print(message, "\n")

   def sinalizaErroSintatico(self, message):
      print("[Erro Sintatico] na linha " + str(self.token.getLinha()) + " e coluna " + str(self.token.getColuna()) + ": ")
      print(message, "\n")

   def advance(self):
      print("[DEBUG] token: ", self.token.toString())
      self.token = self.lexer.proxToken()
      if self.token is None: # erro no Lexer
        sys.exit(0)
   
   def skip(self, message):
      self.sinalizaErroSintatico(message)
      self.advance()

   # verifica token esperado t 
   def eat(self, t):
      if(self.token.getNome() == t):
         self.advance()
         return True
      else:
         return False

   """
   LEMBRETE:
   Todas as decisoes do Parser, sao guiadas pela Tabela Preditiva (TP)
   """
   '''
   # Programa -> CMD EOF
   def prog(self):
      self.Cmd()
      if(self.token.getNome() != Tag.EOF):
         self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)
   '''
   # prog → “program” “id” body
   def prog(self):
      self.eat(Tag.KW_PROGRAM)
      self.eat(Tag.ID)
      self.body()
      if(self.token.getNome() != Tag.EOF):
            self.sinalizaErroSintatico("Esperado \"EOF\"; encontrado " + "\"" + self.token.getLexema() + "\"")
            sys.exit(0)
          
   # body → decl-list “{“ stmt-list “}”
   def body(self):
      self.decl_list()
      self.eat(Tag.SMB_OBC)
      #self.stmt_list()
      self.eat(Tag.SMB_CBC)
   
   # decl_list → decl “;” decl_list  | ε    
   def decl_list(self):
      if (self.eat(Tag.NUM_CONST) or self.eat(Tag.CHAR_CONST)):
         self.eat(Tag.SMB_SEM)
         self.decl_list()

   # decl → type id-list
   def decl(self):
      self.type()
      self.id_list()

   # type → “num” | “char”
   def type(self):
      if (self.token.getNome() == Tag.NUM_CONST):
         self.eat(Tag.NUM_CONST)
      elif (self.token.getNome() == Tag.CHAR_CONST):
         self.eat(Tag.CHAR_CONST)
      else:
         self.sinalizaErroSintatico("Esperado \"num\" ou \"char\"; encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)

   # id_list → “id” id_list_linha
   def id_list(self):
      self.eat(Tag.ID)
      self.id_list_linha()

   # id_list_linha → “,” id_list | ε
   def id_list_linha(self):
      if (self.token.getNome() == Tag.SMB_COM):
         self.eat(Tag.SMB_COM)
         self.id_list()
          
   # expression → simple_expr expression_linha
   def expression(self):
      self.simple_expr()
      self.expression_linha()

   #expression_linha → logop simple_expr expression_linha | ε
   def expression_linha(self):
      if (self.eat(Tag.KW_AND) or self.eat(Tag.KW_OR)):
         self.simple_expr()
         self.expression_linha()

   #simple_expr → term simple_exp_linha
   def simple_expr(self):
      self.term()
      self.simple_exp_linha()

   # simple_exp_linha → relop term simple_exp_linha | ε
   def simple_exp_linha(self):
      if(self.eat(Tag.OP_EQ) or self.eat(Tag.OP_GT) or self.eat(Tag.OP_GE) or 
         self.eat(Tag.OP_LT) or self.eat(Tag.OP_LE) or self.eat(Tag.OP_NE)):
            self.term()
            self.simple_exp_linha()

   # term → factor_b term_linha
   def term(self):
      self.factor_b()
      self.term_linha()

   # term_linha → addop factor_b term_linha | ε
   def term_linha(self):
      if (self.eat(Tag.OP_AD) or self.eat(Tag.OP_MIN)):
         self.factor_b()
         self.term_linha()

   # factor_b → factor_a factor_b_linha
   def factor_b(self):
      self.factor_a()
      self.factor_b_linha()

   # factor_b_linha → mulop factor_a factor_b_linha | ε
   def factor_b_linha(self):
      if (self.eat(Tag.OP_MUL) or self.eat(Tag.OP_DIV)):
         self.factor_a()
         self.factor_b_linha()

   # factor_a → factor | not factor
   def factor_a(self):
      if (self.eat(Tag.KW_NOT)):
         self.factor()
      else:
         self.factor()
   
   # factor → “id” | constant | “(“ expression “)”
   def factor(self):
      if (self.token.getNome() == Tag.ID):
         self.eat(Tag.ID)
      elif (self.token.getNome() == Tag.NUM_CONST):
         self.eat(Tag.NUM_CONST)
      elif (self.token.getNome() == Tag.CHAR_CONST):
         self.eat(Tag.CHAR_CONST)
      elif (self.token.getNome() == Tag.SMB_OPA):
         self.eat(Tag.SMB_OPA)
      else:
         self.sinalizaErroSintatico("Esperado \"id\", \"num_const\", \"char_const\" ou \"(\"; encontrado " + "\"" + self.token.getLexema() + "\"")
         sys.exit(0)