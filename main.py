# -*- coding: utf-8 -*-

import sys
import os
import cv2

# 動画バージョン
def video_main(mask_img_path, cascade_file_path, camera_port):
    check_input('Mask', mask_img_path)
    mark_rgba = cv2.imread(mask_img_path, cv2.IMREAD_UNCHANGED)
    cascade = cv2.CascadeClassifier(cascade_file_path)

    try:
        capture = cv2.VideoCapture(camera_port)
        print('capture start: ', capture)
        while(True):
            ret, target_frame = capture.read()
            target_frame_gray = cv2.cvtColor(target_frame, cv2.COLOR_BGR2GRAY)
            # faces = cascade.detectMultiScale(target_frame_gray, scaleFactor=1.1, minNeighbors=3, minSize=(75, 75))
            # for face_ps in faces:
            #     replace_face(face_ps, target_frame, mark_rgba)
            cv2.imshow("frame_orig", target_frame)
            cv2.waitKey(100)
    except Exception as e:
        print(f'exception: {e}')


def check_camera_connections(max_camera_num):
    true_camera_is = []

    for camera_number in range(0, max_camera_num):
        try:
            capture = cv2.VideoCapture(camera_number)
            ret, frame = capture.read()
            print(frame.shape)
            if ret is True:
                true_camera_is.append(camera_number)
                cv2.imwrite(f'output_img/camera{camera_number}.png', frame)
                print(f'port {camera_number} found')
        except Exception as e:
            print(f'exception: {e}')
    print('Connected', len(true_camera_is), 'cameras')


def check_input(filetype, img_path):
    if not os.path.exists(img_path):
        print(f'No {filetype} File.')
        exit(1)


def replace_face(face_ps, target_img, mark_rgba):
    # 画像合成用にコピー
    mark_alpha_tmp = mark_rgba.copy()
    x, y, w, h = face_ps
    mark_alpha_tmp = cv2.resize(mark_alpha_tmp, dsize=(w, h))

    # 入力画像の顔の部分にはめ込む
    for dx in range(0, w):
        for dy in range(0, h):
            # アルファチャネルが0でないなら画像を入れ替える
            if mark_alpha_tmp[dy, dx, 3] != 0:
                target_img[y + dy, x + dx, :3] = mark_alpha_tmp[dy, dx, :3]


# 画像バージョン
def img_main(input_img_path, mask_img_path, cascade_file_path):

    check_input('Input', input_img_path)
    check_input('Mask', mask_img_path)
    mark_rgba = cv2.imread(mask_img_path, cv2.IMREAD_UNCHANGED)
    cascade = cv2.CascadeClassifier(cascade_file_path)

    target_img = cv2.imread(input_img_path)
    faces = cascade.detectMultiScale(target_img, scaleFactor=1.1, minNeighbors=3, minSize=(75, 75))

    for face_ps in faces:
        replace_face(face_ps, target_img, mark_rgba)

    output_img(input_img_path, target_img)


def output_img(input_img_path, target_img):
    output_img_path = 'output_img/{}'.format('/'.join(input_img.split('/')[1:]))
    print(f'Output: {output_img_path}')
    cv2.imwrite(output_img_path, target_img)


if __name__ == '__main__':
    input_img = 'input_img/vlcsnap-2025-01-02-16h14m25s916.png'
    mask_img = 'input_img/waraiotoko.png'
    cascade_file = 'haarcascade_frontalface_default.xml'

    if len(sys.argv) < 2:
        print('set option imege/check/video')
        exit(1)
    if sys.argv[1] == 'image':
        img_main(input_img, mask_img, cascade_file)
    elif sys.argv[1] == 'check':
        try:
            max_camera_num = int(sys.argv[2])
        except:
            max_camera_num = 10
        check_camera_connections(max_camera_num)
    elif sys.argv[1] == 'video':
        camera_port = 0
        video_main(mask_img, cascade_file, camera_port)
