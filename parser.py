from lexer import Lexer
from Token import Token,TokenType
from typing import Callable
from enum import Enum, auto

from AST import Statement, Expression , Program
from AST import ExpressionStatement, LetStatement, FunctionStatement,  ReturnStatement, BlockStatement, AssignStatement , IfStatement
from AST import InfixExpression, CallExpression
from AST import IntegerLiteral, FloatLiteral, IdentifierLiteral, BooleanLiteral
from AST import FunctionParamter
#Prodecure types
class PrecedenceType(Enum):
    P_LOWEST = 0
    P_EQULALS = auto()
    P_LESSGREATER = auto()
    P_SUM = auto()
    P_PRODUCT = auto()
    P_PREFIX = auto()
    P_EXPONENT = auto()
    P_CALL = auto()
    P_INDEX = auto()


#Precedence mapping
PRECEDENCES: dict[TokenType, PrecedenceType] = {
    TokenType.PLUS: PrecedenceType.P_SUM,
    TokenType.MINUS: PrecedenceType.P_SUM,
    TokenType.SLASH: PrecedenceType.P_PRODUCT,
    TokenType.ASTERISK: PrecedenceType.P_PRODUCT,
    TokenType.MODULUS: PrecedenceType.P_PRODUCT,
    TokenType.POW: PrecedenceType.P_EXPONENT,
    TokenType.EQ_EQ : PrecedenceType.P_EQULALS,
    TokenType.NOT_EQ : PrecedenceType.P_EQULALS,
    TokenType.LT : PrecedenceType.P_LESSGREATER,
    TokenType.GT : PrecedenceType.P_LESSGREATER,
    TokenType.LT_EQ : PrecedenceType.P_LESSGREATER,
    TokenType.GT_EQ : PrecedenceType.P_LESSGREATER,
    TokenType.LPAREN : PrecedenceType.P_CALL,
}

class Parser:
    def __init__(self, lexer: Lexer) -> None:
        self.lexer: Lexer = lexer
        self.errors: list[str] = []
        self.cur_token: Token = None
        self.peek_token: Token = None

        self.prefix_parse_fns: dict[TokenType, Callable] = {
            TokenType.IDENT: self.__parse_identifier,
            TokenType.INT: self.__parse_int_literal,
            TokenType.FLOAT: self.__parse_float_literal,
            TokenType.LPAREN: self.__parse_grouped_expression,
            TokenType.IF: self.__parse_if_statement,
            TokenType.TRUE: self.__parse_boolean,
            TokenType.FALSE: self.__parse_boolean,
        }
        self.infix_parse_fns: dict[TokenType, Callable] = {
            TokenType.PLUS: self.__parse_infix_expression,
            TokenType.MINUS: self.__parse_infix_expression,
            TokenType.SLASH: self.__parse_infix_expression,
            TokenType.ASTERISK: self.__parse_infix_expression,
            TokenType.POW: self.__parse_infix_expression,
            TokenType.MODULUS: self.__parse_infix_expression,
            TokenType.EQ_EQ : self.__parse_infix_expression,
            TokenType.NOT_EQ : self.__parse_infix_expression,
            TokenType.LT : self.__parse_infix_expression,
            TokenType.GT : self.__parse_infix_expression,
            TokenType.LT_EQ : self.__parse_infix_expression,
            TokenType.GT_EQ : self.__parse_infix_expression,
            TokenType.LPAREN : self.__parse_call_expression
        }

        self.__next_token()
        self.__next_token()

#region Parser Helpers

    def __next_token(self) -> None:
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()
        
    def __current_token_is(self, tt: TokenType)->bool:
        return self.cur_token.type == tt

    def __peek_token_is(self, tt: TokenType) -> bool:
        return self.peek_token.type == tt

    def __expect_peek(self, tt: TokenType) -> bool:
        if self.__peek_token_is(tt):
            self.__next_token()
            return True
        else:
            self.__peek_error(tt)
            return False
        
    def __peek_error(self, tt: TokenType) -> None:
        self.errors.append(f"Expected next token to be {tt}, got {self.peek_token.type} instead")


    def __no_prefix_parse_fn_error(self, tt: TokenType) -> None:
        self.errors.append(f"No prefix parse function for {tt} found")

