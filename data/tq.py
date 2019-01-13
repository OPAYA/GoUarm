import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

pre_img = Image.open("omok_2"'.png').convert('L')

pre_arr = np.array(pre_img)

cur_img = Image.open("omok_3"'.png').convert('L')

cur_arr = np.array(cur_img)

check_arr = abs(pre_arr - cur_arr)

check_img = Image.fromarray(check_arr)

check_img.show()

check_change = True
while (check_change):
    img_list = []

    check_stable = True
    while (check_stable):
        # img_list push_back
        # time delay

        if (len(img_list) >= 5):
            # stable check
            check_stable = False

    # change check
    check_change = False


