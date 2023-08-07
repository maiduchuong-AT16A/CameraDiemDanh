import pandas as pd
import datetime
from pandas import DataFrame
import numpy as np
import csv

class SinhVien:

    def __init__(self,id,name):
        self._id = id
        self._name = name


    def nhapSinhVien(self):
        # Khởi tạo một sinh viên mới
        id = int(input("Nhap ID sinh vien: "))
        self._id = id




