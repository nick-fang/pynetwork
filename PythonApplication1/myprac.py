
"""使用内置函数str.replace()"""
source = r'D:/icnet/data/cityscape/leftImg8bit/train\aachen'
source.replace('\\', '/')



"""使用re库"""
import re
source = r'D:/icnet/data/cityscape/leftImg8bit/train\aachen'
re.search(pattern=r'\\\w', string=source)
re.search(pattern='(\\\\)(\\w)', string=source)




