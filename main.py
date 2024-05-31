from typing import List, Tuple, Dict, Set

special_symbols = {'epsilon', 'id', 'or', 'not', 'and', 'true', 'false'}

def read_input_file(filename):
    """
    Reads the input file and parses the grammar cases.

    Args:
    filename (str): The name of the input file.

    Returns:
    list: A list of dictionaries, each representing a grammar case.
    """
    with open(filename, 'r') as f:
        n = int(f.readline().strip())  # Number of cases
        cases = []
        for _ in range(n): # Iterate over the number of cases
            k = int(f.readline().strip())  # Number of non-terminals in this case
            grammar = {}
            # Read and store the grammar
            for _ in range(k):
                line = f.readline().strip()
                non_terminal, productions = line.split(' -> ')
                productions = productions.split('|')
                grammar[non_terminal] = [production.strip() for production in productions]
            cases.append(grammar)
    return cases

def extract_non_terminals_and_terminals(grammar):
    """
    Extracts non-terminals and terminals from the grammar.

    Args:
    grammar (dict): The grammar dictionary.

    Returns:
    tuple: A set of non-terminals and a set of terminals.
    """
    non_terminals = set(grammar.keys()) # Extract non terminals into a set
    terminals = set()
    special_symbols
    # Extract terminals into a set
    for productions in grammar.values():
        for production in productions:
            for symbol in production:
                if production in special_symbols:
                    if production not in terminals:
                        terminals.add(production)
                    else:
                        pass
                elif symbol not in non_terminals and not symbol.isupper():
                    terminals.add(symbol)
    return non_terminals, terminals

def first(grammar):
    """
    Computes the FIRST sets for the given grammar.

    Args:
    grammar (dict): The grammar dictionary.

    Returns:
    dict: A dictionary with non-terminals as keys and their FIRST sets as values.
    """
    non_terminals, terminals = extract_non_terminals_and_terminals(grammar)
    firsts = {non_terminal: set() for non_terminal in grammar} # Generates the initial set to store FIRST sets

    # Initialize FIRST sets with direct terminals
    for non_terminal in grammar:
        for production in grammar[non_terminal]:
            if production and production[0] in terminals:
                firsts[non_terminal].add(production[0])

    # Iteratively compute the FIRST sets
    changes = True
    while changes:
        changes = False
        for non_terminal in grammar:
            for production in grammar[non_terminal]:
                i = 0
                while i < len(production):
                    if production in special_symbols:
                        symbol = production
                    else:
                        symbol = production[i]
                    if symbol in terminals:
                        # Add terminal to FIRST set
                        if symbol not in firsts[non_terminal]:
                            firsts[non_terminal].add(symbol)
                            changes = True
                        break
                    elif symbol in non_terminals:
                        # Add FIRST set of non-terminal, excluding 'epsilon'
                        before = len(firsts[non_terminal])
                        firsts[non_terminal].update(firsts[symbol] - {'epsilon'})
                        after = len(firsts[non_terminal])
                        if before != after:
                            changes = True
                        if 'epsilon' not in firsts[symbol]:
                            break
                    i += 1
                else:
                    # If all symbols can produce epsilon, add 'epsilon' to FIRST set
                    if 'epsilon' not in firsts[non_terminal]:
                        firsts[non_terminal].add('epsilon')
                        changes = True

    return {k: list(v) for k, v in firsts.items()}

def follow(grammar, firsts):
    non_terminals, terminals = extract_non_terminals_and_terminals(grammar)
    follows = {non_terminal: set() for non_terminal in grammar}
    start_symbol = next(iter(grammar))
    follows[start_symbol].add('$')  # End of input symbol


    changes = True
    while changes:
        changes = False
        for non_terminal in grammar:
            for production in grammar[non_terminal]:
                for i, symbol in enumerate(production):
                    if symbol in non_terminals:
                        # Check for epsilon in the FIRST sets of symbols to the right
                        j = i + 1
                        while j < len(production):
                            next_symbol = production[j]
                            if next_symbol in non_terminals:
                                follows[symbol].update(firsts[next_symbol])
                                if 'epsilon' in follows[symbol]:
                                    follows[symbol].remove('epsilon')
                                if 'epsilon' in firsts[next_symbol]:
                                    j += 1  # Stop if we find a non-epsilon
                                else:
                                    break
                            else:  # If next_symbol is a terminal
                                follows[symbol].add(next_symbol)
                                break

                        # If the loop completes (no break), it means all symbols to the right were epsilon
                        if j == len(production):
                            if follows[symbol].update(follows[non_terminal]):
                                changes = True

                        # Check for the FOLLOW of the non-terminal on the left-hand side
                        if i == len(production) - 1:
                            if follows[symbol].update(follows[non_terminal]):
                                changes = True

    return {k: list(v) for k, v in follows.items()}

def write_output_file(filename: str, cases: List[Dict[str, List[str]]], firsts_list: List[Dict[str, List[str]]], follows_list: List[Dict[str, List[str]]]) -> None:
    """

    Writes the FIRST and FOLLOW sets into a txt

    Args:
    filename: A string with the name of the output file
    cases: A list with the stored cases
    first_list: A list with the FIRST sets
    follow_list: A list with the FOLLOW sets

    Returns:
    A file with the information given
    """
    with open(filename, 'w') as f:
        f.write(f"{len(cases)}\n")
        for i in range(len(cases)):
            grammar = cases[i]
            firsts = firsts_list[i]
            follows = follows_list[i]
            f.write(f"{len(grammar)}\n")
            for non_terminal in grammar:
                f.write(f"Pr({non_terminal}) = {{{', '.join(firsts[non_terminal])}}}\n")
            for non_terminal in grammar:
                f.write(f"Sig({non_terminal}) = {{{', '.join(follows[non_terminal])}}}\n")

# Main code
filename = 'glcs.in'
cases = read_input_file(filename)

firsts_list = []
follows_list = []

for idx, grammar in enumerate(cases, start=1):
    print(f"Case {idx}:")
    first_sets = first(grammar)
    follow_sets = follow(grammar, first_sets)
    firsts_list.append(first_sets)
    follows_list.append(follow_sets)
    print("Grammar:")
    for nt, prods in grammar.items():
        print(f"{nt} -> {' | '.join(prods)}")
    print("First sets:")
    for nt, first_set in first_sets.items():
        print(f"{nt}: {first_set}")
    print("Follow sets:")
    for nt, follow_set in follow_sets.items():
        print(f"{nt}: {follow_set}")
    print("--------------------------------------------------------------------------------")

output_filename = 'pr_sig.out'
write_output_file(output_filename, cases, firsts_list, follows_list)