# EntitySearch State Data

Sidebar verileri için yapılandırılmış eyalet düzeyinde veri seti. Bu veriler harici web sitelerinde sidebar component'lerinde kullanılmak üzere tasarlanmıştır.

## Yapı

```
entitysearch-state-data/
├── README.md
├── schema/
│   └── state.schema.json      # JSON validasyon şeması
├── states/                    # Her eyalet için JSON dosyaları
│   └── alabama.json           # Örnek eyalet dosyası
└── assets/
    ├── seals/                 # Eyalet logoları (.webp)
    └── provider-logos/       # Bizee, Northwest, IncAuthority logoları
```

## Şema Kuralları

| Alan | Tip | Açıklama |
|------|-----|----------|
| `stateName` | string | Tam eyalet adı |
| `stateAbbr` | string | 2 harfli eyalet kısaltması (örn: AL) |
| `stateSlug` | string | URL-dostu slug (örn: alabama) |
| `stateSeal` | string\|null | Eyalet logosu URL (WebP tercih edilir) |
| `businessEntitySearch` | object | Arama CTA ve URL |
| `secretaryOfState` | object | Kurum bilgileri |
| `hours` | object | Çalışma saatleri |
| `physicalAddresses` | array | Fiziksel adresler |
| `mailingAddress` | object | Posta adresi |
| `renewals` | object | Renewal linkleri |
| `corporateDocuments` | object | Şablon linkleri |
| `filingFacts` | object | LLC fee, annual report, name reservation |
| `sources` | array | Resmi kaynaklar |
| `lastVerified` | string | ISO tarih (YYYY-MM-DD) |

## Optional Enrichment Alanları

Aşağıdaki alanlar entity search deneyimi için zorunlu core veri değildir ve
eksik kalmaları veri kalitesi sorunu sayılmaz:

| Alan | Durum | Not |
|------|------|-----|
| `stateSeal` | Optional | Seal/logo assetleri tüketen uygulamada, örn. Astro `src/assets/images/statesseals`, yönetilebilir. |
| `secretaryOfState.officialName` | Optional | Mevcut görevli adı/since bilgisi zaman hassas siyasi/personel veridir; ayrı bakım süreci olmadan boş kalabilir. |
| `corporateDocuments` | Optional | Operating agreement, bylaws ve partnership agreement template sayfaları internal içerik olarak ayrıca üretilebilir. Resmi state template yoksa `null` kalır. |

Core veri hedefi: entity search kullanıcısına pratik olarak yarayan resmi arama
URL'i, kurum web sitesi, phone/email varsa contact bilgisi, adres, saat,
filing/renewal facts ve kaynak takibidir.

## Veri Kuralları

- **Sadece resmi kaynaklar** (.gov domainleri)
- **Bilinmeyen değerler:** `null` veya boş bırakılır
- **Tarih formatı:** ISO 8601 (`YYYY-MM-DD`)
- **Görsel formatı:** WebP tercih edilir
- **URL validasyonu:** Geçerli URI formatı gerekli

## Kullanım

```javascript
const stateData = require('./states/alabama.json');

// Sidebar'da kullanım örneği
console.log(stateData.stateName); // "Alabama"
console.log(stateData.secretaryOfState.website); // "https://www.sos.alabama.gov"
```

## Validasyon

JSON dosyalarını `state.schema.json` ile validate etmek için:

```bash
npx ajv validate -s schema/state.schema.json -d states/*.json
```

## Veri Güncelleme Workflow

1. Resmi (.gov) kaynaktan veri araştır
2. Veriyi JSON dosyasına gir
3. `lastVerified` tarihini güncelle
4. Şema validasyonunu çalıştır

---

*Bu dataset `us-llc-fees-dataset` reposunun bir parçasıdır.*
