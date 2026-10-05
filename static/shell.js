/* CS101 顶栏行为：主题按钮、账号菜单、窄屏导航菜单。
 *
 * 改动前这段逻辑在 7 个页面里各复制一份，而且只有首页那份带账号菜单 ——
 * 其余页面登录后只剩一个用户名，退不了登录。markup 由 server.py 的
 * ACCOUNT_MENU 注入（占位符 __ACCOUNT_MENU__），这里只管行为。
 *
 * 由 THEME_HEAD 以 defer 加载，执行时 DOM 已解析完；页面上没有对应元素就什么都不做，
 * 所以登录页这类没有顶栏的页面也可以安全地带着它。
 */
(function () {
  "use strict";
  var root = document.documentElement;

  var themeBtn = document.getElementById("theme");
  if (themeBtn) {
    var applyTheme = function (name) {
      root.dataset.theme = name;
      themeBtn.textContent = name === "dark" ? "浅色" : "深色";
      themeBtn.setAttribute("aria-label", name === "dark" ? "切换到浅色模式" : "切换到深色模式");
      try { localStorage.setItem("cs101-theme", name); } catch (e) {}
    };
    applyTheme(root.dataset.theme === "dark" ? "dark" : "light");
    themeBtn.addEventListener("click", function () {
      applyTheme(root.dataset.theme === "dark" ? "light" : "dark");
    });
  }

  var control = document.getElementById("account-control");
  if (!control) return;
  var trigger = control.querySelector(".account-trigger");
  var account = document.getElementById("account");

  // 登录链接带上 next，登录完回到原页面，而不是被丢回首页。
  if (account && location.pathname.indexOf("/auth/") !== 0) {
    account.href = "/auth/login/?next=" + encodeURIComponent(location.pathname + location.search);
  }

  // 触屏没有 hover，iOS Safari 点按钮也不一定让它拿到焦点 —— 所以靠点击切 .open。
  function setMenu(open) {
    control.classList.toggle("open", open);
    trigger.setAttribute("aria-expanded", String(open));
  }
  trigger.addEventListener("click", function (e) {
    e.stopPropagation();
    setMenu(!control.classList.contains("open"));
  });
  document.addEventListener("click", function (e) { if (!control.contains(e.target)) setMenu(false); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && control.classList.contains("open")) { setMenu(false); trigger.focus(); }
  });

  // 当前页对应的菜单项标出来，窄屏下一眼知道自己在哪。
  Array.prototype.forEach.call(control.querySelectorAll("a"), function (a) {
    if (a.getAttribute("href") === location.pathname) a.setAttribute("aria-current", "page");
  });

  var logout = document.getElementById("logout");
  if (logout) logout.addEventListener("click", function () {
    fetch("/api/logout", { method: "POST", credentials: "same-origin" })
      .finally(function () { location.reload(); });
  });

  fetch("/api/me", { credentials: "same-origin" }).then(function (r) { return r.json(); }).then(function (me) {
    if (!me.authenticated) return;
    control.classList.remove("guest");
    trigger.textContent = me.user;
    trigger.title = "已登录：" + me.user;
    if (account) account.hidden = true;
    return fetch("/api/settings", { credentials: "same-origin" }).then(function (r) { return r.json(); });
  }).then(function (settings) {
    var admin = document.getElementById("admin-link");
    if (settings && settings.is_admin && admin) admin.hidden = false;
  }).catch(function () {});
})();
