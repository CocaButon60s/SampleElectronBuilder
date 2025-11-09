const decryptBtn = document.getElementById("decrypt-btn");
if (decryptBtn) {
  decryptBtn.onclick = async () => {
    const txt = decryptBtn.querySelector("span");
    const svg = decryptBtn.querySelector("svg");
    decryptBtn.disabled = true;
    txt.textContent = "解凍中...";
    svg.removeAttribute("hidden");

    const msg = await window.electronAPI.decrypt();
    document.getElementById("msg").textContent = msg;

    svg.setAttribute("hidden", "");
    txt.textContent = "解凍";
    decryptBtn.disabled = false;
  };
}
