#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pbsdailyanalysis.py
"""Read and analyze an OmniPro planar dose for PBS daily QA."""
# Copyright (c) 2015 Aditya Panchal


import pandas as pd
import numpy as np
from math import sqrt, log
# import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from scipy.interpolate import interp1d
from matplotlib.patches import Circle, Ellipse


def fwhmpos(halfmax, maxarray, ascending=True):
    """Determine the position of the Full width at half max
       for the given array.

       If ascending is true, check for the negative side position.
       Otherwise if false, check for the positive side position."""

    values = maxarray.values
    positions = np.array(maxarray.index, dtype=np.float32)
    if ascending:
        s = interp1d(values[:values.argmax()],
                     positions[:values.argmax()])
    else:
        s = interp1d(values[values.argmax():],
                     positions[values.argmax():])

    return s(halfmax)


def read_file(filename):
    """Read the position file and return a dataframe used for analysis."""

    df = pd.read_csv(filename, sep="\t", header=25, index_col=0).ix[1:-2]
    df = df.drop(df.columns[-1], axis=1)

    Spot1A = df.loc['-10.000   ':' -6.000   ', '-10.000 ':' -6.000 ']
    Spot2A = df.loc['-10.000   ':' -6.000   ', ' -6.200 ':' -2.200 ']
    Spot5A = df.loc['-10.000   ':' -6.000   ', '  2.200 ':'  6.200 ']
    Spot6A = df.loc['-10.000   ':' -6.000   ', '  6.000 ':' 10.000 ']

    Spot3A = df.loc[' -6.200   ':' -2.200   ', '-10.000 ':' -6.000 ']
    Spot4A = df.loc[' -6.200   ':' -2.200   ', ' -6.200 ':' -2.200 ']
    Spot7A = df.loc[' -6.200   ':' -2.200   ', '  2.200 ':'  6.200 ']
    Spot8A = df.loc[' -6.200   ':' -2.200   ', '  6.000 ':' 10.000 ']

    Spot5B = df.loc['  2.200   ':'  6.200   ', '-10.000 ':' -6.000 ']
    Spot6B = df.loc['  2.200   ':'  6.200   ', ' -6.200 ':' -2.200 ']
    Spot1B = df.loc['  2.200   ':'  6.200   ', '  2.200 ':'  6.200 ']
    Spot2B = df.loc['  2.200   ':'  6.200   ', '  6.000 ':' 10.000 ']

    Spot7B = df.loc['  6.000   ':' 10.000   ', '-10.000 ':' -6.000 ']
    Spot8B = df.loc['  6.000   ':' 10.000   ', ' -6.200 ':' -2.200 ']
    Spot3B = df.loc['  6.000   ':' 10.000   ', '  2.200 ':'  6.200 ']
    Spot4B = df.loc['  6.000   ':' 10.000   ', '  6.000 ':' 10.000 ']

    spots = [Spot1A, Spot2A, Spot5A, Spot6A,
             Spot3A, Spot4A, Spot7A, Spot8A,
             Spot5B, Spot6B, Spot1B, Spot2B,
             Spot7B, Spot8B, Spot3B, Spot4B]

    ActualFWHMY1A = 11.1247051608056
    ActualFWHMY2A = 14.0175810440288
    ActualFWHMY5A = 12.4253703811076
    ActualFWHMY6A = 17.0572244550148
    ActualFWHMY3A = 15.8049030455876
    ActualFWHMY4A = 10.12564
    ActualFWHMY7A = 18.36744
    ActualFWHMY8A = 9.9363231954308
    ActualFWHMY5B = 12.4253703811076
    ActualFWHMY6B = 17.0572244550148
    ActualFWHMY1B = 11.1247051608056
    ActualFWHMY2B = 14.0175810440288
    ActualFWHMY7B = 18.36744
    ActualFWHMY8B = 9.9363231954308
    ActualFWHMY3B = 15.8049030455876
    ActualFWHMY4B = 10.12564

    ActualFWHMX1A = 10.9356585577624
    ActualFWHMX2A = 13.8930985922848
    ActualFWHMX5A = 12.301982918428
    ActualFWHMX6A = 16.5682702861368
    ActualFWHMX3A = 15.5336685559552
    ActualFWHMX4A = 10.0079
    ActualFWHMX7A = 17.661
    ActualFWHMX8A = 9.9388035886888
    ActualFWHMX5B = 12.301982918428
    ActualFWHMX6B = 16.5682702861368
    ActualFWHMX1B = 10.9356585577624
    ActualFWHMX2B = 13.8930985922848
    ActualFWHMX7B = 17.661
    ActualFWHMX8B = 9.9388035886888
    ActualFWHMX3B = 15.5336685559552
    ActualFWHMX4B = 10.0079

    ActualPosY1A = -8
    ActualPosY2A = -8
    ActualPosY5A = -8
    ActualPosY6A = -8
    ActualPosY3A = -4.2
    ActualPosY4A = -4.2
    ActualPosY7A = -4.2
    ActualPosY8A = -4.2
    ActualPosY5B = 4.2
    ActualPosY6B = 4.2
    ActualPosY1B = 4.2
    ActualPosY2B = 4.2
    ActualPosY7B = 8
    ActualPosY8B = 8
    ActualPosY3B = 8
    ActualPosY4B = 8

    ActualPosX1A = -8
    ActualPosX2A = -4.2
    ActualPosX5A = 4.2
    ActualPosX6A = 8
    ActualPosX3A = -8
    ActualPosX4A = -4.2
    ActualPosX7A = 4.2
    ActualPosX8A = 8
    ActualPosX5B = -8
    ActualPosX6B = -4.2
    ActualPosX1B = 4.2
    ActualPosX2B = 8
    ActualPosX7B = -8
    ActualPosX8B = -4.2
    ActualPosX3B = 4.2
    ActualPosX4B = 8

    ActualEnergy1A = 8
    ActualEnergy2A = 30
    ActualEnergy5A = 12
    ActualEnergy6A = 25
    ActualEnergy3A = 18
    ActualEnergy4A = 10
    ActualEnergy7A = 21
    ActualEnergy8A = 15
    ActualEnergy1B = 8
    ActualEnergy2B = 30
    ActualEnergy5B = 12
    ActualEnergy6B = 25
    ActualEnergy3B = 18
    ActualEnergy4B = 10
    ActualEnergy7B = 21
    ActualEnergy8B = 15

    ActualFWHMY = [ActualFWHMY1A, ActualFWHMY2A, ActualFWHMY5A, ActualFWHMY6A,
                   ActualFWHMY3A, ActualFWHMY4A, ActualFWHMY7A, ActualFWHMY8A,
                   ActualFWHMY5B, ActualFWHMY6B, ActualFWHMY1B, ActualFWHMY2B,
                   ActualFWHMY7B, ActualFWHMY8B, ActualFWHMY3B, ActualFWHMY4B]

    ActualFWHMX = [ActualFWHMX1A, ActualFWHMX2A, ActualFWHMX5A, ActualFWHMX6A,
                   ActualFWHMX3A, ActualFWHMX4A, ActualFWHMX7A, ActualFWHMX8A,
                   ActualFWHMX5B, ActualFWHMX6B, ActualFWHMX1B, ActualFWHMX2B,
                   ActualFWHMX7B, ActualFWHMX8B, ActualFWHMX3B, ActualFWHMX4B]

    ActualPositionY = [ActualPosY1A, ActualPosY2A, ActualPosY5A, ActualPosY6A,
                       ActualPosY3A, ActualPosY4A, ActualPosY7A, ActualPosY8A,
                       ActualPosY5B, ActualPosY6B, ActualPosY1B, ActualPosY2B,
                       ActualPosY7B, ActualPosY8B, ActualPosY3B, ActualPosY4B]

    ActualPositionX = [ActualPosX1A, ActualPosX2A, ActualPosX5A, ActualPosX6A,
                       ActualPosX3A, ActualPosX4A, ActualPosX7A, ActualPosX8A,
                       ActualPosX5B, ActualPosX6B, ActualPosX1B, ActualPosX2B,
                       ActualPosX7B, ActualPosX8B, ActualPosX3B, ActualPosX4B]

    ActualEnergy = [
        ActualEnergy1A, ActualEnergy2A, ActualEnergy5A, ActualEnergy6A,
        ActualEnergy3A, ActualEnergy4A, ActualEnergy7A, ActualEnergy8A,
        ActualEnergy5B, ActualEnergy6B, ActualEnergy1B, ActualEnergy2B,
        ActualEnergy7B, ActualEnergy8B, ActualEnergy3B, ActualEnergy4B]

    # Calculate the reference sigma value from FWHM (i.e. divide by 2.355)
    ActualSigmaY = [(x / (2 * sqrt(2*log(2)))) for x in ActualFWHMY]
    ActualSigmaX = [(x / (2 * sqrt(2*log(2)))) for x in ActualFWHMX]

    BaselineX = df.loc['  0.000   ', ' -8.000 ':'  8.000 '].mean()
    BaselineY = df.loc[' -8.000   ':'  8.000   ', '  0.000 '].mean()

    Background = BaselineX if (BaselineX > BaselineY) else BaselineY

    def roundup(df):
        """Round negative values to zero."""
        dfc = df.copy()
        dfc[dfc < 0] = 0
        return dfc

    x = []
    y = []
    for s in spots:
        s = s.copy() - Background
        x.append(roundup(np.max(s, axis=0)))
        y.append(roundup(np.max(s, axis=1)))

    Halfmax = np.zeros(16)
    positionY = np.zeros(16)
    positionX = np.zeros(16)
    SpotSizeY = np.zeros(16)
    SpotSizeX = np.zeros(16)
    sigmaY = np.zeros(16)
    sigmaX = np.zeros(16)
    DiffPosY = np.zeros(16)
    DiffPosX = np.zeros(16)
    DiffSizeY = np.zeros(16)
    DiffSizeX = np.zeros(16)
    PerDiffSizeY = np.zeros(16)
    PerDiffSizeX = np.zeros(16)

    for i, s in enumerate(spots):
        Halfmax[i] = np.max(y[i])/2

        # ascending y interpolation
        fwhmposy1 = fwhmpos(Halfmax[i], y[i], ascending=True)
        fwhmposy2 = fwhmpos(Halfmax[i], y[i], ascending=False)
        fwhmposx1 = fwhmpos(Halfmax[i], x[i], ascending=True)
        fwhmposx2 = fwhmpos(Halfmax[i], x[i], ascending=False)

        # Calculate spot position and difference
        positionY[i] = 0.5 * (fwhmposy1+fwhmposy2)
        positionX[i] = 0.5 * (fwhmposx1+fwhmposx2)

        DiffPosY[i] = (positionY[i] - ActualPositionY[i]) * 10
        DiffPosX[i] = (positionX[i] - ActualPositionX[i]) * 10

        # Calculate spot sigma and difference
        SpotSizeY[i] = abs(fwhmposy1 - fwhmposy2) * 10
        SpotSizeX[i] = abs(fwhmposx1 - fwhmposx2) * 10

        DiffSizeY[i] = SpotSizeY[i] - ActualFWHMY[i]
        DiffSizeX[i] = SpotSizeX[i] - ActualFWHMX[i]

        PerDiffSizeY[i] = (DiffSizeY[i]/ActualFWHMY[i]) * 100
        PerDiffSizeX[i] = (DiffSizeX[i]/ActualFWHMX[i]) * 100

        sigmaY[i] = SpotSizeY[i] / (2 * sqrt(2*log(2)))
        sigmaX[i] = SpotSizeX[i] / (2 * sqrt(2*log(2)))

    # Flatness / symmetry calculation
    backgroundX = df.loc['  0.000   ', ' -7.000 ':'  7.000 ']
    flatnessX = 100 * (backgroundX.max() - backgroundX.min()) / \
        (backgroundX.max() + backgroundX.min())
    backgroundY = df.loc[' -7.000   ':'  7.000   ', '  0.000 ']
    flatnessY = 100 * (backgroundY.max() - backgroundY.min()) / \
        (backgroundY.max() + backgroundY.min())

    sumX1 = df.loc['  0.000   ', ' -8.000 ': '  0.000 '].sum()
    sumX2 = df.loc['  0.000   ', '  0.000 ': '  8.000 '].sum()
    symmetryX = (100 * (abs(sumX1 * 0.1 - sumX2 * 0.1) /
                 abs(sumX1 * 0.1 + sumX2 * 0.1))) / 2

    sumY1 = df.loc[' -8.000   ':'  0.000   ', '  0.000 '].sum()
    sumY2 = df.loc['  0.000   ':'  8.600   ', '  0.000 '].sum()
    symmetryY = (100 * (abs(sumY1 * 0.1 - sumY2 * 0.1) /
                 abs(sumY1 * 0.1 + sumY2 * 0.1))) / 2

    return spots, {
        'x': x,
        'y': y,
        'spots': spots,
        'Halfmax': Halfmax,
        'Background': Background,
        'positionY': positionY.tolist(),
        'positionX': positionX.tolist(),
        'SpotSizeY': SpotSizeY.tolist(),
        'SpotSizeX': SpotSizeX.tolist(),
        'sigmaY': sigmaY,
        'sigmaX': sigmaX,
        'flatnessY': flatnessY,
        'flatnessX': flatnessX,
        'symmetryY': symmetryY,
        'symmetryX': symmetryX,
        'ActualPositionY': ActualPositionY,
        'ActualPositionX': ActualPositionX,
        'ActualFWHMY': ActualFWHMY,
        'ActualFWHMX': ActualFWHMX,
        'ActualEnergy': ActualEnergy,
        'ActualSigmaY': ActualSigmaY,
        'ActualSigmaX': ActualSigmaX
    }


