import re

import openpyxl as xls

commands, codes = [], []
wb = xls.load_workbook('codes.xlsx')
commands = [i.value for i in wb['Лист1']['A']][1:]
commands = [i if '*' not in i else i.replace('*', '') for i in commands]
commands_masks = [i.value for i in wb['Лист1']['E']][1:]
masks_and = [''.join(str(i.value).split()) for i in wb['Лист1']['H']][1:]
masks_xor = [''.join(str(i.value).split()) for i in wb['Лист1']['I']][1:]
args = []

res_and, res_xor = [], []

def fix_ldi_ser(input_data) -> str:
    ldi_args = get_args(input_data, 'ldi')
    ldi_args_values = [ldi_args[arg] for arg in ldi_args.keys()]

    if ldi_args_values[0] == ldi_args_values[1]:
        return 'ldi'
    else:
        return 'ser'

def correct_commands() -> None:
    for item in commands:
        temp = list(item.split())
        temp[-1] = temp[-1].split(',')
        commands[commands.index(item)] = temp[0]
        args.append(temp[-1])

    return None

def get_command(input_data: str) -> list[str]:
    global masks_xor, masks_and, commands

    data = bin(int(input_data, 2))
    res = []
    for id in range(len(masks_and)):
        if ((int(data, 2) & int(masks_and[id], 2))^int(masks_xor[id], 2)) == 0:
            res.append(commands[id])
            res.append(args[id])

    #custom data fix because of incorrect AVR codes
    if len(res) == 0:
        res = ['subi', args[5]]
    """
    :return list: [command, listOfArgsNames]
    """
    return [res[0], res[1]]

def get_args(input_data: str, command: str) -> dict:
    command_id = commands.index(command)
    mask = list(commands_masks[command_id])
    # input_data = '0'*(len(mask)-len(input_data)) + input_data
    while mask.count(' ') != 0:
        del mask[mask.index(' ')]
    # print(f'{''.join(mask)}\n{input_data}\n{command}')
    if len(input_data) == len(mask):
        pass
    elif len(mask) > len(input_data):
        input_data = '0' * (len(mask) - len(input_data)) + input_data

    #init all data
    args_keys = []
    args_values = []
    or_masks = []
    for i in mask:
        if i != '0' and i != '1':
            if i not in args_keys:
                args_keys.append(i)
            if len(args_values) != len(args_keys):
                args_values.append('')
                or_masks.append('')

    #create or masks for each arg
    temp = ''.join(mask)
    # print(temp, input_data, '##', sep='\n')
    for char in temp:
        if char in args_keys:
            # print(input_data, ''.join(mask))
            or_masks[args_keys.index(char)] += input_data[temp.index(char)]
            temp = temp.replace(char, ' ', 1)
            # print(temp, or_masks)

    bitwise_cmd = ['rjump', 'rcall', 'ldi', 'sbci', 'adiw', 'sbiw', 'brbs', 'brbc', 'sbic', 'sbis', 'jmp', 'call']
    for arg in args_keys:
        # print(or_masks[args_keys.index(arg)])
        if command in bitwise_cmd:
            args_values[args_keys.index(arg)] += hex(int(or_masks[args_keys.index(arg)], 2) << 1)
        else:
            if command in ['ldi', 'subi', 'sub', 'sbr', 'cbr', 'cpi', 'andi', 'ori', 'sbci'] and int(or_masks[args_keys.index(arg)], 2) < 16:
                args_values[args_keys.index(arg)] += hex(int(or_masks[args_keys.index(arg)], 2) + 16)
            else:
                args_values[args_keys.index(arg)] += hex(int(or_masks[args_keys.index(arg)], 2))

    #all args in dict
    res = {}
    for arg in args_keys:
        res.update({
            arg: args_values[args_keys.index(arg)]
        })

    """
    :return dict of args with arg's names as keys
            {
                arg's name: arg value
            }
    """
    return res

def check_sign(input_data: str) -> tuple:
    input_data = bin(int(input_data, 16))[2:]
    if input_data[0] == 0:
        return (False, int(input_data, 2))
    else:
        input_data = ''.join(['0' if i=='1' else '1' for i in input_data])
        input_data = int(input_data, 2)+1
        return (True, '.'+str(-1*input_data))
