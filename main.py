import parser as pars
import serializer
from serializer import get_command, correct_commands, check_sign

def get_data():
    with open('output.txt', 'r') as file:
        data = file.readlines()
    return data

def main():
    # pars.init()
    res = []
    correct_commands()
    data = get_data()
    for line in data:
        res_line = []
        for num in list(line.split()):
            result_command = []

            #insert space every 2 chars
            try:
                t = str(hex(int(num, 2)))
                new_t = ''
                for i in range(0, len(t), 2):
                    new_t += t[i:i+2] + ' '
                new_t = list(new_t[3:-1].split())
                for i in range(0, len(new_t), 2):
                    new_t[i], new_t[i+1] = new_t[i+1], new_t[i]
                result_command.append(' '.join(new_t))
            except:
                pass

            #get command
            command_info = get_command(num)
            result_command.append(command_info[0])

            #get args
            args = serializer.get_args(num, command_info[0])
            # print(args.keys(), args.values())
            changed_indexes = []
            for arg in args.keys():
                elem = None
                decimal_cmd = [
                    'rjmp', 'rcall', 'brbs', 'brbc', 'brcc', 'brcs', 'breq', 'brge',
                    'brhc', 'brhs', 'brid', 'brie', 'brlo', 'brlt', 'brmi', 'brne',
                    'brpl', 'brsh', 'brtc', 'brts', 'brvc', 'brvs'
                ]

                for el in command_info[1]:
                    if el == arg:
                        elem = el
                    if len(el) == 2:
                        if el[1] == arg:
                            elem = el
                if len(elem) == 2:
                    args[arg] = 'r'+str(int(args[arg][2:], 16))
                    break
                if command_info[0] in decimal_cmd:
                    args[arg] = check_sign(args[arg])[1]
                            
            for arg in args.keys():
                result_command.append((f'{args[arg]},' if arg == [i for i in args.keys()][0] else f'{args[arg]}') if len(args.keys()) != 1 else f'{args[arg]}')
            res_line.append(result_command)

        for t in res_line:
            if t[0][0] != 'nop':
                # print(' '.join(t))
                res.append(' '.join(t))
            else:
                res.append('00 00 nop')

    last = 0
    final = [f'{last}: '+res[0]]
    for el in res[1:]:
        pred_el = final[res[1:].index(el)]
        if ('lds' in pred_el or 'sts' in pred_el or ' jmp' in pred_el or ' call' in pred_el):
            last += 4
            final.append(f'{hex(last)[2:]}: '+el)
        else:
            last += 2
            final.append(f'{hex(last)[2:]}: '+el)

    print(*final, sep='\n')
    with open('assembler.txt', 'r+') as file:
        file.writelines('\n'.join(final))
        # print(*res_line, sep=' ', end='\n')

main()