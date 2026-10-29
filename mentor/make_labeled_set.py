"""Для автора/ментора: збирає розмічену копію набору з ключа.
Запуск з кореня репозиторію (де лежать sets/ і mentor/):
  python mentor/make_labeled_set.py l09_labels.lab          # -> sets/l09_labels.jsonl
  python mentor/make_labeled_set.py l09_lab_pool l09_lab_pool.labeled
Ключ читається з mentor/<набір>.key.jsonl. Сам ключ НЕ кладіть у sets/: це не набір кейсів
(loader вимагає input або turns і падає на ньому). Розмічену копію студентам не віддавати.
"""
import json, sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
src = sys.argv[1]
if not (root / "mentor" / f"{src}.key.jsonl").exists():
    sys.exit(f"Немає mentor/{src}.key.jsonl. Назва — це ім'я набору в sets/ без .jsonl, "
             f"наприклад l09_labels.lab, а не l09_labels.")
dst = sys.argv[2] if len(sys.argv) > 2 else src.replace(".lab", "")
key = {}
for l in (root / "mentor" / f"{src}.key.jsonl").read_text(encoding="utf-8").splitlines():
    if l.strip():
        k = json.loads(l); key[k["id"]] = k
out, n = [], 0
for l in (root / "sets" / f"{src}.jsonl").read_text(encoding="utf-8").splitlines():
    if not l.strip() or l.startswith("//"):
        continue
    c = json.loads(l)
    if c["id"] not in key:
        sys.exit(f"У ключі mentor/{src}.key.jsonl немає id {c['id']}: набір sets/{src}.jsonl "
                 f"і ключ з різних версій. Візьміть обидва файли з одного архіву.")
    k = key[c["id"]]; m = c["additional_metadata"]
    m["label"] = k["label"]; m["disputed"] = k["bucket"] != "obvious"
    if k.get("note") and m["disputed"]:
        m["why_disputed"] = k["note"]
    out.append(json.dumps(c, ensure_ascii=False)); n += 1
(root / "sets" / f"{dst}.jsonl").write_text("\n".join(out) + "\n", encoding="utf-8")
print(f"sets/{dst}.jsonl: {n} кейсів з міткою")