def plot_data(spotdata, plot_type='profile', annotations='position', axis='x'):
    """spotdata: dictionary of spot properties
       plot_type: string representing plot type ('profile', 'spot')
       annotations: string respresenting annotations to show on plot
                    ('position', 'size')
       axis: string representing line profile axis ('x', 'y')
    """

    def subtract(df):
        """Subtract the background."""
        dfc = df.copy()
        dfc -= spotdata['Background']
        return dfc

    x = spotdata['x']
    y = spotdata['y']
    if plot_type == 'profile':
        spots = x if axis == 'x' else y
    else:
        spots = [subtract(s) for s in spotdata['spots']]
    # Background = spotdata['Background']
    Halfmax = spotdata['Halfmax']
    positionY = spotdata['positionY']
    positionX = spotdata['positionX']
    # SpotSizeY = spotdata['SpotSizeY']
    # SpotSizeX = spotdata['SpotSizeX']
    sigmaY = spotdata['sigmaY']
    sigmaX = spotdata['sigmaY']
    ActualPositionY = spotdata['ActualPositionY']
    ActualPositionX = spotdata['ActualPositionX']
    ActualFWHMY = spotdata['ActualFWHMY']
    ActualFWHMX = spotdata['ActualFWHMX']
    ActualEnergy = spotdata['ActualEnergy']
    ActualSigmaY = spotdata['ActualSigmaY']
    ActualSigmaX = spotdata['ActualSigmaX']

    f = Figure()
    f = Figure(dpi=72, facecolor="white")
    dpi = f.get_dpi()
    f.set_size_inches(720 / dpi, 600 / dpi)
    if plot_type == 'profile':
        if annotations == 'position':
            # f, axarr = plt.subplots(4, 4)
            k = 0
            for i in range(4):
                for j in range(4):
                    xs = np.array(spots[k].index, dtype=np.float32)
                    ax = f.add_subplot(4, 4, k + 1)
                    ax.plot(xs, spots[k])
                    if axis == 'y':
                        actpos = ActualPositionY[k]
                        pos = positionY[k]
                    elif axis == 'x':
                        actpos = ActualPositionX[k]
                        pos = positionX[k]
                    opacity_pass, opacity_tol, opacity_act = 0.2, 0.2, 0.2
                    if pos <= actpos + 0.2 and pos >= actpos - 0.2:
                        opacity_pass = 0.5
                    elif (pos >= actpos + 0.2 and pos <= actpos + 0.5) or \
                         (pos <= actpos - 0.2 and pos >= actpos - 0.5):
                        opacity_tol = 0.5
                    elif pos >= actpos + 0.5 or pos <= actpos - 0.5:
                        opacity_act = 0.5
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=np.logical_and(xs >= actpos, xs <= actpos + .2),
                        color='green', alpha=opacity_pass)
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=np.logical_and(xs <= actpos, xs >= actpos - .2),
                        color='green', alpha=opacity_pass)
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=np.logical_and(
                            xs >= actpos + .2, xs <= actpos + 0.5),
                        color='orange', alpha=opacity_tol)
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=np.logical_and(
                            xs <= actpos - .2, xs >= actpos - 0.5),
                        color='orange', alpha=opacity_tol)
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=(xs >= actpos + .5), color='red',
                        alpha=opacity_act)
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=(xs <= actpos - .5), color='red',
                        alpha=opacity_act)
                    ax.axvline(
                        x=pos, linewidth=2,
                        color='r', ls='dashed')
                    ax.axvline(x=actpos, linewidth=1, color='b')
                    xticks = ax.xaxis.get_major_ticks()
                    for n in range(len(xticks)):
                        if n != 0 and n != 1:
                            xticks[-n].label1.set_visible(False)
                    yticks = ax.yaxis.get_major_ticks()
                    for n in range(len(yticks)):
                        if n != 0 and n != 1:
                            yticks[-n].label1.set_visible(False)
                    ax.set_title(
                        axis + '(' + str(ActualPositionY[k])
                        + ',' + str(ActualPositionX[k]) + ', R' +
                        str(ActualEnergy[k]) + ')',
                        fontsize=10, color='blue')
                    if k >= 12:
                        ax.set_xlabel('Millimeters', fontsize=10)
                    k += 1
        elif annotations == 'size':
            # f, axarr = plt.subplots(4, 4)
            k = 0
            for i in range(4):
                for j in range(4):
                    xs = np.array(spots[k].index, dtype=np.float32)
                    ax = f.add_subplot(4, 4, k + 1)
                    ax.plot(xs, spots[k])
                    if axis == 'y':
                        actsize = ActualFWHMY[k] / 20
                        actpos = ActualPositionY[k]
                        pos = positionY[k]
                    elif axis == 'x':
                        actsize = ActualFWHMX[k] / 20
                        actpos = ActualPositionX[k]
                        pos = positionX[k]
                    fwhm = fwhmpos(Halfmax[k], spots[k])
