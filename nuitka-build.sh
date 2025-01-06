nuitka \
    --standalone --onefile --follow-imports --jobs=4 \
    --windows-icon-from-ico="icons/icon.ico" --linux-icon="icons/icon_256x256.png" \
    --company-name="Romanin" --product-name="SeaPlayer" \
    --file-version="0.10.0.36" --product-version="0.10.0.36" \
    --file-description="SeaPlayer is a player that works in the terminal." \
    --output-dir="bin/nuitka" --output-filename="seaplayer" "./seplayer-main.py"
cp -Rf "./seaplayer/assets" "./bin/nuitka/assets"
cp -Rf "./seaplayer/style" "./bin/nuitka/style"
cp -Rf "./seaplayer/langs" "./bin/nuitka/langs"