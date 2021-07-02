from tag import Tag

class Token:
   '''
   Classe que representa um Token
   '''
   def __init__(self, nome, lexema, linha, coluna):
      self.nome = nome
      self.lexema = lexema
      self.tipo = Tag.TIPO_VAZIO
      self.linha = linha
      self.coluna = coluna

   def getNome(self):
      return self.nome

   def getLexema(self):
      return self.lexema

   def getLinha(self):
      return self.linha

   def setLinha(self, linha):
      self.linha = linha

   def getColuna(self):
      return self.coluna

   def setColuna(self, coluna):
      self.coluna = coluna

   def toString(self):
      return ('<' + str(self.nome.name) + ', "' + str(self.lexema) + '"' 
      + ', ' + str(self.tipo) + ', ' + str(self.linha) + ',' + str(self.coluna) + '>')

   def getTipo(self):
      return self.tipo

   def setTipo(self, tipo):
      self.tipo = tipo