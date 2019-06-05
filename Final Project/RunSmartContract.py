from hashlib import sha256
import time
import dis
import sys
from io import StringIO

def transfer(addr, value, fee):
    print('transfer: {}'.format((addr, value, fee)))

old_stdout = sys.stdout
redirected_output = sys.stdout = StringIO()
exec('_con_wrapper(smartcon, allowance)', {'time': time, 'hash': sha256, 'emit': print, 'send': transfer, 'balances': account_balances, 'blockhash': blockhash, 'blocknum': blocknum, 'smartcon': smartcon, 'allowance': allowance, 'sys.stdout': sys.stdout, 'StringIO': StringIO, 'dis.dis': dis.dis})
sys.stdout = old_stdout

print(redirected_output.getvalue())  # the emits and sends

# there are some statements that are not allowed in the smart contracts,
# namely try clauses and break/continue statements

def _con_wrapper(smartcon_code, allowance, name_values=[]):
    #if len(names) != name_values:
    #    raise KeyError('names and values do not match')

    _new_lines = _find_loops(smartcon_code)
    for _line in _new_lines:
        if len(_line.split('\n')) == 1 or _line.split()[0] == 'def':
            allowance -= _line_cost(_line)
            if allowance <= 0:
                return 0
            else:
                exec(_line)
        else:
            if _line.split()[0] == 'if':
                allowance = _if_wrapper(_line, allowance)
            else:
                allowance = _loop_wrapper(_line, allowance)
        if allowance == 0:
            return 0
    return allowance

def _if_wrapper(whole_code, allowance, name_values=[]):
    _by_line = whole_code.split('\n')
    _statement = _by_line[0][3:-1]
    allowance -= _line_cost(_statement)
    if allowance <= 0:
        return 0
    else:
        if 'else' in _by_line:
            before_else = '\n'.join([x[1:] for x in _by_line[1: _by_line.index('else')]])
            after_else = '\n'.join([x[1:] for x in _by_line[_by_line.index('else') + 1:]])
            if eval(_statement):
                allowance = _con_wrapper(before_else, allowance)
            else:
                allowance = _con_wrapper(after_else, allowance)
        else:
            if eval(_statement):
                allowance = _con_wrapper('\n'.join([x[1:] for x in _by_line[1:]]), allowance)
    return allowance

def _loop_wrapper(loop_clause, inner_code, allowance, name_values=[]):
    if loop_clause.split()[0] == 'while':
        _statement = loop_clause[6:-1]
        _state_cost = _line_cost(_statement)
        while eval(_statement):
            allowance -= _state_cost
            if allowance <= 0:
                return 0
            allowance = _con_wrapper(inner_code, allowance)
    else:
        for eval(loop_clause[4:-1]):
            allowance -= 12
            if allowance <= 0:
                return 0
            allowance = _con_wrapper(inner_code, allowance)

    return allowance

def _find_clauses(loop_code):
    # find loops and clauses
    clause_names = ['for', 'if', 'while', 'def']
    try_names = ['try', 'except', 'finally']
    after_names = ['else', 'elif']
    big_names = ['break', 'continue']
    new_chunks = []
    on_lines = loop_code.split('\n')
    line_cycle = 0
    while line_cycle < len(on_lines):
        l = on_lines[line_cycle]
        if l.split() == []:
            line_cycle += 1
            continue
        if l.split()[0] in clause_names:
            indent_level = _count_ts(l)
            this_for = [l[indent_level:]]
            new_cycle = line_cycle + 1
            if new_cycle < len(on_lines):
                while on_lines[new_cycle].split() != [] and (_count_ts(on_lines[new_cycle]) > indent_level or on_lines[new_cycle].split()[0] in after_names):
                    this_for.append(on_lines[new_cycle][indent_level:])
                    new_cycle += 1
            new_chunks.append('\n'.join(this_for))
            line_cycle = new_cycle
        elif l.split()[0] in try_names:
            indent_level = _count_ts(l) + 1
            this_for = []
            new_cycle = line_cycle + 1
            if new_cycle < len(on_lines):
                while on_lines[new_cycle].split() != [] and _count_ts(on_lines[new_cycle]) > indent_level:
                    this_for.append(on_lines[new_cycle][indent_level:])
                    new_cycle += 1
            new_chunks.extend(this_for)
            line_cycle = new_cycle
        else:
            new_chunks.append(l)
            line_cycle += 1
    return new_chunks

def _count_ts(indented):
    post_indent = indented.lstrip('\t')
    return len(indented) - len(post_indent)

def _line_cost(in_line):
    if in_line.split()[0] == 'def':
        return len(in_line) + 30
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    dis.dis(in_line)
    sys.stdout = old_stdout
    disr = redirected_output.getvalue().split()
    total = 0
    cycle = 0
    for particle in disr:  # assigning values to opnames
        # explanation in https://hackernoon.com/ether-purchase-power-df40a38c5a2f
        # inspiration from https://github.com/djrtwo/evm-opcode-gas-costs/blob/master/opcode-gas-costs_EIP-150_revision-1e18248_2017-04-12.csv
        if 'JUMP' in particle:  # BREAK_LOOP CONTINUE_LOOP
            total += 8
        if 'POP' in particle or 'DELETE' in particle:
            total += 2
        if 'IF' in particle:
            total += 2
        if 'LOAD' in particle:
            total += 4
        if 'UNARY' in particle:
            total += 1
        if 'INPLACE' in particle:
            total += 3
        if 'BINARY' in particle:
            total += 4
        if 'STORE' in particle:
            total += 4
        if 'BUILD' in particle:
            total += 20
        if 'DIVIDE' in particle:
            total += 2
        if 'MULTIPLY' in particle:
            total += 2
        if 'POWER' in particle:
            total += 10*len(disr[cycle-2])
        if 'MODULO' in particle:
            total += 2
        if 'SHIFT' in particle:
            total += 5
        if 'COMPARE' in particle:
            total += 3
        if 'create' in particle:
            total += 10000
        if 'send' in particle or 'emit' in particle:
            total += 40
        if 'hash' in particle:
            total += 100 + 6*len(disr[cycle-2])
        cycle += 1
    return total


# for the profiling create a wrapper function that runs inside the
# official exec, and takes the smartcon as input, and execs each line seperately
