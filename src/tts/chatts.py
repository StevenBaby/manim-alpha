import datetime
import os
import zipfile
import re
from io import BytesIO
from pathlib import Path

from manim import logger
from manim_voiceover.helper import prompt_ask_missing_package, remove_bookmarks, wav2mp3
from manim_voiceover.services.base import SpeechService
from manim_voiceover import VoiceoverScene

import requests

chattts_service_host = os.environ.get("CHATTTS_SERVICE_HOST", "localhost")
chattts_service_port = os.environ.get("CHATTTS_SERVICE_PORT", "8000")

CHATTTS_URL = f"http://{chattts_service_host}:{chattts_service_port}/generate_voice"


def generate_voice(text, output_path):
    # main infer params
    body = {
        "text": [text],
        "stream": False,
        "lang": None,
        "skip_refine_text": True,
        "refine_text_only": False,
        "use_decoder": False,
        "audio_seed": 1111,
        "text_seed": None,
        "do_text_normalization": False,
        "do_homophone_replacement": False,
    }

    # refine text params
    params_refine_text = {
        "prompt": "",
        "top_P": 0.9,
        "top_K": 3,
        "temperature": 0.0,
        "repetition_penalty": 1,
        "max_new_token": 384,
        "min_new_token": 0,
        "show_tqdm": True,
        "ensure_non_empty": True,
        "stream_batch": 24,
    }
    body["params_refine_text"] = params_refine_text

    # infer code params
    params_infer_code = {
        "prompt": "[speed_8][oral_1][laugh_0][break_5]",
        "top_P": 0.75,
        "top_K": 20,
        "temperature": 0.0001,
        "repetition_penalty": 1.05,
        "max_new_token": 2048,
        "min_new_token": 0,
        "show_tqdm": True,
        "ensure_non_empty": False,
        "stream_batch": True,
        "spk_emb": '蘁淰敥欀栂跞弋竌蛵蛏斋腻虚揝撌僳侌譓睅嬽咶涉篒湀櫱如毫就専娇犭奰莜毀購湳蛫楑棓滏糝廣政箑櫁擿覱櫭蘱嘆脓劺蟵啅嘠壴葖艼礬虎夵蚧弤乁劮滸恍尻僈峏荁窖枥臙琮怅滒诗嫂玓琶缎揾淫蘹歩緺蕰畆禚旰侱攄儏漥煄羯罆弴籞癭籷莗磧喤櫱蛆痫兲瀓泈捕績尼厸蕇坱絍审焄肠嗭篸恿絙厗半兼貦偟凎不尢凈呤簇贃棹淽涞科褰篕媪渨豈崌臎苅僌蜘媆繬承蜞翻敌剄灏仹虙污肳単斈峴囕堷緬徕朰俾毈脯敵瘮槳巟糴茭订攪叝擡澽薈礞氌璤渹哜奏眬戽伡笶泩簯擉磽勏晗贏崲溩呃犯硜菼臬庾洝域絻堓蘲紗撓屧杔璆廂歜幇歚欜岾咧痾嗓栿啣擟茣膹暪苸嚯呉仠偔媹譌惖筋摑疨疨谼磥囵蝟氯牍蜊壐亝絖焒訣凒杭俁賾咛腞幪緯簆笶弢襠桏枸皿徺泅氆謽豫檢湸臗灙亮禆篊蕄楄愨搶蕬昣囂暿懂衘昜窷值榙晦砗垭嘏蚚愢丝求澨垯诧蜢戋档志蠛誚唄廰怲柈墍識詣絉救孀藳筳櫬斂忯惬膮桰襞帪害壴焓旽盾笾楁蜝粆簅苄浠穤瀖盓熌糎貿筨貝幵监岔莢統湌恋跞至泡旸粢剥垞萔瓱稥腁疛偀仼濇章獞泩葲訩情爄暡櫷呲謫殹幫诶傊獟噊皂挴剫煸潐詄纽胉萶岕婘氪蝓譚房忰竘献牦蕯翪艏撻优筙冏奖握渼僵梉檴澹挟族儡漍朥竺侫緇外卯参矫耄湏昕縝氌嚏獐泊熞該濽曱筜訦湊膣唪裬嵤焈毪紬翾磡潶洢裀氚甛謧祍衺烦瞻兿岃僼祂茒曧寥娮敲哤瀿挚罕妤楹磇樷篊惙岆棫寨秇檄瘉设壣畷搹豃诅猂墭歰绮汢拠葑坡居庢熘棼揨犌員幭虬卹萬岱藟妦喚啑梔計剔浽垆箇諍惩譔欒筄嵳僭嬝扴彆兊罌眡玔瞬埓爜愉眓矱嘀厖箩脋噭抸濞孂玳芦緧晧貗荑漳寠杶羕讯諞跾讪回筯瀴膛殘峃肧賌萋炰楹壡沣享涾稵瀧杣糬潍艏讽嬽裰噲剃稬荆展甸傘峼傼壥璾嚏漪礗坪簠墯蝟皆笴蜱堃壊聸欚檡貸劒墲筓箇潓嶈刓瓬唷璉缜氭謆旚缰蛂瑜蓩襛獜蕸糯夋谾朰竏薥塑濊为茽艹缄滻箔硇薺兛羜檑嫢紒峙粬斱囉枟攱氶赚脺哝煠甼曊嘦眏店视斧兂諏稴曲漼瀤訩貾窓繴蚊唠愆寙珷撣孡缚曣徉誔襸禝佦儓簡粁芁笧歰毊襁椿刈袅譔昋聟囼唗眅账借浑纬恻箒褊泋湑玂構葴淬蘆肰缃崂泠禯蜷圜栲发崜諘詞徕臉惴狅敌罖訽榟稫虋屼渔伡幕矍蘀弇爲眴悌皸奩勺僺蔊剘莱砳晥聪紪囧戺趦熥幖旤艹棇仩賿攞仚岆细苘枒肐渇誮堣奰蝊泇缞茚哦朘癄监滫娼滓矧璨偗恭蝶讷奄椶旇堕紓摐藕蚬擲椗訪岝夛臬炜櫝藉撢犝窬叩稔膦滓栝畲莈毐嵳厣缓赗譫瘀',
    }
    body["params_infer_code"] = params_infer_code

    try:
        response = requests.post(CHATTTS_URL, json=body)
        response.raise_for_status()
        with zipfile.ZipFile(BytesIO(response.content), "r") as zip_ref:
            # save files for each request in a different folder
            # dt = datetime.datetime.now()
            # ts = int(dt.timestamp())
            # os.makedirs(os.path.dirname(output_path), 0o755, exist_ok=True)
            zip_ref.extract('0.mp3', os.path.dirname(output_path))
            os.rename(os.path.join(os.path.dirname(
                output_path), '0.mp3'), output_path)
            # print("Extracted files into", output_path)

    except requests.exceptions.RequestException as e:
        print(f"Request Error: {e}")


class ChatTTSService(SpeechService):

    def generate_from_text(
        self, text: str, cache_dir: str = None, path: str = None, **kwargs
    ) -> dict:
        if cache_dir is None:
            cache_dir = self.cache_dir

        input_text = remove_bookmarks(text)
        input_data = {"input_text": text, "service": "chattts"}
        cached_result = self.get_cached_result(input_data, cache_dir)
        if cached_result is not None:
            return cached_result

        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".mp3"
        else:
            audio_path = path

        output_path = str(Path(cache_dir) / audio_path)

        generate_voice(text, output_path)

        json_dict = {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
            # "word_boundaries": word_boundaries,
        }

        return json_dict


class ChatTTSScence(VoiceoverScene):

    def add_subcaption(self, content, duration=1, offset=0):
        content = re.sub(r'( *\[.+\] *?|，|。)', ' ', content)
        return super().add_subcaption(content, duration, offset)


if __name__ == '__main__':
    generate_voice('我看到我的爱恋 我飞到她的身边', 'media/1.mp3')