#                    ax.axvline(x = fwhm, linewidth = 2, \
#                    color = 'r', ls = ':')
#                    ax.axvline(x = (2 * actpos - fwhm), \
#                    linewidth = 2, color = 'r', ls = ':')
                    ax.plot(
                        [fwhm, fwhm], [0, Halfmax[k]],
                        color='red', linewidth=2, ls='dashed')
                    ax.plot(
                        [2 * pos - fwhm, 2 * pos - fwhm],
                        [0, Halfmax[k]], color='red', linewidth=2,
                        ls='dashed')
                    ax.plot(
                        [fwhm, 2 * pos - fwhm],
                        [Halfmax[k], Halfmax[k]], color='red',
                        linewidth=2, ls='dashed')
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=np.logical_and(
                            (xs >= actpos),
                            (xs <= (actpos + actsize) + (actsize * 0.1))),
                        color='green', alpha=0.2)
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=np.logical_and(
                            (xs <= actpos),
                            (xs >= (actpos - actsize) - (actsize * 0.1))),
                        color='green', alpha=0.2)
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=np.logical_and(
                            (xs >= (actpos + actsize) + (actsize * 0.1)),
                            (xs <= (actpos + actsize) + (actsize * 0.2))),
                        color='orange', alpha=0.2)
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=np.logical_and(
                            (xs <= (actpos - actsize) - (actsize * 0.1)),
                            (xs >= (actpos - actsize) - (actsize * 0.2))),
                        color='orange', alpha=0.2)
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=(xs >= (actpos + actsize) + (actsize * 0.2)),
                        color = 'red', alpha = 0.2)
                    ax.fill_between(
                        xs, 0, spots[k],
                        where=(xs <= (actpos - actsize) - (actsize * 0.2)),
                        color = 'red', alpha = 0.2)
                    xticks = ax.xaxis.get_major_ticks()
                    for n in range(len(xticks)):
                        if n != 0 and n != 1:
                            xticks[-n].label1.set_visible(False)
                    yticks = ax.yaxis.get_major_ticks()
                    for n in range(len(yticks)):
                        if n != 0 and n != 1:
                            yticks[-n].label1.set_visible(False)
                    if axis == 'y':
                        ax.set_title(
                            axis + '(' + str(ActualPositionY[k])
                            + ',' + str(ActualPositionX[k]) + ':'
                            + str("%.3g" % ActualSigmaY[k]) + ')',
                            fontsize=10, color='blue')
                    elif axis == 'x':
                        ax.set_title(
                            axis + '(' + str(ActualPositionY[k])
                            + ',' + str(ActualPositionX[k]) + ':'
                            + str("%.3g" % ActualSigmaX[k]) + ')',
                            fontsize=10, color='blue')
                    if k >= 12:
                        ax.set_xlabel('Millimeters', fontsize=10)
                    k += 1
    elif plot_type == 'spot':
        if annotations == 'position':
            # f, axarr = plt.subplots(4,4)
            k = 0
            for i in range(4):
                for j in range(4):
                    ax = f.add_subplot(4, 4, k + 1)
                    ys = np.array(spots[k].index, dtype=np.float32)
                    xs = np.array(spots[k].columns, dtype=np.float32)
                    ax.imshow(
                        spots[k], aspect='equal',
                        extent=(xs[0], xs[-1], ys[-1], ys[0]), cmap='jet')
                    circle_tol = Circle(
                        (ActualPositionX[k], ActualPositionY[k]), .2,
                        color='white', fill=False, ls='solid', linewidth=1)
                    ax.add_patch(circle_tol)
                    circle_fail = Circle(
                        (ActualPositionX[k], ActualPositionY[k]), .3,
                        color='white', fill=False, ls='solid', linewidth=1)
                    ax.add_patch(circle_fail)
                    ax.axvline(
                        x=ActualPositionX[k], linewidth=1,
                        color='white')
                    ax.axhline(
                        y=ActualPositionY[k], linewidth=1,
                        color='white')
                    ax.axvline(
                        x=positionX[k], linewidth=1,
                        color='black', ls='dashed')
                    ax.axhline(
                        y=positionY[k], linewidth=1,
                        color='black', ls='dashed')
                    xticks = ax.xaxis.get_major_ticks()
                    for n in range(len(xticks)):
                        if n != (len(xticks) - 2) and n != 1:
                            xticks[-(n + 1)].label1.set_visible(False)
                    yticks = ax.yaxis.get_major_ticks()
                    for n in range(len(yticks)):
                        if n != (len(yticks) - 2) and n != 1:
                            yticks[-(n + 1)].label1.set_visible(False)
                    ax.set_title(
                        'spot' + '(' + str(ActualPositionY[k])
                        + ',' + str(ActualPositionX[k]) + ':'
                        + 'R' + str(ActualEnergy[k]) + ')',
                        fontsize=10, color='blue')
                    if k >= 12:
                        ax.set_xlabel('Millimeters', fontsize=10)
                    k += 1
        elif annotations == 'size':
            # f, axarr = plt.subplots(4,4)
            k = 0
            for i in range(4):
                for j in range(4):
                    ax = f.add_subplot(4, 4, k + 1)
                    ys = np.array(spots[k].index, dtype=np.float32)
                    xs = np.array(spots[k].columns, dtype=np.float32)
                    ax.imshow(
                        (spots[k] >= (Halfmax[k])) * 512,
                        aspect='equal',
                        extent=(xs[0], xs[-1], ys[-1], ys[0]),
                        cmap='Blues')
                    # print 'x', Halfmax[k], (Halfmax[k] + Background), \
                    #     spots[k].values.max(), spots[k].values.min(), \
                    #     spots[k].values.mean()
                    fwhmpos(Halfmax[k], x[k], ascending=False), \
                        positionX[k] - sigmaX[k] / 10, positionX[k] + sigmaX[k] / 10, \
                        positionY[k], positionY[k]
                    # Plot FWHM X
                    ax.plot(
                        [fwhmpos(Halfmax[k], x[k]),
                         fwhmpos(Halfmax[k], x[k], ascending=False)],
                        [positionY[k], positionY[k]],
                        color='white', linewidth=1)
                    # Plot Sigma X
                    # ax.plot(
                    #     [positionX[k] - sigmaX[k] / 10,
                    #      positionX[k] + sigmaX[k] / 10],
                    #     [positionY[k], positionY[k]],
                    #     color='blue', linewidth=1)
                    # Plot Act Sigma X
                    # ax.plot(
                    #     [positionX[k] - ActualSigmaX[k] / 10,
                    #      positionX[k] + ActualSigmaX[k] / 10],
                    #     [positionY[k], positionY[k]],
                    #     color='green', linewidth=1)
                    # Plot FWHM Y
                    ax.plot(
                        [positionX[k], positionX[k]],
                        [fwhmpos(Halfmax[k], y[k]),
                         fwhmpos(Halfmax[k], y[k], ascending=False)],
                        color='white', linewidth=1)
                    # Plot Sigma Y
                    # ax.plot(
                    #     [positionX[k], positionX[k]],
                    #     [positionY[k] - sigmaY[k] / 10,
                    #      positionY[k] + sigmaY[k] / 10],
                    #     color='blue', linewidth=1)
                    # Plot Actual Sigma Y
                    # ax.plot(
                    #     [positionX[k], positionX[k]],
                    #     [positionY[k] - ActualSigmaY[k] / 10,
                    #      positionY[k] + ActualSigmaY[k] / 10],
                    #     color='green', linewidth=1)
                    # Plot Sigma Tolerance
                    ellipse_tol = Ellipse(
                        (positionX[k], positionY[k]),
                        width=2 * (sigmaX[k] / 10) * 1.1,
                        height=2 * (sigmaY[k] / 10) * 1.1, color='orange',
                        fill=False, ls='solid', linewidth=1)
                    ax.add_patch(ellipse_tol)
                    ellipse_fail = Ellipse(
                        (positionX[k], positionY[k]),
                        width=2 * (sigmaX[k] / 10) * 1.2,
                        height=2 * (sigmaY[k] / 10) * 1.2, color='red',
                        fill=False, ls='solid', linewidth=1)
                    ax.add_patch(ellipse_fail)
                    xticks = ax.xaxis.get_major_ticks()
                    for n in range(len(xticks)):
                        if n != (len(xticks) - 2) and n != 1:
                            xticks[-(n + 1)].label1.set_visible(False)
                    yticks = ax.yaxis.get_major_ticks()
                    for n in range(len(yticks)):
                        if n != (len(yticks) - 2) and n != 1:
                            yticks[-(n + 1)].label1.set_visible(False)
                    ax.set_title(
                        'spot' + '(' + str(ActualPositionY[k])
                        + ',' + str(ActualPositionX[k]) + ',' +
                        'Y:' + str("%.3g" % ActualSigmaY[k]) + ',' + 'X:'
                        + str("%.3g" % ActualSigmaX[k]) + ')',
                        fontsize=10, color='blue')
                    if k >= 12:
                        ax.set_xlabel('Millimeters', fontsize=10)
                    k += 1
    return f
