"""
@author: lxy
@email: linxy59@mail2.sysu.edu.cn
@date: 2021/9/27
@description: null
"""
import re


def filter_tags(x):
    """
    # Python通过正则表达式去除(过滤)HTML标签
    :param x:
    :return:
    """
    # 先过滤CDATA
    re_cdata = re.compile('//<!\
    CDATA\[[ >]∗ //\
    CDATA\[[ >]∗ //\
    \] > ', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)
    # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)
    # style
    re_br = re.compile('<br\s*?/?>')
    # 处理换行
    re_h = re.compile('</?\w+[^>]*>')
    # HTML标签
    re_comment = re.compile('<!--[^>]*-->')

    # HTML注释
    s = re_cdata.sub('', x)
    # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)
    # 去掉style
    s = re_br.sub('\n', s)
    # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)
    # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    return s


def replace_char_entity(x):
    """
    :param x:HTML字符串
    :function:过滤HTML中的标签
    """
    CHAR_ENTITIES = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }

    re_charEntity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_charEntity.search(x)
    while sz:
        entity = sz.group()  # entity全称，如>
        key = sz.group('name')  # 去除&;后entity,如>为gt
        try:
            x = re_charEntity.sub(CHAR_ENTITIES[key], x, 1)
            sz = re_charEntity.search(x)
        except KeyError:
            # 以空串代替
            x = re_charEntity.sub('', x, 1)
            sz = re_charEntity.search(x)
    return x


def remove_empty_lines(x):
    lines = [line.strip() for line in x.split()]
    lines = [line for line in lines if len(line) > 0]
    return "\n".join(lines)


def replace_with_hunman_read(x):
    return str(x).replace('<p>&nbsp; &nbsp; &nbsp; &nbsp;', '') \
        .replace('</p><p><br></p>', '') \
        .replace('<br>', '').replace('</p>', '').replace('<p>', '').replace('       ', '').replace('[图片]', '').strip()


def cleaning_data(x):
    chain = [
        replace_with_hunman_read,
        filter_tags,
        replace_char_entity,
        remove_empty_lines,
    ]
    for f in chain:
        x = f(x)
    return x
