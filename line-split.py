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
# output_fls = int(input('请输入分割后每文件行数:\n'))
# output_fnh = input('请输入分割后文件名:\n')
output_fls = int(input_with_locale('请输入分割后每文件行数:\n', 'Please input the number of lines per file:\n'))
output_fnh = input_with_locale('请输入分割后文件名:\n', 'Please input the file name after splitting:\n')


def split_file(input_file, output_prefix, num_lines_per_file):
    # 用UTF-8编码打开文件
    with codecs.open(input_file, 'r', encoding='utf-8') as f:
        # 为当前行号创建一个计数器
        line_number = 1
        # 为当前输出文件数创建一个计数器
        file_number = 1
        # 使用正确的文件编号创建输出文件
        output_file = codecs.open(f'{output_prefix}_{file_number}.txt', 'w', encoding='utf-8')

        # 遍历输入文件中的行
        for line in f:
            # 将行写入输出文件
            output_file.write(line)
            # 增加行计数器
            line_number += 1
            # 如果行计数器大于每个文件的行数，
            # 关闭输出文件，递增文件计数器，并创建一个新的输出文件
            if line_number > num_lines_per_file:
                output_file.close()
                file_number += 1
                line_number = 1
                output_file = codecs.open(f'{output_prefix}_{file_number}.txt', 'w', encoding='utf-8')

        # 关闭最后一个输出文件
        output_file.close()


split_file(input_fn, output_fnh, output_fls)  # 调用函数分割
