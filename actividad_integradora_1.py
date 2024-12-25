# =========================================================
# File: actividad_integradora_1.py
# Author: Carlos Galicia - A01709890
# Date: 13/03/2024
# =========================================================
# Convierte la expresion con el operador "+" a su equivalente con el operador "*"
def transform_plus_to_klene(expression):  # Complejidad O(n^2)
    result = ""
    i = 0
    while i < len(expression):  # Por cada caracter en la expresion
        if expression[i] == "(":  # Se se encuentra un  "("
            j = i + 1  # j es fin del grupo
            start = i  # Inicio del grupo

            # Mientras que se no encuentre el parentesis de cierre
            while j < len(expression) and expression[j] != ")":
                j += 1  # j (el fin del grupo) aumenta 1
            group = expression[start:j+1]  # Se hace un grupo desde el start hasta el fin del grupo

            index = 0
            while "+" in group and index < len(group):  # Si el grupo tiene un signo +
                if group[index] == "+":
                    rest = group[index+1:]
                    group = "(" + group[index-1] + group[index-1] + "*" + rest

                index += 1

            if j + 1 < len(expression):

                if j < len(expression) and expression[j+1] == "+":
                    transformed_group = "(" + group[1:-1] + ")" + "(" + group[1:-1] + ")*"
                    result += transformed_group
                    i = j + 2
                else:  # de lo contrario solo sumarle el grupo al result
                    result += group
                    i = j + 1

            else:
                result += expression[i]
                i += 1

        elif expression[i].isalnum():  # Si la expresion no contiene ningun "(" o ")"...

            # Si el largo de la expresion menos 1 es mayor a i, y el siguiente caracter es un "+"...
            if i < len(expression) - 1 and expression[i+1] == "+":
                # Sumarle al resultado dos veces el caracter y el simbolo "*"
                result += expression[i] + expression[i] + "*"
                # Sumarle 2 al iterador para saltarse el propio caracter y el "+"
                i += 2

            else:  # Sumarle solo el caracter a la expresion
                result += expression[i]
                # Sumarle 1 al iterador
                i += 1

        else:
            result += expression[i]
            i += 1

    return result


# Extraer las letras de la lista de simbolos y expresion regex
def extract_letters(input_string):  # Complejidad O(n)
    return ''.join(char for char in input_string if char.isalpha() or char.isalnum())

# Encuentra el estado inicial del NFA creado
def find_initial(count, lista_adj):  # Complejidad O(n^2)

    found = False
    for i in range(count):

        for elem in lista_adj:

            if len(elem) > 1:

                if i == elem[0][0] or i == elem[1][0]:
                    found = True
                    break

            else:

                if i == elem[0][0]:
                    found = True
                    break

        if found is False:
            return i
        found = False


# Ver cuales son los estados a los que se puede llegar por medio de "#" (epsilon) desde el estado de entrada
def e_closure(initial_states, transitions):  # Complejidad O(n^2)

    if len(initial_states) == 0:
        return initial_states

    else:
        max_state = max(max(initial_states), max([t[0] for trans in transitions for t in trans], default=0))
        transition_functions = [[] for _ in range(max_state + 1)]

        for s, transitions_from_s in enumerate(transitions):
            for next_state, symbol in transitions_from_s:
                transition_functions[s].append((next_state, symbol))

        closure = set(initial_states)
        stack = list(initial_states)

        while stack:
            current_state = stack.pop()
            for next_state, symbol in transition_functions[current_state]:
                if symbol == '#' and next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        ordered_states = sorted(closure)
        closure_list = list(ordered_states)

        return closure_list


# Ver que estados bajo un simbolo determinado llegan a otros estados
def move(initial_states, symbol, transitions, max_state):  # Complejidad O(n^2)

    result = []
    for state in initial_states:

        if state == max_state:
            break

        else:

            for next_state, transition_symbol in transitions[state]:

                if transition_symbol == symbol:
                    result.append(next_state)
    return result


