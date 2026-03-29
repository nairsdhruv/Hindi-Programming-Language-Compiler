from deep_translator import GoogleTranslator

# Your Hindi DSL code
hindi_code = """
कार्य मुख्य() -> अंक {
    मान लो a : अंक = 0 अंत
    जब a < 10 {
        लिखो("a = %d \n", a) अंत
        a बराबर a + 1 अंत
    }
}
"""

# 1. Keyword mapping from Hindi → English DSL
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
english_dsl = hindi_code
for hi, en in keyword_map.items():
    english_dsl = english_dsl.replace(hi, en)

print("=== English DSL ===")
print(english_dsl)