import sys

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

def n_bezier(points: list[float], verbose: bool) -> str:
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
            bezier = quad_bezier(*points)
            if verbose:
                print("Quadratic Bézier curve: " + bezier.replace(".0 ", " ").replace(".0(", "("))
            return bezier
        case _: # Use the recursive definition of a Bézier curve for higher-order curves
            b1 = n_bezier(points[:-1], verbose)
            b1 = ("" if b1 == "" else ("(1 - t)" + mul + "(" + b1 + ")"))
            b2 = n_bezier(points[1:], verbose)
            b2 = ("" if b2 == "" else ("t" + mul + "(" + b2 + ")"))
            if verbose:
                pl = "Cubic" if len(points) == 4 else (str(len(points)) + "-order")
                print(pl + " Bézier curve: " + b1.replace(".0 ", " ").replace(".0(", "("))
                print(pl + " Bézier curve: " + b2.replace(".0 ", " ").replace(".0(", "("))
            return b1 + ("" if b1 == "" or b2 == "" else " + ") + b2

if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 0 or "-h" in args or "--help" in args:
        print("Usage: python main.py [OPTIONS] [POINTS]")
        print("")
        print("Possible options:")
        print("  -h, --help     Display this help message")
        print("  -o, --output   Output type (0 = human-readable, 1 = Python, 2 = MatLab)")
        print("  -c, --compress Compress the output")
        print("  -v, --verbose  Verbose output (useful for debugging)")
        print("")
        print("Example: python main.py -o 2 -c 1 3 5 7 9")
        print("This example will generate a compressed MatLab equation for the points 1, 3, 5, 7, and 9.")
        exit()

    # DEFAULT SETTINGS
    OUTPUT_TYPE = 0 # Type of output (see the help message)
    COMPRESS = False  # Output compression
    VERBOSE = False # Verbose output

    if "-o" in args or "--output" in args:
        i = args.index("-o") if "-o" in args else args.index("--output")
        try:
            OUTPUT_TYPE = int(args[i + 1])
            args = args[:i] + args[i + 2:]
        except IndexError:
            print("Error: Missing output type")
            exit()
    if OUTPUT_TYPE not in [0, 1, 2]:
        print("Error: Invalid output type")
        exit()

    if "-c" in args or "--compress" in args:
        COMPRESS = True
        del args[args.index("-c") if "-c" in args else args.index("--compress")]

    if "-v" in args or "--verbose" in args:
        VERBOSE = True
        del args[args.index("-v") if "-v" in args else args.index("--verbose")]

    if len(args) < 1:
        print("Error: No points provided")
        exit()

    # Settings stuff
    mul = " * " if OUTPUT_TYPE in [0, 1] else ".*"  # multiplication sign
    m_off = 3 if OUTPUT_TYPE in [0, 1] else 2  # offset of multiplication sign
    power = "²" if OUTPUT_TYPE == 0 else ("**2" if OUTPUT_TYPE == 1 else ".^2")  # power (of two) sign

    if VERBOSE:
        print("--- VERBOSE MODE ACTIVE ---")
        print("Points:", args)
        print("Output type:", OUTPUT_TYPE)
        print("Compression:", COMPRESS)
        print("")
    output = n_bezier([float(arg) for arg in args], VERBOSE).replace(".0 ", " ").replace(".0(", "(")
    if VERBOSE:
        print("--- END OF VERBOSE SECTION ---")
    # Compress output if needed
    print(mul.strip().join("-".join("+".join(output.split(" + ")).split(" - ")).split(mul)) if COMPRESS else output)