def main():  # Complejidad O(n^4)
    # Validacion de entrada de simbolos utilizados
    alphabet = str(input("Alphabet: "))
    while len(alphabet) == 0:
        print("Entrada no valida")
        alphabet = str(input("Alphabet: "))
    letters_list = extract_letters(str(alphabet))

    expression = input("RegEx: ")
    print("---RESULTS---\nINPUT:\n" + expression + "\n")
    result = ""
    expression = transform_plus_to_klene(str(expression))
    for i in range(len(expression) - 1):  # Colocar . entre concatenaciones

        if (expression[i].isalpha() and expression[i + 1].isalpha()) or \
                (expression[i].isdigit() and expression[i + 1].isdigit()) or \
                (expression[i].isalpha() and expression[i + 1] == "(") or \
                (expression[i].isdigit() and expression[i + 1] == "(") or\
                (expression[i] in [")", "*"] and expression[i + 1].isalpha()) or \
                (expression[i] in [")", "*"] and expression[i + 1].isdigit()) or \
                (expression[i] in [")", "*"] and expression[i + 1] == "("):
            result += expression[i] + "."

        else:
            result += expression[i]
    result += expression[-1]  # Añade el último caracter
    expression = str(result)

    # Establecer precedencia para caracteres de mayor a menor , closure "*", concatenacion ".", or "|"
    operadores = {'*': 100,
                  '.': 99,
                  '|': 98}

    # Regex a expresion postfija
    fila = []
    stack = []
    for token in expression:  # Complejidad O(n^2)

        if token.isalpha() or token.isdigit():
            fila.append(token)

        elif token in operadores:

            while len(stack) > 0 and stack[-1] != "(" and operadores.get(stack[-1]) >= operadores.get(token):
                oper = stack.pop()
                fila.append(oper)
            stack.append(token)

        elif token == "(":
            stack.append(token)

        elif token == ")":

            while stack[-1] != "(" and len(stack) > 0:
                oper = stack.pop()
                fila.append(oper)
            stack.pop()

    while len(stack) > 0:
        oper = stack.pop()
        fila.append(oper)

    postfija = ''.join(char for char in fila if char.isalpha() or char.isdigit() or char == "|" or char == "*" or char == ".")

    # Creacion del NFA
    regex = ''.join(postfija)

    keys = letters_list

    transiciones = []  # Lista de transiciones
    stack = []  # Stack de NFAs (cada uno con un estado final e inicial)
    start = 0  # Estado inicial
    end = 1  # Estado final

    contador = -1
    c1 = 0  # Contador de estado inicial
    c2 = 0  # Contador de estado final

    for i in regex:  # Complejidad O(n)
        if i in keys:  # Si i es una letra
            contador = contador + 1
            c1 = contador
            contador = contador + 1
            c2 = contador
            transiciones.append({})  # Se añaden 2 transiciones vacias al stack de transiciones
            transiciones.append({})
            stack.append([c1, c2])  # Se añade el nfa con estado inicial y final
            transiciones[c1][i] = c2  # La transicion con indice c1 se le asigna la llave i y el valor c2

        elif i == '*':  # Si es un "*", remueve el ultimo elemento del stack y añade los simbolos epsilon hacia las
            # Transiciones al estado final del NFA del stack y hacia el estado final del NFA construido
            r1, r2 = stack.pop()
            contador = contador + 1
            c1 = contador
            contador = contador + 1
            c2 = contador
            transiciones.append({})
            transiciones.append({})
            stack.append([c1, c2])
            transiciones[r2]['#'] = (r1, c2)
            transiciones[c1]['#'] = (r1, c2)

            # Si el estado inicial es el estado inicial del NFA1, adquiere el valor de c1
            if start == r1:
                start = c1

            # Si el estado final es el estado final del NFA1, adquiere el valor de c2
            if end == r2:
                end = c2

        elif i == '.':  # Si i es un ".", remueve los 2 ultimos elementos del stack y los divide en su 1er y 2do estado,
            # Tambien añade los simbolos epsilon hacia las transicioes del estado inicial de NFA2
            r11, r12 = stack.pop()
            r21, r22 = stack.pop()
            stack.append([r21, r12])
            transiciones[r22]['#'] = r11

            # Si el estado inicial es el estado inicial del NFA2, adquiere el valor del estado inicial de NFA1
            if start == r11:
                start = r21

            # Si el estado final es el estado final del NFA2, adquiere el valor del estado final de NFA1
            if end == r22:
                end = r12

        else:  # Llave "|", remueve los 2 ultimos elementos del stack y los divide en su 1er y 2do estado y añade los
            # Simbolos epsilon hacia las transiciones al estado final del NFA construido y los estados iniciales del NFA1 y
            #  NFA2 del stack
            contador = contador + 1
            c1 = contador
            contador = contador + 1
            c2 = contador
            transiciones.append({})
            transiciones.append({})
            r11, r12 = stack.pop()
            r21, r22 = stack.pop()
            stack.append([c1, c2])
            transiciones[c1]['#'] = (r21, r11)
            transiciones[r12]['#'] = c2
            transiciones[r22]['#'] = c2

            # Si el estado inicial es el estado inicial del NFA1 o NFA2, adquiere el valor de c1
            if start == r11 or start == r21:
                start = c1

            # Si el estado final es el estado final del NFA1 o NFA2, adquiere el valor de c2
            if end == r22 or end == r12:
                end = c2


    transiciones.pop()

    print("NFA:")

    lista_adj = []
    count = 0
    max_state = 0
    # Imprimir transiciones del NFA:
    for elem in transiciones:  # Complejidad O(n)
        t = []
        key = str(list(transiciones[count]))[-3]

        if type(elem.get(key)) is tuple:
            t.append((elem.get(key)[0], key))
            t.append((elem.get(key)[1], key))
            if max(elem.get(key)[0], (elem.get(key)[1])) > max_state:
                max_state = max(elem.get(key)[0], (elem.get(key)[1]))
        else:
            t.append((elem.get(key), key))
            if elem.get(key) > max_state:
                max_state = elem.get(key)
        lista_adj.append(t)
        print(str(count) + " =>", t)
        count += 1

    print("Accepting state: " + str(max_state) + "\n")

    # Creacion de DFA

    print("DFA:")
    letters = {}
    accepting_states = []
    d_states = []
    fila_de_transiciones = []
    fila_estados = []
    transiciones_existentes = {}
    ascii_letter = 65  # Valor ascii para 'A'
    state = find_initial(count, lista_adj)  # Primer estado del nfa
    initial_state = [state]
    states = e_closure(initial_state, lista_adj)
    d_states.append(states)
    d_states.append([])
    transiciones_existentes[chr(ascii_letter)] = d_states
    fila_estados.append([chr(ascii_letter), states])

    while len(fila_estados) > 0:  # Complejidad O(n^4)
        letra, states = fila_estados.pop(0)

        if max_state in states:
            accepting_states.append(letra)

        fila_de_transiciones = []

        for simbol in letters_list:
            d_states = []
            new_states = e_closure(move(states, simbol, lista_adj, max_state), lista_adj)  # Complejidad O(n^2)
            encontrado = False

            if len(new_states) == 0:
                d_states.append(states)
                d_states.append([])
                fila_de_transiciones.append("-")
                d_states[1].append(fila_de_transiciones)
                transiciones_existentes[letra] = d_states

            else:

                # Busca si los estados de los moves ya estan registrados
                for key, value in list(transiciones_existentes.items()):
                    if new_states == value[0]:
                        encontrado = True

                        # Añadir los estados bajo las letras
                        d_states.append(states)
                        d_states.append([])
                        fila_de_transiciones.append(key)
                        d_states[1].append(fila_de_transiciones)
                        transiciones_existentes[letra] = d_states

                # Si no se encuentra se añade la letra y su estado a la lista de transiciones
                if encontrado is False:
                    d_states.append(new_states)
                    d_states.append([])
                    transiciones_existentes[chr(ord(key) + 1)] = d_states
                    d_states = []
                    d_states.append(states)
                    d_states.append([])
                    fila_de_transiciones.append(chr(ord(key) + 1))
                    d_states[1].append(fila_de_transiciones)
                    transiciones_existentes[letra] = d_states
                    fila_estados.append([chr(ord(key) + 1), new_states])

    for key, value in list(transiciones_existentes.items()):  # Complejidad O(n^2)
        t_list = []
        count = 0

        for elem in value[1][0]:

            if elem != "-":
                t_list.append((elem, letters_list[count]))
            count += 1
        print(key, "=>", t_list)

    final_states = sorted(accepting_states)
    accepting_states = list(final_states)
    print("Accepting states:", accepting_states)


main()
