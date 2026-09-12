# Written for this repository from the public problem statement; no external submission used.
import sys


def main():
    tokens = sys.stdin.read().split()
    if not tokens:
        return
    student_number_n = int(tokens[0])
    headers = tokens[1:8]
    rows = []
    pos = {name: i for i, name in enumerate(headers)}
    at = 8
    for _ in range(student_number_n):
        fields = tokens[at:at + 7]
        at += 7
        row = {name: fields[pos[name]] for name in headers}
        row["Chinese"] = int(row["Chinese"])
        row["Math"] = int(row["Math"])
        row["English"] = int(row["English"])
        row["Height"] = float(row["Height"])
        rows.append(row)

    best_score = max(r["Chinese"] + r["Math"] + r["English"] for r in rows)
    best_name = min(r["Name"] for r in rows if r["Chinese"] + r["Math"] + r["English"] == best_score)
    out = [f"{best_name} {best_score}"]

    quarters = [[] for _ in range(4)]
    for r in rows:
        month = int(r["Birth"].split("-")[1])
        quarters[(month - 1) // 3].append(r["Height"])
    for i, values in enumerate(quarters, 1):
        average = sum(values) / len(values) if values else 0.0
        out.append(f"Q{i} {len(values)} {average:.1f}")

    girls = [r for r in rows if r["Gender"] == "F" and
             (r["Chinese"] + r["Math"] + r["English"]) / 3 >= 80.0 and
             min(r["Chinese"], r["Math"], r["English"]) >= 70]
    girls.sort(key=lambda r: (-(r["Chinese"] + r["Math"] + r["English"]), r["Name"]))
    out.append(str(len(girls)))
    out.extend(f"{r['Name']} {r['Chinese']} {r['Math']} {r['English']} {r['Chinese'] + r['Math'] + r['English']}" for r in girls)
    print("\n".join(out))


if __name__ == "__main__":
    main()
