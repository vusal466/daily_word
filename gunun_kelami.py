#!/usr/bin/env python3
"""
Günün Kəlamı — Notion Yeniləyici
Mövcud callout blokunu yerindəcə yeniləyir (silmir).
Format: ❝ İfadə ❞  —  Müəllif  ·  Mənbə  ·  Mövzu  ·  Növ
"""

import urllib.request
import urllib.error
import json
import datetime
import sys
import os

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "")
PAGE_ID      = os.environ.get("PAGE_ID", "32605da2439581068e3cf1a18b6e0a52")

SITATLAR = [
    {"text": "Bəzən uçmaq üçün düşmək lazımdır.",
     "muellif": "Albus Dambldor", "menbe": "Harry Potter", "nov": "📚 Kitab", "movzu": "💪 İradə", "tarix": "2026-03-18"},
    {"text": "Həyat sənin nə etdiyinlə deyil, nə olmadığınla ölçülür.",
     "muellif": "Tyler Durden", "menbe": "Fight Club (1999)", "nov": "🎬 Film", "movzu": "🧠 Düşüncə", "tarix": "2026-03-19"},
    {"text": "Ən böyük cəsarət, özün olmağın cəsarətidir.",
     "muellif": "Ralph Waldo Emerson", "menbe": "Self-Reliance", "nov": "📚 Kitab", "movzu": "💪 İradə", "tarix": "2026-03-20"},
    {"text": "Müvəffəqiyyət uğursuzluqdan uğursuzluğa coşqu itirmədən getməkdir.",
     "muellif": "Winston Churchill", "menbe": "Nitqlər", "nov": "👤 Şəxsiyyət", "movzu": "🔥 Motivasiya", "tarix": "2026-03-21"},
    {"text": "Ya taparsam bir yol, ya da özüm açaram.",
     "muellif": "Hannibal Barca", "menbe": "Tarix", "nov": "🧠 Filosof", "movzu": "🎯 Hədəf", "tarix": "2026-03-22"},
    {"text": "Həyat, başqasının fikirləri ilə yaşamaqdan ibarət deyil.",
     "muellif": "Steve Jobs", "menbe": "Stanford Nitqi, 2005", "nov": "👤 Şəxsiyyət", "movzu": "❤️ Həyat", "tarix": "2026-03-23"},
    {"text": "Ümid bir yuxu deyil — onu həyata keçirməyənlər üçün yuxudur.",
     "muellif": "Aragorn", "menbe": "Yüzüklərin Hökmdarı (2003)", "nov": "🎬 Film", "movzu": "🔥 Motivasiya", "tarix": "2026-03-24"},
    {"text": "Bir adam yalnız öldüyündə itir, unudulduğunda yox.",
     "muellif": "Hector", "menbe": "Coco (2017)", "nov": "🎬 Film", "movzu": "❤️ Həyat", "tarix": "2026-03-25"},
    {"text": "Özünü sev, çünki sən kainatda tək nüsxəsən.",
     "muellif": "Oscar Wilde", "menbe": "Aforizmler", "nov": "✍️ Yazıçı", "movzu": "❤️ Həyat", "tarix": "2026-03-26"},
    {"text": "Fırtına keçəcək. Amma sən olduğun kimi qal.",
     "muellif": "Paulo Coelho", "menbe": "Alxemik", "nov": "📚 Kitab", "movzu": "💪 İradə", "tarix": "2026-03-27"},
    {"text": "Qorxma — qorxmağı öyrən, amma hərəkət et.",
     "muellif": "Nelson Mandela", "menbe": "Uzun Azadlığa Yol", "nov": "📚 Kitab", "movzu": "💪 İradə", "tarix": "2026-03-28"},
    {"text": "Zaman puldur deyirlər, amma vaxt pulsuz əldə edilə bilmir.",
     "muellif": "Benjamin Franklin", "menbe": "Poor Richard's Almanack", "nov": "✍️ Yazıçı", "movzu": "🎯 Hədəf", "tarix": "2026-03-29"},
    {"text": "Hər gün yeni bir başlanğıcdır.",
     "muellif": "L.M. Montgomery", "menbe": "Anne of Green Gables", "nov": "📚 Kitab", "movzu": "🌱 Böyümə", "tarix": "2026-03-30"},
    {"text": "Xoşbəxtlik bir hədəf deyil — yaşanılma tərzidir.",
     "muellif": "Albert Camus", "menbe": "Sezifin Əfsanəsi", "nov": "📚 Kitab", "movzu": "❤️ Həyat", "tarix": "2026-03-31"},
    {"text": "Dünya sənin gördüyündən daha böyükdür.",
     "muellif": "Mufasa", "menbe": "Şir Padşahı (1994)", "nov": "🎬 Film", "movzu": "🌱 Böyümə", "tarix": "2026-04-01"},
    {"text": "Heç bir sual axmaq deyil — amma sualı verməmək axmaqlıqdır.",
     "muellif": "Richard Feynman", "menbe": "Elm üzərindəki düşüncələr", "nov": "🧠 Filosof", "movzu": "🧠 Düşüncə", "tarix": "2026-04-02"},
    {"text": "Uğur gizlənmir — o, hər gün etdiyin kiçik işlərdə gizlənir.",
     "muellif": "Elon Musk", "menbe": "Müsahibələr", "nov": "👤 Şəxsiyyət", "movzu": "🎯 Hədəf", "tarix": "2026-04-03"},
    {"text": "İnsan öz xarakterini seçmir, amma onu qurmaq onun əlindədir.",
     "muellif": "Aristotel", "menbe": "Nikomaxos Etikası", "nov": "🧠 Filosof", "movzu": "🌱 Böyümə", "tarix": "2026-04-04"},
    {"text": "Kitablar bizi yalnız olmayan yerə aparır.",
     "muellif": "Thomas à Kempis", "menbe": "Məsihin Təqlidi", "nov": "📚 Kitab", "movzu": "🧠 Düşüncə", "tarix": "2026-04-05"},
    {"text": "Sənin ən böyük rəqibin dünənki özündür.",
     "muellif": "Muhammad Ali", "menbe": "Müsahibələr", "nov": "👤 Şəxsiyyət", "movzu": "💪 İradə", "tarix": "2026-04-06"},
    {"text": "Bir gün başlamaq üçün mükəmməl olmağı gözləmə.",
     "muellif": "Mark Twain", "menbe": "Aforizmler", "nov": "✍️ Yazıçı", "movzu": "🔥 Motivasiya", "tarix": "2026-04-07"},
    {"text": "Kainat öz sirlərini yalnız cəsarətlilərə açır.",
     "muellif": "Paulo Coelho", "menbe": "Alxemik", "nov": "📚 Kitab", "movzu": "🎯 Hədəf", "tarix": "2026-04-08"},
    {"text": "Pul çox şey satın ala bilər, amma vaxtı geri qaytara bilməz.",
     "muellif": "Seneka", "menbe": "Həyatın Qıslığı Üzərinə", "nov": "🧠 Filosof", "movzu": "❤️ Həyat", "tarix": "2026-04-09"},
    {"text": "Biz qəhrəman doğulmayırıq — biz qəhrəman seçirik.",
     "muellif": "Hermiona Grencer", "menbe": "Harry Potter", "nov": "📚 Kitab", "movzu": "💪 İradə", "tarix": "2026-04-10"},
    {"text": "Düşüncəni idarə edən, həyatı idarə edir.",
     "muellif": "Marcus Aurelius", "menbe": "Özümə Düşüncələr", "nov": "🧠 Filosof", "movzu": "🧠 Düşüncə", "tarix": "2026-04-11"},
    {"text": "Hər böyük iş kiçik bir addımla başlayır.",
     "muellif": "Lao Tzu", "menbe": "Tao Te Ching", "nov": "🧠 Filosof", "movzu": "🎯 Hədəf", "tarix": "2026-04-12"},
    {"text": "Uğurun sirri: başqaları nə düşünür bilmədən irəliləmək.",
     "muellif": "Jay Gatsby", "menbe": "Böyük Gatsby", "nov": "📚 Kitab", "movzu": "🔥 Motivasiya", "tarix": "2026-04-13"},
    {"text": "Öyrənmək — yaşadığın müddətcə davam etməli olan bir macəradır.",
     "muellif": "Albert Einstein", "menbe": "Məktublar", "nov": "👤 Şəxsiyyət", "movzu": "🌱 Böyümə", "tarix": "2026-04-14"},
    {"text": "Həyat ya cəsarətli bir macəradır, ya da heç nədir.",
     "muellif": "Helen Keller", "menbe": "The Open Door", "nov": "✍️ Yazıçı", "movzu": "❤️ Həyat", "tarix": "2026-04-15"},
    {"text": "Güc qaldırmaqda deyil — qaldırdıqdan sonra düşməməkdədir.",
     "muellif": "Rocky Balboa", "menbe": "Rocky (1976)", "nov": "🎬 Film", "movzu": "💪 İradə", "tarix": "2026-04-16"},
]