#endregion

    def parse_program(self):
        program: Program = Program()

        while self.cur_token.type != TokenType.EOF:
            stmt: Statement = self.__parse_statement()
            if stmt:
                program.statements.append(stmt)

            self.__next_token()

        return program

    

    #region statments methods
    def __parse_statement(self) ->Statement:
        if self.cur_token.type == TokenType.IDENT and self.__peek_token_is(TokenType.EQ):
            return self.__parse_assignment_statement()
        match self.cur_token.type:
            case TokenType.LET:
                return self.__parse_let_statement()
            case TokenType.FN:
                return self.__parse_function_statement()
            case TokenType.RETURN:
                return self.__parse_return_statement()
            case _:
                return self.__parse_expression_statement()
    def __parse_expression_statement(self) -> ExpressionStatement:
        expr = self.__parse_expression(PrecedenceType.P_LOWEST)

        if self.__peek_token_is(TokenType.SEMICOLON):
            self.__next_token()

        stmt: ExpressionStatement = ExpressionStatement(expression = expr)

        return stmt
    
    def __parse_function_statement(self) -> FunctionStatement:
        stmt: FunctionStatement = FunctionStatement()
        
        if not self.__expect_peek(TokenType.IDENT):
            return None
        
        stmt.name =IdentifierLiteral(value = self.cur_token.literal)
        
        if not self.__expect_peek(TokenType.LPAREN):
            return None
        
        stmt.parameters = self.__parse_function_parameters()
        
        if not self.__expect_peek(TokenType.ARROW):
            return None
        
        if not self.__expect_peek(TokenType.TYPE):
            return None
        
        stmt.return_type = self.cur_token.literal
        
        if not self.__expect_peek(TokenType.LBRACE):
            return None
        
        stmt.body = self.__parse_block_statement()
        
        return stmt
    
    def __parse_function_parameters(self) -> list[FunctionParamter]:
        params: list[FunctionParamter] =[]

        if self.__peek_token_is(TokenType.RPAREN):
            self.__next_token()
            return params
        
        self.__next_token()

        first_param: FunctionParamter = FunctionParamter(name = self.cur_token.literal)
        params.append(first_param)
        if not self.__expect_peek(TokenType.COLON):
            return None
        
        self.__next_token()

        first_param.value_type = self.cur_token.literal

        while self.__peek_token_is(TokenType.COMMA):
            self.__next_token()
            self.__next_token()

            param: FunctionParamter = FunctionParamter(name = self.cur_token.literal)

            if not self.__expect_peek(TokenType.COLON):
                return None
            
            self.__next_token()

            param.value_type = self.cur_token.literal
            params.append(param)

        if not self.__expect_peek(TokenType.RPAREN):
            return None
        
        return params
    
    def __parse_return_statement(self) -> ReturnStatement:
        stmt: ReturnStatement = ReturnStatement()
        
        self.__next_token()
        
        stmt.return_value = self.__parse_expression(PrecedenceType.P_LOWEST)
        
        if self.__peek_token_is(TokenType.SEMICOLON):
            self.__next_token()
        
        return stmt
    
    def __parse_block_statement(self) -> BlockStatement:
        block_stmt: BlockStatement = BlockStatement()
        
        self.__next_token()
    
        while not self.__current_token_is(TokenType.RBRACE) and not self.__current_token_is(TokenType.EOF):
            stmt: Statement = self.__parse_statement()
            if stmt is not None:
                block_stmt.statements.append(stmt)
                
            self.__next_token()
            
        return block_stmt

    # def __parse_block_statement(self) -> BlockStatement:
    #     block_stmt = BlockStatement()

    #     self.__next_token()

    #     while not self.__current_token_is(TokenType.RBRACE) and not self.__current_token_is(TokenType.EOF):
    #         stmt = self.__parse_statement()

    #         if stmt is not None:
    #             block_stmt.statements.append(stmt)

    #         # REMOVE this next_token
    #         # self.__next_token()

    #     return block_stmt
    
    # def __parse_assignment_statement(self) -> AssignStatement:
    #     stmt: AssignStatement = AssignStatement()

    #     stmt.ident = IdentifierLiteral(value = self.cur_token.literal)

    #     self.__next_token()
    #     self.__next_token()

    #     stmt.right_value = self.__parse_expression(PrecedenceType.P_LOWEST)
    #     self.__next_token()

    #     return stmt 
    def __parse_assignment_statement(self) -> AssignStatement:
        stmt = AssignStatement()

        stmt.ident = IdentifierLiteral(value=self.cur_token.literal)

        if not self.__expect_peek(TokenType.EQ):
            return None

        self.__next_token()

        stmt.right_value = self.__parse_expression(PrecedenceType.P_LOWEST)

        if self.__peek_token_is(TokenType.SEMICOLON):
            self.__next_token()

        return stmt
    
    def __parse_if_statement(self) ->IfStatement:
        condition: Expression = None
        consequence: BlockStatement = None
        alternative: BlockStatement = None

        self.__next_token()

        condition = self.__parse_expression(PrecedenceType.P_LOWEST)
        if not self.__expect_peek(TokenType.LBRACE):
            return None
        
        consequence = self.__parse_block_statement()

        if self.__peek_token_is(TokenType.ELSE):
            self.__next_token()

            if not self.__expect_peek(TokenType.LBRACE):
                return None
            
            alternative = self.__parse_block_statement()

        return IfStatement(condition , consequence , alternative)


    
#end region

