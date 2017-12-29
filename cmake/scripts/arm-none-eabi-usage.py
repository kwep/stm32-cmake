#!/usr/bin/env python

import os
import sys
import subprocess

def tobytes(s):
  val = 0
  s = s.strip().lower()
  if s.endswith('m'):
    val = int(s[:-1]) * 1024 * 1024
  elif s.endswith('k'):
    val = int(s[:-1]) * 1024
  else:
    val = int(s)
  return val

if len(sys.argv) < 5:
  print('error: Too few arguments for arm-none-eabi-usage')
  sys.exit(1)

sizestr = ''
try:
  sizestr = subprocess.check_output([sys.argv[1], sys.argv[2]])
except subprocess.CalledProcessError as e:
  sys.exit(1)
except OSError as e:
  print('error: executing arm-none-eabi-size: ' + e.strerror)
  sys.exit(1)

inlnines = sizestr.split('\n')
if len(inlnines) < 2:
  print('error: unexpected arm-none-eabi-size output')
  sys.exit(1)

sizes = map(lambda s: int(s), map(lambda s: s.strip(), inlnines[1].split('\t'))[:-2])

used_flash = float(sizes[0] + sizes[1])
used_ram = float(sizes[2] + sizes[1])

avail_flash = float(tobytes(sys.argv[3]))
avail_ram = float(tobytes(sys.argv[4]))

perc_flash = round(used_flash / avail_flash * 100, 2)
perc_ram = round(used_ram / avail_ram * 100, 2)

ind_flash = round(used_flash / avail_flash * 25, 0)
ind_ram = round(used_ram / avail_ram * 25, 0)

istr_flash = ''
istr_ram = ''
for i in range(25):
  istr_flash += '=' if i < ind_flash else '-'
  istr_ram += '=' if i < ind_ram else '-'

print('')
print('FLASH Usage: [{0}] {1}% ({2} / {3})'.format(istr_flash, perc_flash, int(used_flash), int(avail_flash)))
print('RAM Usage:   [{0}] {1}% ({2} / {3})'.format(istr_ram, perc_ram, int(used_ram), int(avail_ram)))
print('')
