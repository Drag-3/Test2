
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftFEEDBACKleftSTREAMMERGEleftCHAINleftSTREAMSPLITleftORleftANDnonassocEQUALSNEGTLTGELEleftPLUSMINUSleftMULTIPLYDIVIDErightNOTrightUMINUSUPLUSAND ASSIGN ATTACH CALL CHAIN COMMA CONST DIVIDE ELSE EOF EQUALS EVENT FALSE FEEDBACK FILTEROP FLOAT FN FOR GE GT IDENTIFIER IF INT LAMBDA LBRACE LBRACKET LE LPAREN LT MAP MINUS MULTIPLY NE NEWLINE NOT OR PLUS RBRACE RBRACKET REDUCE RETURN RPAREN SBOOL SEMICOLON SEVENT SFLOAT SINT SSTREAM SSTRING STREAM STREAMMERGE STREAMSPLIT STRING TO_STREAM TRUE TYPEHINTCOLON VAR WHILEprogram : statement_liststatement : declaration\n| expression SEMICOLON\n| return_statement SEMICOLON\n| control_flow\n| assignment SEMICOLONstatement_list : statement\n| statement_list statementfunction_call : IDENTIFIER LPAREN opt_arg_list RPARENopt_arg_list : arg_list\n| emptyarg_list : expression\n| arg_list COMMA expressionfunction_definition : FN IDENTIFIER LPAREN opt_param_list RPAREN block_statement\n| FN IDENTIFIER LPAREN opt_param_list RPAREN typehint block_statementreturn_statement : RETURN expressionblock_statement : LBRACE statement_list RBRACElambda_function : FN LPAREN opt_param_list RPAREN LAMBDA block_statement\n| FN LPAREN opt_param_list RPAREN typehint LAMBDA block_statement\n| LPAREN opt_param_list RPAREN LAMBDA block_statement\n| LPAREN opt_param_list RPAREN typehint LAMBDA block_statement\n| LPAREN opt_param_list RPAREN LAMBDA expressionopt_param_list : param_list\n| emptyparam_list : param\n| param_list COMMA paramparam : IDENTIFIER\n| IDENTIFIER typehintdeclaration : VAR declaration_base SEMICOLON\n| CONST declaration_base SEMICOLON\n| function_definitiondeclaration_base : IDENTIFIER\n| IDENTIFIER ASSIGN expression\n| IDENTIFIER typehint\n| IDENTIFIER typehint ASSIGN expressiontypehint : TYPEHINTCOLON typetype : SINT\n| SFLOAT\n| SSTRING\n| SBOOL\n| SSTREAM\n| SEVENTptype : INT\n| FLOAT\n| STRING\n| TRUE\n| FALSEexpression : expression PLUS expression\n| expression MINUS expression\n| expression MULTIPLY expression\n| expression DIVIDE expression\n| expression EQUALS expression\n| expression NE expression\n| expression GT expression\n| expression LT expression\n| expression GE expression\n| expression LE expression\n| expression AND expression\n| expression OR expression\n| expression CHAIN expression\n| expression STREAMSPLIT expression\n| expression STREAMMERGE expression\n| expression FEEDBACK expression\nexpression : MINUS expression %prec UMINUS\n| PLUS expression %prec UPLUS\n| NOT expression\ncontrol_flow : conditional\n| loopexpression : LPAREN expression RPARENexpression : INT\n| FLOATexpression : STRINGexpression : TRUE\n| FALSEexpression : IDENTIFIERexpression : function_callexpression : expression TO_STREAMexpression : lambda_functionconditional : IF LPAREN expression RPAREN block_statement ELSE block_statement\n| IF LPAREN expression RPAREN block_statementloop : FOR LPAREN declaration SEMICOLON expression SEMICOLON expression RPAREN block_statement\n| WHILE LPAREN expression RPAREN block_statementassignment : IDENTIFIER ASSIGN expressionempty :'
    
