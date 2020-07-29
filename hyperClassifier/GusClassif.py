from spectral import *
import cv2
import numpy as np
import os


def classify(img, gt):
    img = open_image(img).load()
    gt1 = cv2.imread(gt)
    gt = np.asarray(gt1[:, :, 0])
    (m, n) = gt.shape
    for i in range(m):
        for j in range(n):
            if gt[i, j] < 127:
                gt[i, j] = 10
            else:
                gt[i, j] = 255

    classes = create_training_classes(img, gt)
    gmlc = GaussianClassifier(classes)
    # gmlc = MahalanobisDistanceClassifier(classes)
    return gmlc


def imgClass(imgxway, gtway1, gtway2, file_dir, out_dir=None):
    if out_dir is None:
        out_dir = file_dir
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)
    gmlc1 = classify(imgxway, gtway1)
    gmlc2 = classify(imgxway, gtway2)
    for files in os.listdir(file_dir):
        # 当前文件夹所有文件
        if files.endswith('.hdr'):  # 判断是否以.hdr结尾
            print('doing img:' + files)
            file = file_dir + '\\' + files
            img = open_image(file).load()
            clmap1 = gmlc1.classify_image(img)
            clmap2 = gmlc2.classify_image(img)
            (filename, extension) = os.path.splitext(files)
            outputway = out_dir + '\\{a}.jpg'.format(a=filename)
            clmap = cv2.bitwise_or(clmap1, clmap2)
            save_rgb(outputway, clmap)


if __name__ == '__main__':
    imgWay = r'E:\HE+CAM5\PreproEasy'                                      # 需要分类的图片所在文件夹
    outWay = r'E:\HE+CAM5\PreproEasy\res'                                  # 分类结果输出文件夹（可不选）
    img_way = r'E:\HE+CAM5\PreproEasy\HE_CAM52_mono_E_roi1_prePro.hdr'     # 训练图片路径
    gt_way1 = r'E:\HE+CAM5\PreproEasy\rgb-down\roi1_SVM.jpg'                            # 训练图片掩膜路径
    gt_way2 = r'E:\HE+CAM5\PreproEasy\rgb-down\roi1_SVMcvtnot.jpg'
    imgClass(img_way, gt_way1, gt_way2, imgWay, outWay)

