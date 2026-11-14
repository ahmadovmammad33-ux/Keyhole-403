# 🚀 KEYHOLE-403

**Multi-Server & Multi-Framework 403 Forbidden Bypass Payload Generator**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Author](https://img.shields.io/badge/Author-Məmməd%20Əhmədov-orange)
![Version](https://img.shields.io/badge/Version-1.0-red.svg)

---

## 🎯 Layihə Haqqında

**Keyhole-403**, Bug Bounty tədqiqatçıları və Penetration Tester-lər üçün hazırlanmış, **403 Forbidden** xətasını bypass etmək üçün xüsusi payload-lar generasiya edən interaktiv CLI alətidir.

### ❓ Niyə Bu Tool Lazımdır?

Bug Bounty və Penetration Testing zamanı ən çox qarşılaşılan problemlərdən biri **403 Forbidden** xətasıdır. Bu xəta, server-in və ya tətbiqin müəyyən resurslara girişi qadağan etdiyini göstərir. Manual olaraq yüzlərlə bypass texnikasını sınaqdan keçirmək **saatlarla vaxt** aparır və səhv etmə ehtimalı yüksəkdir.

**Keyhole-403** bu problemi həll edir:
- ✅ **Avtomatlaşdırma:** Saatlarla çəkən manual testləri dəqiqələrə endirir.
- ✅ **Çoxsaylı Server Dəstəyi:** Nginx, Apache, IIS, Tomcat, Node.js, Cloudflare.
- ✅ **Framework Dəstəyi:** Laravel, Django, Spring Boot, Express.js.
- ✅ **Burp Suite uyğun:** Birbaşa import edilə bilən, düzgün formatlanmış HTTP request-ləri.
- ✅ **WAF Stealth:** Avtomatik Real Brauzer User-Agent dəstəyi.

---

## ✨ Xüsusiyyətlər

### 🔧 Texniki Xüsusiyyətlər

| Xüsusiyyət | Təsvir |
|------------|--------|
| **Path Manipulyasiyası** | URL encoding, double slash, semicolon bypass, null byte, case manipulation |
| **Header Injection** | X-Forwarded-For, X-Original-URL, X-Rewrite-URL və s. |
| **Body Payload-ları** | JSON, XML, Form-data bypass texnikaları |
| **HTTP Method Dəstəyi** | GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS, TRACE, CONNECT, PROPFIND, COPY, MOVE |
| **Burp Suite İnteqrasiyası** | Blank-line problemi həll olunmuş, birbaşa import edilə bilən fayllar |
| **WAF Bypass** | Unicode encoding, overlong UTF-8, double encoding texnikaları |

### 🖥️ Dəstəklənən Server-lər

- **Nginx** - `try_files`, `location` regex bypass-ları
- **Apache** - `.htaccess`, `mod_rewrite`, MultiViews bypass-ları
- **Microsoft IIS** - Case-insensitive, NTFS ADS, WebDAV bypass-ları
- **Apache Tomcat** - `jsessionid`, `..;/`, PUT bypass-ları
- **Node.js / Express** - Query trick, prototype pollution bypass-ları
- **Cloudflare / WAF** - Unicode encoding, header ordering bypass-ları

### 🏗️ Dəstəklənən Framework-lər

- **Laravel** - `public/` bypass, route middleware, `_method` override
- **Django** - Admin bypass, query trick, CSRF bypass
- **Spring Boot** - Actuator endpoint bypass, method override
- **Express.js** - Route mounting, prototype pollution

---

## 🛠️ Quraşdırma və İşə Salma

Bu tool **heç bir xarici kitabxana tələb etmir** (yalnız Python-un daxili modullarından istifadə edir) və həm **Windows**, həm də **Linux/macOS** əməliyyat sistemlərində problemsiz işləyir.

### ⚡ Üsul 1: Birbaşa Yükləmə (Tövsiyə olunur - Linux/Kali/macOS)

Terminalı açın və aşağıdakı əmrlə skripti birbaşa GitHub-dan çəkin:


curl -O https://raw.githubusercontent.com/ahmadovmammad33-ux/Keyhole-403/main/keyhole403.py

(Əgər curl yoxdursa, wget https://raw.githubusercontent.com/ahmadovmammad33-ux/Keyhole-403/main/keyhole403.py istifadə edə bilərsiniz).

Yükləndikdən sonra birbaşa işə salın:

python3 keyhole403.py

### Üsul 2: Windows üçün (PowerShell və ya CMD)

Windows istifadəçiləri aşağıdakı əmri PowerShell-də işə salaraq skripti yükləyə bilərlər:

Invoke-WebRequest -Uri "https://raw.githubusercontent.com/ahmadovmammad33-ux/Keyhole-403/main/keyhole403.py" -OutFile "keyhole403.py"

Yükləndikdən sonra işə salın:

python keyhole403.py

### 🌐 Üsul 3: Brauzer ilə Manuel Yükləmə
Əgər əmrlərlə işləmək istəmirsinizsə, sadəcə aşağıdakı birbaşa linkə daxil olun, səhifədəki kodu kopyalayıb keyhole403.py adlı fayl yaradıb içinə yapışdırın:

🔗 keyhole403.py -    https://github.com/ahmadovmammad33-ux/Keyhole-403/blob/main/keyhole403.py


### 📖 İstifadə Qaydası

Tool-u işə saldıqdan sonra sizə kosmik banner göstərəcək və interaktiv suallar soruşacaq. Bilmədiyiniz sahələr üçün sadəcə Enter basın və ya none yazın.
Sualların İzahı:

1.Hədəf Path: 403 aldığınız URL (məs: /administrator/user/login/).

2.HTTP Method: Əgər bilmirsinizsə ALL yazın (bütün methodları yoxlayacaq).

3.Server Tipi: Hədəf serveri (məs: nginx, apache, iis). Bilmirsinizsə unknown yazın.

4.Framework: Arxa plandakı texnologiya (məs: laravel, django). Yoxdursa none yazın.

5.User-Agent: WAF-ları aldatmaq üçün boş buraxın (avtomatik real Chrome UA-sı qoyacaq).

6.Hədəf Host: Domen adı (məs: example.com).


### 🐞 Burp Suite ilə İnteqrasiya

Tool output/ qovluğunda sizə 4 əsas fayl təqdim edir:

 *_paths.txt (URL manipulyasiyaları üçün)
 
 *_headers.txt (Header injection üçün)

 *_body.txt (Body/JSON manipulyasiyaları üçün)

 *_all_requests.txt (Bütün request-lərin birləşmiş forması)

### ⚙️ Addım-addım Burp Intruder Quraşdırması:

1.Burp Suite-də 403 verən request-i tutun və Send to Intruder edin.

2.Positions tab-ında Clear § düyməsini basın.

## A) Path Testi üçün:
Request-dəki URL path-ini seçin və §§ ilə işarələyin:

GET §/administrator/user/login/§ HTTP/1.1

Host: example.com

...

Payloads tab-ında *_paths.txt faylını yükləyin.

## B) Header Testi üçün:
Request-in ən sonundakı boş sətirdən ƏVVƏL yeni bir sətir əlavə edin və §§ qoyun:

GET /administrator/user/login/ HTTP/1.1

Host: example.com

User-Agent: Mozilla/5.0...

§§

Payloads tab-ında *_headers.txt faylını yükləyin.

### ⚠️ VACİB QEYD: WAF TETİKLENMƏ PROBLEMİ VƏ HƏLLİ
Header payload-larını test edərkən əgər WAF (Web Application Firewall) dərhal tetiklenirsə və 403/418 xətası verirsə, bunun səbəbi payload-ın HTTP Body-sinə düşməsidir.
Həlli:
Burp Intruder-də payload işarəsini (§§) User-Agent header-inin DƏRHAL ALTINA (boş sətirdən əvvəl) yerləşdirdiyinizdən əmin olun. Bu, server-in payload-ı düzgün "Header" kimi parse (təhlil) etməsini təmin edir və WAF-ın davranış analizindən yayınmağa kömək edir.

DOĞRU QURULUŞ:


GET /admin HTTP/1.1

Host: target.com

User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)

§X-Forwarded-For: 127.0.0.1§



### 🤝 Töhfə (Contribution)

Bu layihə açıq mənbədir və töhfələrinizi məmnuniyyətlə qarşılayırıq! Əgər yeni bypass texnikaları tapmısınızsa, xəta aşkar etmisinizsə və ya kodu təkmilləşdirmək istəyirsinizsə, Pull Request göndərin!

### ⚖️ Lisenziya və Məsuliyyət
Bu layihə yalnız təhsil və icazəli təhlükəsizlik testləri (Bug Bounty, Penetration Testing) məqsədi ilə hazırlanmışdır. İcazəsiz sistemlərə qarşı istifadə qanunsuzdur və müəllif heç bir məsuliyyət daşımır.

### 👨‍💻 Müəllif
Məmməd Əhmədov

Penetration Tester | Bug Bounty Hunter | Security Researcher

Əgər bu tool işinizə yaradısa, repository-yə ⭐ Star verməyi unutmayın!
