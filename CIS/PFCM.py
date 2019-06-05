import numpy as np


def pfcm(data, c, expo=2, max_iter=1000, min_impro=0.005, a=1, b=4, nc=3):
    obj_fcn = np.zeros(shape=(max_iter, 1))
    ni = np.zeros(shape=(c, data.shape[0]))
    U = initf(c, data.shape[0])
    T = initf(c, data.shape[0])
    cntr = np.random.uniform(low=np.min(data), high=np.max(data), size=(
        c, data.shape[1]))
    for i in range(max_iter):
        current_cntr = cntr
        U, T, cntr, obj_fcn[i], ni = pstepfcm(
                data, cntr, U, T, expo, a, b, nc, ni)
        if i > 1:
            if abs(obj_fcn[i] - obj_fcn[i-1]) < min_impro:
                break
            elif np.max(abs(cntr - current_cntr)) < min_impro:
                break
    return cntr, U, T, obj_fcn


def pstepfcm(data, cntr, U, T, expo, a, b, nc, ni):
    mf = np.power(U, expo)
    tf = np.power(T, nc)
    tfo = np.power((1-T), nc)
    cntr = (np.dot(a*mf+b*tf, data).T/np.sum(
        a*mf+b*tf, axis=1).T).T
    dist = pdistfcm(cntr, data)
    obj_fcn = np.sum(np.sum(np.power(dist, 2)*(a*mf+b*tf), axis=0)) + np.sum(
        ni*np.sum(tfo, axis=0))
    ni = mf*np.power(dist, 2)/(np.sum(mf, axis=0))
    tmp = np.power(dist, (-2/(nc-1)))
    U = tmp/(np.sum(tmp, axis=0))
    tmpt = np.power((b/ni)*np.power(dist, 2), (1/(nc-1)))
    T = 1/(1+tmpt)
    return U, T, cntr, obj_fcn, ni


def initf(c, data_n):
    A = np.random.random(size=(c, data_n))
    col_sum = np.sum(A, axis=0)
    return A/col_sum


def pdistfcm(cntr, data):
    out = np.zeros(shape=(cntr.shape[0], data.shape[0]))
    for k in range(cntr.shape[0]):
        out[k] = np.sqrt(np.sum((np.power(data-cntr[k], 2)).T, axis=0))
    return out
