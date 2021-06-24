from tag import Tag
from token import Token
from lexer import Lexer
from myparser import Parser

if __name__ == "__main__":
   lexer = Lexer('prog1.txt')
   parser = Parser(lexer)
   print('\n=> ####### INICIANDO PARSER #########')
   print("\n=> ANALISE SINTÁTICA: \n")
   
   #Código referente ao Lexer
   '''
   token = lexer.proxToken()
   while(token is not None and token.getNome() != Tag.EOF):
      print(token.toString(), "Linha: " + str(token.getLinha()) + " Coluna: " + str(token.getColuna()))
      token = lexer.proxToken()
   '''
   parser.prog()
   parser.lexer.closeFile()
   
   print("\n-----------------------------------------------------")
   print("\n=> Tabela de Simbolos: \n")
   lexer.printTS()
   lexer.closeFile()
  
   print('\n=> ####### FIM DO PROGRAMA #########')
