grammar Hello;

// Parser rules
program: 'hello' ID '!'?;

// Lexer rules
ID: [a-zA-Z]+;
WS: [ \t\r\n]+ -> channel(HIDDEN);
COMMENT: '//' .*? '\n' -> skip;
