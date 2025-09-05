# Quadratic Bézier curve (one-dimensional) equation function
def quad_bezier(p0: float, p1: float, p2: float) -> str:
    p2 = p2 - p1
    p2n = p2 < 0 # is it negative?
    p2 *= -1 if p2n else 1 # Make it positive
    p2 = (" - " if p2n else " + ") + ("" if p2 == 1 else (str(p2) + " * ")) # Turn to string
    if p0 == p1:
        output = str(p1) + ("" if p2[3:-3] == "0" else (p2 + "t²"))
        return "" if output == "0" else output
    # Same steps as above
    p0 = p0 - p1
    p0n = p0 < 0
    p0 *= -1 if p0n else 1
    p0 = (" - " if p0n else " + ") + ("" if p0 == 1 else (str(p0) + " * "))
    if p2 == 0:
        return str(p1) + p0 + "(1 - t)²"
    if p0[3:] == p2[3:]: # Ignore signs
        if p1 == 0:
            return ""
        return ("" if p1 == 1 else ("-" if p1 == -1 else str(p1))) + p0[:-3] + "((1 - t)² + t²)"
    return ("" if p1 == 0 else str(p1)) + ((("- " if p0 == " - " else "") + "1") if p0 in [" + ", " - "] and p1 == 0 else (p0 + "(1 - t)²")) + ("" if p2[3:-3] == "0" else (p2 + "t²"))

def cubic_bezier(p0: float, p1: float, p2: float, p3: float) -> str:
    b1 = quad_bezier(p0, p1, p2)
    b2 = quad_bezier(p1, p2, p3)
    return ("" if b1 == "" else ("(1 - t) * " + "(" + b1 + ")")) + ("" if b1 == "" or b2 == "" else " + ") + ("" if b2 == "" else ("t * (" + b2 + ")"))