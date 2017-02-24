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

    def query(self, color="B-V", c=0, uc=1, m=None, n=int(1e4), verbose=True):

        if n is None:
            n = self.n

        if color == 'B-V':
            M_str = 'Mv'
        elif color == 'V-Ks':
            M_str = 'Mv'
        elif color == 'J-H':
            M_str = 'M_J'
        elif color == 'H-K':
            M_str = 'M_Ks'
        elif color == 'Ks-W1':
            M_str = 'M_Ks'

        s = np.random.randn(n) * uc + c

        df = self.df.sort_values(by=color)

        out = {}

        targ = 'Teff'
        res = np.interp(s, df[color].values, df[targ].values)
        out[targ] = [np.nanmean(res), np.nanstd(res)]
        msg = "{0} = {1:.0f} +/- {2:.0f}".format(targ, np.nanmean(res), np.nanstd(res))

        targ = 'logL'
        res = np.interp(s, df[color].values, df[targ].values)
        out[targ] = [np.nanmean(res), np.nanstd(res)]
        msg += "\n{0} = {1:.2f} +/- {2:.2f}".format(targ, np.nanmean(res), np.nanstd(res))

        targ = 'Msun'
        res = np.interp(s, df[color].values, df[targ].values)
        out[targ] = [np.nanmean(res), np.nanstd(res)]
        msg += "\n{0} = {1:.2f} +/- {2:.2f}".format(targ, np.nanmean(res), np.nanstd(res))

        targ = 'SpT_num'
        res = np.interp(s, df[color].values, df[targ].values)
        spt = np.interp(s, df[color].values, df.index.values)
        spt_let = df['SpT_let'][int(round(np.nanmean(spt)))]
        out["SpT"] = "{0}{1:.1f}V +/- {2:.1f}".format(spt_let, np.nanmean(res), np.nanstd(res))
        msg += "\nSpT = {0}{1:.1f}V +/- {2:.1f}".format(spt_let, np.nanmean(res), np.nanstd(res))

        if m is not None:
            targ = M_str
            idx = ~df[[color,targ]].isnull().any(axis=1)
            res = np.interp(s, df[idx][color].values, df[idx][targ].values)
            d = dist(m, res)
            out["Dphot"] = [np.nanmean(d), np.nanstd(d)]
            msg += "\nDphot = {0:.0f} +/- {1:.0f} pc".format(np.nanmean(d), np.nanstd(d))

        if verbose:
            print msg

        return out
