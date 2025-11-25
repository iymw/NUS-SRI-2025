import pandas as pd
import random
import re
import os

rows = 250

file_raw_name = f"./Data/Test/raw_{rows}.csv"
file_ins_name = f"./Data/Test/ins_{rows}.txt"
file_res_name = f"./Data/Test/res_{rows}.csv"

file_raw_name_with_typos = f"./Data/Test/raw_{rows}_with_typos.csv"
file_ins_name_with_typos = f"./Data/Test/ins_{rows}_with_typos.txt"
file_res_name_with_typos = f"./Data/Test/res_{rows}_with_typos.csv"

columns = [
    'Pendidikan Agama',
    'Pendidikan Pancasila',
    'Bahasa Indonesia',
    'Bahasa Inggris',
    'Matematika',
    'Fisika',
    'Kimia',
    'Biologi'
]

typos = {
    "read": [
        "Red the value of '{col}' for NISN Siswa {nisn}",
        "Reed the value of '{col}' for NISN Siswa {nisn}",
        "Read the val of '{col}' for NISN Siswa {nisn}",
        "Read value '{col}' NISN {nisn}",
        "Read the value of {col} for student {nisn}"
    ],
    "update": [
        "Updat NISN Siswa {nisn} with values: {updates}",
        "Update NISN Siswa {nisn} values {updates}",
        "Update student {nisn} with vals: {updates}",
        "Update NISN Siswa {nisn} wth values: {updates}",
        "Uppdate NISN Siswa {nisn} with values {updates}"
    ],
    "delete": [
        "Delet the entry with NISN Siswa {nisn}",
        "Delete entry NISN {nisn}",
        "Delte the entry with NISN Siswa {nisn}",
        "Delete the record of student {nisn}",
        "Delete the entry with NIS {nisn}"
    ]
}

arr = []
ids = set()


def generate_nisn():
    return random.randint(1000000000, 9999999999)


for _ in range(100):
    nisn = generate_nisn()
    if (nisn in ids):
        while nisn in ids:
            nisn = generate_nisn()
    ids.add(nisn)

    row = {"NISN Siswa": nisn, **{x: "" for x in columns}}
    arr.append(row)

df_raw = pd.DataFrame(arr)
df_raw.to_csv(file_raw_name, index=False)

df = pd.read_csv(file_raw_name, dtype={'NISN Siswa': str})
list_nisn_siswa = df['NISN Siswa'].tolist()

perintah = ['read', 'update', 'delete']

arr = []
arr_typos = []

for i in range(rows):
    op = random.choices(
        perintah, weights=[0.2, 0.5, 0.3], k=1)[0]

    random_id = random.choice(list_nisn_siswa)
    num = i + 1

    match op:
        case "read":
            col = random.choice(columns)
            arr.append(
                [num, f"Read the value of '{col}' for NISN Siswa {random_id}"])
            arr_typos.append(
                [num, random.choice(typos['read']).format(col=col, nisn=random_id)])
        case "update":
            num_cols_to_update = random.randint(1, len(columns))
            selected_cols = random.sample(columns, num_cols_to_update)
            updates = {col: random.randint(50, 100) for col in selected_cols}
            update_str = ", ".join(
                f"{col}: {val}" for col, val in updates.items())
            arr.append(
                [num, f"Update NISN Siswa {random_id} with values: {update_str}"])
            arr_typos.append(
                [num, random.choice(typos['update']).format(nisn=random_id, updates=update_str)])
        case _:
            arr.append([num, f"Delete the entry with NISN Siswa {random_id}"])
            arr_typos.append(
                [num, random.choice(typos['delete']).format(nisn=random_id)])
            list_nisn_siswa.remove(random_id)

with open(file_ins_name, "w") as file:
    for num, line in arr:
        file.write(f"{num}. {line}\n")

with open(file_ins_name_with_typos, "w") as file:
    for num, line in arr_typos:
        file.write(f"{num}. {line}\n")

with open(file_ins_name, "r") as file:
    perintah = file.readlines()

for line in perintah:
    line = line.strip()
    if not line:
        continue
    line = line.split(". ", 1)[1]

    ins = "Read" if line.startswith(
        "Read") else "Update" if line.startswith("Update") else "Delete"

    match ins:
        case "Read":
            col = re.search(r"Read the value of '(.+?)'", line).group(1)
            nisn = re.search(r"NISN Siswa (\d+)", line).group(1)
            row = df[df['NISN Siswa'] == nisn]
            value = row.iloc[0][col]
            print(f"Read: NISN Siswa {nisn} {col} = {value}")
        case "Update":
            nisn_match = re.search(r"Update NISN Siswa (\d+)", line)
            values_match = re.search(r"values: (.+)$", line)

            nisn = nisn_match.group(1) if nisn_match else None
            updates_str = values_match.group(1) if values_match else ""

            updates = {}
            if updates_str:
                pairs = [pair.strip() for pair in updates_str.split(",")]
                for pair in pairs:
                    if ": " in pair:
                        key, val = pair.split(": ", 1)
                        updates[key] = int(val)

            idx = df.index[df['NISN Siswa'] == nisn]
            for col, val in updates.items():
                df.at[idx[0], col] = str(val)
        case _:
            nisn = re.search(r"NISN Siswa (\d+)", line).group(1)
            df = df[df['NISN Siswa'] != nisn]

df.to_csv(file_res_name, index=False)

os.rename(file_raw_name, file_raw_name_with_typos)
os.remove(file_ins_name)
os.rename(file_res_name, file_res_name_with_typos)

print("Done")
