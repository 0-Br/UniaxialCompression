import os
import json
import shutil
import argparse
import time
import math
import CoSim
from CoSim.DEMSimulation import DEMSimulation


os.chdir(os.getcwd()) # 或者手动指定main目录
CoSim.setDevice(0)


def log_params(dir: str, name:str, params: dict):
    """"""
    with open(os.path.join(dir, f"{name}.json"), "w") as f:
        json.dump(params, f)


class DEMSimulator:

    def __init__(self, save_dir: str, matPlate: dict, matSample: dict):
        """"""
        self.save_dir = save_dir
        self.matPlate = matPlate
        self.matSample = matSample

        sim = DEMSimulation()
        sim.CreateEngine3D("main", save_dir)

        sim.DEMMaterial('FricMat', 'plate', matPlate)
        sim.DEMMaterial('CohFricMat', 'rock', matSample)

        sim.ImportElement('STL', 'main_bot.stl', 'bot')

        sim.ImportElement('STL', 'main_top.stl', 'top')
        sim.ImportElement('Polyhedron', 'main_sample.poly')

        sim.DEMAssemble(['bot', 'plate'], ['sample', 'rock'], ['top','plate'])
        sim.DEMContacts(['CohFrac_Poly_Poly', 'cpp', { 'ECCMethod' : 0, 'useViscocity' : False }], ['Fric_Poly_Mesh', 'fpm', { 'useViscocity' : False }])

        sim.DEMNeighborSearch({ 'end' :  [ 0.051999999999999998, 0.051999999999999998, 0.10199999999999999 ], 'origin' :  [ -0.051999999999999998, -0.051999999999999998, -0.002 ], 'type' : 'BVH' })

        sim.Initialize()

        self.sim = sim

    def run(self, nsteps: int, frec: int, tempsaving: int):
        """"""
        top.Boundary.Vel([0, 0, -1e-07])

        log_params(os.path.join(os.getcwd(), self.save_dir), "matPlate", matPlate)
        log_params(os.path.join(os.getcwd(), self.save_dir), "matSample", matSample)

        self.sim.DEMHistory({'Set': ['top'], 'Frequency': frec, 'Variable': ['Fxyz','Vxyz','Dxyz']})
        sim_para = { 'Gravity' :  [ 0.0, 0.0, 0.0 ], 'TempSaving' : tempsaving, 'TimeStep' : self.sim.GetDt() * 0.99, 'TranslatingDamping' : 0.10000000000000001, 'RollingDamping' : 0.10000000000000001 }
        self.sim.StepEngine3D(sim_para)
        self.sim.Run(nsteps + 1)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="default")
    parser.add_argument("--dir", type=str)
    parser.add_argument("--num", type=int, default=200)
    parser.add_argument("--frec", type=int, default=1)
    parser.add_argument("--tempsaving", type=int, default=20)
    args = parser.parse_args()

    matPlate = json.load(open("matPlate.json", "r"))
    matSample = json.load(open("matSample.json", "r"))

    DS = DEMSimulator(args.dir, matPlate, matSample) # param: 保存路径，板材材料，样品材料

    DS.run(args.num, args.frec, args.tempsaving) # param: 运行步数(建议设置为1000)，保存间隔(default=10)

    shutil.rmtree("Results")
    os.remove("matPlate.json")
    os.remove("matSample.json")
