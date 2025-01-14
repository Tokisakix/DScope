import os
from typing import Dict, List, Tuple

from .settings import LOG_ROOT

def dscopeLogDump(dscopeLogs:List[Tuple[str, str, Dict[str, int], str]], logname:str) -> None:
    if not os.path.isdir(LOG_ROOT):
        os.makedirs(LOG_ROOT)

    with open(os.path.join(LOG_ROOT, logname), "w", encoding="utf-8") as f:
        for log in dscopeLogs:
            message = f"[{log[0]}] [{log[1]}] {log[2]} {log[3]}\n"
            message = message.replace("'", "\"")
            f.write(message)
            print(f"[{log[0]}] [{log[1]}] {log[3]}")
    return

def dscopeLogToVectorLog(dscopeLogs:List[Tuple[str, str, str, str, str]]) -> List[Tuple[str, str, Dict[str, int], str]]:
    from collections import defaultdict
    vector_clocks = defaultdict(lambda: defaultdict(int))

    def update_vector_clock(host, vector_clock):
        vector_clocks[host][host] += 1
        return vector_clocks[host].copy()

    def merge_vector_clocks(host, received_clock):
        for key, value in received_clock.items():
            vector_clocks[host][key] = max(vector_clocks[host][key], value)
        vector_clocks[host][host] += 1
        return vector_clocks[host].copy()

    def convert_transaction_log(log):
        vector_log = []
        for entry in log:
            timestamp, mode, src_host, dst_host, description = entry

            if mode in ['send', 'none']:
                vector_clock = update_vector_clock(src_host, vector_clocks[src_host])
                host = src_host
            elif mode == 'recv':
                vector_clock = merge_vector_clocks(dst_host, vector_clocks[src_host])
                host = dst_host

            new_entry = (timestamp, host, dict(vector_clock), description)
            vector_log.append(new_entry)
        return vector_log

    vector_log = convert_transaction_log(dscopeLogs)
    return vector_log