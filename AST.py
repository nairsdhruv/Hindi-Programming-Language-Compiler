from abc import ABC , abstractmethod
from enum import Enum

class NodeType(Enum):
    Program = "Program"

    ExpressionStatement = "ExpressionStatement"
    LetStatement = "LetStatement"
    FunctionStatement = "FunctionStatement"
    BlockStatement = "BlockStatement"
    ReturnStatement = "ReturnStatement"

    InfixExpression = "InfixExpression"

    IntegerLiteral = "IntegerLiteral"

    FloatLiteral = "FloatLiteral"
    IdentifierLiteral = "IdentifierLiteral"


class Node(ABC):
    @abstractmethod
    def type(self) -> NodeType:
        pass

    @abstractmethod
    def json(self) -> dict:
        pass

class Statement(Node):
    pass

class Expression(Node):
    pass

class Program(Node):
    def __init__(self) -> None:
        self.statements : list[Statement] = []

    def type(self) -> NodeType:
        return NodeType.Program

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "statements": [{stat.type().value: stat.json()} for stat in self.statements]
        }
    
#region Expression Statements

class ExpressionStatement(Statement):
    def __init__(self, expression: Expression = None) -> None:
        self.expression: Expression = expression

    def type(self) -> NodeType:
        return NodeType.ExpressionStatement

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "expression": self.expression.json() if self.expression else None
        }
#endregion

#region Expressions

class LetStatement(Statement):
    def __init__(self, name:Expression= None , value:Expression = None , value_type:str = None) -> None:
        self.name = name
        self.value = value
        self.value_type = value_type
        
    def type(self)->NodeType:
        return NodeType.LetStatement
    
    def json(self) -> dict:
        return{
            "type": self.type().value,
            "name":self.name.json(),
            "value": self.value.json(),
            "value_type": self.value_type
        }

class BlockStatement(Statement):
    def __init__(self, statements: list[Statement]= None) ->None:
        self.statements = statements if statements is not None else []
    
    def type(self) -> NodeType:
        return NodeType.BlockStatement
    
    def json(self) -> dict:return{
        "type": self.type().value,
        "statements": [stmt.json() for stmt in self.statements]
    }
    
class ReturnStatement(Statement):
    def __init__(self, return_value: Expression= None) ->None:
        self.return_value = return_value
    
    def type(self) -> NodeType:
        return NodeType.ReturnStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "return_value": self.return_value.json()
        }
        
class FunctionStatement(Statement):
    def __init__(self, parameters:list = [], body: BlockStatement= None , name = None, return_type: str = None)-> None:
        self.parameters = parameters
        self.body = body
        self.name = name
        self.return_type = return_type
        
    def type(self) -> NodeType:
        return NodeType.FunctionStatement
    
    def json(self) -> dict:
        return {
            "type": self.type().value,
            "name":self.name.json(),
            "return_type": self.return_type,
            "parameters": [p.json() for p in self.parameters],
            "body": self.body.json()      
        }

class InfixExpression(Expression):
    def __init__(self, left_node: Expression, operator: str, right_node: Expression = None) -> None:
        self.left: Expression = left_node
        self.operator: str = operator
        self.right: Expression = right_node

    def type(self) -> NodeType:
        return NodeType.InfixExpression

    def json(self) -> dict:
        return {
            "type": self.type().value,
            "left": self.left.json() if self.left else None,
            "operator": self.operator,
            "right": self.right.json() if self.right else None
        }
    
class IntegerLiteral(Expression):
    def __init__(self, value:int = None) -> None:
        self.value: int = value

    def type(self) -> NodeType:
        return NodeType.IntegerLiteral
    
    def json(self):
        return {
            "type": self.type().value,
            "value": self.value
        }
    
    
class FloatLiteral(Expression):
    def __init__(self, value:float = None) -> None:
        self.value: float = value

    def type(self) -> NodeType:
        return NodeType.FloatLiteral
    
    def json(self):
        return {
            "type": self.type().value,
            "value": self.value
        }
        
class IdentifierLiteral(Expression):
    def __init__(self, value:str = None) -> None:
        self.value: str = value

    def type(self) -> NodeType:
        return NodeType.IdentifierLiteral
    
    def json(self):
        return {
            "type": self.type().value,
            "value": self.value
        }