#expression methods region

    def __parse_expression(self , precedence :PrecedenceType) -> Expression:
        prefix_fn: Callable | None = self.prefix_parse_fns.get(self.cur_token.type)
        if prefix_fn is None:
            self.__no_prefix_parse_fn_error(self.cur_token.type)
            return None
        
        left_expr:Expression = prefix_fn()
        while not self.__peek_token_is(TokenType.SEMICOLON) and precedence.value < self.__peek_precedence().value:
            infix_fn:Callable | None = self.infix_parse_fns.get(self.peek_token.type)
            if infix_fn is None:
                return left_expr
            
            self.__next_token()

            left_expr = infix_fn(left_expr)

        return left_expr

    def __parse_infix_expression(self , left_node: Expression) -> Expression:
        infix_epxr: InfixExpression = InfixExpression(left_node = left_node, operator = self.cur_token.literal)

        precedence = self.__current_precedence()

        self.__next_token()

        infix_epxr.right = self.__parse_expression(precedence)

        return infix_epxr
    
    def __parse_let_statement (self) ->LetStatement:
        stmt: LetStatement = LetStatement()
        
        if not self.__expect_peek(TokenType.IDENT):
            return None
        
        stmt.name = IdentifierLiteral(value=self.cur_token.literal)
        if not self.__expect_peek(TokenType.COLON):
            return None
        
        if not self.__expect_peek(TokenType.TYPE):
            return None
        
        stmt.value_type = self.cur_token.literal
        
        if not self.__expect_peek(TokenType.EQ):
            return None
        
        self.__next_token()
        
        stmt.value = self.__parse_expression(PrecedenceType.P_LOWEST)
        
        # while not self.__current_token_is(TokenType.SEMICOLON)and not self.__current_token_is(TokenType.EOF):
        #     self.__next_token()
        
        if self.__peek_token_is(TokenType.SEMICOLON):
            self.__next_token()
            
        return stmt 
    
    # def __parse_let_statement(self) -> LetStatement:
    #     stmt: LetStatement = LetStatement()

    #     if not self.__expect_peek(TokenType.IDENT):
    #         return None

    #     stmt.name = IdentifierLiteral(value=self.cur_token.literal)

    #     if not self.__expect_peek(TokenType.EQ):
    #         return None

    #     self.__next_token()

    #     stmt.value = self.__parse_expression(PrecedenceType.P_LOWEST)

    #     if self.__peek_token_is(TokenType.SEMICOLON):
    #         self.__next_token()

    #     return stmt

    def __parse_grouped_expression (self) ->Expression:
        self.__next_token()

        expr: Expression = self.__parse_expression(PrecedenceType.P_LOWEST)

        if not self.__expect_peek(TokenType.RPAREN):
            return None
        
        return expr
    
    def __parse_call_expression(self , function:Expression) ->CallExpression:
        expr: CallExpression = CallExpression(function=function)
        expr.arguments = self.__parse_expression_list(TokenType.RPAREN)
        
        return expr
    
    def __parse_expression_list(self , end:TokenType) -> list[Expression]:
        e_list: list[Expression] = []

        if self.__peek_token_is(end):
            self.__next_token()
            return e_list
        
        self.__next_token()
        
        e_list.append(self.__parse_expression(PrecedenceType.P_LOWEST))

        while self.__peek_token_is(TokenType.COMMA):
            self.__next_token()
            self.__next_token()

            e_list.append(self.__parse_expression(PrecedenceType.P_LOWEST))
        
        if not self.__expect_peek(end):
            return None
        
        return e_list


    #region of Prefix methods
    
    def __parse_identifier(self) -> IdentifierLiteral:
        return IdentifierLiteral(value = self.cur_token.literal)

    def __parse_int_literal(self) -> Expression:
        """Parses and Integerliteral node from the current token"""
        
        int_lit: IntegerLiteral = IntegerLiteral()
        
        try:
            int_lit.value = int(self.cur_token.literal)
        except:
            self.errors.append(f"Could not parse `{self.cur_token.literal} as an integer`")
            return None
        
        return int_lit


    def __parse_float_literal(self) -> Expression:
        """Parses and FloatLieral node from the current token"""
        
        float_lit: FloatLiteral = FloatLiteral()
        
        try:
            float_lit.value = float(self.cur_token.literal)
        except:
            self.errors.append(f"Could not parse `{self.cur_token.literal} as a float`")
            return None
        
        return float_lit
    
    def __parse_boolean(self)-> BooleanLiteral:
        return BooleanLiteral(value = self.__current_token_is(TokenType.TRUE))
    
    def __peek_precedence(self) -> PrecedenceType:
        return PRECEDENCES.get(self.peek_token.type, PrecedenceType.P_LOWEST)

    def __current_precedence(self) -> PrecedenceType:
        return PRECEDENCES.get(self.cur_token.type, PrecedenceType.P_LOWEST)
