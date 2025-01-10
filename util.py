# -*- coding: utf-8 -*-

import os
import cv2

def check_file(filetype, img_path):
    if not os.path.exists(img_path):
        print(f'No {filetype} File. {img_path}')
        exit(1)


def setup_detector(detector_type: str, detector_files, width, height):
    detector = None
    if detector_type == 'cascade':
        detector = cv2.CascadeClassifier(detector_files['cascade'])
    elif detector_type == 'caffe':
        detector = cv2.dnn_DetectionModel(
            cv2.dnn.readNet(detector_files['caffemodel'], detector_files['prototxt']))
        detector.setInputSize(300, 300)
        detector.setInputMean((104.0, 177.0, 123.0))
    elif detector_type == 'yunet':
        detector = cv2.FaceDetectorYN.create(detector_files['yunet'], "", (0, 0))
        detector.setInputSize((width, height))
    return detector


def detect_face_boxes(detector_type: str, detector, target_image):
    if detector_type == 'cascade':
        target_frame_gray = cv2.cvtColor(target_image, cv2.COLOR_BGR2GRAY)
        face_boxes = detector.detectMultiScale(target_image, scaleFactor=1.1, minNeighbors=3, minSize=(50, 50))
    elif detector_type == 'caffe':
        _, _, face_boxes = detector.detect(target_image)
    elif detector_type == 'yunet':
        _, face_boxes = detector.detect(target_image)
    face_boxes = face_boxes if face_boxes is not None else []
    return face_boxes


def replace_face(face_box, target_img, mark_rgba):
    # 画像合成用にコピー
    mark_alpha_tmp = mark_rgba.copy()
    x, y, w, h = list(map(int, face_box[:4]))
    mark_alpha_tmp = cv2.resize(mark_alpha_tmp, dsize=(w, h))

    # 入力画像の顔の部分にはめ込む
    for dx in range(0, w):
        for dy in range(0, h):
            # アルファチャネルが0でないなら画像を入れ替える
            if mark_alpha_tmp[dy, dx, 3] != 0:
                target_img[y + dy, x + dx, :3] = mark_alpha_tmp[dy, dx, :3]

def replace_face_whitecycle(face_box, target_img):
    x, y, w, h = list(map(int, face_box[:4]))
    # 入力画像の顔の部分にはめ込む
    for dx in range(0, w):
        for dy in range(0, h):
            # 楕円内に含まれるなら
            if ((dx - w/2)**2 / (w/2)**2 + (dy - h/2)**2 / (h/2)**2) <= 1:
                target_img[y + dy, x + dx, :3] = (255, 255, 255)


def output_img(input_img_path, target_img):
    output_img_path = 'output_img/{}'.format('/'.join(input_img_path.split('/')[1:]))
    print(f'Output: {output_img_path}')
    cv2.imwrite(output_img_path, target_img)
