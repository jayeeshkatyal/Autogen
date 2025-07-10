# 🚀 Code Parser & Analyzer (Using Microsoft AutoGen)

This project parses Python code and generates:
- 🌳 Abstract Syntax Tree (AST)  
- 🗂 Symbol Table  
- 🌐 Intermediate Representation (IR)

It uses **Microsoft AutoGen** to simulate a collaboration between a developer and an AI assistant for refining code structure.

---

## 🛠 Tools & Technologies
- 🐍 Python 3.9+
- 🤖 Microsoft AutoGen (`pyautogen`)
- 📦 PrettyTable (for table formatting)

---

## ⚙️ How It Works
1. Parses raw code from `input_code.py`.
2. Generates AST & Symbol Table using Python libraries.
3. Uses AutoGen agents:  
   - `AssistantAgent` (AI assistant)  
   - `UserProxyAgent` (developer proxy)
4. Saves refined data into `intermediate_representation.json`.

---

## 📦 Setup Instructions
1. Clone the repository:

git clone https://github.com/devsinghsolanki/Code-Parser-Analyzer-AutoGen.git
cd Code-Parser-Analyzer-AutoGen

