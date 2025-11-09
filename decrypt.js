const path = require("node:path");

const getErcd = async () => {
  const ercdPath = process.defaultApp
    ? path.join(__dirname, "src", "ercd.json")
    : path.join(process.resourcesPath, "ercd.json");

  return await require("node:fs/promises")
    .readFile(ercdPath, "utf-8")
    .then(JSON.parse);
};

const decrypt = async (zipPath, pswd) => {
  const decryptor = process.defaultApp
    ? path.join(__dirname, "src", "dist", "decrypt.exe")
    : path.join(process.resourcesPath, "decrypt.exe");

  const execFile = require("node:util").promisify(
    require("node:child_process").execFile
  );

  return execFile(decryptor, [zipPath, pswd], { encoding: "buffer" });
};

module.exports = () => {
  const { ipcMain, dialog } = require("electron/main");
  ipcMain.handle("decrypt", async () => {
    const { canceled, filePaths } = await dialog.showOpenDialog();
    if (canceled) return;

    const ercd = await getErcd();

    const pswds = ["password1", "password2", "abcdefg", "password3"];

    let msg = "";
    for (const pswd of pswds) {
      try {
        await decrypt(filePaths[0], pswd);
        return "";
      } catch (err) {
        msg = err.stderr;
        if (err.code !== ercd["ERR_WRONG_PASSWORD"]) break;
      }
    }
    return require("iconv-lite").decode(
      msg,
      process.platform === "win32" ? "cp932" : "utf-8"
    );
  });
};
