import random
from datetime import datetime

from dscope.utils import dscopeLogToVectorLog, dscopeLogDump

transaction_log = []

def log_transaction(mode, src_host, dst_host, description):
    timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]
    transaction_log.append((timestamp, mode, src_host, dst_host, description))

class Proposer:
    def __init__(self, host_id):
        self.host_id = f"Proposer#{host_id}"
        self.proposal_number = random.randint(1, 99)

    def prepare(self, acceptors):
        self.proposal_number += 1
        promises = []
        for acceptor in acceptors:
            log_transaction("send", self.host_id, acceptor.host_id, f"Prepare with proposal number {self.proposal_number}")
            response = acceptor.receive_prepare(self.proposal_number, self.host_id)
            if response:
                promises.append(response)
        return promises

    def propose(self, acceptors, value):
        promises = self.prepare(acceptors)
        if len(promises) >= (len(acceptors) // 2 + 1):
            for acceptor in acceptors:
                log_transaction("send", self.host_id, acceptor.host_id, f"Propose value {value} with proposal number {self.proposal_number}")
                acceptor.receive_propose(self.proposal_number, value, self.host_id)

class Acceptor:
    def __init__(self, host_id):
        self.host_id = f"Acceptor#{host_id}"
        self.promised_number = 0
        self.accepted_number = 0
        self.accepted_value = None

    def receive_prepare(self, proposal_number, src_host):
        if proposal_number > self.promised_number:
            self.promised_number = proposal_number
            log_transaction("recv", src_host, self.host_id, f"Promise to accept proposal number {proposal_number}")
            return (self.accepted_number, self.accepted_value)
        return None

    def receive_propose(self, proposal_number, value, src_host):
        if proposal_number >= self.promised_number:
            self.promised_number = proposal_number
            self.accepted_number = proposal_number
            self.accepted_value = value
            log_transaction("recv", src_host, self.host_id, f"Accepted value {value} with proposal number {proposal_number}")

class Learner:
    def __init__(self, host_id):
        self.host_id = f"Learner#{host_id}"
        self.learned_value = None

    def learn(self, acceptors):
        values = {}
        for acceptor in acceptors:
            if acceptor.accepted_value:
                values[acceptor.accepted_value] = values.get(acceptor.accepted_value, 0) + 1
        if values:
            self.learned_value = max(values, key=values.get)
            log_transaction("none", self.host_id, self.host_id, f"Learned value {self.learned_value}")

# 模拟运行
def simulate_paxos(num_proposer, num_learner):
    proposer = Proposer(0)
    acceptors = [Acceptor(i) for i in range(num_proposer)]
    learners = [Learner(i) for i in range(num_learner)]

    proposer.propose(acceptors, random.randint(1, 100))

    for learner in learners:
        learner.learn(acceptors)

    # print("Transaction Log:")
    # for log in transaction_log:
    #     print(log)
    return

def paxos_simulator():
    from dscope.settings import (
        LOGICAL_CLOCK_NUM_PROPOSSER,
        LOGICAL_CLOCK_NUM_LEARNER,
    )
    simulate_paxos(
        LOGICAL_CLOCK_NUM_PROPOSSER,
        LOGICAL_CLOCK_NUM_LEARNER,
    )
    vector_log = dscopeLogToVectorLog(transaction_log)
    dscopeLogDump(vector_log, "paxos.log")
    return "Paxos simulate successfully!"