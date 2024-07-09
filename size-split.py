# txt-split by shingyu
#
# To the extent possible under law, the person who associated CC0 with
# txt-split has waived all copyright and related or neighboring rights
# to txt-split.
#
# You should have received a copy of the CC0 legalcode along with this
# work.  If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.


import codecs
import sys
import re
import locale

CN = False
default_lang, _ = locale.getdefaultlocale()
if default_lang.startswith('zh'):
    CN = True
else:
    CN = False


def print_with_locale(msgcn, msgen):
    if CN:
        print(msgcn)
    else:
        print(msgen)


def input_with_locale(msgcn, msgen):
    if CN:
        return input(msgcn)
    else:
        return input(msgen)


# 获取命令行参数或输入
if len(sys.argv) < 2:
    # input_fn = input('请输入分割文件名/路径(可直接拖入文件):\n(也可将文件拖动到exe文件上分割):\n')
    input_fn = input_with_locale('请输入分割文件名/路径(可直接拖入文件):\n(也可将文件拖动到exe文件上分割):\n',
                                 'Please input the file name/path to split:\n'
                                 '(You can drag the file to the exe file to split):\n')
else:
    input_fn = sys.argv[1]

# 获取分割后文件信息
# size_input = input('请输入分割后每文件大小（如10MiB, 20MB, 300KB, 500KiB）:\n')
# output_fnh = input('请输入分割后文件名:\n')
size_input = input_with_locale('请输入分割后每文件大小（如10MiB, 20MB, 300KB, 500KiB）:\n',
                               'Please input the size of each file after splitting:\n'
                               '(such as 10MiB, 20MB, 300KB, 500KiB):\n')
output_fnh = input_with_locale('请输入分割后文件名:\n', 'Please input the file name after splitting:\n')


def parse_size(size_str):
    units = {"B": 1, "KB": 10**3, "MB": 10**6, "GB": 10**9, "TB": 10**12,
             "KiB": 2**10, "MiB": 2**20, "GiB": 2**30, "TiB": 2**40}
    size_str = size_str.upper().replace(" ", "")
    match = re.match(r"(\d+(?:\.\d+)?)([KMGT]?I?B)", size_str)
    if not match:
        raise ValueError("Invalid size string")
    size, unit = match.groups()
    size = float(size)
    return int(size * units[unit])


def split_file_by_size(input_file, output_prefix, max_size):
    # 用UTF-8编码打开文件
    with codecs.open(input_file, 'r', encoding='utf-8') as f:
        # 为当前输出文件数创建一个计数器
        file_number = 1
        # 使用正确的文件编号创建输出文件
        output_file = codecs.open(f'{output_prefix}_{file_number}.txt', 'w', encoding='utf-8')
        current_size = 0

        # 遍历输入文件中的行
        for line in f:
            line_size = len(line.encode('utf-8'))
            # 如果当前大小加上新行的大小超过最大大小，关闭当前文件并创建一个新文件
            if current_size + line_size > max_size:
                output_file.close()
                file_number += 1
                current_size = 0
                output_file = codecs.open(f'{output_prefix}_{file_number}.txt', 'w', encoding='utf-8')

            # 写入新行并更新当前文件大小
            output_file.write(line)
            current_size += line_size

        # 关闭最后一个输出文件
        output_file.close()


# 解析输入大小
output_size = parse_size(size_input)

# 使用输入文件和每个输出文件的指定大小测试函数
split_file_by_size(input_fn, output_fnh, output_size)  # 调用函数分割
