nuitka `
    --standalone --onefile --follow-imports --jobs=4 `
    --windows-icon-from-ico="icons/icon.ico" --linux-icon="icons/icon_256x256.png" `
    --company-name="Romanin" --product-name="SeaPlayer" `
    --file-version="0.10.0.40" --product-version="0.10.0.40" `
    --file-description="SeaPlayer is a player that works in the terminal." `
    --output-dir="bin/nuitka" --output-filename="seaplayer" "./seaplayer-main.py"
Copy-Item "./seaplayer/assets" -Recurse "./bin/nuitka/assets" -Force -Confirm
Copy-Item "./seaplayer/style" -Recurse "./bin/nuitka/style" -Force -Confirm
Copy-Item "./seaplayer/langs" -Recurse "./bin/nuitka/langs" -Force -Confirm