#!/usr/bin/env bash
# Regenerate the shared subset CJK webfonts used by the Chinese covers of every post
# (posts/red/01 and posts/red/02). Output lands in assets/fonts/ so any page can use it.
# Downloads Noto Serif SC (headline, echoes Fraunces) + Noto Sans SC (bullets, echoes
# Urbanist), then subsets each to just the characters the covers use → build/fonts/*.woff2
# (~10KB each). make_cover.py @font-face's those woff2. Re-run only if the cover copy adds
# new Chinese characters (extend TXT below) or the fonts are missing.
#
#   bash posts/red/01/subset_cjk.sh && uv run python posts/red/01/make_cover.py
set -euo pipefail
cd "$(dirname "$0")/.."   # repo root
SRC=.cache/fonts_src; OUT=assets/fonts
mkdir -p "$SRC" "$OUT"
base="https://raw.githubusercontent.com/notofonts/noto-cjk/main"
declare -A F=(
  [NotoSerifSC-SemiBold.otf]="Serif/SubsetOTF/SC/NotoSerifSC-SemiBold.otf"
  [NotoSansSC-Regular.otf]="Sans/SubsetOTF/SC/NotoSansSC-Regular.otf"
  [NotoSansSC-Bold.otf]="Sans/SubsetOTF/SC/NotoSansSC-Bold.otf"
)
for f in "${!F[@]}"; do [ -f "$SRC/$f" ] || curl -sSL "$base/${F[$f]}" -o "$SRC/$f"; done

# Every Chinese character used across the -zh covers (headline + bullets + labels + footer).
# DO NOT extend this by hand from memory — that has silently dropped characters twice (向, then
# 上/同), and a missing glyph is invisible on any machine that has Noto CJK installed system-wide,
# because the fallback is the same typeface. Derive it and diff it:
#   uv run --with fonttools --with brotli python - <<'EOF'
#   import re; from pathlib import Path; from fontTools.ttLib import TTFont
#   need=set()
#   for d in ("posts/red/01","posts/red/02"):
#       src=Path(d,"make_cover.py").read_text()
#       src=re.sub(r"^from playwright.*$","",src,flags=re.M).split("def _wait_for_server")[0]
#       ns={"__file__":f"{d}/make_cover.py"}; exec(compile(src,d,"exec"),ns)
#       # every module-level string, with NO name filter: red/02's BA_ZH is rendered but matches
#       # no obvious prefix, and a name filter is the same blind spot this recipe exists to close.
#       for v in ns.values():
#           if isinstance(v,str):
#               need|={c for c in re.sub(r"<[^>]+>","",v) if '\u3000'<=c<='\u9fff'}
#   for f in ("SansSC-Regular","SansSC-Bold","SerifSC"):
#       cm=TTFont(f"assets/fonts/{f}.woff2").getBestCmap()
#       print(f, "missing:", "".join(sorted(c for c in need if ord(c) not in cm)) or "none")
#   EOF
TXT="高效框架一个面向开源平台提供所需的一切任何电脑上同轻量可扩展的沙盒内置可验证任务统数据集前沿评测支持覆盖桌面浏览器与移动端训练生态免虚拟机自带不止整套去掉更省并行内存约意主容与器、，。：·每奖励既也底座持续"
sub(){ pyftsubset "$SRC/$1" --text="$TXT" --flavor=woff2 --output-file="$OUT/$2" --no-hinting --desubroutinize; }
sub NotoSerifSC-SemiBold.otf SerifSC.woff2
sub NotoSansSC-Regular.otf   SansSC-Regular.woff2
sub NotoSansSC-Bold.otf      SansSC-Bold.woff2
echo "subset → $OUT/ (SerifSC, SansSC-Regular, SansSC-Bold .woff2)"
