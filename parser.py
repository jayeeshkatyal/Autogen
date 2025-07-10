from autogen import AssistantAgent, UserProxyAgent
import ast
import symtable
import json
from prettytable import PrettyTable

# STEP 1: Load raw code
with open("input_code.py", "r") as file:
    raw_code = file.read()
print("\n Raw code loaded from input_code.py")

# STEP 2: Generate AST (Abstract Syntax Tree)
tree = ast.parse(raw_code)
ast_json = ast.dump(tree, indent=4)
print("\n AST Generated:")
print(ast_json)

# STEP 3: Generate Symbol Table
symbol_table = symtable.symtable(raw_code, "<string>", "exec")

# Display Symbol Table nicely
table = PrettyTable(["Symbol Name", "Is Global", "Is Parameter"])
for symbol in symbol_table.get_symbols():
    table.add_row([
        symbol.get_name(),
        symbol.is_global(),
        symbol.is_parameter()
    ])
print("\n Symbol Table:")
print(table)

# STEP 4: Save AST and Symbol Table to JSON file
output = {
    "AST": ast_json,
    "SymbolTable": [
        {
            "name": symbol.get_name(),
            "is_global": symbol.is_global(),
            "is_parameter": symbol.is_parameter()
        }
        for symbol in symbol_table.get_symbols()
    ]
}
with open("intermediate_representation.json", "w") as f:
    json.dump(output, f, indent=4)
print("\n IR saved to intermediate_representation.json")

# STEP 5: Simulate AutoGen Analysis
assistant = AssistantAgent(name="CodeParserAI")
user = UserProxyAgent(
    name="Developer",
    human_input_mode="ALWAYS",  # So you can control replies
    code_execution_config={
        "use_docker": False  # Disable Docker
    }
)

# Start a simulated chat with AutoGen
user.initiate_chat(
    assistant,
    message="""
    I have parsed Python code into AST, Symbol Table, and saved IR in JSON.
    Now help me create a language-neutral Intermediate Representation (IR).
    """
)