MOVZU_IKON = {
    "💪 İradə": "💪", "🧠 Düşüncə": "🧠", "🔥 Motivasiya": "🔥",
    "❤️ Həyat": "❤️", "🎯 Hədəf": "🎯", "🌱 Böyümə": "🌱",
}


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
    def get_children(block_id):
        result = notion_request("GET", f"blocks/{block_id}/children?page_size=100")
        blocks = result.get("results", [])
        all_blocks = []
        for b in blocks:
            all_blocks.append(b)
            if b.get("type") in ("column_list", "column"):
                all_blocks.extend(get_children(b["id"]))
        return all_blocks
    return get_children(PAGE_ID)


def bloku_yenile(block_id, sitat):
    """Mövcud callout blokun mətnini yerindəcə yeniləyir."""
    ikon = MOVZU_IKON.get(sitat["movzu"], "💡")
    # Format: ❝ İfadə ❞  —  Müəllif  ·  Mənbə  ·  Növ  ·  Mövzu
    metn = (
        f"❝ {sitat['text']} ❞"
        f"  —  {sitat['muellif']}"
        f"  ·  {sitat['menbe']}"
        f"  ·  {sitat['nov']}"
        f"  ·  {sitat['movzu']}"
    )
    data = {
        "callout": {
            "rich_text": [{"type": "text", "text": {"content": metn}}],
            "icon": {"type": "emoji", "emoji": ikon},
            "color": "purple_background",
        }
    }
    notion_request("PATCH", f"blocks/{block_id}", data)


