# pillow的使用,  open save. 廖雪峰
import base64

import requests
from PIL import Image, ImageFilter
from pygments import BytesIO
from pytesseract import image_to_string


def main():
    gui_do_img = Image.open(open('a2.jpg', 'rb'))
    gui_do_img1 = gui_do_img.filter(ImageFilter.GaussianBlur)
    gui_do_img1.save(open('a2a.jpg', 'wb'))

    img1 = Image.open(open('a7.jpg', 'rb'))
    img2 = img1.point(lambda x: 0 if x < 128 else 255)
    img2.save(open('a7a.jpg', 'wb'))

    print(image_to_string(img2))

    resp = requests.get(
        'https://pin2.aliyun.com/get_img?type=150_40&identity=mailsso.mxhichina.com&sessionid=k0xHyBxU3K3dGXb59mP9cdeTXxL9gLHSTKhRZCryHxpOoyk4lAVuJhgw==')
    img3 = Image.open(BytesIO(resp.content))
    img3.save('hello.jpg')
    print(image_to_string(img3))
    print(base64.b64encode(resp.content))


if __name__ == '__main__':
    main()