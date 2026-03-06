import numpy as np
from math import pi, cos, sin, atan2


def dft(x):
    """
    Geoptimaliseerde DFT - compatibel met originele input formaat.
    Input: lijst van tuples [(re, im), (re, im), ...]
    """
    N = len(x)
    
    # Converteer input naar numpy array
    x_array = np.array([complex(re, im) for re, im in x])
    
    # Maak frequentie arrays
    k = np.arange(N)
    n = k.reshape((N, 1))
    
    # Bereken exponent matrix: e^(-2πikn/N)
    exponent = np.exp(-2j * np.pi * k * n / N)
    
    # Matrix vermenigvuldiging voor DFT
    X_complex = np.dot(exponent, x_array) / N
    
    # Bereken frequentie, amplitude en fase
    freq = k
    amp = np.abs(X_complex)
    phase = np.angle(X_complex)
    
    # Combineer resultaten als lijst van lijsten
    X = [[int(f), float(a), float(p)] for f, a, p in zip(freq, amp, phase)]
    
    # Sorteer op amplitude (descending)
    X.sort(key=lambda item: item[1], reverse=True)
    
    return X


def dft_fft(x):
    """
    FFT versie - veel sneller voor grote N.
    Input: lijst van tuples [(re, im), (re, im), ...]
    """
    N = len(x)
    
    # Converteer input
    x_array = np.array([complex(re, im) for re, im in x])
    
    # Gebruik FFT
    X_complex = np.fft.fft(x_array) / N
    
    # Bereken frequentie, amplitude en fase
    freq = np.arange(N)
    amp = np.abs(X_complex)
    phase = np.angle(X_complex)
    
    # Combineer resultaten
    X = [[int(f), float(a), float(p)] for f, a, p in zip(freq, amp, phase)]
    
    # Sorteer op amplitude (descending)
    X.sort(key=lambda item: item[1], reverse=True)
    
    return X


def dft_original_improved(x):
    """
    Verbeterde versie van originele code (geen NumPy nodig).
    Gebruikt built-in complex type en vermijdt print statements.
    """
    N = len(x)
    X = []
    
    # Pre-bereken cos/sin waarden
    angles = [[2 * pi * k * n / N for n in range(N)] for k in range(N)]
    
    for k in range(N):
        som_re = 0.0
        som_im = 0.0
        
        for n in range(N):
            phi = angles[k][n]
            cos_phi = cos(phi)
            sin_phi = sin(phi)
            
            # Complex vermenigvuldiging
            re = x[n][0] * cos_phi - x[n][1] * sin_phi
            im = x[n][0] * sin_phi + x[n][1] * cos_phi
            
            som_re += re
            som_im += im
        
        som_re /= N
        som_im /= N
        
        freq = k
        amp = (som_re * som_re + som_im * som_im) ** 0.5
        phase = atan2(som_im, som_re)
        
        X.append([freq, amp, phase])
    
    X.sort(key=lambda item: item[1], reverse=True)
    return X
