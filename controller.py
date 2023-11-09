#!/bin/python3
import os
import signal


pipe_1_0 = os.pipe()
pipe_0_2 = os.pipe()
pipe_2_0 = os.pipe()


pid1 = os.fork()
if pid1 == 0:
    # process 1
    # writes to pipe 1->0, it is stdout
    os.dup2(pipe_1_0[1], 1)

    # close all except for pipe 1->0 read
    for fd in pipe_1_0[0], *pipe_0_2, *pipe_2_0:
        os.close(fd)
    
    # run producer
    os.execl("./producer.py", "producer.py")
# process 0
# reads from pipe_1_0


pid2 = os.fork()
if pid2 == 0:
    # process 2
    # reads from pipe 0->2 and it is stdin
    os.dup2(pipe_0_2[0], 0)
    # writes to pipe 2->0 and it is stdout
    os.dup2(pipe_2_0[1], 1)

    # close all except for these fd
    for fd in *pipe_1_0, pipe_0_2[1], pipe_2_0[0]:
        os.close(fd)
    
    # run bc
    os.execl("/usr/bin/bc", "bc")

# process 0 will write into pipe 0->2 and read from pipe 2->0
# close all others
for fd in pipe_0_2[0], pipe_1_0[1], pipe_2_0[1]:
    os.close(fd)

# open
in_1 = os.fdopen(pipe_1_0[0])  
in_2 = os.fdopen(pipe_2_0[0])
out_2 = os.fdopen(pipe_0_2[1], "w")

# signal handler
produced_count = 0
def handler(signal, frame):
    os.write(2, f"Produced: {produced_count}\n".encode("utf-8"))
    os.kill(pid1, 15)
    os.kill(pid2, 15)
    exit()
signal.signal(10, handler)


while True:
    line = in_1.readline()
    if not line:
        break
    out_2.write(line)
    out_2.flush()
    answer = in_2.readline()
    print(f"{line[:-1]} = {answer[:-1]}")
    produced_count += 1

in_1.close()
in_2.close()
out_2.close()
