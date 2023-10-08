from cnocr import CnOcr
from pprint import pformat

'''
训练模型：https://blog.csdn.net/WinerChopin/article/details/100066468
安装：https://blog.csdn.net/yukai08008/article/details/117085542
'''


class OcrImage:

    def __init__(self):
        print()

    '''
    OCR中文识别
    '''

    def scan_cn_image(self, image_path):
        ocr = CnOcr(det_model_name='naive_det')

        res = ocr.ocr(image_path)
        print("Predicted Chars:", res)

    '''
    OCR英文识别
    '''

    def scan_eng_image(self, image_path):
        ocr = CnOcr(rec_model_name='en_PP-OCRv3')

        res = ocr.ocr(image_path)
        print("Predicted Chars:", res)

    '''
    OCR中英文识别
    '''

    def scan_english_cn_image(self, image_path):
        ocr = CnOcr(rec_model_name='densenet_lite_136-gru')

        res = ocr.ocr(image_path)
        text = ' '.join([x['text'] for x in res])
        print(text)

        self.print_preds(res)

    '''
    标准化输出
    '''

    def print_preds(self, pred):
        print("Predicted Chars:\n", pformat(pred))

    '''
    单行文字识别
    
    '''

    def ocr_for_single_line(self, image_path):
        ocr = CnOcr()
        out = ocr.ocr_for_single_line(image_path)
        print(out)



    def test(self, img_fp):
        import mxnet as mx
        from cnocr import CnOcr
        ocr = CnOcr()
        # img_fp = 'examples/multi-line_cn1.png'
        img = mx.image.imread(img_fp, 1)
        res = ocr.ocr(img)
        print("Predicted Chars:", res)

'''
OCR测试
'''
if __name__ == "__main__":
    image_path = '/data/image'
    # OCR_image('/Users/zhangmingming/pyProjects/vcrawl/ocr/test.png').scan_cn_image()
    # OcrImage().scan_english_cn_image('./tes.jpg')
    OcrImage().test('./tes.jpg')

    # OCR_image(image_path+'/cn_english.png').scan_english_cn_image()
    # OCR_image(image_path+'/single_img.png').ocr_for_single_line()
