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

# every Chinese character used across the -zh covers (headline + bullets + labels + footer)
TXT="高效框架一个开源平台提供所需的一切任何电脑轻量可扩展的沙盒内置可验证任务统数据集前沿评测支持覆盖桌面浏览器与移动端训练生态免虚拟机自带不止整套去掉更省并行内存约意主容与器、，。：·每奖励既也底座持续"
sub(){ pyftsubset "$SRC/$1" --text="$TXT" --flavor=woff2 --output-file="$OUT/$2" --no-hinting --desubroutinize; }
sub NotoSerifSC-SemiBold.otf SerifSC.woff2
sub NotoSansSC-Regular.otf   SansSC-Regular.woff2
sub NotoSansSC-Bold.otf      SansSC-Bold.woff2
echo "subset → $OUT/ (SerifSC, SansSC-Regular, SansSC-Bold .woff2)"
