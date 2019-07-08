# 放置一些小方法，用来做特殊的功能

def str_to_list(s):
    """
    当一个list通过str方法之间转换成了字符串，可以通过该方法还原成原列表,
    当列表中的元素含有列表时该方法不适合
    :param s:通过str之间转换成字符串的list列表，即字符串为列表格式
    :return :列表样式的字符串还原成列表类型
    """
    return s.replace("[","").replace("]","").replace("'","").replace('"', '').split(",")