#!/usr/bin/env python3
"""
Günün Kəlamı — Notion Yeniləyici
GitHub Actions tərəfindən hər gün avtomatik işə salınır.
Skript: köhnə kəlamı silir, yenisini səhifənin ən üstünə əlavə edir.
"""

import urllib.request
import urllib.error
import json
import datetime
import sys
import os

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
PAGE_ID       = os.environ.get("PAGE_ID", "32605da2439581068e3cf1a18b6e0a52")

SITATLAR = [
    {"text": "Bəzən uçmaq üçün düşmək lazımdır.",
     "muellif": "Albus Dambldor", "menbe": "Harry Potter", "movzu": "💪 İradə", "tarix": "2026-03-18"},
    {"text": "Həyat sənin nə etdiyinlə deyil, nə olmadığınla ölçülür.",
     "muellif": "Tyler Durden", "menbe": "Fight Club (1999)", "movzu": "🧠 Düşüncə", "tarix": "2026-03-19"},
    {"text": "Ən böyük cəsarət, özün olmağın cəsarətidir.",
     "muellif": "Ralph Waldo Emerson", "menbe": "Self-Reliance", "movzu": "💪 İradə", "tarix": "2026-03-20"},
    {"text": "Müvəffəqiyyət uğursuzluqdan uğursuzluğa coşqu itirmədən getməkdir.",
     "muellif": "Winston Churchill", "menbe": "Nitqlər", "movzu": "🔥 Motivasiya", "tarix": "2026-03-21"},
    {"text": "Ya taparsam bir yol, ya da özüm açaram.",
     "muellif": "Hannibal Barca", "menbe": "Tarix", "movzu": "🎯 Hədəf", "tarix": "2026-03-22"},
    {"text": "Həyat, başqasının fikirləri ilə yaşamaqdan ibarət deyil.",
     "muellif": "Steve Jobs", "menbe": "Stanford Nitqi, 2005", "movzu": "❤️ Həyat", "tarix": "2026-03-23"},
    {"text": "Ümid bir yuxu deyil — onu həyata keçirməyənlər üçün yuxudur.",
     "muellif": "Aragorn", "menbe": "Yüzüklərin Hökmdarı (2003)", "movzu": "🔥 Motivasiya", "tarix": "2026-03-24"},
    {"text": "Bir adam yalnız öldüyündə itir, unudulduğunda yox.",
     "muellif": "Hector", "menbe": "Coco (2017)", "movzu": "❤️ Həyat", "tarix": "2026-03-25"},
    {"text": "Özünü sev, çünki sən kainatda tək nüsxəsən.",
     "muellif": "Oscar Wilde", "menbe": "Aforizmler", "movzu": "❤️ Həyat", "tarix": "2026-03-26"},
    {"text": "Fırtına keçəcək. Amma sən olduğun kimi qal.",
     "muellif": "Paulo Coelho", "menbe": "Alxemik", "movzu": "💪 İradə", "tarix": "2026-03-27"},
    {"text": "Qorxma — qorxmağı öyrən, amma hərəkət et.",
     "muellif": "Nelson Mandela", "menbe": "Uzun Azadlığa Yol", "movzu": "💪 İradə", "tarix": "2026-03-28"},
    {"text": "Zaman puldur deyirlər, amma vaxt pulsuz əldə edilə bilmir.",
     "muellif": "Benjamin Franklin", "menbe": "Poor Richard's Almanack", "movzu": "🎯 Hədəf", "tarix": "2026-03-29"},
    {"text": "Hər gün yeni bir başlanğıcdır.",
     "muellif": "L.M. Montgomery", "menbe": "Anne of Green Gables", "movzu": "🌱 Böyümə", "tarix": "2026-03-30"},
    {"text": "Xoşbəxtlik bir hədəf deyil — yaşanılma tərzidir.",
     "muellif": "Albert Camus", "menbe": "Sezifin Əfsanəsi", "movzu": "❤️ Həyat", "tarix": "2026-03-31"},
    {"text": "Dünya sənin gördüyündən daha böyükdür.",
     "muellif": "Mufasa", "menbe": "Şir Padşahı (1994)", "movzu": "🌱 Böyümə", "tarix": "2026-04-01"},
    {"text": "Heç bir sual axmaq deyil — amma sualı verməmək axmaqlıqdır.",
     "muellif": "Richard Feynman", "menbe": "Elm üzərindəki düşüncələr", "movzu": "🧠 Düşüncə", "tarix": "2026-04-02"},
    {"text": "Uğur gizlənmir — o, hər gün etdiyin kiçik işlərdə gizlənir.",
     "muellif": "Elon Musk", "menbe": "Müsahibələr", "movzu": "🎯 Hədəf", "tarix": "2026-04-03"},
    {"text": "İnsan öz xarakterini seçmir, amma onu qurmaq onun əlindədir.",
     "muellif": "Aristotel", "menbe": "Nikomaxos Etikası", "movzu": "🌱 Böyümə", "tarix": "2026-04-04"},
    {"text": "Kitablar bizi yalnız olmayan yerə aparır.",
     "muellif": "Thomas à Kempis", "menbe": "Məsihin Təqlidi", "movzu": "🧠 Düşüncə", "tarix": "2026-04-05"},
    {"text": "Sənin ən böyük rəqibin dünənki özündür.",
     "muellif": "Muhammad Ali", "menbe": "Müsahibələr", "movzu": "💪 İradə", "tarix": "2026-04-06"},
    {"text": "Bir gün başlamaq üçün mükəmməl olmağı gözləmə.",
     "muellif": "Mark Twain", "menbe": "Aforizmler", "movzu": "🔥 Motivasiya", "tarix": "2026-04-07"},
    {"text": "Kainat öz sirlərini yalnız cəsarətlilərə açır.",
     "muellif": "Paulo Coelho", "menbe": "Alxemik", "movzu": "🎯 Hədəf", "tarix": "2026-04-08"},
    {"text": "Pul çox şey satın ala bilər, amma vaxtı geri qaytara bilməz.",
     "muellif": "Seneka", "menbe": "Həyatın Qıslığı Üzərinə", "movzu": "❤️ Həyat", "tarix": "2026-04-09"},
    {"text": "Biz qəhrəman doğulmayırıq — biz qəhrəman seçirik.",
     "muellif": "Hermiona Grencer", "menbe": "Harry Potter", "movzu": "💪 İradə", "tarix": "2026-04-10"},
    {"text": "Düşüncəni idarə edən, həyatı idarə edir.",
     "muellif": "Marcus Aurelius", "menbe": "Özümə Düşüncələr", "movzu": "🧠 Düşüncə", "tarix": "2026-04-11"},
    {"text": "Hər böyük iş kiçik bir addımla başlayır.",
     "muellif": "Lao Tzu", "menbe": "Tao Te Ching", "movzu": "🎯 Hədəf", "tarix": "2026-04-12"},
    {"text": "Uğurun sirri: başqaları nə düşünür bilmədən irəliləmək.",
     "muellif": "Jay Gatsby", "menbe": "Böyük Gatsby", "movzu": "🔥 Motivasiya", "tarix": "2026-04-13"},
    {"text": "Öyrənmək — yaşadığın müddətcə davam etməli olan bir macəradır.",
     "muellif": "Albert Einstein", "menbe": "Məktublar", "movzu": "🌱 Böyümə", "tarix": "2026-04-14"},
    {"text": "Həyat ya cəsarətli bir macəradır, ya da heç nədir.",
     "muellif": "Helen Keller", "menbe": "The Open Door", "movzu": "❤️ Həyat", "tarix": "2026-04-15"},
    {"text": "Güc qaldırmaqda deyil — qaldırdıqdan sonra düşməməkdədir.",
     "muellif": "Rocky Balboa", "menbe": "Rocky (1976)", "movzu": "💪 İradə", "tarix": "2026-04-16"},
]