_lr_action_items = {'VAR':([0,2,3,4,7,11,25,26,31,32,50,51,72,90,94,133,139,141,142,144,150,151,153,156,],[9,9,-7,-2,-5,-31,-67,-68,-8,-3,-4,-6,9,-29,-30,9,-80,-82,9,-14,-17,-15,-79,-81,]),'CONST':([0,2,3,4,7,11,25,26,31,32,50,51,72,90,94,133,139,141,142,144,150,151,153,156,],[10,10,-7,-2,-5,-31,-67,-68,-8,-3,-4,-6,10,-29,-30,10,-80,-82,10,-14,-17,-15,-79,-81,]),'MINUS':([0,2,3,4,5,7,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,55,56,58,59,60,62,66,67,68,71,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,94,95,99,103,107,110,111,112,120,123,124,128,130,131,132,133,135,139,140,141,142,143,144,146,149,150,151,152,153,154,156,],[13,13,-7,-2,34,-5,-31,13,13,13,13,-70,-71,-72,-73,-74,-75,-76,-78,13,-67,-68,-8,-3,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,13,-77,-4,-6,-65,-75,-64,-66,34,-75,13,13,34,13,13,-48,-49,-50,-51,34,34,34,34,34,34,34,34,34,34,34,34,-29,13,-30,-69,34,34,34,34,34,13,13,-9,13,13,34,-20,34,13,34,-80,34,-82,13,-21,-14,-18,13,-17,-15,-19,-79,34,-81,]),'PLUS':([0,2,3,4,5,7,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,55,56,58,59,60,62,66,67,68,71,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,91,94,95,99,103,107,110,111,112,120,123,124,128,130,131,132,133,135,139,140,141,142,143,144,146,149,150,151,152,153,154,156,],[12,12,-7,-2,33,-5,-31,12,12,12,12,-70,-71,-72,-73,-74,-75,-76,-78,12,-67,-68,-8,-3,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,12,-77,-4,-6,-65,-75,-64,-66,33,-75,12,12,33,12,12,-48,-49,-50,-51,33,33,33,33,33,33,33,33,33,33,33,33,-29,12,-30,-69,33,33,33,33,33,12,12,-9,12,12,33,-20,33,12,33,-80,33,-82,12,-21,-14,-18,12,-17,-15,-19,-79,33,-81,]),'NOT':([0,2,3,4,7,11,12,13,14,15,24,25,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,66,67,71,73,90,91,94,112,120,124,128,133,139,141,142,144,149,150,151,153,156,],[14,14,-7,-2,-5,-31,14,14,14,14,14,-67,-68,-8,-3,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,-4,-6,14,14,14,14,-29,14,-30,14,14,14,14,14,-80,-82,14,-14,14,-17,-15,-79,-81,]),'LPAREN':([0,2,3,4,7,11,12,13,14,15,21,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,56,57,62,66,67,69,71,73,90,91,94,112,120,124,128,133,139,141,142,144,149,150,151,153,156,],[15,15,-7,-2,-5,-31,15,15,15,15,67,15,-67,-68,70,71,72,73,-8,-3,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,15,-4,-6,67,70,67,15,15,104,15,15,-29,15,-30,15,15,15,15,15,-80,-82,15,-14,15,-17,-15,-79,-81,]),'INT':([0,2,3,4,7,11,12,13,14,15,24,25,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,66,67,71,73,90,91,94,112,120,124,128,133,139,141,142,144,149,150,151,153,156,],[16,16,-7,-2,-5,-31,16,16,16,16,16,-67,-68,-8,-3,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,16,-4,-6,16,16,16,16,-29,16,-30,16,16,16,16,16,-80,-82,16,-14,16,-17,-15,-79,-81,]),'FLOAT':([0,2,3,4,7,11,12,13,14,15,24,25,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,66,67,71,73,90,91,94,112,120,124,128,133,139,141,142,144,149,150,151,153,156,],[17,17,-7,-2,-5,-31,17,17,17,17,17,-67,-68,-8,-3,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,-4,-6,17,17,17,17,-29,17,-30,17,17,17,17,17,-80,-82,17,-14,17,-17,-15,-79,-81,]),'STRING':([0,2,3,4,7,11,12,13,14,15,24,25,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,66,67,71,73,90,91,94,112,120,124,128,133,139,141,142,144,149,150,151,153,156,],[18,18,-7,-2,-5,-31,18,18,18,18,18,-67,-68,-8,-3,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,-4,-6,18,18,18,18,-29,18,-30,18,18,18,18,18,-80,-82,18,-14,18,-17,-15,-79,-81,]),'TRUE':([0,2,3,4,7,11,12,13,14,15,24,25,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,66,67,71,73,90,91,94,112,120,124,128,133,139,141,142,144,149,150,151,153,156,],[19,19,-7,-2,-5,-31,19,19,19,19,19,-67,-68,-8,-3,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,-4,-6,19,19,19,19,-29,19,-30,19,19,19,19,19,-80,-82,19,-14,19,-17,-15,-79,-81,]),'FALSE':([0,2,3,4,7,11,12,13,14,15,24,25,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,66,67,71,73,90,91,94,112,120,124,128,133,139,141,142,144,149,150,151,153,156,],[20,20,-7,-2,-5,-31,20,20,20,20,20,-67,-68,-8,-3,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,-4,-6,20,20,20,20,-29,20,-30,20,20,20,20,20,-80,-82,20,-14,20,-17,-15,-79,-81,]),'IDENTIFIER':([0,2,3,4,7,9,10,11,12,13,14,15,24,25,26,27,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,66,67,70,71,73,90,91,94,98,104,109,112,120,124,128,133,139,141,142,144,149,150,151,153,156,],[21,21,-7,-2,-5,53,53,-31,56,56,56,62,56,-67,-68,69,-8,-3,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,56,-4,-6,56,56,106,56,56,-29,56,-30,106,106,69,56,56,56,56,21,-80,-82,21,-14,56,-17,-15,-79,-81,]),'RETURN':([0,2,3,4,7,11,25,26,31,32,50,51,90,94,133,139,141,142,144,150,151,153,156,],[24,24,-7,-2,-5,-31,-67,-68,-8,-3,-4,-6,-29,-30,24,-80,-82,24,-14,-17,-15,-79,-81,]),'FN':([0,2,3,4,7,11,12,13,14,15,24,25,26,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,50,51,66,67,71,72,73,90,91,94,112,120,124,128,133,139,141,142,144,149,150,151,153,156,],[27,27,-7,-2,-5,-31,57,57,57,57,57,-67,-68,-8,-3,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,57,-4,-6,57,57,57,109,57,-29,57,-30,57,57,57,57,27,-80,-82,27,-14,57,-17,-15,-79,-81,]),'IF':([0,2,3,4,7,11,25,26,31,32,50,51,90,94,133,139,141,142,144,150,151,153,156,],[28,28,-7,-2,-5,-31,-67,-68,-8,-3,-4,-6,-29,-30,28,-80,-82,28,-14,-17,-15,-79,-81,]),'FOR':([0,2,3,4,7,11,25,26,31,32,50,51,90,94,133,139,141,142,144,150,151,153,156,],[29,29,-7,-2,-5,-31,-67,-68,-8,-3,-4,-6,-29,-30,29,-80,-82,29,-14,-17,-15,-79,-81,]),'WHILE':([0,2,3,4,7,11,25,26,31,32,50,51,90,94,133,139,141,142,144,150,151,153,156,],[30,30,-7,-2,-5,-31,-67,-68,-8,-3,-4,-6,-29,-30,30,-80,-82,30,-14,-17,-15,-79,-81,]),'$end':([1,2,3,4,7,11,25,26,31,32,50,51,90,94,139,141,144,150,151,153,156,],[0,-1,-7,-2,-5,-31,-67,-68,-8,-3,-4,-6,-29,-30,-80,-82,-14,-17,-15,-79,-81,]),'RBRACE':([3,4,7,11,25,26,31,32,50,51,90,94,139,141,142,144,150,151,153,156,],[-7,-2,-5,-31,-67,-68,-8,-3,-4,-6,-29,-30,-80,-82,150,-14,-17,-15,-79,-81,]),'SEMICOLON':([5,6,8,11,16,17,18,19,20,21,22,23,49,52,53,54,55,56,58,59,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,90,92,94,95,99,108,111,113,114,115,116,117,118,119,123,130,131,132,140,143,144,146,150,151,152,],[32,50,51,-31,-70,-71,-72,-73,-74,-75,-76,-78,-77,90,-32,94,-65,-75,-64,-66,-16,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-29,-34,-30,-69,-83,128,-33,-36,-37,-38,-39,-40,-41,-42,-9,-35,-20,-22,149,-21,-14,-18,-17,-15,-19,]),'MULTIPLY':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[35,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,35,-75,35,35,35,-50,-51,35,35,35,35,35,35,35,35,35,35,35,35,-69,35,35,35,35,35,-9,35,-20,35,35,35,-21,-18,-17,-19,35,]),'DIVIDE':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[36,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,36,-75,36,36,36,-50,-51,36,36,36,36,36,36,36,36,36,36,36,36,-69,36,36,36,36,36,-9,36,-20,36,36,36,-21,-18,-17,-19,36,]),'EQUALS':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[37,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,37,-75,37,-48,-49,-50,-51,None,None,None,None,None,None,37,37,37,37,37,37,-69,37,37,37,37,37,-9,37,-20,37,37,37,-21,-18,-17,-19,37,]),'NE':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[38,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,38,-75,38,-48,-49,-50,-51,None,None,None,None,None,None,38,38,38,38,38,38,-69,38,38,38,38,38,-9,38,-20,38,38,38,-21,-18,-17,-19,38,]),'GT':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[39,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,39,-75,39,-48,-49,-50,-51,None,None,None,None,None,None,39,39,39,39,39,39,-69,39,39,39,39,39,-9,39,-20,39,39,39,-21,-18,-17,-19,39,]),'LT':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[40,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,40,-75,40,-48,-49,-50,-51,None,None,None,None,None,None,40,40,40,40,40,40,-69,40,40,40,40,40,-9,40,-20,40,40,40,-21,-18,-17,-19,40,]),'GE':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[41,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,41,-75,41,-48,-49,-50,-51,None,None,None,None,None,None,41,41,41,41,41,41,-69,41,41,41,41,41,-9,41,-20,41,41,41,-21,-18,-17,-19,41,]),'LE':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[42,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,42,-75,42,-48,-49,-50,-51,None,None,None,None,None,None,42,42,42,42,42,42,-69,42,42,42,42,42,-9,42,-20,42,42,42,-21,-18,-17,-19,42,]),'AND':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[43,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,43,-75,43,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,43,43,43,43,43,-69,43,43,43,43,43,-9,43,-20,43,43,43,-21,-18,-17,-19,43,]),'OR':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[44,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,44,-75,44,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,44,44,44,44,-69,44,44,44,44,44,-9,44,-20,44,44,44,-21,-18,-17,-19,44,]),'CHAIN':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[45,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,45,-75,45,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,45,45,-69,45,45,45,45,45,-9,45,-20,45,45,45,-21,-18,-17,-19,45,]),'STREAMSPLIT':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[46,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,46,-75,46,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,46,-61,46,46,-69,46,46,46,46,46,-9,46,-20,46,46,46,-21,-18,-17,-19,46,]),'STREAMMERGE':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[47,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,47,-75,47,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,47,-69,47,47,47,47,47,-9,47,-20,47,47,47,-21,-18,-17,-19,47,]),'FEEDBACK':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[48,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,48,-75,48,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-69,48,48,48,48,48,-9,48,-20,48,48,48,-21,-18,-17,-19,48,]),'TO_STREAM':([5,16,17,18,19,20,21,22,23,49,55,56,58,59,60,62,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,99,103,107,110,111,123,130,131,132,135,140,143,146,150,152,154,],[49,-70,-71,-72,-73,-74,-75,-76,-78,-77,-65,-75,-64,-66,49,-75,49,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-69,49,49,49,49,49,-9,49,-20,49,49,49,-21,-18,-17,-19,49,]),'RPAREN':([15,16,17,18,19,20,22,23,49,55,56,58,59,60,61,62,63,64,65,67,70,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,97,100,101,102,103,104,105,106,107,110,113,114,115,116,117,118,119,122,123,125,131,132,135,143,146,150,152,154,],[-84,-70,-71,-72,-73,-74,-76,-78,-77,-65,-75,-64,-66,95,96,-27,-23,-24,-25,-84,-84,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-69,-28,123,-10,-11,-12,-84,126,-27,127,129,-36,-37,-38,-39,-40,-41,-42,-26,-9,136,-20,-22,-13,-21,-18,-17,-19,155,]),'COMMA':([16,17,18,19,20,22,23,49,55,56,58,59,62,63,65,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,95,97,101,103,106,113,114,115,116,117,118,119,122,123,131,132,135,143,146,150,152,],[-70,-71,-72,-73,-74,-76,-78,-77,-65,-75,-64,-66,-27,98,-25,-48,-49,-50,-51,-52,-53,-54,-55,-56,-57,-58,-59,-60,-61,-62,-63,-69,-28,124,-12,-27,-36,-37,-38,-39,-40,-41,-42,-26,-9,-20,-22,-13,-21,-18,-17,-19,]),'ASSIGN':([21,53,92,113,114,115,116,117,118,119,],[66,91,112,-36,-37,-38,-39,-40,-41,-42,]),'TYPEHINTCOLON':([53,62,96,106,126,136,],[93,93,93,93,93,93,]),'SINT':([93,],[114,]),'SFLOAT':([93,],[115,]),'SSTRING':([93,],[116,]),'SBOOL':([93,],[117,]),'SSTREAM':([93,],[118,]),'SEVENT':([93,],[119,]),'LAMBDA':([96,113,114,115,116,117,118,119,121,126,138,],[120,-36,-37,-38,-39,-40,-41,-42,134,137,147,]),'LBRACE':([113,114,115,116,117,118,119,120,127,129,134,136,137,145,147,148,155,],[-36,-37,-38,-39,-40,-41,-42,133,133,133,133,133,133,133,133,133,133,]),'ELSE':([139,150,],[148,-17,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'statement_list':([0,133,],[2,142,]),'statement':([0,2,133,142,],[3,31,3,31,]),'declaration':([0,2,72,133,142,],[4,4,108,4,4,]),'expression':([0,2,12,13,14,15,24,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,66,67,71,73,91,112,120,124,128,133,142,149,],[5,5,55,58,59,60,68,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,89,99,103,107,110,111,130,132,135,140,5,5,154,]),'return_statement':([0,2,133,142,],[6,6,6,6,]),'control_flow':([0,2,133,142,],[7,7,7,7,]),'assignment':([0,2,133,142,],[8,8,8,8,]),'function_definition':([0,2,72,133,142,],[11,11,11,11,11,]),'function_call':([0,2,12,13,14,15,24,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,66,67,71,73,91,112,120,124,128,133,142,149,],[22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,]),'lambda_function':([0,2,12,13,14,15,24,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,66,67,71,73,91,112,120,124,128,133,142,149,],[23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,23,]),'conditional':([0,2,133,142,],[25,25,25,25,]),'loop':([0,2,133,142,],[26,26,26,26,]),'declaration_base':([9,10,],[52,54,]),'opt_param_list':([15,70,104,],[61,105,125,]),'param_list':([15,70,104,],[63,63,63,]),'empty':([15,67,70,104,],[64,102,64,64,]),'param':([15,70,98,104,],[65,65,122,65,]),'typehint':([53,62,96,106,126,136,],[92,97,121,97,138,145,]),'opt_arg_list':([67,],[100,]),'arg_list':([67,],[101,]),'type':([93,],[113,]),'block_statement':([120,127,129,134,136,137,145,147,148,155,],[131,139,141,143,144,146,151,152,153,156,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> statement_list','program',1,'p_program','parser.py',34),
  ('statement -> declaration','statement',1,'p_statement','parser.py',40),
  ('statement -> expression SEMICOLON','statement',2,'p_statement','parser.py',41),
  ('statement -> return_statement SEMICOLON','statement',2,'p_statement','parser.py',42),
  ('statement -> control_flow','statement',1,'p_statement','parser.py',43),
  ('statement -> assignment SEMICOLON','statement',2,'p_statement','parser.py',44),
  ('statement_list -> statement','statement_list',1,'p_statement_list','parser.py',49),
  ('statement_list -> statement_list statement','statement_list',2,'p_statement_list','parser.py',50),
  ('function_call -> IDENTIFIER LPAREN opt_arg_list RPAREN','function_call',4,'p_function_call','parser.py',59),
  ('opt_arg_list -> arg_list','opt_arg_list',1,'p_opt_arg_list','parser.py',65),
  ('opt_arg_list -> empty','opt_arg_list',1,'p_opt_arg_list','parser.py',66),
  ('arg_list -> expression','arg_list',1,'p_arg_list','parser.py',74),
  ('arg_list -> arg_list COMMA expression','arg_list',3,'p_arg_list','parser.py',75),
  ('function_definition -> FN IDENTIFIER LPAREN opt_param_list RPAREN block_statement','function_definition',6,'p_function_definition','parser.py',84),
  ('function_definition -> FN IDENTIFIER LPAREN opt_param_list RPAREN typehint block_statement','function_definition',7,'p_function_definition','parser.py',85),
  ('return_statement -> RETURN expression','return_statement',2,'p_return_statement','parser.py',98),
  ('block_statement -> LBRACE statement_list RBRACE','block_statement',3,'p_block_statement','parser.py',102),
  ('lambda_function -> FN LPAREN opt_param_list RPAREN LAMBDA block_statement','lambda_function',6,'p_lambda_function','parser.py',107),
  ('lambda_function -> FN LPAREN opt_param_list RPAREN typehint LAMBDA block_statement','lambda_function',7,'p_lambda_function','parser.py',108),
  ('lambda_function -> LPAREN opt_param_list RPAREN LAMBDA block_statement','lambda_function',5,'p_lambda_function','parser.py',109),
  ('lambda_function -> LPAREN opt_param_list RPAREN typehint LAMBDA block_statement','lambda_function',6,'p_lambda_function','parser.py',110),
  ('lambda_function -> LPAREN opt_param_list RPAREN LAMBDA expression','lambda_function',5,'p_lambda_function','parser.py',111),
  ('opt_param_list -> param_list','opt_param_list',1,'p_opt_param_list','parser.py',127),
  ('opt_param_list -> empty','opt_param_list',1,'p_opt_param_list','parser.py',128),
  ('param_list -> param','param_list',1,'p_param_list','parser.py',133),
  ('param_list -> param_list COMMA param','param_list',3,'p_param_list','parser.py',134),
  ('param -> IDENTIFIER','param',1,'p_param','parser.py',142),
  ('param -> IDENTIFIER typehint','param',2,'p_param','parser.py',143),
  ('declaration -> VAR declaration_base SEMICOLON','declaration',3,'p_declaration','parser.py',152),
  ('declaration -> CONST declaration_base SEMICOLON','declaration',3,'p_declaration','parser.py',153),
  ('declaration -> function_definition','declaration',1,'p_declaration','parser.py',154),
  ('declaration_base -> IDENTIFIER','declaration_base',1,'p_declaration_base','parser.py',167),
  ('declaration_base -> IDENTIFIER ASSIGN expression','declaration_base',3,'p_declaration_base','parser.py',168),
  ('declaration_base -> IDENTIFIER typehint','declaration_base',2,'p_declaration_base','parser.py',169),
  ('declaration_base -> IDENTIFIER typehint ASSIGN expression','declaration_base',4,'p_declaration_base','parser.py',170),
  ('typehint -> TYPEHINTCOLON type','typehint',2,'p_typehint','parser.py',190),
  ('type -> SINT','type',1,'p_type','parser.py',196),
  ('type -> SFLOAT','type',1,'p_type','parser.py',197),
  ('type -> SSTRING','type',1,'p_type','parser.py',198),
  ('type -> SBOOL','type',1,'p_type','parser.py',199),
  ('type -> SSTREAM','type',1,'p_type','parser.py',200),
  ('type -> SEVENT','type',1,'p_type','parser.py',201),
  ('ptype -> INT','ptype',1,'p_primitive_type','parser.py',205),
  ('ptype -> FLOAT','ptype',1,'p_primitive_type','parser.py',206),
  ('ptype -> STRING','ptype',1,'p_primitive_type','parser.py',207),
  ('ptype -> TRUE','ptype',1,'p_primitive_type','parser.py',208),
  ('ptype -> FALSE','ptype',1,'p_primitive_type','parser.py',209),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','parser.py',226),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','parser.py',227),
  ('expression -> expression MULTIPLY expression','expression',3,'p_expression_binop','parser.py',228),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','parser.py',229),
  ('expression -> expression EQUALS expression','expression',3,'p_expression_binop','parser.py',230),
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
  ('expression -> MINUS expression','expression',2,'p_expression_unary','parser.py',251),
  ('expression -> PLUS expression','expression',2,'p_expression_unary','parser.py',252),
  ('expression -> NOT expression','expression',2,'p_expression_unary','parser.py',253),
  ('control_flow -> conditional','control_flow',1,'p_control_flow','parser.py',261),
  ('control_flow -> loop','control_flow',1,'p_control_flow','parser.py',262),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','parser.py',266),
  ('expression -> INT','expression',1,'p_expression_number','parser.py',270),
  ('expression -> FLOAT','expression',1,'p_expression_number','parser.py',271),
  ('expression -> STRING','expression',1,'p_expression_string','parser.py',278),
  ('expression -> TRUE','expression',1,'p_expression_boolean','parser.py',282),
  ('expression -> FALSE','expression',1,'p_expression_boolean','parser.py',283),
  ('expression -> IDENTIFIER','expression',1,'p_expression_identifier','parser.py',288),
  ('expression -> function_call','expression',1,'p_expression_function_call','parser.py',292),
  ('expression -> expression TO_STREAM','expression',2,'p_expression_to_stream','parser.py',300),
  ('expression -> lambda_function','expression',1,'p_expression_lambda','parser.py',305),
  ('conditional -> IF LPAREN expression RPAREN block_statement ELSE block_statement','conditional',7,'p_conditional','parser.py',311),
  ('conditional -> IF LPAREN expression RPAREN block_statement','conditional',5,'p_conditional','parser.py',312),
  ('loop -> FOR LPAREN declaration SEMICOLON expression SEMICOLON expression RPAREN block_statement','loop',9,'p_loop','parser.py',321),
  ('loop -> WHILE LPAREN expression RPAREN block_statement','loop',5,'p_loop','parser.py',322),
  ('assignment -> IDENTIFIER ASSIGN expression','assignment',3,'p_assignment','parser.py',329),
  ('empty -> <empty>','empty',0,'p_empty','parser.py',336),
]
