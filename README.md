# 基于 DEM 模拟与机器学习的岩石单轴压缩试验研究

# Rock Uniaxial Compression Test: DEM Simulation & Machine Learning

## 项目背景 | Background

本项目为清华大学水利水电工程系徐文杰老师《工程地质》课程的研究项目。

项目使用离散元法（DEM）模拟 15 种岩石的单轴压缩试验，从力-位移曲线中提取特征，并基于机器学习实现：

- **岩石分类**：根据力学响应特征识别岩石类型
- **参数回归**：从力学响应预测摩擦角和黏聚力等材料参数

This is a research project for the *Engineering Geology* course taught by Prof. Xu Wenjie at the Department of Hydraulic Engineering, Tsinghua University.

The project uses the Discrete Element Method (DEM) to simulate uniaxial compression tests on 15 rock types, extracts features from force-displacement curves, and applies machine learning for:

- **Rock classification**: identifying rock types from mechanical response features
- **Parameter regression**: predicting material parameters (friction angle, cohesion) from mechanical responses

## 方法概述 | Methodology

```
材料参数设定 → CoSim DEM 模拟 → 力-位移曲线 → 特征工程 → 机器学习（分类 / 回归）
```

1. **数据生成**：通过 CoSim 软件，对每种岩石在不同材料参数组合下运行 DEM 单轴压缩模拟，每种岩石约 396 组模拟
2. **特征工程**：从力-位移曲线中提取 9 个特征（峰值力、峰值位移、曲线下面积等）
3. **机器学习**：
   - 分类：Logistic Regression, Decision Tree, Random Forest, Naive Bayes, KNN, SVM, AdaBoost, Gradient Boosting
   - 回归：预测静摩擦角（tan(StaticFric)）和正黏聚力（normalCohesion）

## 岩石类型 | Rock Types

共 15 种岩石，分为 4 组：

| A 组 | B 组 | C 组 | D 组 |
|------|------|------|------|
| 砂岩 Sandstone | 安山岩 Andesite | 片麻岩 Gneiss | 砾岩 Conglomerate |
| 流纹岩 Rhyolite | 闪长岩 Diorite | 板岩 Slate | 页岩 Shale |
| 花岗岩 Granite | 辉长岩 Gabbro | 石英岩 Quartzite | 石灰岩 Limestone |
| 正长岩 Syenite | 玄武岩 Basalt | 大理岩 Marble | 白云岩 Dolomite |

## 项目结构 | Project Structure

```
UniaxialCompression/
├── main/                        # DEM 模拟相关文件
│   ├── runme.py                 # 数据生成主脚本（遍历参数组合，调用 DEM 模拟）
│   ├── DEM.py                   # CoSim DEM 模拟封装
│   ├── main_top.stl             # 上压板 3D 模型
│   ├── main_bot.stl             # 下压板 3D 模型
│   └── main_sample.poly         # 岩石样品多面体模型
├── base.py                      # 数据加载与特征工程
├── ml.ipynb                     # 机器学习分析 notebook（分类 + 回归）
├── data/                        # 模拟结果数据（15 种岩石 × ~396 组）
│   └── <岩石名>/
│       └── <编号>/
│           ├── main_top_History.txt   # 力-位移时程数据
│           ├── matSample.json         # 样品材料参数
│           └── matPlate.json          # 压板材料参数
├── matPlate.json                # 默认压板材料参数
├── matSample.json               # 默认样品材料参数
├── default.sim                  # CoSim 模拟配置文件
└── CoSim软件使用手册-2024R2.pdf  # CoSim 软件手册
```

## 使用方法 | Usage

### 1. 数据生成（需要 CoSim 环境）

1. 在 `main/runme.py` 中将 `cosim` 变量修改为你本地 CoSim 附带的 Python 环境路径
2. 根据目标岩石类型设定材料参数（密度、杨氏模量、泊松比、摩擦角、黏聚力）
3. 在 `main/` 目录下运行：
   ```bash
   python runme.py
   ```
4. 运行完成后，将生成的 `outputs/` 文件夹重命名为对应岩石名称，再进行下一组

### 2. 机器学习分析

打开 `ml.ipynb`，依次运行各 cell 即可完成数据加载、特征提取、分类与回归分析。

## 依赖 | Dependencies

- **DEM 模拟**：[CoSim](https://www.cosimgroup.com/) 及其附带的 Python 环境
- **机器学习**：NumPy, scikit-learn, Matplotlib, Seaborn
