with open("playerData.txt", "r") as f:
    content = f.readlines()
print('read')
with open("playerData.txt", "w") as f:
    for line in content:
        print(line + '------------')
        if line.startswith('Tropic Mango#6755' + '~'):
            print('found')
            splice_line = line.split('|')
            splice_line[1] = int(splice_line[1]) + 10
            n_line = '|'.join(str(e) for e in splice_line)
            f.write(n_line + '\n')
        else:
            f.write(line)
