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
          self.stmt_list()
          self.eat(Tag.SMB_CBC)
   
   # decl-list → decl “;” decl-list  | ε 
   def decl_list(self):
          self.decl()
          self.eat(Tag.SMB_SEM)
          self.decl_list()        
          
          
  
