import time
import random
from tqdm import tqdm
from datetime import datetime

from dscope.utils import dscopeLogToVectorLog, dscopeLogDump

transaction_log = []

class LogicalClock:
    def __init__(self):
        self.time = 0
        return

    def increment(self):
        self.time += 1
        return self.time

    def update(self, received_time):
        self.time = max(self.time, received_time) + 1
        return self.time

class Process:
    def __init__(self, pid, nproc, p):
        self.pid = pid
        self.clock = LogicalClock()
        self.nproc = nproc
        self.p = p
        return

    def execute_transaction(self):
        if random.random() < self.p and self.nproc > 1:
            dst_host = random.choice([i for i in range(self.nproc) if i != self.pid])
            self.send_message(dst_host)
        else:
            self.internal_transaction()
        return

    def send_message(self, dst_host):
        current_time = self.clock.increment()
        log_entry = (datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3], "send", f"#{self.pid}", f"#{dst_host}", f"message: {self.pid} -> {dst_host}, logical clock: {current_time}")
        transaction_log.append(log_entry)
        time.sleep(random.uniform(0.01, 0.1))
        processes[dst_host].receive_message(self.pid, current_time)
        return

    def receive_message(self, src_host, received_time):
        current_time = self.clock.update(received_time)
        log_entry = (datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3], "recv", f"#{src_host}", f"#{self.pid}", f"message: {src_host} -> {self.pid}, logical clock: {current_time}")
        transaction_log.append(log_entry)
        return

    def internal_transaction(self):
        current_time = self.clock.increment()
        log_entry = (datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3], "none", f"#{self.pid}", f"#{self.pid}", f"message: {self.pid} do something, logical clock: {current_time}")
        transaction_log.append(log_entry)
        return

def simulate_distributed_system(nproc, steps, p):
    global processes
    processes = [Process(i, nproc, p) for i in range(nproc)]

    for step in tqdm(range(steps)):
        for process in processes:
            process.execute_transaction()

    return

def logical_clock_simulator():
    from dscope.settings import (
        LOGICAL_CLOCK_NPROC,
        LOGICAL_CLOCK_STEPS,
        LOGICAL_CLOCK_P,
    )
    simulate_distributed_system(
        LOGICAL_CLOCK_NPROC,
        LOGICAL_CLOCK_STEPS,
        LOGICAL_CLOCK_P,
    )
    vector_log = dscopeLogToVectorLog(transaction_log)
    dscopeLogDump(vector_log, "logical_clock.log")
    return "Logical clock simulate successfully!"