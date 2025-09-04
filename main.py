from automat import pep614

test_equation = "t * t * t + t * t + 3 * t + 2 * t"

# Simplify a written-out equation into something simpler
def simplify_equation(equation: str, variable: str = "t") -> str:
    split_add = equation.split("+")

    least_var_content = 10000 # Something really high so it doesn't interfere with anything
    for i in range(len(split_add)):
        add = split_add[i]
        var_content = add.count(variable)
        if var_content < least_var_content:
            least_var_content = var_content
        split_add[i] = add.strip()
    if least_var_content > 0:
        number_terms = dict()
        for i in range(len(split_add)):
            if split_add[i].strip().count(variable + " * " + variable) == 0:
                split_add[i] = split_add[i].replace(variable, "").replace("*", "").strip()
                if split_add[i] == "":
                    split_add[i] = "1"
                number_terms.update({i: int(split_add[i])})
                continue
            split_add[i] = split_add[i].replace(variable + " * ", "", least_x_content).strip()
        number_count = 0
        i_offset = 0
        if len(number_terms) != 0:
            for [i, number] in number_terms.items():
                number_count += number
                del split_add[i + i_offset]
                i_offset -= 1
                if i == max(number_terms.keys()):
                    split_add.append(str(number_count))
    equation = " + ".join(split_add)
    if least_var_content > 0:
        for i in range(least_var_content):
            if i == 0:
                equation = variable + " * (" + equation + ")"
            else:
                equation = variable + " * " + equation
    return equation

# Quadratic Bézier curve (one-dimensional) equation function
def quad_bezier(p0: float, p1: float, p2: float) -> str:
    p2p1 = p2 - p1
    p2p1n = p2p1 < 0 # is it negative?
    p2p1 *= -1 if p2p1n else 1 # Make it positive
    if p0 == p1:
        return str(p1) + ("" if p1 == p2 else ((" - " if p2p1n else " + ") + ("" if p2 - p0 == 1 else (str(p2p1) + " * ")) +  "t * t"))
    p0p1 = p0 - p1
    p0p1n = p0p1 < 0 # is it negative?
    p0p1 *= -1 if p0p1n else 1 # Make it positive
    if p2 == p1:
        return str(p1) + (" - " if p0p1n else " + ") + ("" if p0p1 == 1 else (str(p0p1) + " * ")) + "(1 - t) * (1 - t)"
    if p0p1 == p2p1:
        return str(p1) + (" - " if p0p1n else " + ") + ("" if p0p1 == 1 else str(p0p1)) + "((1 - t) * (1 - t) + t * t)"
    return (str(p1) + (" - " if p0p1n else " + ") + ("" if p0p1 == 1 else (str(p0p1) + " * ")) + "(1 - t) * (1 - t)" +
            (" - " if p2p1n else " + ") + ("" if p2p1 == 1 else (str(p2p1) + " * ")) + "t * t")

print(quad_bezier(1, 2, 3))