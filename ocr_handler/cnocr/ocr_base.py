from cnocr import CnOcr
from pprint import pformat

'''
训练模型：https://blog.csdn.net/WinerChopin/article/details/100066468
安装：https://blog.csdn.net/yukai08008/article/details/117085542
'''

class OCR_image:

    def __init__(self, path):

        self.image_path=path


    '''
    OCR÷中文识别
    '''
    def scan_cn_image(self):
        ocr = CnOcr(det_model_name='naive_det')

        res = ocr.ocr(self.image_path)
        print("Predicted Chars:", res)

    '''
    OCR英文识别
    '''
    def scan_eng_image(self):
        ocr = CnOcr( rec_model_name='en_PP-OCRv3')

        res = ocr.ocr(self.image_path)
        print("Predicted Chars:", res)


    '''
    OCR中英文识别
    '''
    def scan_english_cn_image(self):
        ocr = CnOcr( rec_model_name='densenet_lite_136-gru')

        res = ocr.ocr(self.image_path)

        self.print_preds(res)

    '''
    标准化输出
    '''
    def print_preds(self, pred):
        print("Predicted Chars:\n", pformat(pred))

    '''
    单行文字识别
    
    '''
    def ocr_for_single_line(self):
        ocr = CnOcr()
        out = ocr.ocr_for_single_line(self.image_path)
        print(out)




'''
OCR测试
'''
if __name__ == "__main__":
    image_path= '/data/image'
    # OCR_image('/Users/zhangmingming/pyProjects/vcrawl/ocr/test.png').scan_cn_image()
    OCR_image(image_path+'/test1.png').scan_english_cn_image()


    # OCR_image(image_path+'/cn_english.png').scan_english_cn_image()
    # OCR_image(image_path+'/single_img.png').ocr_for_single_line()















