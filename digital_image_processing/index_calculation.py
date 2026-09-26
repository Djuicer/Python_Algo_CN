# Author: João Gustavo A. Amorim
# Author email: joaogustavoamorim@gmail.com
# Coding date:  jan 2019
# python/black: True

# 导入
import numpy as np


# 用于计算指数的类
class IndexCalculation:
    """
    # 类概述
        本算法用于计算植被指数，这些指数可用于精准农业或遥感等领域。
        类中提供了定义数据和计算已实现指数的函数。

    # 植被指数
        https://en.wikipedia.org/wiki/Vegetation_Index
        植被指数（Vegetation Index，VI）是对两个或更多波段进行的光谱变换，
        用于增强植被属性的贡献，并可靠地比较陆地光合活动和冠层结构变化
        在空间和时间上的差异。

    # 通道信息（各通道的波长范围）
        * nir - 近红外
            https://www.malvernpanalytical.com/br/products/technology/near-infrared-spectroscopy
            波长范围：700 nm 到 2500 nm
        * 红边
            https://en.wikipedia.org/wiki/Red_edge
            波长范围：680 nm 到 730 nm
        * red
            https://en.wikipedia.org/wiki/Color
            波长范围：635 nm 到 700 nm
        * blue
            https://en.wikipedia.org/wiki/Color
            波长范围：450 nm 到 490 nm
        * green
            https://en.wikipedia.org/wiki/Color
            波长范围：520 nm 到 560 nm


    # 已实现的指数列表
            #"abbreviationOfIndexName" -- 使用的通道列表

            #"ARVI2"            --  red, nir
            #"CCCI"             --  red, redEdge, nir
            #"CVI"              --  red, green, nir
            #"GLI"              --  red, green, blue
            #"NDVI"             --  red, nir
            #"BNDVI"            --  blue, nir
            #"redEdgeNDVI"      --  red, redEdge
            #"GNDVI"            --  green, nir
            #"GBNDVI"           --  green, blue, nir
            #"GRNDVI"           --  red, green, nir
            #"RBNDVI"           --  red, blue, nir
            #"PNDVI"            --  red, green, blue, nir
            #"ATSAVI"           --  red, nir
            #"BWDRVI"           --  blue, nir
            #"CIgreen"          --  green, nir
            #"CIrededge"        --  redEdge, nir
            #"CI"               --  red, blue
            #"CTVI"             --  red, nir
            #"GDVI"             --  green, nir
            #"EVI"              --  red, blue, nir
            #"GEMI"             --  red, nir
            #"GOSAVI"           --  green, nir
            #"GSAVI"            --  green, nir
            #"Hue"              --  red, green, blue
            #"IVI"              --  red, nir
            #"IPVI"             --  red, nir
            #"I"                --  red, green, blue
            #"RVI"              --  red, nir
            #"MRVI"             --  red, nir
            #"MSAVI"            --  red, nir
            #"NormG"            --  red, green, nir
            #"NormNIR"          --  red, green, nir
            #"NormR"            --  red, green, nir
            #"NGRDI"            --  red, green
            #"RI"               --  red, green
            #"S"                --  red, green, blue
            #"IF"               --  red, green, blue
            #"DVI"              --  red, nir
            #"TVI"              --  red, nir
            #"NDRE"               --  redEdge, nir

    # 所有已实现指数的列表
        #allIndex = ["ARVI2", "CCCI", "CVI", "GLI", "NDVI", "BNDVI", "redEdgeNDVI",
                    "GNDVI", "GBNDVI", "GRNDVI", "RBNDVI", "PNDVI", "ATSAVI",
                    "BWDRVI", "CIgreen", "CIrededge", "CI", "CTVI", "GDVI", "EVI",
                    "GEMI", "GOSAVI", "GSAVI", "Hue", "IVI", "IPVI", "I", "RVI",
                    "MRVI", "MSAVI", "NormG", "NormNIR", "NormR", "NGRDI", "RI",
                    "S", "IF", "DVI", "TVI", "NDRE"]

    # 不使用蓝色通道的指数列表
        #notBlueIndex = ["ARVI2", "CCCI", "CVI", "NDVI", "redEdgeNDVI", "GNDVI",
                         "GRNDVI", "ATSAVI", "CIgreen", "CIrededge", "CTVI", "GDVI",
                         "GEMI", "GOSAVI", "GSAVI", "IVI", "IPVI", "RVI", "MRVI",
                         "MSAVI", "NormG", "NormNIR", "NormR", "NGRDI", "RI", "DVI",
                         "TVI", "NDRE"]

    # 仅使用 RGB 通道的指数列表
        #RGBIndex = ["GLI", "CI", "Hue", "I", "NGRDI", "RI", "S", "IF"]
    """

    def __init__(
        self, red=None, green=None, blue=None, red_edge=None, nir=None
    ) -> None:
        self.set_matricies(red=red, green=green, blue=blue, red_edge=red_edge, nir=nir)

    def set_matricies(
        self, red=None, green=None, blue=None, red_edge=None, nir=None
    ) -> bool:
        if red is not None:
            self.red = red
        if green is not None:
            self.green = green
        if blue is not None:
            self.blue = blue
        if red_edge is not None:
            self.redEdge = red_edge
        if nir is not None:
            self.nir = nir
        return True

    def calculation(
        self, index="", red=None, green=None, blue=None, red_edge=None, nir=None
    ):
        """
        使用类中实例化的数值计算指数。
        :str index: 要计算的指数名称缩写
        """
        self.set_matricies(red=red, green=green, blue=blue, red_edge=red_edge, nir=nir)
        funcs = {
            "ARVI2": self.arv12,
            "CCCI": self.ccci,
            "CVI": self.cvi,
            "GLI": self.gli,
            "NDVI": self.ndvi,
            "BNDVI": self.bndvi,
            "redEdgeNDVI": self.red_edge_ndvi,
            "GNDVI": self.gndvi,
            "GBNDVI": self.gbndvi,
            "GRNDVI": self.grndvi,
            "RBNDVI": self.rbndvi,
            "PNDVI": self.pndvi,
            "ATSAVI": self.atsavi,
            "BWDRVI": self.bwdrvi,
            "CIgreen": self.ci_green,
            "CIrededge": self.ci_rededge,
            "CI": self.ci,
            "CTVI": self.ctvi,
            "GDVI": self.gdvi,
            "EVI": self.evi,
            "GEMI": self.gemi,
            "GOSAVI": self.gosavi,
            "GSAVI": self.gsavi,
            "Hue": self.hue,
            "IVI": self.ivi,
            "IPVI": self.ipvi,
            "I": self.i,
            "RVI": self.rvi,
            "MRVI": self.mrvi,
            "MSAVI": self.m_savi,
            "NormG": self.norm_g,
            "NormNIR": self.norm_nir,
            "NormR": self.norm_r,
            "NGRDI": self.ngrdi,
            "RI": self.ri,
            "S": self.s,
            "IF": self._if,
            "DVI": self.dvi,
            "TVI": self.tvi,
            "NDRE": self.ndre,
        }

        try:
            return funcs[index]()
        except KeyError:
            print("Index not in the list!")
            return False

    def arv12(self):
        """
        抗大气植被指数 2（Atmospherically Resistant Vegetation Index 2）
        https://www.indexdatabase.de/db/i-single.php?id=396
        :return: 指数
            -0.18+1.17*(self.nir-self.red)/(self.nir+self.red)
        """
        return -0.18 + (1.17 * ((self.nir - self.red) / (self.nir + self.red)))

    def ccci(self):
        """
        冠层叶绿素含量指数（Canopy Chlorophyll Content Index）
        https://www.indexdatabase.de/db/i-single.php?id=224
        :return: 指数
        """
        return ((self.nir - self.redEdge) / (self.nir + self.redEdge)) / (
            (self.nir - self.red) / (self.nir + self.red)
        )

    def cvi(self):
        """
        叶绿素植被指数（Chlorophyll Vegetation Index）
        https://www.indexdatabase.de/db/i-single.php?id=391
        :return: 指数
        """
        return self.nir * (self.red / (self.green**2))

    def gli(self):
        """
        绿叶指数（Green Leaf Index）
        https://www.indexdatabase.de/db/i-single.php?id=375
        :return: 指数
        """
        return (2 * self.green - self.red - self.blue) / (
            2 * self.green + self.red + self.blue
        )

    def ndvi(self):
        """
        self.nir/self.red 归一化差值植被指数（Normalized Difference Vegetation
        Index），校准 NDVI（CDVI）
        https://www.indexdatabase.de/db/i-single.php?id=58
        :return: 指数
        """
        return (self.nir - self.red) / (self.nir + self.red)

    def bndvi(self):
        """
        self.nir/self.blue 蓝光归一化差值植被指数
        https://www.indexdatabase.de/db/i-single.php?id=135
        :return: 指数
        """
        return (self.nir - self.blue) / (self.nir + self.blue)

    def red_edge_ndvi(self):
        """
        self.redEdge/self.red 归一化差值指数
        https://www.indexdatabase.de/db/i-single.php?id=235
        :return: 指数
        """
        return (self.redEdge - self.red) / (self.redEdge + self.red)

    def gndvi(self):
        """
        self.nir/self.green 绿色归一化差值植被指数（Green NDVI）
        https://www.indexdatabase.de/db/i-single.php?id=401
        :return: 指数
        """
        return (self.nir - self.green) / (self.nir + self.green)

    def gbndvi(self):
        """
        self.green-self.blue NDVI
        https://www.indexdatabase.de/db/i-single.php?id=186
        :return: 指数
        """
        return (self.nir - (self.green + self.blue)) / (
            self.nir + (self.green + self.blue)
        )

    def grndvi(self):
        """
        self.green-self.red NDVI
        https://www.indexdatabase.de/db/i-single.php?id=185
        :return: 指数
        """
        return (self.nir - (self.green + self.red)) / (
            self.nir + (self.green + self.red)
        )

    def rbndvi(self):
        """
        self.red-self.blue NDVI
        https://www.indexdatabase.de/db/i-single.php?id=187
        :return: 指数
        """
        return (self.nir - (self.blue + self.red)) / (self.nir + (self.blue + self.red))

    def pndvi(self):
        """
        全色 NDVI（Pan NDVI）
        https://www.indexdatabase.de/db/i-single.php?id=188
        :return: 指数
        """
        return (self.nir - (self.green + self.red + self.blue)) / (
            self.nir + (self.green + self.red + self.blue)
        )

    def atsavi(self, x=0.08, a=1.22, b=0.03):
        """
        调整型转换土壤调节植被指数
        https://www.indexdatabase.de/db/i-single.php?id=209
        :return: 指数
        """
        return a * (
            (self.nir - a * self.red - b)
            / (a * self.nir + self.red - a * b + x * (1 + a**2))
        )

    def bwdrvi(self):
        """
        蓝光宽动态范围植被指数
        https://www.indexdatabase.de/db/i-single.php?id=136
        :return: 指数
        """
        return (0.1 * self.nir - self.blue) / (0.1 * self.nir + self.blue)

    def ci_green(self):
        """
        绿色叶绿素指数
        https://www.indexdatabase.de/db/i-single.php?id=128
        :return: 指数
        """
        return (self.nir / self.green) - 1

    def ci_rededge(self):
        """
        红边叶绿素指数
        https://www.indexdatabase.de/db/i-single.php?id=131
        :return: 指数
        """
        return (self.nir / self.redEdge) - 1

    def ci(self):
        """
        着色指数（Coloration Index）
        https://www.indexdatabase.de/db/i-single.php?id=11
        :return: 指数
        """
        return (self.red - self.blue) / self.red

    def ctvi(self):
        """
        校正转换植被指数（Corrected Transformed Vegetation Index）
        https://www.indexdatabase.de/db/i-single.php?id=244
        :return: 指数
        """
        ndvi = self.ndvi()
        return ((ndvi + 0.5) / (abs(ndvi + 0.5))) * (abs(ndvi + 0.5) ** (1 / 2))

    def gdvi(self):
        """
        self.nir/self.green 绿色差值植被指数
        https://www.indexdatabase.de/db/i-single.php?id=27
        :return: 指数
        """
        return self.nir - self.green

    def evi(self):
        """
        增强植被指数（Enhanced Vegetation Index）
        https://www.indexdatabase.de/db/i-single.php?id=16
        :return: 指数
        """
        return 2.5 * (
            (self.nir - self.red) / (self.nir + 6 * self.red - 7.5 * self.blue + 1)
        )

    def gemi(self):
        """
        全球环境监测指数（Global Environment Monitoring Index）
        https://www.indexdatabase.de/db/i-single.php?id=25
        :return: 指数
        """
        n = (2 * (self.nir**2 - self.red**2) + 1.5 * self.nir + 0.5 * self.red) / (
            self.nir + self.red + 0.5
        )
        return n * (1 - 0.25 * n) - (self.red - 0.125) / (1 - self.red)

    def gosavi(self, y=0.16):
        """
        绿色优化土壤调节植被指数
        https://www.indexdatabase.de/db/i-single.php?id=29
        其中 Y = 0,16
        :return: 指数
        """
        return (self.nir - self.green) / (self.nir + self.green + y)

    def gsavi(self, n=0.5):
        """
        绿色土壤调节植被指数
        https://www.indexdatabase.de/db/i-single.php?id=31
        其中 N = 0,5
        :return: 指数
        """
        return ((self.nir - self.green) / (self.nir + self.green + n)) * (1 + n)

    def hue(self):
        """
        色相（Hue）
        https://www.indexdatabase.de/db/i-single.php?id=34
        :return: 指数
        """
        return np.arctan(
            ((2 * self.red - self.green - self.blue) / 30.5) * (self.green - self.blue)
        )

    def ivi(self, a=None, b=None):
        """
        理想植被指数（Ideal Vegetation Index）
        https://www.indexdatabase.de/db/i-single.php?id=276
        b=植被线截距
        a=土壤线斜率
        :return: 指数
        """
        return (self.nir - b) / (a * self.red)

    def ipvi(self):
        """
        红外百分比植被指数
        https://www.indexdatabase.de/db/i-single.php?id=35
        :return: 指数
        """
        return (self.nir / ((self.nir + self.red) / 2)) * (self.ndvi() + 1)

    def i(self):
        """
        强度（Intensity）
        https://www.indexdatabase.de/db/i-single.php?id=36
        :return: 指数
        """
        return (self.red + self.green + self.blue) / 30.5

    def rvi(self):
        """
        比值植被指数（Ratio Vegetation Index）
        http://www.seos-project.eu/modules/remotesensing/remotesensing-c03-s01-p01.html
        :return: 指数
        """
        return self.nir / self.red

    def mrvi(self):
        """
        改进归一化差值植被指数 RVI
        https://www.indexdatabase.de/db/i-single.php?id=275
        :return: 指数
        """
        return (self.rvi() - 1) / (self.rvi() + 1)

    def m_savi(self):
        """
        改进土壤调节植被指数
        https://www.indexdatabase.de/db/i-single.php?id=44
        :return: 指数
        """
        return (
            (2 * self.nir + 1)
            - ((2 * self.nir + 1) ** 2 - 8 * (self.nir - self.red)) ** (1 / 2)
        ) / 2

    def norm_g(self):
        """
        归一化 G
        https://www.indexdatabase.de/db/i-single.php?id=50
        :return: 指数
        """
        return self.green / (self.nir + self.red + self.green)

    def norm_nir(self):
        """
        归一化 self.nir
        https://www.indexdatabase.de/db/i-single.php?id=51
        :return: 指数
        """
        return self.nir / (self.nir + self.red + self.green)

    def norm_r(self):
        """
        归一化 R
        https://www.indexdatabase.de/db/i-single.php?id=52
        :return: 指数
        """
        return self.red / (self.nir + self.red + self.green)

    def ngrdi(self):
        """
        self.green/self.red 归一化差值指数，即绿色可见光抗大气指数（VIself.green）
        https://www.indexdatabase.de/db/i-single.php?id=390
        :return: 指数
        """
        return (self.green - self.red) / (self.green + self.red)

    def ri(self):
        """
        self.red/self.green 归一化差值红度指数
        https://www.indexdatabase.de/db/i-single.php?id=74
        :return: 指数
        """
        return (self.red - self.green) / (self.red + self.green)

    def s(self):
        """
        饱和度（Saturation）
        https://www.indexdatabase.de/db/i-single.php?id=77
        :return: 指数
        """
        max_value = np.max([np.max(self.red), np.max(self.green), np.max(self.blue)])
        min_value = np.min([np.min(self.red), np.min(self.green), np.min(self.blue)])
        return (max_value - min_value) / max_value

    def _if(self):
        """
        形状指数（Shape Index）
        https://www.indexdatabase.de/db/i-single.php?id=79
        :return: 指数
        """
        return (2 * self.red - self.green - self.blue) / (self.green - self.blue)

    def dvi(self):
        """
        self.nir/self.red 简单比值差值植被指数，即植被指数数值（VIN）
        https://www.indexdatabase.de/db/i-single.php?id=12
        :return: 指数
        """
        return self.nir / self.red

    def tvi(self):
        """
        转换植被指数（Transformed Vegetation Index）
        https://www.indexdatabase.de/db/i-single.php?id=98
        :return: 指数
        """
        return (self.ndvi() + 0.5) ** (1 / 2)

    def ndre(self):
        return (self.nir - self.redEdge) / (self.nir + self.redEdge)


