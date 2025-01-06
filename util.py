import os
import cv2

def check_file(filetype, img_path):
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


def output_img(input_img_path, target_img):
    output_img_path = 'output_img/{}'.format('/'.join(input_img_path.split('/')[1:]))
    print(f'Output: {output_img_path}')
    cv2.imwrite(output_img_path, target_img)
