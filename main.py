from tag import Tag
from token import Token
from lexer import Lexer

if __name__ == "__main__":
   lexer = Lexer('prog1.txt')
   print('\n=> ####### INICIANDO LEXER #########')
   print("\n=> Lista de tokens encontrados: \n")
   token = lexer.proxToken()
   while(token is not None and token.getNome() != Tag.EOF):
      print(token.toString(), "Linha: " + str(token.getLinha()) + " Coluna: " + str(token.getColuna()))
      token = lexer.proxToken()
   
   print("\n-----------------------------------------------------")
   print("\n=> Tabela de Simbolos: \n")
   lexer.printTS()
   lexer.closeFile()
    
   print('\n=> ####### FIM DO PROGRAMA #########')
