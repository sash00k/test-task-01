import json
import re
import time


# какое-то неочевидное поле "дст" было в файле результатов, никакого пояснения по нему я не нашел,
# и не заметил, чтобы оно как-то фигурировало в итоговом файле - просто не использовал его

# какие-то лишние нецифровые символы были перед первым номером в обоих файлах
# решил эту особенность формата данных обработать отдельно в следующей функции


def fix_number_format(_number_: str) -> int:
    return int(re.findall(r'\d+', str(_number_))[0])


def main():

    competitors = json.load(open('competitors2.json'))
    for number in frozenset(competitors.keys()):
        correct_number = fix_number_format(number)
        competitors[correct_number] = competitors.pop(number)

    for row in open('results_RUN.txt').read().splitlines():
        line = row.replace(',', ' ').split(' ')

        number = fix_number_format(line[0])
        competitors[number][line[1]] = time.mktime(time.strptime(line[2], '%H:%M:%S'))

    for number in competitors.keys():
        if 'finish' in competitors[number] and 'start' in competitors[number]:
            result = time.strftime('%H:%M,%S', time.gmtime(competitors[number]['finish']-competitors[number]['start']))
        else:
            result = 'no result'
        competitors[number]['result'] = result

    results = [(num, data['Name'], data['Surname'], data['result']) for num, data in competitors.items()]
    results.sort(key=lambda x: (x[3], x[2], x[1], x[0]))

    output = open('results.csv', 'w')
    output.write('Место\tНагрудный номер\tИмя\tФамилия\tРезультат\n')
    for result, i in zip(results, range(len(results))):
        output.write(str(i+1)+'\t'+'\t'.join(map(str, result))+'\n')


if __name__ == "__main__":
    main()
