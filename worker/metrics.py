from prometheus_client import Counter, Histogram

BUCKETS = [
    0.2,
    0.4,
    0.6,
    0.8,
    1.0,
    1.2,
    1.4,
    1.6,
    1.8,
    2.0,
    float('+inf'),
]

LATENCY = Histogram(
    "latency_seconds_worker",
    "Number of seconds",
)

TOTAL_REQ = Counter(
    'counter_handler_worker',
    'Считает то-то',
)
TOTAL_REQ.inc()

TOTAL_SEND_MESSAGES = Counter(
    'send_messages_worker',
    'Считает то-то',
)

TOTAL_REQ.inc()