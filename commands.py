from mcrcon import MCRcon
import utils
import time
import requests
import subprocess
import re
import json

rcon = MCRcon('localhost', 'rcon')
rcon.connect()

setattr(rcon, 'say', lambda s: rcon.command(f'say {s}'))

with open('warps.json') as fp:
    warps = json.load(fp)

def write_warps():
    with open('warps.json', 'w+') as fp:
        json.dump(warps, fp) 

def command_exec(name: str, args: str):
    rcon.say(utils.exec_python(args))

def command_joke(name: str, args: str):
    rcon.say(get_joke())

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
    loc, x, y, z = cmd.split(' ')
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

callbacks = {
    'exec': command_exec,
    'joke': command_joke,
    'warps': command_warps,
    'warp': command_warp,
    'addwarp': command_add_warp,
    'delwarp': command_del_warp,
    'sun': command_sun
}


while True:

    latest = subprocess.check_output(['tail', '-n', '1', '/root/server/logs/latest.log'], encoding='utf-8')

    matches = re.search(r'<(.*?)> (.*)', latest)

    if matches is None:
        time.sleep(1)
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
        callbacks[cmd](name, args)
    except KeyError:
        pass


rcon.disconnect()