from llvmlite import ir 
from AST import Node, NodeType, Program,Expression,Statement
from AST import ExpressionStatement, LetStatement, BlockStatement, FunctionStatement , ReturnStatement
from AST import InfixExpression
from AST import IntegerLiteral, FloatLiteral, IdentifierLiteral
from Environment import Environment

class Compiler:
    def __init__ (self) -> None:
        self.type_map: dict[str, ir.Type] = {
            'int': ir.IntType(32),
            'float': ir.FloatType(),
            'ank': ir.IntType(32),      
            'dashamlav': ir.FloatType() 
        }
        
        self.module : ir.Module = ir.Module('mukhya')
        
        self.builder: ir.IRBuilder = ir.IRBuilder()
        
        self.env:Environment = Environment()
        
    def compile(self, node:Node) -> None:
        match node.type():
            case NodeType.Program:
                return  self .__visit_program(node)
                    
            #Statements
            case NodeType.ExpressionStatement:
                return  self.__visit_expression_statement(node)
            case NodeType.LetStatement:
                self.__visit_let_statement(node)
            case NodeType.FunctionStatement:
                self.__visit_function_statement(node)
            case NodeType.BlockStatement:
                self.__visit_block_statement(node)
            case NodeType.ReturnStatement:
                self.__visit_return_statement(node)
                
            #Expressions
            case NodeType.InfixExpression:
                return self.__visit_infix_expression(node)
            
            case NodeType.IntegerLiteral | NodeType.FloatLiteral:
                return self.__resolve_value(node)   
                    
#region visit methods
    def __visit_program(self,node:Program) ->None:
        # func_name: str = "main"
        # param_types: list [ir.Type] = {}
        # return_type :ir.Type = self.type_map["int"]
        
        
        # fnty = ir.FunctionType(return_type, param_types)
        # func = ir.Function(self.module , fnty , name= func_name)
        
        # block = func.append_basic_block(f"{func_name}_entry")
        
        
        # self.builder = ir.IRBuilder(block )
        
        # last_value = None
        
        for stmt in node.statements:
            last_value = self.compile(stmt)
            
        # if last_value is not None:
        #     value, _ = last_value
        #     self.builder.ret(value)
        # else:
        #     self.builder.ret(ir.Constant(self.type_map["int"], 0))
            
        # return_value: ir.Constant = ir.Constant(self.type_map["int"], 69)
        # self.builder.ret(return_value)
        
        
    def __visit_expression_statement(self , node:ExpressionStatement)->None:
        return self.compile(node.expression)
        
    def __visit_let_statement(self, node: LetStatement) -> None:
        name:str = node.name.value
        value:Expression = node.value
        value_type:str = node.value_type #TODO
        
        value, Type = self.__resolve_value(node= value)
        
        if self.env.lookup(name) is None:
            ptr = self.builder.alloca(Type)
            
            self.builder.store(value, ptr)
            
            self.env.define(name, ptr , Type)
        else:
            ptr , _= self.env.lookup(name)
            self.builder.store(value, ptr)
            
    def __visit_block_statement(self, node: BlockStatement) -> None:
        for stmt in node.statements:
            self.compile(stmt)
            
    
    def __visit_return_statement(self , node:ReturnStatement)->None:
        value: Expression = node.return_value
        value, Type = self.__resolve_value(value)
        
        self.builder.ret(value)
        
    def __visit_function_statement(self, node:FunctionStatement)->None:
        name: str = node.name.value
        body: BlockStatement = node.body
        params: list[IdentifierLiteral] = node.parameters
        
        param_names: list[str] = [p.value for p in params]
        
        param_types: list[ir.Type] = [] #TODO
        
        return_type:ir.Type = self.type_map[node.return_type]
        
        fnty: ir.FunctionType = ir.FunctionType(return_type, param_types)
        func: ir.Function = ir.Function(self.module, fnty , name=name)
        
        block: ir.Block= func.append_basic_block(f"{name}_entry")
        previous_builder = self.builder
        
        self.builder = ir.IRBuilder(block)
        previous_env = self.env
        self.env = Environment(parent= self.env)
        self.env.define(name , func , return_type)
        
        self.compile(body)
        self.env = previous_env
        self.env.define(name , func , return_type)
        self.builder = previous_builder
        
    def __visit_infix_expression(self , node:InfixExpression)->None:
        operator:str = node.operator
        left_value, left_type= self.__resolve_value(node.left)
        right_value, right_type= self.__resolve_value(node.right)
        
        value = None
        Type = None 
        if isinstance (right_type, ir.IntType) and isinstance(left_type, ir.IntType):
            Type = self.type_map['int']
            match operator:
                case '+':
                    value = self.builder.add(left_value, right_value)
                case '-':
                    value = self.builder.sub(left_value, right_value)
                case '*':
                    value = self.builder.mul(left_value, right_value)
                case '/':
                    value = self.builder.sdiv(left_value, right_value)
                case '%':
                    value = self.builder.srem(left_value, right_value)
                case '^':
                    #TODO
                    pass
        elif isinstance(right_type, ir.FloatType) and isinstance(left_type, ir.FloatType):
            Type = ir.FloatType()
            match operator:
                case '+':
                    value = self.builder.fadd(left_value, right_value)
                case '-':
                    value = self.builder.fsub(left_value, right_value)
                case '*':
                    value = self.builder.fmul(left_value, right_value)
                case '/':
                    value = self.builder.fdiv(left_value, right_value)
                case '%':
                    value = self.builder.frem(left_value, right_value)
                case '^':
                    #TODO
                    pass
            
                    
                    
        return value , Type
        
    #endrgion
    
    
    #Helper methods
    def __resolve_value(self, node:Expression, value_type: str=None)->tuple[ir.Value, ir.Type]:
        match node.type():
            case NodeType.IntegerLiteral:
                node:IntegerLiteral= node
                value , Type = node.value , self.type_map['int' if value_type is None else value_type]
                return ir.Constant(Type, value), Type
            case NodeType.FloatLiteral:
                node:FloatLiteral= node
                value , Type = node.value , self.type_map['float' if value_type is None else value_type]
                return ir.Constant(Type, value), Type
            case NodeType.IdentifierLiteral:
                node:IdentifierLiteral = node
                ptr , Type = self.env.lookup(node.value)
                return self.builder.load(ptr), Type
            case NodeType.InfixExpression:
                return self.__visit_infix_expression(node)
        #end region