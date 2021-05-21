# pasc
Compilador da linguagem PasC em Python


############ Regras Faltantes TP1 #################################

-> Implementar linha e coluna
-> Incrementar linha pq apareceu o caractere de quebra de linha
-> Incrementar coluna toda vez que ler um caractere, incrementar a coluna
-> Quando tiver quebra de linha a coluna deve ser voltada para 1 e incrementado a linha
-> Quando incremetar as linhas e colunas, assim como, quando decrementar ou reinicia-las. Lembre-se, ambas 
	comecam em 1.	

-> Implementar modo pânico (Erro léxico)

-> Resolver comentario EOF
-> O programa deverá informar o erro e o local onde ocorreu (linha e coluna).
Os erros verificados serão: 
i) caracteres desconhecidos (não esperados em um padrão ou inválidos)
ii) string não fechada antes de quebra de linha
iii) string não-fechada antes do fim de arquivo. Se o analisador léxico encontrar mais do que um erro léxico, o processo de compilação deve ser
interrompido.
