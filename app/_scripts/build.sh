set -eux

yarn build-react
rm -rf dist
mkdir -p dist
cp -r electron dist/electron
mv build dist/react
cp package.json dist/package.json
yarn --cwd dist --production
pushd dist
./node_modules/.bin/electron-rebuild
popd

if [ ${1} == "deb" ]; then
yarn electron-packager dist cruster --overwrite --asar --platform=linux --arch=x64 --icon=../logo/icons/log.icns --prune=true --out=release
yarn electron-installer-debian --src release/cruster-linux-x64/ --arch amd64 --config _scripts/debian.json --overwrite
fi

if [ ${1} == "win" ]; then
yarn electron-packager dist cruster --overwrite --asar --platform=win32 --arch=x64 --icon=../logo/icons/windows.ico --prune=true --out=release --version-string.CompanyName=CE --version-string.FileDescription=CE --version-string.ProductName="Cruster"
fi

# Mac OS X
# yarn electron-packager dist Cruster --overwrite --platform=darwin --arch=x64 --icon=../logo/icons/logo.icns --prune=true --out=./release
# yarn electron-installer-dmg ./release/cruster-darwin-x64/Cruster.app release/Cruster --dmg --overwrite