#!/usr/bin/env bash

mkdir -p detectors

curl 'https://raw.githubusercontent.com/opencv/opencv/refs/heads/4.x/data/haarcascades/haarcascade_frontalface_default.xml' -o detectors/haarcascade_frontalface_default.xml

# curl 'https://raw.githubusercontent.com/opencv/opencv_3rdparty/refs/heads/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel' -o detectors/opencv_face_detector.caffemodel
curl 'https://raw.githubusercontent.com/dkurt/cvpr2019/refs/heads/master/opencv_face_detector.caffemodel' -o detectors/opencv_face_detector.caffemodel
curl 'https://raw.githubusercontent.com/dkurt/cvpr2019/refs/heads/master/opencv_face_detector.prototxt' -o detectors/opencv_face_detector.prototxt

curl 'https://raw.githubusercontent.com/ShiqiYu/libfacedetection.train/refs/heads/master/onnx/yunet_n_640_640.onnx' -o detectors/yunet_n_640_640.onnx
