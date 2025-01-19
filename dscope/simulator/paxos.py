import random
from datetime import datetime

from dscope.utils import dscopeLogToVectorLog, dscopeLogDump

transaction_log = []

def log_transaction(mode, src_host, dst_host, description):
    timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]
    transaction_log.append((timestamp, mode, src_host, dst_host, description))
    return

class Proposer:
    def __init__(self, host_id):
        self.host_id = f"提议者#{host_id}"
        self.proposal_number = random.randint(1, 99)

    def prepare(self, acceptors):
        self.proposal_number += 1
        promises = []
        for acceptor in acceptors:
            log_transaction("send", self.host_id, acceptor.host_id, f"设置准备号为 {self.proposal_number}")
            response = acceptor.receive_prepare(self.proposal_number, self.host_id)
            if response:
                promises.append(response)
        for acceptor in acceptors:
            log_transaction("recv", acceptor.host_id, self.host_id, f"确认准备号为 {self.proposal_number}")
        return promises

    def propose(self, acceptors, value):
        promises = self.prepare(acceptors)
        if len(promises) >= (len(acceptors) // 2 + 1):
            for acceptor in acceptors:
                log_transaction("send", self.host_id, acceptor.host_id, f"发送准备号为 {self.proposal_number} 的数值 {value}")
                acceptor.receive_propose(self.proposal_number, value, self.host_id)
            for acceptor in acceptors:
                log_transaction("recv", acceptor.host_id, self.host_id, f"确认数值为 {value}")
                log_transaction("none", acceptor.host_id, acceptor.host_id, f"设置数值为 {value}")

class Acceptor:
    def __init__(self, host_id):
        self.host_id = f"接受者#{host_id}"
        self.promised_number = 0
        self.accepted_number = 0
        self.accepted_value = None

    def receive_prepare(self, proposal_number, src_host):
        if proposal_number > self.promised_number:
            self.promised_number = proposal_number
            log_transaction("recv", src_host, self.host_id, f"收到准备号为 {proposal_number}")
            log_transaction("send", self.host_id, src_host, f"确认准备号为 {proposal_number}")
            return (self.accepted_number, self.accepted_value)
        return None

    def receive_propose(self, proposal_number, value, src_host):
        if proposal_number >= self.promised_number:
            self.promised_number = proposal_number
            self.accepted_number = proposal_number
            self.accepted_value = value
            log_transaction("recv", src_host, self.host_id, f"收到准备号为 {proposal_number} 的数值 {value}")
            log_transaction("send", self.host_id, src_host, f"确认数值为 {value}")

class Learner:
    def __init__(self, host_id):
        self.host_id = f"学习者#{host_id}"
        self.learned_value = None

    def learn(self, proposer, acceptors):
        values = {}
        for acceptor in acceptors:
            if acceptor.accepted_value:
                values[acceptor.accepted_value] = values.get(acceptor.accepted_value, 0) + 1
        if values:
            self.learned_value = max(values, key=values.get)
            log_transaction("send", proposer.host_id, self.host_id, f"学习数值为 {self.learned_value}")
            log_transaction("recv", proposer.host_id, self.host_id, f"学习数值为 {self.learned_value}")
            log_transaction("none", self.host_id, self.host_id, f"设置数值为 {self.learned_value}")

# 模拟运行
def simulate_paxos(num_proposer, num_learner):
    proposer = Proposer(0)
    acceptors = [Acceptor(i) for i in range(num_proposer)]
    learners = [Learner(i) for i in range(num_learner)]

    proposer.propose(acceptors, random.randint(1, 100))

    for learner in learners:
        learner.learn(proposer, acceptors)
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