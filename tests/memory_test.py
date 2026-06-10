from memory.memory import save_weight_log, get_weight_logs


save_weight_log(
    1,
    89
)

save_weight_log(
    1,
    88.5
)

save_weight_log(
    1,
    88
)

print(
    get_weight_logs(1)
)