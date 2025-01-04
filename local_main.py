# -*- coding: utf-8 -*-

import sys
import cv2

import util


## カメラ or 動画 ローカル表示
def video_movie_local(input_path_or_port, mask_img_path, cascade_file_path):
    util.check_file('Mask', mask_img_path)
    mark_rgba = cv2.imread(mask_img_path, cv2.IMREAD_UNCHANGED)
    cascade = cv2.CascadeClassifier(cascade_file_path)

    capture = cv2.VideoCapture(input_path_or_port)
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
    try:
        while True:
            ret, target_frame = capture.read()
            target_frame_gray = cv2.cvtColor(target_frame, cv2.COLOR_BGR2GRAY)
            faces = cascade.detectMultiScale(target_frame_gray, scaleFactor=1.1, minNeighbors=3, minSize=(75, 75))
            for face_ps in faces:
                util.replace_face(face_ps, target_frame, mark_rgba)
            cv2.imshow("Masked", target_frame)

            # 'q' キーが押されたらループを抜ける
            if cv2.waitKey(1) == ord("q"):
                break
    except Exception as e:
        print(f'exception: {e}')
    finally:
        capture.release()
        cv2.destroyAllWindows()


## カメラ 接続チェック
def check_camera_connections(max_camera_num):
    true_camera_is = []

    for camera_number in range(0, max_camera_num):
        try:
            capture = cv2.VideoCapture(camera_number)
            capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
            ret, frame = capture.read()
            if ret is True:
                true_camera_is.append(camera_number)
                cv2.imwrite(f'output_img/camera{camera_number}.png', frame)
                print(f'port {camera_number} found. shape:', frame.shape)
        except Exception as e:
            print(f'exception: {e}')
    print('Connected', len(true_camera_is), 'cameras')


## 画像 ローカル保存
def image_local(input_img_path, mask_img_path, cascade_file_path):

    util.check_file('Input', input_img_path)
    util.check_file('Mask', mask_img_path)
    mark_rgba = cv2.imread(mask_img_path, cv2.IMREAD_UNCHANGED)
    cascade = cv2.CascadeClassifier(cascade_file_path)

    target_img = cv2.imread(input_img_path)
    faces = cascade.detectMultiScale(target_img, scaleFactor=1.1, minNeighbors=3, minSize=(75, 75))

    for face_ps in faces:
        util.replace_face(face_ps, target_img, mark_rgba)
    util.output_img(input_img_path, target_img)


if __name__ == '__main__':
    mask_img = 'input_img/waraiotoko.png'
    # mask_img = 'input_img/dynamicloop.png'
    cascade_file = 'haarcascade_frontalface_default.xml'

    if len(sys.argv) < 2:
        print('set option imege/camcheck/video/movie')
        exit(1)
    if sys.argv[1] == 'image':
        try:
            input_img = sys.argv[2]
        except:
            input_img = 'input_img/vlcsnap-2025-01-02-16h14m25s916.png'
        image_local(input_img, mask_img, cascade_file)
    elif sys.argv[1] == 'camcheck':
        try:
            max_camera_num = int(sys.argv[2])
        except:
            max_camera_num = 1
        check_camera_connections(max_camera_num)
    elif sys.argv[1] == 'video':
        try:
            camera_port = int(sys.argv[2])
        except:
            camera_port = 0
        video_movie_local(camera_port, mask_img, cascade_file)
    elif sys.argv[1] == 'movie':
        try:
            input_movie = sys.argv[2]
        except:
            input_movie = 'input_movie/FourPeople_1280x720_60.mp4'
        video_movie_local(input_movie, mask_img, cascade_file)
