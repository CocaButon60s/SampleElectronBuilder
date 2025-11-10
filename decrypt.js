const path = require("node:path");

const decrypt = async (arg) => {
  const decryptor = process.defaultApp
    ? path.join(__dirname, "src", "dist", "decrypt.exe")
    : path.join(process.resourcesPath, "decrypt.exe");

  const execFile = require("node:util").promisify(
    require("node:child_process").execFile
  );

  return execFile(decryptor, [arg], { encoding: "buffer" });
};

module.exports = () => {
  const { ipcMain, dialog } = require("electron/main");
  ipcMain.handle("decrypt", async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog();
    if (canceled) return;

    const argInfo = {
      zipfile: filePaths[0],
      data: [
        { pswd: "password1", marker: "dev1" },
        { pswd: "password2", marker: "dev2" },
        { pswd: "abcdefg", marker: "dev3" },
        { pswd: "password3", marker: "dev4" },
      ],
    };

    try {
      const { stdout, stderr } = await decrypt(JSON.stringify(argInfo));
      msg = stdout;
    } catch (err) {
      msg = err.stderr;
    }
    const tmp = require("iconv-lite").decode(
      msg,
      process.platform === "win32" ? "cp932" : "utf-8"
    );

    return require("iconv-lite").decode(
      msg,
      process.platform === "win32" ? "cp932" : "utf-8"
    );
  });
};
