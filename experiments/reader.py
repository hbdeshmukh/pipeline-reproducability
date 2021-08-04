# Read configuration file and create experimental configs.
# Lines in the file look as below:
# Note that we want the delimiter to be ;
# because we use "," for fields.
# threads,10;format,rowstore;block_size,128kb;query,ALL;seq,
# threads,20;format,rowstore;block_size,2mb;query,ALL;seq,
import pandas as pd
from constants import *

# Return a dictionary of config items
def getConfig(input):
  tokens = input.split(';')
  out = dict()
  for t in tokens:
    subtokens = t.split(',')
    if len(subtokens) == 2:
      out[subtokens[0]] = subtokens[1]
    else:
      out[subtokens[0]] = "-"
  return out

def configFileToDF(filename):
  df = pd.DataFrame()
  with open(filename, "r") as f:
    contents = f.read().splitlines()
    for line in contents:
      c = getConfig(line)
      c[PIPELINING] = PIPE
      df = df.append(c, ignore_index=True)
      c[PIPELINING] = NOPIPE
      df = df.append(c, ignore_index=True)
  return df
