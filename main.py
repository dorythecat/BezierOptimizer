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

print(simplify_equation(test_equation))