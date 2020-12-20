import re


class ScreenSizeCluster:

    @classmethod
    def get_value(cls, screen_sizes):
        pattern = '\d*[\.|,]?\d+'
        ret = []
        for size in screen_sizes:
            ssize = re.findall(pattern, size)[0]
            temp = str(int(float(ssize)))
            ret.append(temp)
        return ret