"""
# 生成随机矩阵以测试此类
red     = np.ones((1000,1000, 1),dtype="float64") * 46787
green   = np.ones((1000,1000, 1),dtype="float64") * 23487
blue    = np.ones((1000,1000, 1),dtype="float64") * 14578
redEdge = np.ones((1000,1000, 1),dtype="float64") * 51045
nir     = np.ones((1000,1000, 1),dtype="float64") * 52200

# 此类的使用示例

# 实例化该类
cl = IndexCalculation()

# 使用给定值实例化该类
#cl = indexCalculation(red=red, green=green, blue=blue, redEdge=redEdge, nir=nir)

# 实例化 cl 后如何设置值（用于更新数据，或未使用给定值实例化该类时）
cl.setMatrices(red=red, green=green, blue=blue, redEdge=redEdge, nir=nir)

# 计算类中已实例化数据的指数
    # 注意：可将 CCCI 换成此类实现的任意指数。
indexValue_form1    = cl.calculation("CCCI", red=red, green=green, blue=blue,
                                     redEdge=redEdge, nir=nir).astype(np.float64)
indexValue_form2    = cl.CCCI()

# 直接使用给定值计算指数——只需设置所需的值
# 注意：*calculation* 函数会调用 *setMatrices*
indexValue_form3    = cl.calculation("CCCI", red=red, green=green, blue=blue,
                                     redEdge=redEdge, nir=nir).astype(np.float64)

print("Form 1: "+np.array2string(indexValue_form1, precision=20, separator=', ',
      floatmode='maxprec_equal'))
print("Form 2: "+np.array2string(indexValue_form2, precision=20, separator=', ',
      floatmode='maxprec_equal'))
print("Form 3: "+np.array2string(indexValue_form3, precision=20, separator=', ',
      floatmode='maxprec_equal'))

# 不同数据类型下的 NDVI 示例结果列表
# float16 ->    0.31567383              #NDVI (red = 50, nir = 100)
# float32 ->    0.31578946              #NDVI (red = 50, nir = 100)
# float64 ->    0.3157894736842105      #NDVI (red = 50, nir = 100)
# longdouble -> 0.3157894736842105      #NDVI (red = 50, nir = 100)
"""
