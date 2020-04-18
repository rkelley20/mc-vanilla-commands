from mcrcon import MCRcon
import constants
import utils
import time
import requests
import subprocess
import re
import json
import random
import threading

rcon = MCRcon('localhost', 'rcon')
rcon.connect()

setattr(rcon, 'say', lambda s: rcon.command(f'say {s}'))

with open('warps.json') as fp:
    warps = json.load(fp)

def write_warps():
    with open('warps.json', 'w+') as fp:
        json.dump(warps, fp) 

def command_exec(name: str, args: str):
    rcon.say(utils.exec_python(args, locals(), globals()))

def command_joke(name: str, args: str):
    rcon.say(utils.get_joke())

def command_warps(name: str, args: str):
    locs = ', '.join(warps)
    rcon.say(f'Available Warps: {locs}')

def command_warp(name: str, args: str):
    coords = warps.get(args)
    if coords is None:
        rcon.say(f'The warp {args} was not found, list warps by typing warps')
    else:
        coords = ' '.join(map(str, coords))
        rcon.command(f'tp {name} {coords}')
        rcon.say(f'{name} teleported to {args}')

def command_add_warp(name: str, args: str):
    if len(warps) >= 10:
        rcon.say('Warps are limited to 10, you must delete a warp before adding another one.')
    else:
        loc, x, y, z = args.split(' ')
        warps[loc] = (x, y, z)
        rcon.say(f'Added warp {loc} at {x}, {y}, {z}')
        write_warps()

def command_del_warp(name: str, args: str):
    try:
        del warps[args]
    except KeyError:
        rcon.say(f'The warp {args} does not exist :(')
    else:
        rcon.say(f'{args} removed from the warp list!')
        write_warps()

def command_sun(name: str, args: str):
    rcon.command('time set day')
    rcon.command('weather clear')
    rcon.say(f'Jesus Christ has blessed us...')

def command_dice(name: str, args: str):
    rcon.say(f'You rolled {random.randint(1, 6)}')

def command_awww_man(name: str, args: str):
    for line in constants.revenge_lyrics:
        rcon.say(line)
        time.sleep(1)

def command_tp(name: str, args: str):
    if name == args:
        rcon.say('Do not tp to yourself idiot')
    else:
        rcon.command(f'tp {name} {args}')
        rcon.say(f'{name} tpd to {args}')

def command_tp_here(name: str, args: str):
    if name == args:
        rcon.say('Do not tp to yourself idiot')
    else:
        rcon.command(f'tp {args} {name}')
        rcon.say(f'{args} tpd to {name}')

callbacks = {
    'exec': command_exec,
    'joke': command_joke,
    'warps': command_warps,
    'warp': command_warp,
    'addwarp': command_add_warp,
    'delwarp': command_del_warp,
    'sun': command_sun,
    'dice': command_dice,
    'awwwman': command_awww_man,
    'tp': command_tp,
    'tphere': command_tp_here
}


while True:

    latest = subprocess.check_output(['tail', '-n', '1', '/root/server/logs/latest.log'], encoding='utf-8')

    matches = re.search(r'<(.*?)> (.*)', latest)

    if matches is None:
        time.sleep(0.5)
        continue

    name = matches.group(1)
    typed = matches.group(2)

    idx = typed.find(' ')
    if idx != -1:
        cmd = typed[:idx].lower()
        args = typed[idx+1:].lower()
    else:
        cmd = typed.lower()
        args = None

    try:
        command = callbacks[cmd]
    except KeyError:
        continue

    try:
        command(name, args)
    except:
        rcon.say('You typed the command wrong Pepega :)')


rcon.disconnect()