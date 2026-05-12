# EntitySearch State Data

Sidebar verileri için yapılandırılmış eyalet düzeyinde veri seti. Bu veriler harici web sitelerinde sidebar component'lerinde kullanılmak üzere tasarlanmıştır.

## Durum

`2026-05-12` itibarıyla 50 eyaletin tamamı için detaylı enrichment batch işlemleri tamamlandı.

- Kapsam: `AL` through `WY`
- Son tamamlanan batch: `WI / WY`
- Her eyalet dosyasında contact, adres, çalışma saatleri, renewal linkleri, LLC filing facts, name reservation bilgisi ve resmi kaynaklar dolduruldu veya resmi kaynakta bulunmuyorsa bilinçli olarak `null` bırakıldı.
- Root [../states.json](../states.json) kayıtları official fee/source düzeltmeleriyle uyumlu hale getirildi.
- Batch audit çıktıları lokal olarak `entitysearch-state-data/audits/` altında üretildi. Bu klasör `.gitignore` kapsamındadır.

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
- **Ücret ve requirement doğrulaması:** Her fee, due date ve filing requirement resmi state government portalı, resmi fee schedule, resmi statute veya resmi filing portal üzerinden doğrulanır
- **Kaynak zorunluluğu:** `sources[]`, root `official_link` ve root `source_url` alanları resmi kaynaklara işaret etmelidir
- **Üçüncü parti kaynak yok:** Legal service provider, blog, SEO sayfası, haber sitesi veya ticari özet kaynak kullanılmaz
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
npx ajv-cli validate --strict=false -s entitysearch-state-data/schema/state.schema.json -d 'entitysearch-state-data/states/*.json'
```

JSON parse kontrolü:

```bash
jq empty states.json entitysearch-state-data/states/*.json
```

## Gelecekteki Güncelleme Workflow

Tüm eyaletler enrich edildiği için bundan sonraki işler yeni batch üretmekten çok periyodik doğrulama, resmi ücret değişikliği takibi ve kaynak linklerinin canlılığını kontrol etme şeklinde yapılmalıdır. Yine de bakım işleri aynı batch mantığıyla ilerlemelidir.

### Batch Seçimi

- Güncellenecek eyaletleri 2-3 eyaletlik küçük batch'lere ayır.
- Her batch için önce mevcut state JSON dosyalarını ve root `states.json` kayıtlarını oku.
- Batch kapsamını final yanıtta ve gerekiyorsa handoff notlarında açıkça belirt.

Örnek:

```bash
sed -n '1,220p' entitysearch-state-data/states/wisconsin.json
sed -n '1,220p' entitysearch-state-data/states/wyoming.json
sed -n '490,540p' states.json
```

### Resmi Kaynak Araştırması

Her state için yalnızca şu kaynak tiplerini kullan:

- Secretary of State veya Department of State corporation/business division sayfaları
- Department of Financial Institutions, Department of Revenue veya resmi filing agency sayfaları
- Resmi fee schedule HTML/PDF sayfaları
- Resmi annual report, renewal veya business filing portalları
- Resmi state statute sayfaları

Şunları kullanma:

- LegalZoom, Northwest, ZenBusiness, Harbor Compliance, Forbes vb. ticari sayfalar
- Bloglar, SEO landing page'leri, haber siteleri
- Sadece search result snippet'i

Resmi portal bot koruması nedeniyle audit'te `403`, timeout veya connection reset döndürürse URL otomatik olarak atılmamalıdır. Kaynak resmi state sayfasıysa korunabilir; mümkünse aynı bilgiyi destekleyen ek resmi `200` dönen kaynak da eklenmelidir.

### Güncellenecek Alanlar

Her state dosyasında şu alanlar kontrol edilmelidir:

- `businessEntitySearch.url`
- `secretaryOfState.agency`
- `secretaryOfState.website`
- `secretaryOfState.phone`
- `secretaryOfState.email`
- `hours.timezone`
- `hours.regular`
- `physicalAddresses[]`
- `mailingAddress`
- `renewals.onlineRenewalUrl`
- `renewals.paperRenewalUrl`
- `renewals.notes`
- `filingFacts.llcFee`
- `filingFacts.llcFeeNotes`
- `filingFacts.annualReport`
- `filingFacts.annualReportDue`
- `filingFacts.nameReservation`
- `filingFacts.nameReservationNotes`
- `sources[]`
- `lastVerified`

Root `states.json` içinde yalnızca resmi veri değiştiyse veya kaynak linki düzeltildiyse şu alanlar güncellenmelidir:

- `formation_fee`
- `annual_report_fee`
- `annual_report_due_date`
- `official_link`
- `source_url`
- `last_verified`
- root `last_updated`

### Timestamp ve Kaynak Formatı

- Dokunulan state dosyasında `lastVerified` güncel ISO tarih olmalıdır.
- Dokunulan source kayıtlarında `lastAccessed` güncel ISO tarih olmalıdır.
- Root `states.json` içinde ilgili state `last_verified` güncellenmelidir.
- Dataset genelinde resmi veri değişikliği yapıldıysa root `last_updated` güncellenmelidir.

### Annual Report ve Fee Kuralları

- Root `states.json` içinde annual report fee yoksa `annual_report_fee: 0` kullanılmalıdır.
- Detay state JSON dosyasında mevcut pattern'e uy: bazı state'lerde annual report yoksa `annualReport: null` ve `annualReportDue: "N/A"` kullanılabilir.
- Online ve paper fee farklıysa kullanıcı açısından en pratik/current online fee ana değer olarak kullanılabilir, paper fee notlarda açıkça belirtilmelidir.
- Minimum/maksimum veya asset-based fee varsa ana değere minimum fee yazılır, değişken yapı `filingFacts.*Notes` ve `renewals.notes` içinde açıklanır.

### Batch Audit

Her batch sonunda URL audit üret:

```bash
scripts/.venv/bin/python scripts/audit_state_urls.py --state WI --state WY --insecure --timeout 8 --output entitysearch-state-data/audits/url-audit-batch-wi-wy-2026-05-12.json
```

Audit özetini çıkarmak için:

```bash
jq -r '.states | to_entries[] as $s | $s.value.urls[] | [$s.key, (.fetched.status // "ERR"), .url, (.fetched.error // "")] | @tsv' entitysearch-state-data/audits/url-audit-batch-wi-wy-2026-05-12.json
```

Audit klasörü git dışında tutulur. Audit dosyası final raporda linklenebilir ama commit'e eklenmez.

### Batch Sonu Kontrol Listesi

1. JSON parse kontrolü çalıştır:

```bash
jq empty states.json entitysearch-state-data/states/*.json
```

2. Şema validasyonunu çalıştır:

```bash
npx ajv-cli validate --strict=false -s entitysearch-state-data/schema/state.schema.json -d 'entitysearch-state-data/states/*.json'
```

3. Batch audit çalıştır ve caveat'leri not et.
4. `handoff.md` varsa güncel batch, audit dosyası, caveat ve sonraki adımı yaz.
5. `git diff` ile sadece beklenen dosyaların değiştiğini kontrol et.
6. Commit mesajını batch kapsamını anlatacak şekilde yaz.

Örnek commit mesajları:

```text
Enrich Wisconsin and Wyoming data
Refresh California and Colorado official fee sources
Audit annual report URLs for southeast batch
```

### Agent Notları

- Değişiklikleri küçük ve batch kapsamıyla sınırlı tut.
- Mevcut kullanıcı veya başka agent değişikliklerini revert etme.
- JSON düzenlemelerinde mevcut alan sırasını ve dosya stilini koru.
- Ücret veya due date değiştiriyorsan final yanıtta özellikle belirt.
- Official URL audit hata verirse bunun otomasyon kaynaklı mı yoksa gerçekten kırık link mi olduğunu ayırmaya çalış.
- Kırık resmi link yerine güncel resmi sayfa bulunursa hem state JSON `sources[]` hem root `states.json` kaynakları güncellenmelidir.

---

*Bu dataset `us-llc-fees-dataset` reposunun bir parçasıdır.*
