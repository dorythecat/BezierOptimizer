import sys

# The type of string to spit out
# 0 = Human-readable equation
# 1 = Python equation
# 2 = MatLab equation
OUTPUT_TYPE = 0
COMPRESS = False # Whether to compress the output

mul = " * " if OUTPUT_TYPE in [0, 1] else ".*" # multiplication sign
m_off = 3 if OUTPUT_TYPE in [0, 1] else 2 # offset of multiplication sign
power = "²" if OUTPUT_TYPE == 0 else ("**2" if OUTPUT_TYPE == 1 else ".^2") # power (of two) sign

# Quadratic Bézier curve (one-dimensional) equation function
def quad_bezier(p0: float, p1: float, p2: float) -> str:
    p2 = p2 - p1
    p2n = p2 < 0 # is it negative?
    p2 *= 1 - p2n * 2 # Make it positive
    p2 = (" - " if p2n else " + ") + ("" if p2 == 1 else (str(p2) + mul)) # Turn to string
    if p0 == p1:
        output = ("" if p1 == 0 else str(p1)) + ("" if p2[3:-m_off] == "0" else (p2 + "t" + power))
        return "" if output == "0" else output
    # Same steps as above
    p0 = p0 - p1
    p0n = p0 < 0
    p0 *= 1 - p0n * 2
    p0 = (" - " if p0n else " + ") + ("" if p0 == 1 else (str(p0) + mul))

    p1 = ("" if p1 == 0 else str(p1)) # Convert to string
    if p2[3:-m_off] == "0":
        return p1 + p0 + "(1 - t)" + power
    if p0[3:] == p2[3:]: # Ignore signs
        if p1 == "":
            return ""
        return ("" if p1 == "1" else ("-" if p1 == "-1" else p1)) + p0[:-m_off] + "((1 - t)" + power + " + t" + power + ")"
    p0 = ((("- " if p0 == " - " else "") + "1") if p0 in [" + ", " - "] and p1 == "" else (p0 + "(1 - t)" + power))
    return p1 + p0 + ("" if p2[3:-m_off] == "0" else (p2 + "t" + power))

def n_bezier(points: list[float]) -> str:
    match len(points):
        case 1: # Constant
            return str(points[0])
        case 2: # Linear interpolation
            p0 = points[0]
            p0 = ("" if p0 == 0 else (("" if p0 == 1 else ("-" if p0 == -1 else str(p0))) + "(1 - t)"))
            p1 = points[1]
            p1 = ("" if p1 == 0 else (("" if p1 == 1 else ("-" if p1 == -1 else str(p1))) + "t"))
            return p0 + ("" if p0 == "" or p1 == "" else " + ") + p1
        case 3: # Quadratic Bézier curve
            return quad_bezier(*points)
        case _: # Use the recursive definition of a Bézier curve for higher-order curves
            b1 = n_bezier(points[:-1])
            b1 = ("" if b1 == "" else ("(1 - t)" + mul + "(" + b1 + ")"))
            b2 = n_bezier(points[1:])
            b2 = ("" if b2 == "" else ("t" + mul + "(" + b2 + ")"))
            return b1 + ("" if b1 == "" or b2 == "" else " + ") + b2

def compress(equation: str) -> str:
    equation = "+".join(equation.split(" + "))
    equation = "-".join(equation.split(" - "))
    equation = mul.strip().join(equation.split(mul))
    return equation

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0:
        print("Usage: python main.py [OPTIONS] [POINTS]")
        print("Possible options:")
        print("  -h, --help     Display this help message")
        print("  -o, --output   Output type (0 = human-readable, 1 = Python, 2 = MatLab)")
        print("  -c, --compress Compress the output")
        exit()
    points = []
    for i in range(len(args)):
        match args[i]:
            case "-h" | "--help":
                print("Usage: python main.py [OPTIONS] [POINTS]")
                print("Possible options:")
                print("  -h, --help     Display this help message")
                print("  -o, --output   Output type (0 = human-readable, 1 = Python, 2 = MatLab)")
                print("  -c, --compress Compress the output")
                exit()
            case "-o" | "--output":
                try:
                    OUTPUT_TYPE = int(args[i + 1])
                except IndexError:
                    print("Error: Missing output type")
                continue
            case "-c" | "--compress":
                COMPRESS = True
                continue
        print(args[i])
        if args[i][0] == "-":
            print("Invalid option: " + args[i])
            continue
        points.append(float(args[i]))
    if len(points) < 1:
        print("Error: No points provided")
        exit()
    output = n_bezier(points).replace(".0 ", " ").replace(".0(", "(")
    print(compress(output) if COMPRESS else output)