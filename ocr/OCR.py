from cnocr import CnOcr


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
        print("Predicted Chars:", res)

'''
OCR测试
'''
if __name__ == "__main__":
    image_path='/Users/zhangmingming/pyProjects/vcrawl/data/image'
    # OCR_image('/Users/zhangmingming/pyProjects/vcrawl/ocr/test.png').scan_cn_image()
    # OCR_image('/Users/zhangmingming/pyProjects/vcrawl/ocr/eng_img.png').scan_eng_cn_image()


    OCR_image(image_path+'/cn_english.png').scan_english_cn_image()















