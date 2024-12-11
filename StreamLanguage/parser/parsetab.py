
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftFEEDBACKleftSTREAMMERGEleftCHAINleftSTREAMSPLITleftORleftANDnonassocEQUALSNEGTLTGELEleftPLUSMINUSleftMULTIPLYDIVIDEMODULUSrightNOTrightUMINUSUPLUSAND ASSIGN ATTACH BREAK CALL CHAIN COMMA CONST CONTINUE DIVIDE ELSE EOF EQUALS EVENT FALSE FEEDBACK FILTEROP FLOAT FN FOR GE GT IDENTIFIER IF INT LAMBDA LBRACE LBRACKET LE LPAREN LT MAP MINUS MODULUS MULTIPLY NE NEWLINE NOT OR PLUS RBRACE RBRACKET REDUCE RETURN RPAREN SBOOL SEMICOLON SEVENT SFLOAT SINT SSTREAM SSTRING STREAM STREAMMERGE STREAMSPLIT STRING TO_STREAM TRUE TYPEHINTCOLON VAR WHILEprogram : statement_liststatement : declaration\n                    | expression SEMICOLON\n                    | return_statement SEMICOLON\n                    | control_flow\n                    | assignment SEMICOLONstatement_list : statement\n                          | statement_list statementfunction_call : IDENTIFIER LPAREN opt_arg_list RPARENopt_arg_list : arg_list\n                        | emptyarg_list : expression\n                    | arg_list COMMA expressionfunction_definition : FN IDENTIFIER LPAREN opt_param_list RPAREN block_statement\n                               | FN IDENTIFIER LPAREN opt_param_list RPAREN typehint block_statementreturn_statement : RETURN expressionblock_statement : LBRACE statement_list RBRACElambda_function : FN LPAREN opt_param_list RPAREN LAMBDA block_statement\n                           | FN LPAREN opt_param_list RPAREN typehint LAMBDA block_statement\n                           | LPAREN opt_param_list RPAREN LAMBDA block_statement\n                           | LPAREN opt_param_list RPAREN typehint LAMBDA block_statement\n                           | LPAREN opt_param_list RPAREN LAMBDA expressionopt_param_list : param_list\n                          | emptyparam_list : param\n                      | param_list COMMA paramparam : IDENTIFIER\n                 | IDENTIFIER typehintdeclaration : VAR declaration_base SEMICOLON\n                       | CONST declaration_base SEMICOLON\n                       | function_definitiondeclaration_base : IDENTIFIER\n                            | IDENTIFIER ASSIGN expression\n                            | IDENTIFIER typehint\n                            | IDENTIFIER typehint ASSIGN expressiontypehint : TYPEHINTCOLON typetype : SINT\n                | SFLOAT\n                | SSTRING\n                | SBOOL\n                | SSTREAM\n                | SEVENTptype : INT\n                 | FLOAT\n                 | STRING\n                 | TRUE\n                 | FALSEexpression : expression PLUS expression\n                      | expression MINUS expression\n                      | expression MULTIPLY expression\n                      | expression DIVIDE expression\n                      | expression EQUALS expression\n                      | expression MODULUS expression\n                      | expression NE expression\n                      | expression GT expression\n                      | expression LT expression\n                      | expression GE expression\n                      | expression LE expression\n                      | expression AND expression\n                      | expression OR expression\n                      | expression CHAIN expression\n                      | expression STREAMSPLIT expression\n                      | expression STREAMMERGE expression\n                      | expression FEEDBACK expression\n        expression : MINUS expression %prec UMINUS\n                      | PLUS expression %prec UPLUS\n                      | NOT expression\n        control_flow : conditional\n                        | loop\n                        | break\n                        | continueexpression : LPAREN expression RPARENexpression : INT\n                      | FLOATexpression : STRINGexpression : TRUE\n                      | FALSEexpression : IDENTIFIERexpression : function_callexpression : expression TO_STREAMexpression : lambda_functionconditional : IF LPAREN expression RPAREN block_statement ELSE block_statement\n                       | IF LPAREN expression RPAREN block_statementloop : FOR LPAREN declaration SEMICOLON expression SEMICOLON expression RPAREN block_statement\n                | WHILE LPAREN expression RPAREN block_statementbreak : BREAK SEMICOLONcontinue : CONTINUE SEMICOLONassignment : IDENTIFIER ASSIGN expressionempty :'
    
