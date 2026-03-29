from lexer import Lexer
from parser import Parser
from AST import Program
import json
from Compiler import Compiler
from ai_codegen import generate_hindi_code
from deep_translator import GoogleTranslator

import time


from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int , c_float

LEXER_DEBUG :bool =True
PARSER_DEBUG : bool = True
COMPILER_DEBUG: bool = True
RUN_CODE:bool = True 

if __name__ == "__main__":
    # with open ("tests/parser.hin", "r") as f:
    #     code: str = f.read()

    mode = input("Choose mode (1=file, 2=AI): ")

    if mode == "1":
        with open("tests/original.hin", "r", encoding="utf-8") as f:
            code = f.read()

        keyword_map = {
            "कार्य": "kaarya",
            "मुख्य": "mukhya",
            "अंक": "ank",
            "मान लो": "maanlo",
            "जब": "jab",
            "लिखो": "likho",
            "बराबर": "barabar",
            "अंत": "ant"
        }

        # 2. Replace Hindi keywords with English
        english_dsl = code
        for hi, en in keyword_map.items():
            english_dsl = english_dsl.replace(hi, en)

        print("=== English DSL ===")
        print(english_dsl)

        code = english_dsl

    elif mode == "2":
        with open("input.txt", "r", encoding="utf-8") as f:
            text = f.read()

        # Translate text to English
        translated_text = GoogleTranslator(source='auto', target='en').translate(text)

        # Save translated text
        with open("eng_input.txt", "w", encoding="utf-8") as f:
            f.write(translated_text)


        with open("eng_input.txt", "r", encoding="utf-8") as f:
            user_prompt = f.read()

        #print(user_prompt)

        code = generate_hindi_code(user_prompt)

        print("\n=== GENERATED CODE ===\n")
        print(code)


        with open("tests/generated.hin", "w", encoding="utf-8") as f:
            f.write(code)

    else:
        print("Invalid choice")
        exit(1)
    
    if LEXER_DEBUG:
        print("===LEXER DEBUG===")
        debug_lex: Lexer = Lexer(source =code)
        while debug_lex.current_char is not None:
            print(debug_lex.next_token())
            
            
    l: Lexer = Lexer(source = code )
    p: Parser = Parser(lexer = l)
    program:Program = p.parse_program()
    if len(p.errors) > 0:
        for err in p.errors:
            print(err)
        exit(1)
    
    if PARSER_DEBUG:
        print("===PARSER DEBUG====")
        
        with open("debug/ast.json", "w") as f:
            json.dump(program.json(), f, indent =4 )
            
        print("Wrote AST to debug /ast.json successfully")
        
        
    c: Compiler = Compiler()
    c.compile(node = program)
    
    module:ir.Module = c.module
    module.triple = llvm.get_default_triple()
    
    if COMPILER_DEBUG:
        with open ("debug/ir.ll", "w") as f:
            f.write(str(module))
    
    if RUN_CODE:
        # llvm.initialize()
        llvm.initialize_native_target()
        llvm.initialize_native_asmprinter()
        
        try:
            llvm_ir_parsed = llvm.parse_assembly(str(module))
            llvm_ir_parsed.verify()
        except Exception as e:
            print(e)
            raise
        
        target_machine = llvm.Target.from_default_triple().create_target_machine()
        engine = llvm.create_mcjit_compiler(llvm_ir_parsed, target_machine)
        engine.finalize_object()
        
        entry = engine.get_function_address('mukhya')
        cfunc = CFUNCTYPE(c_int)(entry)
        
        st = time.time()
        
        result = cfunc()
        
        et = time.time()
        
        print(f"\n Program Returned: {result} \n === Executed in {round((et-st)*1000, 6)} ms. ===")







