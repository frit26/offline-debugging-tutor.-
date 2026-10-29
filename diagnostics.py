"""Rule-based diagnostics for beginner Python code. No network access required."""
import ast
import builtins as py_builtins

RULES = {
    "SyntaxError": {
        "title": "Syntax error",
        "explanation": "Python could not parse this code. Check punctuation, brackets, quotes, colons, and indentation near the reported line.",
        "hints": ["Look closely at the line mentioned in the error.", "Check that brackets and quotes are paired, and that statements such as if/for/def end with a colon.", "Correct the syntax near the indicated line, then analyze the code again."],
        "fix": "Review the indicated line and the line immediately before it."
    },
    "NameError": {
        "title": "Possible undefined variable",
        "explanation": "A NameError usually means a name is used before it has been defined, or its spelling/capitalization does not match.",
        "hints": ["Check the names used in this statement.", "Compare the spelling and capitalization with the variable definitions above.", "Define the variable before using it, or correct the name so it matches its definition."],
        "fix": "Check spelling, capitalization, and whether the variable is defined before use."
    },
    "TypeError": {
        "title": "Possible type mismatch",
        "explanation": "A TypeError often occurs when an operation receives a value of an incompatible type, such as adding a string to an integer.",
        "hints": ["Check the values used in the operation.", "Identify each value's type (for example, str, int, or float).", "Convert values deliberately when needed, such as int(text) for numeric input."],
        "fix": "Make sure the operands or function arguments have compatible types."
    },
    "IndexError": {
        "title": "Possible index out of range",
        "explanation": "An IndexError commonly occurs when a list or sequence is accessed at a position that does not exist.",
        "hints": ["Check the index used to access the sequence.", "Remember that Python indexes start at 0 and the last valid index is len(sequence) - 1.", "Check the sequence length before accessing the index, or adjust the index or loop bounds."],
        "fix": "Check the sequence length and ensure the index is within valid bounds."
    },
    "IndentationError": {
        "title": "Indentation error",
        "explanation": "Python uses indentation to group statements. Inconsistent or missing indentation can prevent code from running.",
        "hints": ["Look at the block around the reported line.", "Statements inside if, for, while, and def blocks must be indented consistently.", "Use consistent spaces (commonly four per level) and align statements belonging to the same block."],
        "fix": "Align the block consistently and ensure each block has an indented body."
    }
}


def _result(kind, line, message, confidence="Rule match"):
    rule = RULES.get(kind, RULES["SyntaxError"])
    return {
        "kind": kind,
        "title": rule["title"],
        "line": line,
        "message": message,
        "explanation": rule["explanation"],
        "hints": rule["hints"],
        "fix": rule["fix"],
        "confidence": confidence,
    }


def analyze_code(source: str):
    """Return a list of explainable findings. This does not execute submitted code."""
    findings = []
    try:
        tree = ast.parse(source)
    except (SyntaxError, IndentationError) as exc:
        kind = "IndentationError" if isinstance(exc, IndentationError) else "SyntaxError"
        findings.append(_result(kind, exc.lineno or 1, exc.msg or str(exc)))
        return findings

    defined = set()
    loaded = []
    builtins = set(dir(py_builtins))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            defined.add(node.name)
            for dec in node.decorator_list:
                for child in ast.walk(dec):
                    if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                        loaded.append((child.id, child.lineno))
        elif isinstance(node, ast.Name):
            if isinstance(node.ctx, (ast.Store, ast.Param)):
                defined.add(node.id)
            elif isinstance(node.ctx, ast.Load):
                loaded.append((node.id, node.lineno))
        elif isinstance(node, ast.arg):
            defined.add(node.arg)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            for alias in node.names:
                defined.add(alias.asname or alias.name.split('.')[0])

    # Only flag likely misspellings/unbound names, and label them as candidates.
    known = defined | builtins
    seen = set()
    for name, line in loaded:
        if name not in known and name not in seen:
            seen.add(name)
            findings.append(_result("NameError", line, f"'{name}' is not obviously defined in this code. This is a heuristic, not proof of a runtime error.", "Heuristic"))

    # Simple type mismatch pattern: string literal + numeric literal (not a complete type checker).
    for node in ast.walk(tree):
        if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
            left, right = node.left, node.right
            mismatch = ((isinstance(left, ast.Constant) and isinstance(left.value, str) and isinstance(right, ast.Constant) and isinstance(right.value, (int, float)) and not isinstance(right.value, bool)) or
                        (isinstance(right, ast.Constant) and isinstance(right.value, str) and isinstance(left, ast.Constant) and isinstance(left.value, (int, float)) and not isinstance(left.value, bool)))
            if mismatch:
                findings.append(_result("TypeError", getattr(node, "lineno", 1), "This expression appears to add a string literal and a number. Confirm the intended types." , "Heuristic"))
                break

    # Obvious constant list-index case.
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.value, (ast.List, ast.Tuple)) and isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, int):
            length = len(node.value.elts)
            index = node.slice.value
            if index >= length or index < -length:
                findings.append(_result("IndexError", getattr(node, "lineno", 1), f"Index {index} is outside a sequence with {length} item(s).", "Rule match"))
                break

    if not findings:
        findings.append({
            "kind": "No supported issue found", "title": "No supported issue found", "line": None,
            "message": "The code passed Python's syntax parser and no included diagnostic rule matched.",
            "explanation": "This does not prove the program is correct. Logical and runtime errors may still exist because this first version does not execute code.",
            "hints": ["Read the code slowly and compare it with the expected behavior.", "Check variable values, conditions, loop boundaries, and function arguments.", "Test small pieces of the program in a separate trusted Python environment."],
            "fix": "No automatic correction is available for this result.", "confidence": "Limited static analysis"
        })
    return findings
