from enum import Enum
from typing import Any

class TokenType(Enum):
    EOF = "EOF"
    ILLEGAL = "ILLEGAL"


    #Data types
    IDENT = "IDENT"
    INT= "INT"
    FLOAT = "FLOAT"

    #Arithematic operators
    PLUS = "PLUS"
    MINUS = "MINUS"
    MULTIPLY = "MULTIPLY"
    DIVIDE = "DIVIDE"
    ASTERISK = "ASTERISK"
    SLASH = "SLASH"
    POW = "POW"
    MODULUS = "MODULUS"
    
    #Assignment Symbols
    EQ = "EQ"

    #symbols
    COLON = "COLON"
    SEMICOLON = "SEMICOLON"
    ARROW = "ARROW"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    LBRACE = "LBRACE"
    RBRACE = "RBRACE"
    
    #keywords
    LET = "LET"
    RETURN = "RETURN"
    FN = "FN"
    
    #typing
    TYPE = "TYPE"
    

class Token:
    def __init__(self, type: TokenType, literal: Any, line_no: int , position: int ) -> None:
        self.type = type
        self.literal = literal
        self.line_no = line_no
        self.position = position

    def __str__(self) ->str:
        return f"Token(type={self.type}, literal={self.literal} , line_no={self.line_no} , position={self.position})"
    
    def __repr__(self) -> str:
        return str(self)
    
KEYWORDS: dict[str, TokenType] ={
    "let": TokenType.LET,
    "fn": TokenType.FN,
    "return":TokenType.RETURN
}

ALT_KEYWORDS: dict[str, TokenType] ={
    "maanlo": TokenType.LET,
    "barabar": TokenType.EQ,
    "ant":TokenType.SEMICOLON,
    "kaarya": TokenType.FN,
    "wapis":TokenType.RETURN,
    "teer":TokenType.ARROW,
    "ank":TokenType.TYPE
    
}

TYPE_KEYWORDS: list[str] = ["int", "float"]

def lookup_ident(ident: str) ->TokenType:
    tt:TokenType | None = KEYWORDS.get(ident)
    if tt is not None:
        return tt
    
    tt:TokenType | None = ALT_KEYWORDS.get(ident)
    if tt is not None:
        return tt
    
    if ident in TYPE_KEYWORDS:
        return TokenType.TYPE
    
    
    return TokenType.IDENT
    