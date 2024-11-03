from .parser import Parser
from .visitors import SemanticAnalyzer
import os


def main():
    text = (
        open(os.path.join(os.path.dirname(__file__), "cebuano.txt"), "r").read().lower()
    )

    parser = Parser()
    errors, tree = parser.parse(text)

    long = len(parser.errors)
    print(text)
    if long == 0:
        print("No errors")
    for x in range(long):
        print("Error #" + str(x + 1))
        print(errors[x].error)
        if errors[x].wrong_value is not None:
            print("Error value: " + str(errors[x].wrong_value))
        print("Solution #" + str(x + 1))
        print(errors[x].correct)
        if errors[x].right_value is not None:
            print("Right values: " + ", ".join(errors[x].right_value))

    semantic_analyzer = SemanticAnalyzer()
    try:
        one = semantic_analyzer.visit(tree)
    except Exception as e:
        print(e)
        raise
    print(one)


if __name__ == "__main__":
    main()
