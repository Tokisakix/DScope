from datetime import datetime

from dscope.utils import dscopeLogToVectorLog, dscopeLogDump

transaction_log = []

def log_transaction(mode, src_host, dst_host, description):
    timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S.%f")[:-3]
    transaction_log.append((timestamp, mode, src_host, dst_host, description))

class Participant:
    def __init__(self, host_id):
        self.host_id = f"参与者#{host_id}"
        self.prepared = False
        self.committed = False

    def prepare(self, coordinator_host):
        self.prepared = True
        log_transaction("recv", coordinator_host, self.host_id, "收到准备请求")
        log_transaction("send", self.host_id, coordinator_host, "准备完成，可以提交")
        return True

    def commit(self, coordinator_host):
        if self.prepared:
            self.committed = True
            log_transaction("recv", coordinator_host, self.host_id, "收到提交请求")
            log_transaction("none", self.host_id, self.host_id, "提交")
            log_transaction("send", self.host_id, coordinator_host, "确认提交")
            return "确认提交"
        else:
            log_transaction("recv", coordinator_host, self.host_id, "收到提交请求但是没有准备")
            log_transaction("send", self.host_id, coordinator_host, "提交终止")
            return "提交终止"

    def rollback(self, coordinator_host):
        if self.prepared:
            log_transaction("recv", coordinator_host, self.host_id, "收到回滚请求")
            log_transaction("none", self.host_id, self.host_id, "回滚")
            log_transaction("send", self.host_id, coordinator_host, "确认回滚")
        else:
            log_transaction("recv", coordinator_host, self.host_id, "收到回滚请求但是没有准备")
            log_transaction("send", self.host_id, coordinator_host, "确认回滚")
        return "确认回滚"

class Coordinator:
    def __init__(self, host_id):
        self.host_id = f"协作者#{host_id}"

    def run_2pc(self, participants):
        log_transaction("none", self.host_id, self.host_id, "开始两阶段提交协议")
        all_agreed = True
        for participant in participants:
            log_transaction("send", self.host_id, participant.host_id, "发送提交请求")
            if not participant.prepare(self.host_id):
                all_agreed = False
        for participant in participants:
            log_transaction("recv", participant.host_id, self.host_id, "准备完成，可以提交")

        if all_agreed:
            log_transaction("none", self.host_id, self.host_id, "所有参与者准备完成，可以提交")
            for participant in participants:
                log_transaction("send", self.host_id, participant.host_id, "发送提交请求")
                info = participant.commit(self.host_id)
            for participant in participants:
                log_transaction("recv", participant.host_id, self.host_id, info)
        else:
            log_transaction("none", self.host_id, self.host_id, "所有参与者反对提交，回滚")
            for participant in participants:
                log_transaction("send", self.host_id, participant.host_id, "发起回滚请求")
                info = participant.rollback(self.host_id)
            for participant in participants:
                log_transaction("recv", participant.host_id, self.host_id, info)

def simulate_2pc(num_participants):
    coordinator = Coordinator(0)
    participants = [Participant(i) for i in range(num_participants)]

    coordinator.run_2pc(participants)
    return

def two_pc_simulator():
    from dscope.settings import (
        TWO_PC_NUM_PARTICIPANTS,
    )
    simulate_2pc(TWO_PC_NUM_PARTICIPANTS)
    vector_log = dscopeLogToVectorLog(transaction_log)
    dscopeLogDump(vector_log, "2pc.log")
    return "2PC simulate successfully!"