def main():
    print("🔍 Notion səhifəsi oxunur...")
    bloqlar = sehifenin_bloklari()

    # ❝ olan callout bloku tap
    kelam_block_id = None
    for blok in bloqlar:
        if blok.get("type") != "callout":
            continue
        metn = "".join(
            t.get("plain_text", "")
            for t in blok.get("callout", {}).get("rich_text", [])
        )
        if "❝" in metn:
            kelam_block_id = blok["id"]
            print(f"✅ Kəlam bloku tapıldı.")
            break

    if not kelam_block_id:
        print("⚠️  Kəlam bloku tapılmadı!")
        print("   Notion səhifəsində ❝ işarəsi olan callout bloku olmalıdır.")
        sys.exit(1)

    sitat = bugunun_sitati()
    print(f"📖 Bugünün kəlamı: \"{sitat['text'][:55]}\"")
    print(f"   — {sitat['muellif']}  ·  {sitat['menbe']}  ·  {sitat['nov']}  ·  {sitat['movzu']}")

    bloku_yenile(kelam_block_id, sitat)
    print("✅ Notion uğurla yeniləndi!")


if __name__ == "__main__":
    if not NOTION_TOKEN:
        print("❌ NOTION_TOKEN tapılmadı!")
        sys.exit(1)
    main()
