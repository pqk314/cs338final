card = '$set(x, $fromHand(1, F)); $trash($get(x)); $gain($chooseSubset($getSubset($getStore(), $makeArray(cost, <=, $addInts($getCost($get(x)), 2)), 1, F)))'

def displayCard(card):
    lines = []
    indent = ""
    line = ""
    skip = False
    for char in card:
        if skip:
            skip = False
            continue
        if char == '(':
            lines.append(indent + line + '(')
            line = ''
            indent += '    '
        elif char == ')':
            if len(line) > 0:
                lines.append(indent + line)
            lines.append(indent + ')')
            indent = indent[4:]
            line = ''
        elif char == ';':
            skip = True
        else:
            line += char
    return "\n".join(lines)

print(displayCard(card))