import numpy as np
from scipy.constants import m_e, c, e, epsilon_0, hbar
from scipy.constants import alpha as alpha_fs
from scipy.interpolate import griddata

J_in_um = 2e6*np.pi*hbar*c

class Utilities:

    def get_full_spectrum(self, spect_filter=None, \
      phot_num=False, lambda0_um = None):

        if self.Args['Mode'] == 'far':
            val = alpha_fs/(4*np.pi**2)*self.Data['Rad']
        elif self.Args['Mode'] == 'near' or self.Args['Mode'] == 'near-circ':
            val = alpha_fs*np.pi/4*self.Data['Rad']

        if spect_filter is not None:
            val *= spect_filter

        if phot_num:
            ax = self.Args['omega']
            val /= ax[:,None,None]
        else:
            val *= J_in_um
            if lambda0_um is None:
                print("Specify normalization wavelength in "+\
                  "microns (lambda0_um) ")
                return  np.zeros_like(val)
            val /= lambda0_um

        return val

    def get_energy_spectrum(self, spect_filter = None, \
      phot_num=False, lambda0_um = None):

        val = self.get_full_spectrum(spect_filter=spect_filter, \
          phot_num=phot_num, lambda0_um=lambda0_um)

        if self.Args['Mode'] == 'far':
            val = 0.5*self.Args['dth']*self.Args['dph']*( (val[1:] + val[:-1]) \
              *np.sin(self.Args['theta'][None,:,None]) ).sum(-1).sum(-1)
        elif self.Args['Mode'] == 'near':
            val = 0.5*self.Args['dx']*self.Args['dy'] \
                  *(val[1:] + val[:-1]).sum(-1).sum(-1)
        elif self.Args['Mode'] == 'near-circ':
            val = 0.5*self.Args['dr']*self.Args['dph']*( (val[1:] + val[:-1]) \
              *self.Args['R'][None,:,None] ).sum(-1).sum(-1)

        return val

    def get_energy(self, spect_filter=None, \
      phot_num=False, lambda0_um = None):

        val = self.get_energy_spectrum(spect_filter=spect_filter, \
          phot_num=phot_num, lambda0_um=lambda0_um)

        val = (val*self.Args['dw']).sum()
        return val

    def get_spot(self, k0=None, spect_filter=None, \
      phot_num=False, lambda0_um = None):

        val = self.get_full_spectrum(spect_filter=spect_filter, \
          phot_num=phot_num, lambda0_um=lambda0_um)

        if k0 is None:
            if val.shape[0]>1:
                val = 0.5*(val[1:] + val[:-1])
            val = (val*self.Args['dw'][:,None,None]).sum(0)
        else:
            ax = self.Args['omega']
            indx = (ax<k0).sum()
            if np.abs(self.Args['omega'][indx+1]-k0) \
              < np.abs(self.Args['omega'][indx]-k0):
                indx += 1
            val = val[indx]
        return val

    def get_spot_cartesian(self, k0=None, th_part=1.0, bins=(200,200), \
      spect_filter=None, phot_num=False, lambda0_um = None):

        val = self.get_spot(spect_filter=spect_filter, \
          k0=k0, phot_num=phot_num, lambda0_um=lambda0_um)

        if self.Args['Mode'] == 'far':
            th,ph = self.Args['theta'], self.Args['phi']
        elif self.Args['Mode'] == 'near-circ':
            th,ph = self.Args['R'], self.Args['phi']
        else:
            print("This function is for 'far' and 'near-circ' modes only")

        ph,th = np.meshgrid(ph,th)
        th_max = th_part*th.max()

        coord = ((th*np.cos(ph)).flatten(), (th*np.sin(ph)).flatten())

        new_coord = np.mgrid[-th_max:th_max:bins[0]*1j,-th_max:th_max:bins[1]*1j]
        val = griddata(coord,val.flatten(),
            (new_coord[0].flatten(), new_coord[1].flatten()),
            fill_value=0., method='linear'
          ).reshape(new_coord[0].shape)
        ext = np.array([-th_max,th_max,-th_max,th_max])
        return val, ext

    def get_spectral_axis(self):
        if 'WavelengthGrid' in self.Args['Features']:
            ax = 0.5*(self.Args['wavelengths'][1:] \
              + self.Args['wavelengths'][:-1])
        else:
            ax = 0.5*(self.Args['omega'][1:] + self.Args['omega'][:-1])
        return ax