def notion_request(method, endpoint, data=None):
    url = f"https://api.notion.com/v1/{endpoint}"
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": "2022-06-28",
        "Content-Type": "application/json",
    }
    body = json.dumps(data).encode("utf-8") if data else None
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        print(f"❌ Xəta {e.code}: {e.read().decode()}")
        sys.exit(1)


def bugunun_sitati():
    bugun = (datetime.datetime.utcnow() + datetime.timedelta(hours=4)).date().isoformat()
    for s in SITATLAR:
        if s["tarix"] == bugun:
            return s
    idx = datetime.date.today().timetuple().tm_yday % len(SITATLAR)
    return SITATLAR[idx]


def sehifenin_bloklari():
    result = notion_request("GET", f"blocks/{PAGE_ID}/children?page_size=100")
    return result.get("results", [])


def bloku_sil(block_id):
    notion_request("DELETE", f"blocks/{block_id}")


def kelam_bloku_yarat(sitat):
    movzu_ikon = {
        "💪 İradə": "💪", "🧠 Düşüncə": "🧠", "🔥 Motivasiya": "🔥",
        "❤️ Həyat": "❤️", "🎯 Hədəf": "🎯", "🌱 Böyümə": "🌱",
    }
    ikon = movzu_ikon.get(sitat["movzu"], "💡")
    metn = f"❝ {sitat['text']} ❞  —  {sitat['muellif']}  ·  {sitat['menbe']}  ·  {sitat['movzu']}"
    return {
        "object": "block",
        "type": "callout",
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": metn}}],
            "icon": {"type": "emoji", "emoji": ikon},
            "color": "purple_background",
        },
    }


def main():
    print("🔍 Notion səhifəsi oxunur...")
    bloqlar = sehifenin_bloklari()

    # Köhnə kəlamı tap və sil (yalnız birinci səviyyədə axtar)
    for blok in bloqlar:
        tip = blok.get("type", "")
        metn_hisseler = blok.get(tip, {}).get("rich_text", []) if tip in ("callout", "paragraph", "quote") else []
        metn = "".join(t.get("plain_text", "") for t in metn_hisseler)
        if "❝" in metn:
            bloku_sil(blok["id"])
            print("🗑️  Köhnə kəlam silindi.")
            break

    # Bugünün sitatı
    sitat = bugunun_sitati()
    print(f"📖 Bugünün kəlamı: \"{sitat['text'][:60]}\"")
    print(f"   — {sitat['muellif']}  ·  {sitat['menbe']}")

    # Səhifənin ən başına əlavə et (after olmadan = başa əlavə olunur)
    notion_request("PATCH", f"blocks/{PAGE_ID}/children", {
        "children": [kelam_bloku_yarat(sitat)]
    })

    print("✅ Notion uğurla yeniləndi!")


if __name__ == "__main__":
    if not NOTION_TOKEN:
        print("❌ NOTION_TOKEN tapılmadı!")
        sys.exit(1)
    main()
