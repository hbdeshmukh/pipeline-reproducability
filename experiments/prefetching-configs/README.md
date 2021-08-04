### Files in this directory

There are three configuration files.
One for each block size.
For the prefetching experiment, we only consider pipelining strategy.

# How to disable prefetching?
First install msr-tools.
sudo apt-get install msr-tools
sudo modprobe msr

Read a value from the 0x1a4 (the one that controls prefetching) register.
sudo rdmsr -p0 0x1a4

This should return 0 meaning prefetching is enabled. 
To disable prefetching, we set bit 0 and bit 1 to 1. (-a means all processors)
sudo wrmsr -a 0x1a4 3

To re-enable prefetching
sudo wrmsr -a 0x1a4 0


