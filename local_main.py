# -*- coding: utf-8 -*-

import sys
import cv2

import util


## カメラ or 動画 ローカル表示
def video_movie_local(input_path_or_port, mark_type, mark_files, detector_type, detector_files):
    if mark_type != 'white':
        util.check_file('Mask', mark_files[mark_type])
        mark_rgba = cv2.imread(mark_files[mark_type], cv2.IMREAD_UNCHANGED)

    capture = cv2.VideoCapture(input_path_or_port)
    capture.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    detector = util.setup_detector(detector_type, detector_files, width, height)

    try:
        while True:
            ret, target_frame = capture.read()
            face_boxes = util.detect_face_boxes(detector_type, detector, target_frame)
            for face_box in face_boxes:
                if mark_type != 'white':
                    util.replace_face(face_box, target_frame, mark_rgba)
                else:
                    util.replace_face_whitecycle(face_box, target_frame)
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
def image_local(input_img_path, mark_type, mark_files, detector_type, detector_files):
    util.check_file('Input', input_img_path)
    if mark_type != 'white':
        util.check_file('Mask', mark_files[mark_type])
        mark_rgba = cv2.imread(mark_files[mark_type], cv2.IMREAD_UNCHANGED)

    target_img = cv2.imread(input_img_path)
    height, width, _ = target_img.shape
    detector = util.setup_detector(detector_type, detector_files, width, height)
    face_boxes = util.detect_face_boxes(detector_type, detector, target_img)

    for face_box in face_boxes:
        if mark_type != 'white':
            util.replace_face(face_box, target_img, mark_rgba)
        else:
            util.replace_face_whitecycle(face_box, target_img)
    util.output_img(input_img_path, target_img)


if __name__ == '__main__':
    detector_type = 'cascade'
    mark_type = 'white'
    mark_files = {
        'dyloop': 'input_img/dynamicloop.png',
        'warai': 'input_img/waraiotoko.png',
    }
    detector_files = {
        'cascade': 'detectors/haarcascade_frontalface_default.xml',
        'caffemodel': 'detectors/opencv_face_detector.caffemodel',
        'prototxt': 'detectors/opencv_face_detector.prototxt',
        'yunet': 'detectors/yunet_n_640_640.onnx',
        }

    if len(sys.argv) < 2:
        print('set option imege/camcheck/video/movie')
        exit(1)
    if sys.argv[1] == 'camcheck':
        try:
            max_camera_num = int(sys.argv[2])
        except:
            max_camera_num = 1
        check_camera_connections(max_camera_num)
    else:
        if len(sys.argv) < 4:
            print('set detector_type cascade/caffe/yunet, mark_type white/dyloop/warai')
            exit(1)
        detector_type = sys.argv[2]
        mark_type = sys.argv[3]

        if sys.argv[1] == 'image':
            try:
                input_img = sys.argv[4]
            except:
                input_img = 'input_img/vlcsnap-2025-01-02-16h14m25s916.png'
            image_local(input_img, mark_type, mark_files, detector_type, detector_files)
        elif sys.argv[1] == 'video':
            try:
                camera_port = int(sys.argv[4])
            except:
                camera_port = 0
            video_movie_local(camera_port, mark_type, mark_files, detector_type, detector_files)
        elif sys.argv[1] == 'movie':
            try:
                input_movie = sys.argv[4]
            except:
                input_movie = 'input_movie/FourPeople_1280x720_60.mp4'
            video_movie_local(input_movie, mark_type, mark_files, detector_type, detector_files)