_lr_action_items = {'VAR':([0,2,3,4,7,11,25,26,27,28,35,36,55,56,77,79,80,98,102,141,147,149,150,152,158,159,161,164,],[9,9,-7,-2,-5,-31,-68,-69,-70,-71,-8,-3,-4,-6,9,-86,-87,-29,-30,9,-83,-85,9,-14,-17,-15,-82,-84,]),'CONST':([0,2,3,4,7,11,25,26,27,28,35,36,55,56,77,79,80,98,102,141,147,149,150,152,158,159,161,164,],[10,10,-7,-2,-5,-31,-68,-69,-70,-71,-8,-3,-4,-6,10,-86,-87,-29,-30,10,-83,-85,10,-14,-17,-15,-82,-84,]),'MINUS':([0,2,3,4,5,7,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,60,61,63,64,65,67,71,72,73,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,102,103,107,111,115,118,119,120,128,131,132,136,138,139,140,141,143,147,148,149,150,151,152,154,157,158,159,160,161,162,164,],[13,13,-7,-2,38,-5,-31,13,13,13,13,-73,-74,-75,-76,-77,-78,-79,-81,13,-68,-69,-70,-71,-8,-3,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,-80,-4,-6,-66,-78,-65,-67,38,-78,13,13,38,13,13,-86,-87,-48,-49,-50,-51,38,-53,38,38,38,38,38,38,38,38,38,38,38,-29,13,-30,-72,38,38,38,38,38,13,13,-9,13,13,38,-20,38,13,38,-83,38,-85,13,-21,-14,-18,13,-17,-15,-19,-82,38,-84,]),'PLUS':([0,2,3,4,5,7,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,60,61,63,64,65,67,71,72,73,76,78,79,80,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,99,102,103,107,111,115,118,119,120,128,131,132,136,138,139,140,141,143,147,148,149,150,151,152,154,157,158,159,160,161,162,164,],[12,12,-7,-2,37,-5,-31,12,12,12,12,-73,-74,-75,-76,-77,-78,-79,-81,12,-68,-69,-70,-71,-8,-3,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,-80,-4,-6,-66,-78,-65,-67,37,-78,12,12,37,12,12,-86,-87,-48,-49,-50,-51,37,-53,37,37,37,37,37,37,37,37,37,37,37,-29,12,-30,-72,37,37,37,37,37,12,12,-9,12,12,37,-20,37,12,37,-83,37,-85,12,-21,-14,-18,12,-17,-15,-19,-82,37,-84,]),'NOT':([0,2,3,4,7,11,12,13,14,15,24,25,26,27,28,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,56,71,72,76,78,79,80,98,99,102,120,128,132,136,141,147,149,150,152,157,158,159,161,164,],[14,14,-7,-2,-5,-31,14,14,14,14,14,-68,-69,-70,-71,-8,-3,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,-4,-6,14,14,14,14,-86,-87,-29,14,-30,14,14,14,14,14,-83,-85,14,-14,14,-17,-15,-82,-84,]),'LPAREN':([0,2,3,4,7,11,12,13,14,15,21,24,25,26,27,28,29,30,31,32,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,56,61,62,67,71,72,74,76,78,79,80,98,99,102,120,128,132,136,141,147,149,150,152,157,158,159,161,164,],[15,15,-7,-2,-5,-31,15,15,15,15,72,15,-68,-69,-70,-71,75,76,77,78,-8,-3,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,-4,-6,72,75,72,15,15,112,15,15,-86,-87,-29,15,-30,15,15,15,15,15,-83,-85,15,-14,15,-17,-15,-82,-84,]),'INT':([0,2,3,4,7,11,12,13,14,15,24,25,26,27,28,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,56,71,72,76,78,79,80,98,99,102,120,128,132,136,141,147,149,150,152,157,158,159,161,164,],[16,16,-7,-2,-5,-31,16,16,16,16,16,-68,-69,-70,-71,-8,-3,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,-4,-6,16,16,16,16,-86,-87,-29,16,-30,16,16,16,16,16,-83,-85,16,-14,16,-17,-15,-82,-84,]),'FLOAT':([0,2,3,4,7,11,12,13,14,15,24,25,26,27,28,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,56,71,72,76,78,79,80,98,99,102,120,128,132,136,141,147,149,150,152,157,158,159,161,164,],[17,17,-7,-2,-5,-31,17,17,17,17,17,-68,-69,-70,-71,-8,-3,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,-4,-6,17,17,17,17,-86,-87,-29,17,-30,17,17,17,17,17,-83,-85,17,-14,17,-17,-15,-82,-84,]),'STRING':([0,2,3,4,7,11,12,13,14,15,24,25,26,27,28,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,56,71,72,76,78,79,80,98,99,102,120,128,132,136,141,147,149,150,152,157,158,159,161,164,],[18,18,-7,-2,-5,-31,18,18,18,18,18,-68,-69,-70,-71,-8,-3,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,-4,-6,18,18,18,18,-86,-87,-29,18,-30,18,18,18,18,18,-83,-85,18,-14,18,-17,-15,-82,-84,]),'TRUE':([0,2,3,4,7,11,12,13,14,15,24,25,26,27,28,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,56,71,72,76,78,79,80,98,99,102,120,128,132,136,141,147,149,150,152,157,158,159,161,164,],[19,19,-7,-2,-5,-31,19,19,19,19,19,-68,-69,-70,-71,-8,-3,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,-4,-6,19,19,19,19,-86,-87,-29,19,-30,19,19,19,19,19,-83,-85,19,-14,19,-17,-15,-82,-84,]),'FALSE':([0,2,3,4,7,11,12,13,14,15,24,25,26,27,28,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,56,71,72,76,78,79,80,98,99,102,120,128,132,136,141,147,149,150,152,157,158,159,161,164,],[20,20,-7,-2,-5,-31,20,20,20,20,20,-68,-69,-70,-71,-8,-3,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,-4,-6,20,20,20,20,-86,-87,-29,20,-30,20,20,20,20,20,-83,-85,20,-14,20,-17,-15,-82,-84,]),'IDENTIFIER':([0,2,3,4,7,9,10,11,12,13,14,15,24,25,26,27,28,29,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,56,71,72,75,76,78,79,80,98,99,102,106,112,117,120,128,132,136,141,147,149,150,152,157,158,159,161,164,],[21,21,-7,-2,-5,58,58,-31,61,61,61,67,61,-68,-69,-70,-71,74,-8,-3,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,61,-4,-6,61,61,114,61,61,-86,-87,-29,61,-30,114,114,74,61,61,61,61,21,-83,-85,21,-14,61,-17,-15,-82,-84,]),'RETURN':([0,2,3,4,7,11,25,26,27,28,35,36,55,56,79,80,98,102,141,147,149,150,152,158,159,161,164,],[24,24,-7,-2,-5,-31,-68,-69,-70,-71,-8,-3,-4,-6,-86,-87,-29,-30,24,-83,-85,24,-14,-17,-15,-82,-84,]),'FN':([0,2,3,4,7,11,12,13,14,15,24,25,26,27,28,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,55,56,71,72,76,77,78,79,80,98,99,102,120,128,132,136,141,147,149,150,152,157,158,159,161,164,],[29,29,-7,-2,-5,-31,62,62,62,62,62,-68,-69,-70,-71,-8,-3,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,62,-4,-6,62,62,62,117,62,-86,-87,-29,62,-30,62,62,62,62,29,-83,-85,29,-14,62,-17,-15,-82,-84,]),'IF':([0,2,3,4,7,11,25,26,27,28,35,36,55,56,79,80,98,102,141,147,149,150,152,158,159,161,164,],[30,30,-7,-2,-5,-31,-68,-69,-70,-71,-8,-3,-4,-6,-86,-87,-29,-30,30,-83,-85,30,-14,-17,-15,-82,-84,]),'FOR':([0,2,3,4,7,11,25,26,27,28,35,36,55,56,79,80,98,102,141,147,149,150,152,158,159,161,164,],[31,31,-7,-2,-5,-31,-68,-69,-70,-71,-8,-3,-4,-6,-86,-87,-29,-30,31,-83,-85,31,-14,-17,-15,-82,-84,]),'WHILE':([0,2,3,4,7,11,25,26,27,28,35,36,55,56,79,80,98,102,141,147,149,150,152,158,159,161,164,],[32,32,-7,-2,-5,-31,-68,-69,-70,-71,-8,-3,-4,-6,-86,-87,-29,-30,32,-83,-85,32,-14,-17,-15,-82,-84,]),'BREAK':([0,2,3,4,7,11,25,26,27,28,35,36,55,56,79,80,98,102,141,147,149,150,152,158,159,161,164,],[33,33,-7,-2,-5,-31,-68,-69,-70,-71,-8,-3,-4,-6,-86,-87,-29,-30,33,-83,-85,33,-14,-17,-15,-82,-84,]),'CONTINUE':([0,2,3,4,7,11,25,26,27,28,35,36,55,56,79,80,98,102,141,147,149,150,152,158,159,161,164,],[34,34,-7,-2,-5,-31,-68,-69,-70,-71,-8,-3,-4,-6,-86,-87,-29,-30,34,-83,-85,34,-14,-17,-15,-82,-84,]),'$end':([1,2,3,4,7,11,25,26,27,28,35,36,55,56,79,80,98,102,147,149,152,158,159,161,164,],[0,-1,-7,-2,-5,-31,-68,-69,-70,-71,-8,-3,-4,-6,-86,-87,-29,-30,-83,-85,-14,-17,-15,-82,-84,]),'RBRACE':([3,4,7,11,25,26,27,28,35,36,55,56,79,80,98,102,147,149,150,152,158,159,161,164,],[-7,-2,-5,-31,-68,-69,-70,-71,-8,-3,-4,-6,-86,-87,-29,-30,-83,-85,158,-14,-17,-15,-82,-84,]),'SEMICOLON':([5,6,8,11,16,17,18,19,20,21,22,23,33,34,54,57,58,59,60,61,63,64,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,98,100,102,103,107,116,119,121,122,123,124,125,126,127,131,138,139,140,148,151,152,154,158,159,160,],[36,55,56,-31,-73,-74,-75,-76,-77,-78,-79,-81,79,80,-80,98,-32,102,-66,-78,-65,-67,-16,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-29,-34,-30,-72,-88,136,-33,-36,-37,-38,-39,-40,-41,-42,-9,-35,-20,-22,157,-21,-14,-18,-17,-15,-19,]),'MULTIPLY':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[39,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,39,-78,39,39,39,-50,-51,39,-53,39,39,39,39,39,39,39,39,39,39,39,-72,39,39,39,39,39,-9,39,-20,39,39,39,-21,-18,-17,-19,39,]),'DIVIDE':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[40,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,40,-78,40,40,40,-50,-51,40,-53,40,40,40,40,40,40,40,40,40,40,40,-72,40,40,40,40,40,-9,40,-20,40,40,40,-21,-18,-17,-19,40,]),'EQUALS':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[41,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,41,-78,41,-48,-49,-50,-51,None,-53,None,None,None,None,None,41,41,41,41,41,41,-72,41,41,41,41,41,-9,41,-20,41,41,41,-21,-18,-17,-19,41,]),'MODULUS':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[42,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,42,-78,42,42,42,-50,-51,42,-53,42,42,42,42,42,42,42,42,42,42,42,-72,42,42,42,42,42,-9,42,-20,42,42,42,-21,-18,-17,-19,42,]),'NE':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[43,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,43,-78,43,-48,-49,-50,-51,None,-53,None,None,None,None,None,43,43,43,43,43,43,-72,43,43,43,43,43,-9,43,-20,43,43,43,-21,-18,-17,-19,43,]),'GT':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[44,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,44,-78,44,-48,-49,-50,-51,None,-53,None,None,None,None,None,44,44,44,44,44,44,-72,44,44,44,44,44,-9,44,-20,44,44,44,-21,-18,-17,-19,44,]),'LT':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[45,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,45,-78,45,-48,-49,-50,-51,None,-53,None,None,None,None,None,45,45,45,45,45,45,-72,45,45,45,45,45,-9,45,-20,45,45,45,-21,-18,-17,-19,45,]),'GE':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[46,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,46,-78,46,-48,-49,-50,-51,None,-53,None,None,None,None,None,46,46,46,46,46,46,-72,46,46,46,46,46,-9,46,-20,46,46,46,-21,-18,-17,-19,46,]),'LE':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[47,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,47,-78,47,-48,-49,-50,-51,None,-53,None,None,None,None,None,47,47,47,47,47,47,-72,47,47,47,47,47,-9,47,-20,47,47,47,-21,-18,-17,-19,47,]),'AND':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[48,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,48,-78,48,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,48,48,48,48,48,-72,48,48,48,48,48,-9,48,-20,48,48,48,-21,-18,-17,-19,48,]),'OR':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[49,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,49,-78,49,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,49,49,49,49,-72,49,49,49,49,49,-9,49,-20,49,49,49,-21,-18,-17,-19,49,]),'CHAIN':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[50,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,50,-78,50,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,50,50,-72,50,50,50,50,50,-9,50,-20,50,50,50,-21,-18,-17,-19,50,]),'STREAMSPLIT':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[51,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,51,-78,51,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,51,-62,51,51,-72,51,51,51,51,51,-9,51,-20,51,51,51,-21,-18,-17,-19,51,]),'STREAMMERGE':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[52,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,52,-78,52,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,52,-72,52,52,52,52,52,-9,52,-20,52,52,52,-21,-18,-17,-19,52,]),'FEEDBACK':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[53,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,53,-78,53,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-72,53,53,53,53,53,-9,53,-20,53,53,53,-21,-18,-17,-19,53,]),'TO_STREAM':([5,16,17,18,19,20,21,22,23,54,60,61,63,64,65,67,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,107,111,115,118,119,131,138,139,140,143,148,151,154,158,160,162,],[54,-73,-74,-75,-76,-77,-78,-79,-81,-80,-66,-78,-65,-67,54,-78,54,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-72,54,54,54,54,54,-9,54,-20,54,54,54,-21,-18,-17,-19,54,]),'RPAREN':([15,16,17,18,19,20,22,23,54,60,61,63,64,65,66,67,68,69,70,72,75,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,105,108,109,110,111,112,113,114,115,118,121,122,123,124,125,126,127,130,131,133,139,140,143,151,154,158,160,162,],[-89,-73,-74,-75,-76,-77,-79,-81,-80,-66,-78,-65,-67,103,104,-27,-23,-24,-25,-89,-89,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-72,-28,131,-10,-11,-12,-89,134,-27,135,137,-36,-37,-38,-39,-40,-41,-42,-26,-9,144,-20,-22,-13,-21,-18,-17,-19,163,]),'COMMA':([16,17,18,19,20,22,23,54,60,61,63,64,67,68,70,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,103,105,109,111,114,121,122,123,124,125,126,127,130,131,139,140,143,151,154,158,160,],[-73,-74,-75,-76,-77,-79,-81,-80,-66,-78,-65,-67,-27,106,-25,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-64,-72,-28,132,-12,-27,-36,-37,-38,-39,-40,-41,-42,-26,-9,-20,-22,-13,-21,-18,-17,-19,]),'ASSIGN':([21,58,100,121,122,123,124,125,126,127,],[71,99,120,-36,-37,-38,-39,-40,-41,-42,]),'TYPEHINTCOLON':([58,67,104,114,134,144,],[101,101,101,101,101,101,]),'SINT':([101,],[122,]),'SFLOAT':([101,],[123,]),'SSTRING':([101,],[124,]),'SBOOL':([101,],[125,]),'SSTREAM':([101,],[126,]),'SEVENT':([101,],[127,]),'LAMBDA':([104,121,122,123,124,125,126,127,129,134,146,],[128,-36,-37,-38,-39,-40,-41,-42,142,145,155,]),'LBRACE':([121,122,123,124,125,126,127,128,135,137,142,144,145,153,155,156,163,],[-36,-37,-38,-39,-40,-41,-42,141,141,141,141,141,141,141,141,141,141,]),'ELSE':([147,158,],[156,-17,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'statement_list':([0,141,],[2,150,]),'statement':([0,2,141,150,],[3,35,3,35,]),'declaration':([0,2,77,141,150,],[4,4,116,4,4,]),'expression':([0,2,12,13,14,15,24,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,71,72,76,78,99,120,128,132,136,141,150,157,],[5,5,60,63,64,65,73,81,82,83,84,85,86,87,88,89,90,91,92,93,94,95,96,97,107,111,115,118,119,138,140,143,148,5,5,162,]),'return_statement':([0,2,141,150,],[6,6,6,6,]),'control_flow':([0,2,141,150,],[7,7,7,7,]),'assignment':([0,2,141,150,],[8,8,8,8,]),'function_definition':([0,2,77,141,150,],[11,11,11,11,11,]),'function_call':([0,2,12,13,14,15,24,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,71,72,76,78,99,120,128,132,136,141,150,157,],[22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,]),'lambda_function':([0,2,12,13,14,15,24,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,71,72,76,78,99,120,128,132,136,141,150,157,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'conditional':([0,2,141,150,],[25,25,25,25,]),'loop':([0,2,141,150,],[26,26,26,26,]),'break':([0,2,141,150,],[27,27,27,27,]),'continue':([0,2,141,150,],[28,28,28,28,]),'declaration_base':([9,10,],[57,59,]),'opt_param_list':([15,75,112,],[66,113,133,]),'param_list':([15,75,112,],[68,68,68,]),'empty':([15,72,75,112,],[69,110,69,69,]),'param':([15,75,106,112,],[70,70,130,70,]),'typehint':([58,67,104,114,134,144,],[100,105,129,105,146,153,]),'opt_arg_list':([72,],[108,]),'arg_list':([72,],[109,]),'type':([101,],[121,]),'block_statement':([128,135,137,142,144,145,153,155,156,163,],[139,147,149,151,152,154,159,160,161,164,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement_list','program',1,'p_program','parser.py',40),
  ('statement -> declaration','statement',1,'p_statement','parser.py',46),
  ('statement -> expression SEMICOLON','statement',2,'p_statement','parser.py',47),
  ('statement -> return_statement SEMICOLON','statement',2,'p_statement','parser.py',48),
  ('statement -> control_flow','statement',1,'p_statement','parser.py',49),
  ('statement -> assignment SEMICOLON','statement',2,'p_statement','parser.py',50),
  ('statement_list -> statement','statement_list',1,'p_statement_list','parser.py',54),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list','parser.py',55),
  ('function_call -> IDENTIFIER LPAREN opt_arg_list RPAREN','function_call',4,'p_function_call','parser.py',62),
  ('opt_arg_list -> arg_list','opt_arg_list',1,'p_opt_arg_list','parser.py',66),
  ('opt_arg_list -> empty','opt_arg_list',1,'p_opt_arg_list','parser.py',67),
  ('arg_list -> expression','arg_list',1,'p_arg_list','parser.py',74),
  ('arg_list -> arg_list COMMA expression','arg_list',3,'p_arg_list','parser.py',75),
  ('function_definition -> FN IDENTIFIER LPAREN opt_param_list RPAREN block_statement','function_definition',6,'p_function_definition','parser.py',83),
  ('function_definition -> FN IDENTIFIER LPAREN opt_param_list RPAREN typehint block_statement','function_definition',7,'p_function_definition','parser.py',84),
  ('return_statement -> RETURN expression','return_statement',2,'p_return_statement','parser.py',103),
  ('block_statement -> LBRACE statement_list RBRACE','block_statement',3,'p_block_statement','parser.py',107),
  ('lambda_function -> FN LPAREN opt_param_list RPAREN LAMBDA block_statement','lambda_function',6,'p_lambda_function','parser.py',111),
  ('lambda_function -> FN LPAREN opt_param_list RPAREN typehint LAMBDA block_statement','lambda_function',7,'p_lambda_function','parser.py',112),
  ('lambda_function -> LPAREN opt_param_list RPAREN LAMBDA block_statement','lambda_function',5,'p_lambda_function','parser.py',113),
  ('lambda_function -> LPAREN opt_param_list RPAREN typehint LAMBDA block_statement','lambda_function',6,'p_lambda_function','parser.py',114),
  ('lambda_function -> LPAREN opt_param_list RPAREN LAMBDA expression','lambda_function',5,'p_lambda_function','parser.py',115),
  ('opt_param_list -> param_list','opt_param_list',1,'p_opt_param_list','parser.py',130),
  ('opt_param_list -> empty','opt_param_list',1,'p_opt_param_list','parser.py',131),
  ('param_list -> param','param_list',1,'p_param_list','parser.py',135),
  ('param_list -> param_list COMMA param','param_list',3,'p_param_list','parser.py',136),
  ('param -> IDENTIFIER','param',1,'p_param','parser.py',143),
  ('param -> IDENTIFIER typehint','param',2,'p_param','parser.py',144),
  ('declaration -> VAR declaration_base SEMICOLON','declaration',3,'p_declaration','parser.py',153),
  ('declaration -> CONST declaration_base SEMICOLON','declaration',3,'p_declaration','parser.py',154),
  ('declaration -> function_definition','declaration',1,'p_declaration','parser.py',155),
  ('declaration_base -> IDENTIFIER','declaration_base',1,'p_declaration_base','parser.py',166),
  ('declaration_base -> IDENTIFIER ASSIGN expression','declaration_base',3,'p_declaration_base','parser.py',167),
  ('declaration_base -> IDENTIFIER typehint','declaration_base',2,'p_declaration_base','parser.py',168),
  ('declaration_base -> IDENTIFIER typehint ASSIGN expression','declaration_base',4,'p_declaration_base','parser.py',169),
  ('typehint -> TYPEHINTCOLON type','typehint',2,'p_typehint','parser.py',188),
  ('type -> SINT','type',1,'p_type','parser.py',195),
  ('type -> SFLOAT','type',1,'p_type','parser.py',196),
  ('type -> SSTRING','type',1,'p_type','parser.py',197),
  ('type -> SBOOL','type',1,'p_type','parser.py',198),
  ('type -> SSTREAM','type',1,'p_type','parser.py',199),
  ('type -> SEVENT','type',1,'p_type','parser.py',200),
  ('ptype -> INT','ptype',1,'p_primitive_type','parser.py',204),
  ('ptype -> FLOAT','ptype',1,'p_primitive_type','parser.py',205),
  ('ptype -> STRING','ptype',1,'p_primitive_type','parser.py',206),
  ('ptype -> TRUE','ptype',1,'p_primitive_type','parser.py',207),
  ('ptype -> FALSE','ptype',1,'p_primitive_type','parser.py',208),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','parser.py',225),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','parser.py',226),
  ('expression -> expression MULTIPLY expression','expression',3,'p_expression_binop','parser.py',227),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','parser.py',228),
  ('expression -> expression EQUALS expression','expression',3,'p_expression_binop','parser.py',229),
  ('expression -> expression MODULUS expression','expression',3,'p_expression_binop','parser.py',230),
  ('expression -> expression NE expression','expression',3,'p_expression_binop','parser.py',231),
  ('expression -> expression GT expression','expression',3,'p_expression_binop','parser.py',232),
  ('expression -> expression LT expression','expression',3,'p_expression_binop','parser.py',233),
  ('expression -> expression GE expression','expression',3,'p_expression_binop','parser.py',234),
  ('expression -> expression LE expression','expression',3,'p_expression_binop','parser.py',235),
  ('expression -> expression AND expression','expression',3,'p_expression_binop','parser.py',236),
  ('expression -> expression OR expression','expression',3,'p_expression_binop','parser.py',237),
  ('expression -> expression CHAIN expression','expression',3,'p_expression_binop','parser.py',238),
  ('expression -> expression STREAMSPLIT expression','expression',3,'p_expression_binop','parser.py',239),
  ('expression -> expression STREAMMERGE expression','expression',3,'p_expression_binop','parser.py',240),
  ('expression -> expression FEEDBACK expression','expression',3,'p_expression_binop','parser.py',241),
  ('expression -> MINUS expression','expression',2,'p_expression_unary','parser.py',250),
  ('expression -> PLUS expression','expression',2,'p_expression_unary','parser.py',251),
  ('expression -> NOT expression','expression',2,'p_expression_unary','parser.py',252),
  ('control_flow -> conditional','control_flow',1,'p_control_flow','parser.py',260),
  ('control_flow -> loop','control_flow',1,'p_control_flow','parser.py',261),
  ('control_flow -> break','control_flow',1,'p_control_flow','parser.py',262),
  ('control_flow -> continue','control_flow',1,'p_control_flow','parser.py',263),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','parser.py',267),
  ('expression -> INT','expression',1,'p_expression_number','parser.py',271),
  ('expression -> FLOAT','expression',1,'p_expression_number','parser.py',272),
  ('expression -> STRING','expression',1,'p_expression_string','parser.py',279),
  ('expression -> TRUE','expression',1,'p_expression_boolean','parser.py',283),
  ('expression -> FALSE','expression',1,'p_expression_boolean','parser.py',284),
  ('expression -> IDENTIFIER','expression',1,'p_expression_identifier','parser.py',289),
  ('expression -> function_call','expression',1,'p_expression_function_call','parser.py',293),
  ('expression -> expression TO_STREAM','expression',2,'p_expression_to_stream','parser.py',301),
  ('expression -> lambda_function','expression',1,'p_expression_lambda','parser.py',305),
  ('conditional -> IF LPAREN expression RPAREN block_statement ELSE block_statement','conditional',7,'p_conditional','parser.py',310),
  ('conditional -> IF LPAREN expression RPAREN block_statement','conditional',5,'p_conditional','parser.py',311),
  ('loop -> FOR LPAREN declaration SEMICOLON expression SEMICOLON expression RPAREN block_statement','loop',9,'p_loop','parser.py',319),
  ('loop -> WHILE LPAREN expression RPAREN block_statement','loop',5,'p_loop','parser.py',320),
  ('break -> BREAK SEMICOLON','break',2,'p_break','parser.py',327),
  ('continue -> CONTINUE SEMICOLON','continue',2,'p_continue','parser.py',331),
  ('assignment -> IDENTIFIER ASSIGN expression','assignment',3,'p_assignment','parser.py',335),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',340),
]
