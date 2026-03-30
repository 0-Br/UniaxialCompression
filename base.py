import os
import json
import random
import numpy as np
import matplotlib as plt


SEED = 42
WINDOW_SIZE = 5
TP_RATIO = 0.7
P_TEST = 0.3


random.seed(SEED)
np.random.seed(SEED)


def moving_average(data, window_size):
    """"""
    window = np.ones(int(window_size)) / float(window_size)
    return np.convolve(data, window, 'valid')


class Sample:

    def __init__(self, dir, type):
        """"""
        self.type = type

        self.Fx = []
        self.Fy = []
        self.Fz = []
        self.Vx = []
        self.Vy = []
        self.Vz = []
        self.Dx = []
        self.Dy = []
        self.Dz = []

        with open(os.path.join(dir, "main_top_History.txt"), 'r') as file:
            lines = file.readlines()[1:]
        for line in lines:
            _, Fx, Fy, Fz, Vx, Vy, Vz, Dx, Dy, Dz = line.split()
            self.Fx.append(np.float64(Fx))
            self.Fy.append(np.float64(Fy))
            self.Fz.append(np.float64(Fz))
            self.Vx.append(np.float64(Vx))
            self.Vy.append(np.float64(Vy))
            self.Vz.append(np.float64(Vz))
            self.Dx.append(np.float64(Dx))
            self.Dy.append(np.float64(Dy))
            self.Dz.append(np.float64(Dz))

        self.Fx = np.array(self.Fx)
        self.Fy = np.array(self.Fy)
        self.Fz = np.array(self.Fz)
        self.Vx = np.array(self.Vx)
        self.Vy = np.array(self.Vy)
        self.Vz = np.array(self.Vz)
        self.Dx = np.array(self.Dx)
        self.Dy = np.array(self.Dy)
        self.Dz = np.array(self.Dz)

        with open(os.path.join(dir, "matSample.json"), 'r') as file:
            self.material = json.load(file)
        with open(os.path.join(dir, "matPlate.json"), 'r') as file:
            self.material_plate = json.load(file)

        # Feature Engineering
        self.arr_D = np.abs(moving_average(self.Dz, WINDOW_SIZE))
        self.arr_F = np.abs(moving_average(self.Fz, WINDOW_SIZE))
        self.length = len(self.arr_D)
        self.D_max = np.max(self.arr_D)
        self.F_max = np.max(self.arr_F)
        self.F_mean = np.mean(self.arr_F)
        self.F_std = np.std(self.arr_F)

        temp_F = self.arr_F - self.F_max * TP_RATIO
        temp_F[temp_F > 0] = -np.inf
        self.id_tp = np.argmax(temp_F)
        self.D_tp = self.arr_D[self.id_tp]
        self.F_tp = self.arr_F[self.id_tp]

        self.S1 = np.trapz(self.arr_F[:self.id_tp], self.arr_D[:self.id_tp])
        self.S2 = np.trapz(self.arr_F[self.id_tp:], self.arr_D[self.id_tp:])

        self.feature = np.array([self.id_tp / self.length,
                                 self.D_tp,
                                 self.F_tp,
                                 self.S1,
                                 self.S2,
                                 self.D_max,
                                 self.F_max,
                                 self.F_mean,
                                 self.F_std])

        self.target = np.array([np.tan(self.material["StaticFric"]),
                                self.material["normalCohesion"]])
