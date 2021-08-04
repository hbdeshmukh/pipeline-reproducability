# For an input file, create its`
# corresponding quickstep-formatted
# config file.
import pprint
import pandas as pd
from reader import configFileToDF
from constants import *

def createQSConfig(filename):
  count = 1
  df = configFileToDF(filename) 
  for row in df.itertuples():
    # for pipe and no-pipe, we want to generate only one loading config.
    if count % 2 != 0:
      with open("tmp-load-" + str(count) + ".cfg", "w") as lf:
        load_config = createLoadConfig(row)
        lf.seek(0)
        lf.write(convertConfigToStr(load_config))
    with open("tmp-run-" + str(count) + ".cfg", "w") as rf: 
      run_config = createConfig(row)
      rf.seek(0)
      rf.write(convertConfigToStr(run_config))
    count = count + 1

# 'config' is a named tuple.
def createConfig(config):
  out = dict()
  out.update(FIXED)
  out.update(updatePaths(config))
  out['QS_ARGS_BASE'] = CONFIGURABLE['QS_ARGS_BASE']
  out.update(updateQueries(config))
  out.update(updateParallelism(config, out))
  out.update(updateSequence(config, out))
  out.update(updatePipelining(config, out))
  out['OUTPUT_FILE'] = getOutputFileName(config)
  return out

def updateQueries(config_tuple):
  out = dict()
  out[QUERIES] = getattr(config_tuple, QUERIES) 
  return out

def updateParallelism(config_tuple, config_dict):
  out = dict()
  parallelism = config_dict['QS_ARGS_BASE']
  num_workers = int(getattr(config_tuple, WORKERS))
  assert num_workers <= len(AFFINITIES), "Number of workers should be at most the number of affinities"
  affinities = ','.join(map(str, AFFINITIES[:num_workers]))
  parallelism += "-" + WORKERS + "=" + str(num_workers) + " "
  parallelism += "-" + WORKER_AFFINITIES + "=" + affinities + " "
  out['QS_ARGS_BASE'] = parallelism
  return out

def updatePaths(config_tuple):
  out = dict()
  block_size = getattr(config_tuple, BLOCK_SIZE)
  storage_format = getattr(config_tuple, FORMAT)
  qs_path = CONFIGURABLE['QS_PREFIX'] + block_size + CONFIGURABLE['QS_SUFFIX'] 
  qs_storage_path = CONFIGURABLE['QS_STORAGE_PREFIX'] + block_size + '-' + storage_format
  out[QS] = qs_path
  out[QS_STORAGE] = qs_storage_path
  return out

def updateSequence(config_tuple, config_dict):
  out = dict()
  seq = getattr(config_tuple, SEQ)
  if len(seq) > 0:
    base = config_dict['QS_ARGS_BASE']
    base = base + "-pipeline_sequence=" + seq + " "
    out['QS_ARGS_BASE'] = base
  return out

def updatePipelining(config_tuple, config_dict):
  out = dict()
  pipelining = getattr(config_tuple, PIPELINING)
  base = config_dict['QS_ARGS_BASE'] + '-intra_pipeline_scheduling_strategy='
  if pipelining == PIPE:
    val = '0'
  else:
    val = '1'
  config_dict['QS_ARGS_BASE'] = base + val + ' '  
  return config_dict

# Note: this file is to store the output of queries.
def getOutputFileName(config_tuple):
  # If sequence is empty
  seq = getattr(config_tuple, SEQ)
  storage_format = getattr(config_tuple, FORMAT)
  pipelining = getattr(config_tuple, PIPELINING)
  block_size = getattr(config_tuple, BLOCK_SIZE)
  workers = getattr(config_tuple, WORKERS)
  filename = str(block_size) + '-' + storage_format + '-' + str(workers) + 'threads-' + pipelining + '.log'
  if len(seq) > 0:
    filename = 'sequence/' + filename
  return filename

def createLoadConfig(config_tuple):
  config = createConfig(config_tuple)
  config['LOAD_DATA'] = 'true'
  config['CREATE_SQL'] = 'create-' + getattr(config_tuple, FORMAT) + '.sql'
  return config

# config is a dict representing the lines in the
# final config file.
def convertConfigToStr(config):
  out = ''
  for k, v in config.iteritems():
    out = out + k + '=' + '\"' + v + '\"\n'
  return out 

filename = 'config.txt'
createQSConfig(filename)
