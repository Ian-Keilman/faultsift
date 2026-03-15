from dataclasses import dataclass
import re


@dataclass(frozen=True)
class LogRule:
    category: str
    severity: str
    score:  int
    patterns: tuple[re.Pattern, ...]

    def matches(self, line: str) -> bool:
        return any(pattern.search(line) for pattern in self.patterns)


def _build_rule(category: str, severity: str, score: int, patterns: list[str]) -> LogRule:
    compiled = tuple(re.compile(pattern, re.IGNORECASE) for pattern in patterns)
    return LogRule(category=category, severity=severity, score=score, patterns=compiled)

# I figured that some kind of scoring scale would be good to add, beacuse not all threast are equal

# Rough score scale I went with:
# 100 = machine is cooked
# 90s = serious crash / corruption
# 80s = very high-priority system issues
# 70s = important and probably urgent
# 50s-60s = meaningful problem, but maybe more localized
# 20s-40s = still worth flagging, just not as scary by itself

# 

DEFAULT_RULES = [
    # Full-on kernel failure. This is the ceiling.
    _build_rule(
        "kernel panic",
        "critical",
        100,
        [
            r"kernel panic" ,
            r"not syncing",
            r"BUG:",
        ],
    ),

    # Crashes are really bad, just usually a little below kernel panic.
    _build_rule(
        "segfault",
        "critical",
        90, 
        [
            r"segfault",
            r"general protection fault",
        ],
    ),

    # Read-only remounts are nasty because the machine may still be up, but writes start failing and everything gets weird.
    _build_rule(
        "filesystem read-only",
        "critical",
        88,
        [
            r"read-only file system",
            r"remounting filesystem read-only",
            r"EXT4-fs error",
        ],
    ),

    # OOM can kill processes and destabilize the system fast.
    _build_rule(
        "out of memory",
        "high",
         85,
        [
            r"out of memory",
            r"oom-killer",
            r"killed process .* out of memory",
        ],
    ),

    # Disk-full events break a lot of normal behavior pretty quickly.
    _build_rule(
        "disk full",
        "high",
        80,
        [
            r"no space left on device",
            r"disk full",
        ],
    ),

    # I/O errors can mean storage trouble, which is never fun.
    _build_rule(
        "i/o error",
        "high",
        75,     
        [
            r"i/o error",
            r"buffer i/o error",
            r"blk_update_request",
        ],
    ),

    # A service dying repeatedly is a pretty strong signal that something is wrong.
    _build_rule(
        "service failure",
        "medium",
        60,
        [
            r"failed with result",
            r"main process exited",
            r"start request repeated too quickly",
        ],
    ),

    # Repeated SSH / auth  failures are more security-flavored than just random noise.
    _build_rule(
        "authentication failure",
        "medium",
        50,
        [
            r"failed password",
            r"authentication failure",
            r"invalid user",
        ],
    ),

    # A little more specific than generic auth failure.
    _build_rule(
        "ssh brute force",
        "medium",
        55,
        [
            r"failed password for invalid user",
            r"maximum authentication attempts exceeded",
            r"received disconnect from .* too many authentication failures",
        ],
    ),

    # Sudo problems matter, but often they're still narrower than crashes/resource issues.
    _build_rule(
        "sudo failure",
        "medium",
        45,
        [
            r"sudo: .* incorrect password",
            r"sudo: .* authentication failure",
            r"sudo: unable to resolve host",
        ],
    ),

    # Very common in real logs, and often breaks scripts/services in annoying ways.
    _build_rule(
        "permission issue",
        "medium",
        40,
        [
            r"permission denied",
            r"operation not permitted",
            r"access denied",
        ],
    ),

    # Timeouts can be important, but they usually need context.
    _build_rule(
        "timeout",
        "medium",
        35,
        [
             r"timed out",
            r"connection timeout",
            r"watchdog",
        ],
    ),

    # DNS failures are worth splitting out because they show up a lot and can explain
    # why something "network-related" is broken even when the network is technically up.
    _build_rule(
        "dns failure",
        "low",
        30,
        [
            r"name or service not known",
            r"temporary failure in name resolution",
            r"could not resolve host",
        ],
    ),

    # Lower score because these can happen for lots of normal reasons too.
    _build_rule(
        "network issue",
        "low",
        25,
        [
            r"network is unreachable" ,
            r"connection refused",
            r"connection reset by peer",
        ],
    ),
]


def get_default_rules() -> list[LogRule]:
    return DEFAULT_RULES.copy()


def match_rules(line: str, rules: list[LogRule] | None = None) -> list[LogRule]:
    active_rules = rules if rules is not None else DEFAULT_RULES
    matches = []

    for rule in active_rules:
        if rule.matches(line):
            matches.append(rule)

    return matches


def best_match(line: str, rules: list[LogRule] | None = None) -> LogRule | None:
    matches = match_rules(line, rules)

    if not matches:
         return None

    return max(matches, key=lambda rule: rule.score)