import unicodedata

from Token import Token, lookup_ident
from Token import TokenType
from typing import Any


class Lexer:
    def __init__(self, source: str) -> None:
        self.source = source 

        self.position = -1
        self.read_position = 0
        self.line_no = 1

        self.current_char : str | None= None

        self.__read_char()

    def __read_char(self) -> None:
        if self.read_position >= len(self.source):
            self.current_char = None
        else:
            self.current_char = self.source[self.read_position]

        self.position = self.read_position
        self.read_position += 1
    
    def __peek_char(self)-> str|None:
        if self.read_position >= len(self.source):
            return None
        return self.source[self.read_position]

    def __skip_whitespace(self) -> None:
        while self.current_char in [' ', '\t', '\r', '\n']:
            if self.current_char == "\n":
                self.line_no += 1
            self.__read_char()

    def __new_token(self, tt: TokenType, literal: Any) -> Token:
        return Token(type = tt, literal = literal, line_no = self.line_no, position = self.position)

    def __is_digit(self, char: str) -> bool:
        return char.isdigit()
    
    def __is_letter(self, ch:str)->bool:
        # return 'a'<=ch and ch <= 'z' or 'A' <= ch and ch <='Z' or ch =='_'
         category = unicodedata.category(ch)
         return (
                category.startswith('L')   # Letters
                or category.startswith('M')  # Marks (important for Hindi matras!)
                or ch == '_'
            )

    def __read_number(self) -> Token:
        start_pos: int = self.position
        dot_count: int = 0

        output: str = ''    
        while self.current_char is not None and (self.current_char.isdigit() or self.current_char == '.'):
            if self.current_char == '.':
                dot_count += 1
                if dot_count > 1:
                    print(f"Error: Invalid number format at line {self.line_no}, position {self.position}")
                    return self.__new_token(TokenType.ILLEGAL, self.source[start_pos:self.position])
            output += self.current_char
            self.__read_char()

        if dot_count == 0:
            return self.__new_token(TokenType.INT, int(output))
        else:
            return self.__new_token(TokenType.FLOAT, float(output))
    
    def __read_identifier(self) ->str:
        position = self.position
        while self.current_char is not None and(self.__is_letter(self.current_char) or self.current_char.isalnum()):
            self.__read_char()
            
        return self.source[position:self.position]

    def next_token(self) -> Token:
        tok: Token = None
        self.__skip_whitespace()

        match self.current_char:
            case '+':
                tok = self.__new_token(TokenType.PLUS, self.current_char)
            case '-':
                if self.__peek_char() == '>':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.ARROW, ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.MINUS, self.current_char)
            case '*':
                tok = self.__new_token(TokenType.ASTERISK, self.current_char)
            case '/':
                tok = self.__new_token(TokenType.SLASH, self.current_char)
            case '%':
                tok = self.__new_token(TokenType.MODULUS, self.current_char)
            case '<':
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.LT_EQ , ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.LT ,  self.current_char)
            case '>':
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.GT_EQ , ch+ self.current_char)
                else:
                    tok = self.__new_token(TokenType.GT ,  self.current_char)
            case '=':
                if self.__peek_char() == '=':
                    ch = self.current_char
                    self.__read_char()
                    tok = self.__new_token(TokenType.EQ_EQ ,ch + self.current_char)
                else:
                    tok = self.__new_token(TokenType.EQ , self.current_char)
           
            # case '=':
            #     tok = self.__new_token(TokenType.EQ, self.current_char)
            case ':':
                tok = self.__new_token(TokenType.COLON, self.current_char)
            case ',':
                tok = self.__new_token(TokenType.COMMA, self.current_char)
            case ';':
                tok = self.__new_token(TokenType.SEMICOLON, self.current_char)
            case '"':
                tok = self.__new_token(TokenType.STRING, self.__read_string())
            case '(':
                tok = self.__new_token(TokenType.LPAREN, self.current_char)
            case ')':
                tok = self.__new_token(TokenType.RPAREN, self.current_char)
            case '{':
                tok = self.__new_token(TokenType.LBRACE, self.current_char)
            case '}':
                tok = self.__new_token(TokenType.RBRACE, self.current_char)
            case None:
                tok = self.__new_token(TokenType.EOF, '')
            case _:
                if self.__is_letter(self.current_char):
                    literal: str = self.__read_identifier()
                    tt:TokenType = lookup_ident(literal)
                    tok = self.__new_token(tt= tt, literal=literal)
                    return tok
                elif self.current_char is not None and self.__is_digit(self.current_char):
                    return self.__read_number()
                else:
                    tok = Token(
                        TokenType.ILLEGAL,
                        self.current_char,
                        self.line_no,
                        self.position
                    )
        self.__read_char()
        return tok
    
    # def __read_string(self) ->str:
    #     position: int = self.position +1
    #     while True:
    #         self.__read_char()
    #         if self.current_char == '"' or self.current_char is None:
    #             break

    #         string = self.source[position:self.position]

    #     return string

    def __read_string(self) -> str:
        position = self.position + 1

        while True:
            self.__read_char()
            if self.current_char == '"' or self.current_char is None:
                break

        return self.source[position:self.position]