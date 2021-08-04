FIXED = {
  'QS_ARGS_NUMA_LOAD' : '',
  'QS_ARGS_NUMA_RUN' : '-preload_buffer_pool=false',
  'TPCH_DATA_PATH' : '/slowdisk/raw-data/tpch-sf50',
  'LOAD_DATA' : 'false',
}

CONFIGURABLE = {
  'QS_PREFIX' : '/fastdisk/incubator-quickstep/build-',
  'QS_SUFFIX' : '/quickstep_cli_shell',
  'QS_ARGS_BASE' : '-printing_enabled=false -visualize_execution_dag=true -use_filter_joins=false -scheduling_strategy=3 ',
  'QS_STORAGE_PREFIX' : '/fastdisk/qs-data/tpch-sf50-',
}

AFFINITIES = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29] 

WORKERS = 'num_workers'
WORKER_AFFINITIES = 'worker_affinities'
FORMAT = 'format'
BLOCK_SIZE = 'block_size'
QUERIES = 'QUERIES'
SEQ = 'seq'
QS = 'QS'
QS_STORAGE = 'QS_STORAGE'
PIPELINING = 'pipelining'
PIPE = 'pipe'
NOPIPE = 'nopipe'
