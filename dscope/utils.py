import os
from typing import Dict, List, Tuple

LOG_ROOT = os.getenv("DSCOPE_LOG_ROOT", "log/")

def dscopeLogDump(dscopeLogs:List[Tuple[str, str, Dict[str, int], str]], logname:str) -> None:
    if not os.path.isdir(LOG_ROOT):
        os.makedirs(LOG_ROOT)

    with open(os.path.join(LOG_ROOT, logname), "w") as f:
        for log in dscopeLogs:
            message = f"[{log[0]}] [{log[1]}] {log[2]} {log[3]}\n"
            f.write(message)
    return