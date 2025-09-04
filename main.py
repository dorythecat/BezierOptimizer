test_equation = "x * x * x + x * x + x"

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
        for i in range(len(split_add)):
            split_add[i] = split_add[i].replace("x", "", least_x_content)
            if split_add[i].startswith(" * "):
                split_add[i] = split_add[i][3:]
            if split_add[i] == "":
                split_add[i] = "1"
    equation = " + ".join(split_add)
    if least_x_content > 0:
        for i in range(least_x_content):
            if i == 0:
                equation = "x * (" + equation + ")"
            else:
                equation = "x * " + equation
    return equation

print(simplify_equation(test_equation))