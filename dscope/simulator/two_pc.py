from datetime import datetime

from dscope.utils import dscopeLogToVectorLog, dscopeLogDump

transaction_log = []

def log_transaction(mode, src_host, dst_host, description):
    timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]
    transaction_log.append((timestamp, mode, src_host, dst_host, description))

class Participant:
    def __init__(self, host_id):
        self.host_id = f"Participant#{host_id}"
        self.prepared = False
        self.committed = False

    def prepare(self, coordinator_host):
        self.prepared = True
        log_transaction("recv", coordinator_host, self.host_id, "Prepare request received")
        log_transaction("send", self.host_id, coordinator_host, "Vote YES to commit")
        return True

    def commit(self, coordinator_host):
        if self.prepared:
            self.committed = True
            log_transaction("recv", coordinator_host, self.host_id, "Commit request received")
            log_transaction("send", self.host_id, coordinator_host, "Acknowledged commit")
        else:
            log_transaction("recv", coordinator_host, self.host_id, "Commit request received but not prepared")
            log_transaction("send", self.host_id, coordinator_host, "Acknowledged abort")

    def rollback(self, coordinator_host):
        if self.prepared:
            log_transaction("recv", coordinator_host, self.host_id, "Rollback request received")
            log_transaction("send", self.host_id, coordinator_host, "Acknowledged rollback")
        else:
            log_transaction("recv", coordinator_host, self.host_id, "Rollback request received but not prepared")
            log_transaction("send", self.host_id, coordinator_host, "Acknowledged rollback")

class Coordinator:
    def __init__(self, host_id):
        self.host_id = f"Coordinator#{host_id}"

    def run_2pc(self, participants):
        log_transaction("none", self.host_id, self.host_id, "Starting 2PC protocol")
        all_agreed = True
        for participant in participants:
            log_transaction("send", self.host_id, participant.host_id, "Prepare request sent")
            if not participant.prepare(self.host_id):
                all_agreed = False

        if all_agreed:
            log_transaction("none", self.host_id, self.host_id, "All participants agreed to commit")
            for participant in participants:
                log_transaction("send", self.host_id, participant.host_id, "Commit request sent")
                participant.commit(self.host_id)
        else:
            log_transaction("none", self.host_id, self.host_id, "Some participants disagreed, rolling back")
            for participant in participants:
                log_transaction("send", self.host_id, participant.host_id, "Rollback request sent")
                participant.rollback(self.host_id)

def simulate_2pc(num_participants):
    coordinator = Coordinator(0)
    participants = [Participant(i) for i in range(num_participants)]

    coordinator.run_2pc(participants)

    # print("Transaction Log:")
    # for log in transaction_log:
    #     print(log)
    return

def two_pc_simulator():
    from dscope.settings import (
        TWO_PC_NUM_PARTICIPANTS,
    )
    simulate_2pc(TWO_PC_NUM_PARTICIPANTS)
    vector_log = dscopeLogToVectorLog(transaction_log)
    dscopeLogDump(vector_log, "2pc.log")
    return "2PC simulate successfully!"