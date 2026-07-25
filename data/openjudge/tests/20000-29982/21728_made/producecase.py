import random, subprocess, tempfile
from pathlib import Path
REFERENCE_SOURCE = 'def main():\n    n = int(input())\n    # Read experiment durations. There are n numbers.\n    durations = list(map(int, input().split()))\n    # Read the order of students. There are n numbers.\n    order = list(map(int, input().split()))\n\n    total_waiting_time = 0\n    current_time = 0\n    # Process students in the given order.\n    for student in order:\n        total_waiting_time += current_time\n        # Convert student id (1-indexed) to index (0-indexed)\n        current_time += durations[student - 1]\n\n    average_waiting_time = total_waiting_time / n\n    # Output the average waiting time rounded to two decimals.\n    print(f"{average_waiting_time:.2f}")\n\n\nif __name__ == "__main__":\n    main()\n'
SAMPLE_IN = '10\n81 365 72 99 22 7 444 203 1024 203\n6 5 3 1 4 8 10 2 7 9\n'
SAMPLE_OUT = '431.90\n'
def generate_case(r):
    n = r.randint(2, 30); durations = [r.randint(1, 1000) for _ in range(n)]; order = list(range(1, n + 1)); r.shuffle(order)
    assert all(x > 0 for x in durations) and sorted(order) == list(range(1, n + 1))
    return f"{n}\n" + " ".join(map(str, durations)) + "\n" + " ".join(map(str, order)) + "\n"

assert SAMPLE_IN == '10\n81 365 72 99 22 7 444 203 1024 203\n6 5 3 1 4 8 10 2 7 9\n'
with tempfile.NamedTemporaryFile("w", suffix=".py", encoding="utf-8") as handle:
    handle.write(REFERENCE_SOURCE); handle.flush()
    root = Path(__file__).parent / "data"
    seen = [SAMPLE_IN]
    for index in range(20):
        if index == 0:
            content = SAMPLE_IN
        else:
            for attempt in range(100):
                content = generate_case(random.Random(21728 + index + attempt * 1000))
                if content not in seen: break
            else: raise AssertionError('insufficient diversity')
        seen.append(content)
        result = subprocess.run(["python3", handle.name], input=content, text=True, capture_output=True, timeout=10, check=True)
        (root / f"{index}.in").write_text(content, encoding="utf-8")
        (root / f"{index}.out").write_text(result.stdout, encoding="utf-8")
