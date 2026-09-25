#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instalador da traducao PT-BR de Castlevania: Dominus Collection.
Funciona em Windows e Steam Deck / Linux (Proton). Requer apenas Python 3.
Aplica os 3 jogos (Order of Ecclesia, Dawn of Sorrow, Portrait of Ruin).

Uso:
    python instalar.py                 (detecta o Steam automaticamente)
    python instalar.py "<pasta>"       (caminho da pasta do jogo ou de windata)
"""
import os, sys, re, struct, lzma, hashlib

PATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "castlevania_ptbr.patch")
GAME_SUBPATH = os.path.join("steamapps", "common", "Castlevania Dominus Collection", "windata")

def log(msg=""): print(msg, flush=True)

def sha1_file(path, limit=None):
    h = hashlib.sha1()
    with open(path, "rb") as f:
        while True:
            b = f.read(1 << 20)
            if not b: break
            h.update(b)
    return h.hexdigest()

def parse_patch():
    raw = lzma.decompress(open(PATCH, "rb").read())
    if raw[:8] != b"CVDOMPT2":
        raise SystemExit("Arquivo de patch invalido ou corrompido.")
    p = 8
    sha_n = raw[p:p+20].hex(); p += 20
    len_n = struct.unpack_from("<Q", raw, p)[0]; p += 8
    nb = struct.unpack_from("<I", raw, p)[0]; p += 4
    bases = {}   # sha1 -> (tamanho, nome): versoes a partir das quais da para instalar
    for _ in range(nb):
        sha = raw[p:p+20].hex(); p += 20
        ln, nl = struct.unpack_from("<QB", raw, p); p += 9
        bases[sha] = (ln, raw[p:p+nl].decode()); p += nl
    nseg = struct.unpack_from("<I", raw, p)[0]; p += 4
    meta = []
    for _ in range(nseg):
        off, ln = struct.unpack_from("<QQ", raw, p); p += 16
        meta.append((off, ln))
    msha_n = raw[p:p+20].hex(); p += 20
    mlen = struct.unpack_from("<I", raw, p)[0]; p += 4
    segs = []
    for off, ln in meta:
        segs.append((off, raw[p:p+ln])); p += ln
    mdata = raw[p:p+mlen]; p += mlen
    return dict(sha_n=sha_n, len_n=len_n, bases=bases, segs=segs, msha_n=msha_n, mdata=mdata)

def _safe_isdir(p):
    try: return os.path.isdir(p)
    except OSError: return False

def _safe_listdir(p):
    try: return os.listdir(p)
    except OSError: return []   # ignora pastas sem permissao (ex.: /run/media/root)

def steam_libraries():
    """Retorna possiveis raizes de biblioteca do Steam (Windows/Linux/Deck)."""
    roots = []
    home = os.path.expanduser("~")
    cand_steam = [
        r"C:\Program Files (x86)\Steam", r"C:\Program Files\Steam",
        os.path.join(home, ".local", "share", "Steam"),
        os.path.join(home, ".steam", "steam"),
        os.path.join(home, ".steam", "root"),
        os.path.join(home, ".var", "app", "com.valvesoftware.Steam", "data", "Steam"),
    ]
    for s in cand_steam:
        if _safe_isdir(s):
            roots.append(s)
            vdf = os.path.join(s, "steamapps", "libraryfolders.vdf")
            try:
                if os.path.isfile(vdf):
                    txt = open(vdf, encoding="utf-8", errors="ignore").read()
                    for m in re.finditer(r'"path"\s*"([^"]+)"', txt):
                        roots.append(m.group(1).replace("\\\\", "\\"))
            except OSError:
                pass
    # cartao SD / drives do Steam Deck (ignorando pastas sem permissao)
    for base in ("/run/media", "/media"):
        if _safe_isdir(base):
            for user in _safe_listdir(base):
                ud = os.path.join(base, user)
                if _safe_isdir(ud):
                    roots.append(ud)
                    for dev in _safe_listdir(ud):
                        roots.append(os.path.join(ud, dev))
    # remove duplicatas preservando a ordem
    seen, uniq = set(), []
    for r in roots:
        if r not in seen:
            seen.add(r); uniq.append(r)
    return uniq

def find_windata(arg):
    # 1) argumento explicito
    if arg:
        arg = os.path.abspath(arg)
        for c in (arg, os.path.join(arg, "windata")):
            if os.path.isfile(os.path.join(c, "alldata.bin")):
                return c
        raise SystemExit("Nao achei 'alldata.bin' em: %s" % arg)
    # 2) auto-deteccao
    for root in steam_libraries():
        c = os.path.join(root, GAME_SUBPATH)
        if os.path.isfile(os.path.join(c, "alldata.bin")):
            return c
    return None

def apply(windata, pd):
    binp = os.path.join(windata, "alldata.bin")
    mp = os.path.join(windata, "alldata.psb.m")
    log("Verificando arquivos originais...")
    cur = sha1_file(binp)
    if cur == pd["sha_n"]:
        log(">> Esta versao da traducao JA esta instalada. Nada a fazer."); return True
    if cur not in pd["bases"]:
        log("!! O 'alldata.bin' nao corresponde a versao esperada do jogo.")
        log("   SHA-1 encontrado: %s" % cur)
        log("   Use 'Verificar integridade dos arquivos' no Steam e tente de novo.")
        return False
    log("OK (%s). Aplicando traducao (in-place, sem duplicar o arquivo)..." % pd["bases"][cur][1])
    with open(binp, "r+b") as f:
        for off, data in pd["segs"]:
            f.seek(off); f.write(data)
        f.truncate(pd["len_n"])
    with open(mp, "wb") as f:
        f.write(pd["mdata"])
    log("Verificando resultado...")
    if sha1_file(binp) != pd["sha_n"]:
        log("!! Falha na verificacao final do alldata.bin.")
        log("   Use 'Verificar integridade dos arquivos' no Steam para restaurar.")
        return False
    if sha1_file(mp) != pd["msha_n"]:
        log("!! Falha na verificacao do indice (alldata.psb.m).")
        return False
    return True

def main():
    log("=" * 56)
    log(" Traducao PT-BR - Castlevania: Dominus Collection")
    log("=" * 56)
    if not os.path.isfile(PATCH):
        raise SystemExit("Nao achei 'castlevania_ptbr.patch' ao lado deste instalador.")
    pd = parse_patch()
    arg = sys.argv[1] if len(sys.argv) > 1 else None
    windata = find_windata(arg)
    if not windata:
        log("Nao consegui achar a pasta do jogo automaticamente.")
        log("Arraste a pasta do jogo ate aqui ou digite o caminho de 'windata':")
        try:
            windata = find_windata(input("> ").strip().strip('"'))
        except (EOFError, KeyboardInterrupt):
            raise SystemExit("Cancelado.")
    log("Pasta do jogo: %s" % windata)
    ok = apply(windata, pd)
    log()
    if ok:
        log("*** CONCLUIDO! Abra o jogo, escolha a European Version e o")
        log("    idioma ESPANOL (Espanol) para jogar em Portugues. ***")
        log("Para reverter: Steam > Propriedades > Arquivos instalados >")
        log("               Verificar integridade dos arquivos.")
    else:
        log("Instalacao NAO concluida (veja a mensagem acima).")
    if os.name == "nt":
        try: input("\nPressione ENTER para sair...")
        except EOFError: pass

if __name__ == "__main__":
    main()
