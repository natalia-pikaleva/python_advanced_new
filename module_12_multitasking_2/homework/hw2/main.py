import subprocess


def process_count(username: str) -> int:
    result = subprocess.run(['pgrep', '-u', username, '-c'], stdout=subprocess.PIPE)
    if result:
        return result.stdout.decode()
    return 0


def volume_os_memory():
    free_process = subprocess.Popen(
        ['free', '-m'],
        stdout=subprocess.PIPE
    )

    grep_process = subprocess.Popen(
        ['grep', 'Mem'],
        stdin=free_process.stdout,
        stdout=subprocess.PIPE
    )

    free_process.stdout.close()

    awk_process = subprocess.Popen(
        ['awk', '{print $2}'],
        stdin=grep_process.stdout,
        stdout=subprocess.PIPE
    )

    grep_process.stdout.close()

    result, _ = awk_process.communicate()

    if result:
        return int(result)

    return 0


def total_memory_usage(root_pid: int) -> float:
    # суммарное потребление памяти древа процессов
    # с корнем root_pid в процентах
    ps_process = subprocess.Popen(
        ['ps', '--ppid', str(root_pid), '-o', 'rss'],
        stdout=subprocess.PIPE
    )

    awk_process = subprocess.Popen(
        ['awk', '{sum += $1} END {print sum}'],
        stdin=ps_process.stdout,
        stdout=subprocess.PIPE
    )

    ps_process.stdout.close()

    total_root_pid_memory, _ = awk_process.communicate()

    if total_root_pid_memory:
        total_os_memory = volume_os_memory() * 1024
        total_root_pid_memory = int(total_root_pid_memory)
        proc_memory = round(total_root_pid_memory / total_os_memory * 100, 2)
        return f'{proc_memory}%'
    return 0


if __name__ == "__main__":
    print('Количество процессов, запущенных пользователем pikaleva_natalya: ', process_count('pikaleva_natalya'))
    print('Суммарное потребление памяти древа процессов с корнем 1:', total_memory_usage(1))
