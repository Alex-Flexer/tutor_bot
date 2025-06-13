# from os import listdir, rename
# from os.path import join


# path = "./oge/"
# for sub_idx, sub_folder in enumerate(sorted(listdir(path), key=lambda x: int(x.replace("вар", "")))):
#     old_sub_path = join(path, sub_folder)
#     new_sub_path = join(path, str(sub_idx))
#     # print(old_sub_path, new_sub_path)
#     # rename(old_sub_path, new_sub_path)
#     # print("\n\n")
#     files = [file for file in listdir(new_sub_path) if file.endswith(".png")]
#     for idx, sub_file in enumerate(sorted(files)):
#         # if sub_file.endswith(".png"):
#             # print(str(idx), sub_file[:-4])
#             # if str(idx) == sub_file[:-4]:
#             #     continue

#           old_sub_file_path = join(new_sub_path, sub_file)
#           new_sub_file_path = join(new_sub_path, (str(idx - 1) if idx > 0 else "img") + ".png")
#           rename(old_sub_file_path, new_sub_file_path)
#         #   print(idx, old_sub_file_path, new_sub_file_path)


# # # print(join("oge"))

# # from json import loads, load

# # json = loads("""{
# #   "ege": [],
# #   "oge": [
# #     [
# #       "1273",
# #       "10",
# #       "5",
# #       "13",
# #       "500",
# #       "11",
# #       "3",
# #       "64",
# #       "-6",
# #       "0.7",
# #       "312",
# #       "-126.4",
# #       "2",
# #       "36",
# #       "137",
# #       "30",
# #       "936",
# #       "2",
# #       "3"
# #     ],
# #     [
# #       "4652",
# #       "12",
# #       "7",
# #       "11",
# #       "600",
# #       "8",
# #       "2",
# #       "81",
# #       "7",
# #       "0.8",
# #       "321",
# #       "-133.6",
# #       "3",
# #       "37",
# #       "132",
# #       "24",
# #       "1620",
# #       "3",
# #       "3"
# #     ],
# #     [
# #       "8526",
# #       "3.2",
# #       "230",
# #       "11",
# #       "830",
# #       "36",
# #       "3",
# #       "144",
# #       "-33",
# #       "0.3",
# #       "312",
# #       "304",
# #       "1",
# #       "68",
# #       "216",
# #       "51",
# #       "86",
# #       "12",
# #       "2"
# #     ],
# #     [
# #       "3428",
# #       "5.76",
# #       "260",
# #       "16",
# #       "750",
# #       "16",
# #       "2",
# #       "189",
# #       "-31",
# #       "0.2",
# #       "123",
# #       "293",
# #       "2",
# #       "88",
# #       "217",
# #       "21",
# #       "88",
# #       "15",
# #       "1"
# #     ],
# #     [
# #       "2413",
# #       "32",
# #       "300",
# #       "310.8",
# #       "2000",
# #       "21",
# #       "4",
# #       "243",
# #       "-10",
# #       "0.28",
# #       "312",
# #       "5",
# #       "4",
# #       "96",
# #       "12",
# #       "11",
# #       "51",
# #       "18",
# #       "13"
# #     ]
# #   ]
# # }""")

# # with open("answers.json", 'r', encoding='utf-8') as file:
# #     old_json = load(file)

# # # for i in range(5):
# # print(old_json["oge"] == json["oge"])
from requests import get
from bs4 import BeautifulSoup
from googletrans import Translator
from transliterate import translit
import asyncio


translator = Translator()


async def translator_translate(word):
    result = await translator.translate(word, dest='en')
    return result.text


def get_temperature(city: str):
    headers = {"Cookie": 'yw_allergy_promo=1; _yasc=C/lSJLsx+LcIFqJEVJ5alUTH0LzCggmYJPuJnUO46jIusznQHntlJ8EOl8v7nLRSYYmAlQ8=; i=X0wHJMzYf0z2cQ8IWvoE0YLjpL6PJbVmy6fwOV0YEihHD2JYSS9tyTQWKE8Kq/oVyeZmqw9XM+Mcnng/aS/+Q0Wc0Rg=; yandexuid=4308001361737620354; yashr=9853474291737620354; bh=YIrR2cAGahLcyumIDvKso64E5cjwjgOUtgI=; is_gdpr=0; is_gdpr_b=CKKpXBD6twIoAg==; receive-cookie-deprecation=1; yuidss=4308001361737620354; yp=2058016242.multib.1#2058016310.udn.cDpzYXNoYWZsZXhzZXI%3D; yandex_login=sashaflexser; maps_routes_travel_mode=masstransit; Session_id=3:1745780859.5.0.1742656310235:vOmMsg:6697.1.2:1|973718500.-1.2.3:1742656310|3:10306641.448704.be7Wt_j_R7vFM8qsDExnrwhh-AI; sessar=1.1201.CiBZn0af6EvXv22ez8a5SV0EwrIxz7LOkrExTuj0sUJ9jA.F_DfrOD2TzV82SS4oA1VDJO24d2_fXjNBJfdQrDNjVc; sessionid2=3:1745780859.5.0.1742656310235:vOmMsg:6697.1.2:1|973718500.-1.2.3:1742656310|3:10306641.448704.fakesign0000000000000000000; skid=6127090731743349570; KIykI=1; coockoos=6'}
    resp = get(f"https://yandex.ru/pogoda/ru/{city}", headers=headers)
    res = None
    if resp.ok:
        bs = BeautifulSoup(resp.text, "html.parser")
        temperature_el = bs.select_one(".AppFactTemperature_wrap__z_f_O")
        if temperature_el is not None:
            res = temperature_el.text.replace("°", "")
    return res

async def main():
    input_city = input()
    translate_city = (await translator_translate(input_city)).lower().replace(" ", "-")
    translite_city = translit(input_city, "ru", reversed=True).lower()
    res = get_temperature(translate_city)
    if not res:
        res = get_temperature(translite_city)
    print(res)

asyncio.run(main())
