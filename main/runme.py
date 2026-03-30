# 数据生成指南
# 单轴压缩试验



# Step1 环境设置

# - 将`cosim`修改为你安装的CoSim软件所附带的python环境路径。
# TODO
cosim = "D:\CoSim\python\python.exe" # CoSim提供的python环境路径



# Step 2 指定材料参数

# - `matPlate`是压缩板的材料参数，不用修改。
matPlate = {
        'Dens': 2.4e+07, # 密度，单位kg/m^3
        'E': 5e+09, # 杨氏模量，单位Pa
        'Pois': 0.2, # 泊松比
        'StaticFric': 40, # 静摩擦角，单位度
        'DynamicFric': 40 # 动摩擦角，单位度
        }

# - 我们需要按照选定的岩石类型，为样品设定材料参数。这里以**花岗岩**为例。

# 1. 选择**1**个常见的密度值，储存在列表`list_Dens`中。
# 查询资料得知：花岗岩的密度范围为2630~2750kg/m^3，因此设定list_Dens如下
# TODO
list_Dens = [2700] # 单位kg/m^3
# 为适配Cosim所作的处理
for i in range(len(list_Dens)):
    list_Dens[i] = list_Dens[i] * 1e+4

# 2. 选择**3**个常见的杨氏模量值，储存在列表`list_E`中。
# 查询资料得知：花岗岩的杨氏模量范围为50~100GPa，因此设定list_E如下
# TODO
list_E = [5e+10, 7.5e+10, 1e+11] # 单位Pa

# 3. 选择**3**个常见的泊松比值，储存在列表`list_Pois`中。
# 查询资料得知：花岗岩的泊松比范围为0.26~0.29，因此设定list_Pois如下
# TODO
list_Pois = [0.26, 0.275, 0.29]

# 4. 在常见范围内，设置**静摩擦角**的最大值和最小值。
# 查询资料得知：花岗岩的静摩擦角范围为45°~60°，因此设定如下
# TODO
minimum = 45 # 单位度
maximum = 60 # 单位度
# 自动计算
num = 6
step = (maximum - minimum) / (num - 1)
list_StaticFric = [(minimum + i * step) for i in range(num)]

# 5. 在常见范围内，设置**正黏聚力**的最大值和最小值。
# 查询资料得知：花岗岩的正黏聚力范围为10~50MPa，因此设定如下
# TODO
minimum = 1e+7 # 单位Pa
maximum = 5e+7 # 单位Pa
# 自动计算
num = 11
step = (maximum - minimum) / (num - 1)
list_normalCohesion = [(minimum + i * step) for i in range(num)]



# Step 3 DEM计算

import os
import json
import shutil
from random import randint


def log_params(dir: str, name:str, params: dict):
    """"""
    with open(os.path.join(dir, f"{name}.json"), "w") as f:
        json.dump(params, f)


index = 0

for StaticFric in list_StaticFric:
    for normalCohesion in list_normalCohesion:
        print("*" * 64)
        print(f"StaticFric: {StaticFric}")
        print(f"normalCohesion: {normalCohesion}")

        for i in range(6):
            print(f">> Done: {i}/6")

            Dens = list_Dens[randint(0, len(list_Dens) - 1)]
            E = list_E[randint(0, len(list_E) - 1)]
            Pois = list_Pois[randint(0, len(list_Pois) - 1)]

            # 根据 E ≈ 2G(1+ν) ，计算拉伸模量
            Et = E / (2 * (1 + Pois))
            # StaticFric = DynamicFric + 3
            DynamicFric = StaticFric - 3
            # normalCohesion = 1.2 shearCohesion
            shearCohesion = normalCohesion / 1.2

            # 设置样品材料参数
            matSample = {
                    'Dens': Dens, # 密度，单位kg/m^3
                    'E': E, # 杨氏模量，单位Pa
                    'Et': Et, # 拉伸模量，单位Pa
                    'Pois': Pois, # 泊松比
                    'StaticFric': StaticFric, # 静摩擦角，单位度
                    'DynamicFric': DynamicFric, # 动摩擦角，单位度
                    'Rc': 0.99, # 恢复系数
                    'normalCohesion': normalCohesion, # 正黏聚力，单位Pa
                    'shearCohesion': shearCohesion, # 切黏聚力，单位Pa
                    'isFricReduction': True,
                    'Vc': 5,
                    'A': 0.5
                    }

            save_dir = f"outputs/{index}"
            index += 1
            log_params(os.getcwd(), "matPlate", matPlate)
            log_params(os.getcwd(), "matSample", matSample)

            print("=" * 64)
            os.system(f"{cosim} DEM.py --dir {save_dir}")
            print("=" * 64)
