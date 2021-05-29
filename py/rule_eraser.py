# 罫線だけ消すやつ
import cv2
import sys
import numpy as np

input_file_path = sys.argv[1]
output_file_path = sys.argv[2]

img1 = cv2.imread(input_file_path, 0)

# 大雑把に罫線を消す
kernel = np.ones((4, 1), np.uint8)
closing1 = cv2.morphologyEx(img1, cv2.MORPH_CLOSE, kernel)

# 除いた罫線
# https://emotionexplorer.blog.fc2.com/blog-entry-181.html
bitwise1 = cv2.bitwise_xor(img1, closing1)

# ブランク画像を作成
rows, cols = img1.shape
blank = np.zeros((rows, cols, 3), np.uint8)
blank = cv2.cvtColor(blank, cv2.COLOR_BGR2GRAY)

#←全ゼロデータに255を足してホワイトにする
blank += 255

# https://kyudy.hatenablog.com/entry/2019/10/26/141330
thresh_spike = cols / 4
vp = np.sum((bitwise1 != 0).astype(np.uint8), axis=1)
loc_y_spike = np.where(vp > thresh_spike)
line1 = blank.copy()

# ブランク画像に線を描画する
for y in loc_y_spike[0]:
    line_color = (0, 0, 0) # black
    cv2.line(line1, (0, y), (cols, y), line_color, thickness=1)

# 線の歪みを考慮して線のシルエットを大きくする
kernel = np.ones((10,10),np.uint8)
line1 = cv2.erode(line1,kernel,iterations = 2)

# 罫線の周囲を切り取る
bitwise2 = cv2.bitwise_or(img1, line1)

# 大雑把に罫線を消す
kernel = np.ones((4,1),np.uint8)
closing2 = cv2.morphologyEx(bitwise2, cv2.MORPH_CLOSE, kernel)

# 黒をつなげる
kernel = np.ones((10, 150), np.uint8) 
opening1 = cv2.morphologyEx(closing2, cv2.MORPH_OPEN, kernel)

# 黒を太くする
kernel = np.ones((5,1),np.uint8)
erosion1 = cv2.erode(opening1, kernel, iterations = 1)

# 大雑把に罫線を消す
kernel = np.ones((3,1),np.uint8)
closing3 = cv2.morphologyEx(bitwise2, cv2.MORPH_CLOSE, kernel)

# 白黒反転
line2 = 255 - line1

# 合成
bitwise3 = cv2.bitwise_or(closing3, erosion1)
bitwise4 = cv2.bitwise_or(img1, line2)
bitwise5 = cv2.bitwise_and(bitwise3, bitwise4)

"""
cv2.imshow("bitwise5", bitwise5)
cv2.imshow("img", img)
cv2.waitKey(0)
"""

cv2.imwrite(output_file_path, bitwise5)
