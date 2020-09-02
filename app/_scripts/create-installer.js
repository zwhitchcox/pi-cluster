const electronInstaller = require('electron-winstaller')
const path = require('path')

;(async () => {
try {
  const rootPath = path.join('./')
  const outPath = path.join(rootPath, 'release')
  await electronInstaller.createWindowsInstaller({
    appDirectory: path.join(outPath, 'cruster-win32-x64'),
    authors: 'Zane Hitchcox',
    outputDirectory: path.join(outPath, 'windows-installer'),
    exe: 'cruster.exe',
    setupExe: 'CrusterInstaller.exe',
    setupIcon: path.join(rootPath, '..', 'logo', 'icons', 'windows.ico')
  });
  console.log('It worked!');
} catch (e) {
  console.log(`No dice: ${e.message}`);
}
})()