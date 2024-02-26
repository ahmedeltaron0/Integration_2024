
from text_spliter import split_text
from language import check_lang
from voice_cloning import voice_cloning
import time
    
def tts_All_code(input_lang,input_text,input_audio):
    start=time.time()
    result=check_lang(input_lang)
    chunks=split_text(input_text)
    finial_result=voice_cloning(input_audio,result,chunks)
    end=time.time()
    excution_time=end-start
    print(excution_time)
    return finial_result

input_audio="amr_adib.wav"
input_text = '''
في عام 1964 م رسب محمد علي في الاختبارات المؤهلة للالتحاق بجيش الولايات المتحدة لأن مهاراته الكتابية واللغوية كانت دون المستوى. على أية حال، في بدايات عام 1966 م تمت مراجعة الاختبارات وصنف محمد علي على أنه ينتمي للمستوى ، مما يؤهله للالتحاق بالقوات المسلحة. كان هذا في غاية الخطورة: لأن الولايات المتحدة كانت في حالة حرب مع فيتنام. عندما تم إخباره بنجاحه في الاختبارات، أعلن أنه يرفض أن يخدم في جيش الولايات المتحدة واعتبر نفسه معارضا للحرب.
قال محمد علي: «هذه الحرب ضد تعاليم القرآن، وإننا - كمسلمين - ليس من المفترض أن نخوض حروبًا إلا إذا كانت في سبيل الله». كما أعلن في عام 1966: «لن أحاربهم فهم لم يلقبوني بالزنجي».
'''
input_lang="ArabIc"
tts_All_code(input_lang, input_text,input_audio)
