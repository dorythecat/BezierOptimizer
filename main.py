test_equation = ("x * x * x + x * x + 3 * x + 2 * x")

def simplify_equation(equation: str) -> str:
    split_add = equation.split("+")

    least_x_content = 10000
    for i in range(len(split_add)):
        add = split_add[i]
        x_content = add.count("x")
        if x_content < least_x_content:
            least_x_content = x_content
        split_add[i] = add.strip()
    if least_x_content > 0:
        number_terms = dict()
        for i in range(len(split_add)):
            if split_add[i].strip().count("x * x") == 0:
                split_add[i] = split_add[i].replace("x", "").replace("*", "").strip()
                if split_add[i] == "":
                    split_add[i] = "1"
                number_terms.update({i: int(split_add[i])})
                continue
            split_add[i] = split_add[i].replace("x * ", "", least_x_content).strip()
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
    if least_x_content > 0:
        for i in range(least_x_content):
            if i == 0:
                equation = "x * (" + equation + ")"
            else:
                equation = "x * " + equation
    return equation

print(simplify_equation(test_equation))