import numpy as np
import pandas as pd

from .util import dist

import pkg_resources
fp = pkg_resources.resource_filename(__name__, 'data/mamajek.csv')

class Mamajek:

    def __init__(self):
        self.df = pd.read_csv(fp)
        self.df['SpT_num'] = [float(i[1:-1]) for i in self.df['SpT']]
        self.df['SpT_let'] = [i[0] for i in self.df['SpT']]
        self.n = int(1e4)

    def query(self, color, c, uc, m, n=None):

        if n is None:
            n = self.n

        if color == 'B-V':
            a_str = 'B'
            b_str = 'V'
            M_str = 'Mv'
        elif color == 'V-Ks':
            a_str = 'V'
            b_str = 'K'
            M_str = 'Mv'
        elif color == 'J-H':
            a_str = 'J'
            b_str = 'H'
            M_str = 'M_J'
        elif color == 'H-K':
            a_str = 'H'
            b_str = 'K'
            M_str = 'M_Ks'
        elif color == 'Ks-W1':
            a_str = 'K'
            b_str = 'W1'
            M_str = 'M_Ks'

        s = np.random.randn(n) * uc + c

        df = self.df.sort_values(by=color)

        targ = 'Teff'
        res = np.interp(s, df[color].values, df[targ].values)
        print "{0} = {1:.0f} +/- {2:.0f}".format(targ, np.nanmean(res), np.nanstd(res))

        targ = 'logL'
        res = np.interp(s, df[color].values, df[targ].values)
        print "{0} = {1:.2f} +/- {2:.2f}".format(targ, np.nanmean(res), np.nanstd(res))

        targ = 'Msun'
        res = np.interp(s, df[color].values, df[targ].values)
        print "{0} = {1:.2f} +/- {2:.2f}".format(targ, np.nanmean(res), np.nanstd(res))

        targ = 'SpT_num'
        res = np.interp(s, df[color].values, df[targ].values)
        spt = np.interp(s, df[color].values, df.index.values)
        spt_let = df['SpT_let'][int(round(np.nanmean(spt)))]
        print "SpT = {0}{1:.1f}V +/- {2:.1f}".format(spt_let, np.nanmean(res), np.nanstd(res))

        targ = M_str
        idx = ~df[[color,targ]].isnull().any(axis=1)
        res = np.interp(s, df[idx][color].values, df[idx][targ].values)
        d = dist(m, res)
        print "Dphot = {0:.0f} +/- {1:.0f} pc".format(np.nanmean(d), np.nanstd(d))
