from CIS import app
import numpy as np
import matplotlib.image as mpimg
import os
from sklearn.cluster import KMeans
import skfuzzy as fuzz
from CIS.PFCM import pfcm
from CIS.VIBGYOR import VIBGYORsegmentation
from CIS.models import Run
try:
    from secrets import token_hex
except ImportError:
    def token_hex(nbytes=None):
        return os.urandom(nbytes).hex()


def create_image(labels, centers):
    dir = os.path.join(app.root_path, 'static', 'output_images')
    img = np.zeros(shape=(labels.shape[0], labels.shape[1], 3))
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            img[i, j] = centers[labels[i, j]]
    if(abs(img.max()) > 1):
        img /= 255
    output_image_name = token_hex(8) + '.jpg'
    output_image_path = os.path.join(dir, output_image_name)
    mpimg.imsave(output_image_path, abs(img))
    img = mpimg.imread(output_image_path)
    for f in os.listdir(dir):
        if f != output_image_name:
            img1 = mpimg.imread(os.path.join(dir, f))
            if np.array_equiv(img, img1):
                os.remove(output_image_path)
                output_image_name = f
                break
    return output_image_name


def create_images(labels, centers):
    dir = os.path.join(app.root_path, 'static', 'output_images')
    output_images = []
    for k in range(centers.shape[0]):
        img = np.zeros(shape=(labels.shape[0], labels.shape[1], 3))
        for i in range(img.shape[0]):
            for j in range(img.shape[1]):
                if labels[i, j] == k:
                    img[i, j] = centers[k]
        if(abs(img.max()) > 1):
            img /= 255
        output_image_name = token_hex(8) + '.jpg'
        output_image_path = os.path.join(dir, output_image_name)
        mpimg.imsave(output_image_path, abs(img))
        img = mpimg.imread(output_image_path)
        for f in os.listdir(dir):
            if f != output_image_name:
                img1 = mpimg.imread(os.path.join(dir, f))
                if np.array_equiv(img, img1):
                    os.remove(output_image_path)
                    output_image_name = f
                    break
        output_images.append(output_image_name)
    return output_images


def empty_input():
    dir = os.path.join(app.root_path, 'static', 'input_images')
    for f in os.listdir(dir):
        if (Run.query.filter_by(input_image=f).count() == 0
                and f != 'default.jpg'):
            os.remove(os.path.join(dir, f))


def empty_output():
    dir = os.path.join(app.root_path, 'static', 'output_images')
    for f in os.listdir(dir):
        s = "%"+f+"%"
        if Run.query.filter(Run.output_image.like(s)).count() == 0:
            os.remove(os.path.join(dir, f))


def save_image(image):
    random_name = token_hex(8)
    dir = os.path.join(app.root_path, 'static', 'input_images')
    _, f_ext = os.path.splitext(image.filename)
    image_name = random_name + f_ext
    image_path = os.path.join(dir, image_name)
    image.save(image_path)
    img1 = mpimg.imread(image_path)
    for f in os.listdir(dir):
        if f != image_name:
            img2 = mpimg.imread(os.path.join(dir, f))
            if np.array_equiv(img1, img2):
                os.remove(image_path)
                image_path = os.path.join(dir, f)
                image_name = f
                break
    return image_path, image_name


def compactness(img, labels, centers):
    if img.shape[2] != 3:
        img = img[:, :, :3]
    WSS = 0
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            WSS += np.sum(np.power(img[i, j]-centers[labels[i, j]], 2))
    return round(WSS, 3)


def separation(labels, centers):
    BSS = 0
    cluster_size = np.zeros(centers.shape[0])
    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            cluster_size[labels[i, j]] += 1
    mean = np.mean(centers, axis=0)
    for k in range(centers.shape[0]):
            BSS += cluster_size[k]*np.sum(np.power(mean - centers[k], 2))
    return round(BSS, 3)


def kmeans_images(img, k):
    data = img.reshape(img.shape[0]*img.shape[1], img.shape[2])
    if data.shape[1] != 3:
        data = data[:, :3]
    kmeans = KMeans(n_clusters=k, random_state=0).fit(data)
    labels = kmeans.labels_.reshape(img.shape[0], img.shape[1])
    centers = kmeans.cluster_centers_
    return labels, centers


def fcm_images(img, c):
    data = img.reshape(img.shape[0]*img.shape[1], img.shape[2]).T
    if data.shape[0] != 3:
        data = data[:3, :]
    cntr, u, _, _, _, _, _ = fuzz.cluster.cmeans(
            data, c, m=2, error=0.005, maxiter=1000, init=None)
    labels = np.argmax(u, axis=0).reshape(img.shape[0], img.shape[1])
    return labels, cntr


def pfcm_images(img, c):
    data = img.reshape(img.shape[0]*img.shape[1], img.shape[2])
    if data.shape[1] != 3:
        data = data[:, :3]
    centers, U, _, _ = pfcm(data, c)
    labels = np.argmax(U, axis=0).reshape(img.shape[0], img.shape[1])
    return labels, centers


def vibgyor(img, color):
    if img.shape[2] != 3:
        img = img[:, :, :3]
    output_image = VIBGYORsegmentation(img, color)
    output_image_name = token_hex(8) + '.jpg'
    output_image_path = os.path.join(app.root_path, 'static',
                                     'output_images', output_image_name)
    mpimg.imsave(output_image_path, output_image)
    return output_image_name
