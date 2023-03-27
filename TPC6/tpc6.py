import ply.lex as lex

tokens = ("COMMENT_SINGLE", "COMMENT_BLOCK",
          "COMMA", "SEMICOLON", "VAR", "INT",
          "FUNCTION","FUNC_NAME", "OPEN_CHAVS", "CLOSE_CHAVS",
          "WHILE", "FOR", "OPERATION", "ATRIBUTION", "CONDITION",
          "VALUE", "IN", "RANGE", "PROGRAM", "PROG_NAME")

t_ignore = ' \t\n'


def t_COMMENT_SINGLE(t):
	r'\/\/.*'
	return t


def t_COMMENT_BLOCK(t):
	r'\/\*(.|\n)*\*\/'
	return t


def t_COMMA(t):
	r','
	return t


def t_SEMICOLON(t):
	r';'
	return t


def t_INT(t):
	# r'int\s*(?P<var>[a-zA-Z_]+)(;|\s*=\s*(?P<value>\d+);)'
	r'int'
	return t


def t_PROGRAM(t):
	r'program'
	return t


def t_PROG_NAME(t):
	r'(?<=program) \w+'


def t_FUNCTION(t):
	r'function'
	return t


def t_FUNC_NAME(t):
	r'[\w]+\(.\)'
	return t


def t_OPEN_CHAVS(t):
	r'\{'
	return t


def t_CLOSE_CHAVS(t):
	r'\}'
	return t


def t_ATRIBUTION(t):
	r'='
	return


def t_OPERATION(t):
	r'[\-\+\*\\\%]'
	return t


def t_CONDITION(t):
	r'[(\==)\<\>\>=\<=]'
	return t


def t_WHILE(t):
	r'while'
	return t


def t_FOR(t):
	r'for'
	return t


def t_IN(t):
	r'in'
	return t


def t_RANGE(t):
	r'\[\d+\.\.\d+\]'
	return t


def t_VALUE(t):
	r'\d+'
	return t


def t_VAR(t):
	r'\w+'
	return t


def t_error(t):
	print(f'Invalid token: {t.value}')
	t.lexer.skip(1)


exemplo1 = '''/* factorial.p
-- 2023-03-20 
-- by jcr
*/

int i;

// Função que calcula o factorial dum número n
function fact(n){
  int res = 1;
  while res > 1 {
    res = res * n;
    res = res - 1;
  }
}

// Programa principal
program myFact{
  for i in [1..10]{
    print(i, fact(i));
  }
}'''

lexer = lex.lex()
lexer.input(exemplo1)
while tok := lex.token():
	print(tok)
