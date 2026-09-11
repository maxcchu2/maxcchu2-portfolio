/* Max Chu — portfolio.
   Smooth page scroll (Lenis), loose momentum rail, theme switch,
   project modal, fades. */
(function () {
  "use strict";
  var reduce = matchMedia("(prefers-reduced-motion: reduce)").matches;
  var root = document.documentElement;
  var lenis = null;

  /* ---------------- themes: light / dark / special ---------------- */
  function stored() { try { return localStorage.getItem("theme"); } catch (e) { return null; } }
  function save(v) { try { localStorage.setItem("theme", v); } catch (e) {} }
  function sysDark() { return matchMedia("(prefers-color-scheme: dark)").matches; }
  function theme() { return root.getAttribute("data-theme") || (sysDark() ? "dark" : "light"); }
  function setTheme(v) { root.setAttribute("data-theme", v); save(v); reflect(); }

  var tools = document.querySelector(".tools");
  function reflect() {
    if (!tools) return;
    var t = theme();
    var m = tools.querySelector('[data-act="mode"]');
    var s = tools.querySelector('[data-act="special"]');
    if (m) m.setAttribute("aria-label", t === "dark" ? "Switch to light" : "Switch to dark");
    if (s) s.setAttribute("aria-pressed", t === "special" ? "true" : "false");
  }
  if (tools) {
    reflect();
    tools.addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (!b) return;
      if (b.getAttribute("data-act") === "special") setTheme(theme() === "special" ? "light" : "special");
      else setTheme(theme() === "dark" ? "light" : "dark");
    });
    if (!stored()) matchMedia("(prefers-color-scheme: dark)").addEventListener("change", reflect);
  }

  /* ---------------- smooth page scroll ---------------- */
  if (!reduce && window.Lenis) {
    lenis = new window.Lenis({ lerp: 0.1, wheelMultiplier: 1, smoothWheel: true, touchMultiplier: 1.6 });
    (function raf(t) { lenis.raf(t); requestAnimationFrame(raf); })();
  }

  /* ---------------- loose momentum rail ---------------- */
  var rail = document.querySelector(".rail");
  if (rail) {
    var af = null, vel = 0, pos = rail.scrollLeft;
    var dragging = false, wasDrag = false, downX = 0, lastX = 0, lastT = 0;
    var maxX = function () { return rail.scrollWidth - rail.clientWidth; };
    var clamp = function (v) { return Math.max(0, Math.min(v, maxX())); };

    function tick() {
      pos = clamp(pos + vel);
      rail.scrollLeft = pos;
      vel *= 0.90;
      if ((pos <= 0 && vel < 0) || (pos >= maxX() && vel > 0)) vel = 0;
      af = Math.abs(vel) > 0.06 ? requestAnimationFrame(tick) : null;
    }
    function kick() { if (!af && !reduce) af = requestAnimationFrame(tick); }
    function stopMomentum() { if (af) { cancelAnimationFrame(af); af = null; } vel = 0; }

    rail.addEventListener("wheel", function (e) {
      var d = Math.abs(e.deltaX) > Math.abs(e.deltaY) ? e.deltaX : e.deltaY;
      if (e.deltaMode === 1) d *= 16;
      if (!d) return;
      var atStart = rail.scrollLeft <= 0, atEnd = rail.scrollLeft >= maxX() - 1;
      if ((d < 0 && atStart) || (d > 0 && atEnd)) return;
      e.preventDefault();
      if (reduce) { rail.scrollLeft += d; return; }
      pos = rail.scrollLeft;
      vel += d * 0.28;
      vel = Math.max(-46, Math.min(46, vel));
      kick();
    }, { passive: false });

    function onMove(e) {
      if (!dragging) return;
      var now = performance.now(), dx = e.clientX - lastX, dt = now - lastT || 16;
      if (Math.abs(e.clientX - downX) > 3) rail.classList.add("dragging");
      e.preventDefault();
      pos = clamp(pos - dx);
      rail.scrollLeft = pos;
      vel = (-dx / dt) * 15;
      lastX = e.clientX; lastT = now;
    }
    function onUp(e) {
      if (!dragging) return;
      dragging = false;
      rail.classList.remove("dragging");
      window.removeEventListener("pointermove", onMove);
      window.removeEventListener("pointerup", onUp);
      window.removeEventListener("pointercancel", onUp);
      wasDrag = Math.abs(e.clientX - downX) > 8;
      vel = Math.max(-64, Math.min(64, vel));
      if (wasDrag && Math.abs(vel) > 0.5) kick();
    }
    rail.addEventListener("pointerdown", function (e) {
      if (e.pointerType === "mouse" && e.button !== 0) return;
      dragging = true; wasDrag = false;
      downX = lastX = e.clientX; lastT = performance.now();
      stopMomentum(); pos = rail.scrollLeft;
      window.addEventListener("pointermove", onMove);
      window.addEventListener("pointerup", onUp);
      window.addEventListener("pointercancel", onUp);
    });

    var openFrom = function (el) {
      var link = el && el.closest && el.closest("a[data-project]");
      if (link) openProject(link.getAttribute("data-project"));
    };
    rail.addEventListener("click", function (e) {
      var link = e.target.closest("a[data-project]");
      if (!link) return;
      e.preventDefault();                 // the rail never navigates
      if (wasDrag) { wasDrag = false; return; }
      openFrom(e.target);
    });
    rail.addEventListener("keydown", function (e) {
      if (e.key === "Enter" || e.key === " ") {
        var link = e.target.closest && e.target.closest("a[data-project]");
        if (link) { e.preventDefault(); openProject(link.getAttribute("data-project")); }
      }
    });
  }

  /* ---------------- work: grid / list view + hover peek ---------------- */
  var work = document.querySelector(".work");
  var worklist = document.querySelector(".worklist");
  var peek = document.querySelector(".peek");
  if (work) {
    // filmstrip is always the view a fresh visit lands on — the toggle
    // only changes the view for the current page, it isn't remembered
    var setView = function (v) {
      work.setAttribute("data-view", v);
      work.querySelectorAll(".viewtoggle button").forEach(function (b) {
        b.setAttribute("aria-pressed", b.getAttribute("data-view") === v ? "true" : "false");
      });
      if (peek) peek.classList.remove("on");
      if (v === "list") preloadPeek();
    };
    work.querySelector(".viewtoggle").addEventListener("click", function (e) {
      var b = e.target.closest("button");
      if (b) setView(b.getAttribute("data-view"));
    });
  }

  var peekPre = false;
  function preloadPeek() {
    if (peekPre || !worklist) return;
    peekPre = true;
    worklist.querySelectorAll(".wrow[data-img]").forEach(function (r) {
      var i = new Image(); i.src = r.getAttribute("data-img");
    });
  }

  if (worklist && peek) {
    var pImgs = peek.querySelectorAll("img");
    var pTop = 0, hideT = null;
    var showPeek = function (src) {
      clearTimeout(hideT);
      var cur = pImgs[pTop], nxt = pImgs[pTop ^ 1];
      if (cur.getAttribute("src") === src) { peek.classList.add("on"); return; }
      nxt.src = src;
      nxt.style.opacity = "1";
      cur.style.opacity = "0";
      pTop ^= 1;
      peek.classList.add("on");
    };
    var hidePeek = function () {
      hideT = setTimeout(function () { peek.classList.remove("on"); }, 90);
    };
    worklist.addEventListener("pointerover", function (e) {
      var r = e.target.closest(".wrow[data-img]");
      if (r) showPeek(r.getAttribute("data-img"));
    });
    worklist.addEventListener("pointerleave", hidePeek);
    worklist.addEventListener("focusin", function (e) {
      var r = e.target.closest(".wrow[data-img]");
      if (r) showPeek(r.getAttribute("data-img"));
    });
    worklist.addEventListener("focusout", hidePeek);

    // list rows are plain links — clear the peek before navigating away
    worklist.addEventListener("click", function (e) {
      if (e.target.closest("a[data-project]")) peek.classList.remove("on");
    });
  }

  /* ---------------- project modal + image zoom ---------------- */
  var modal = document.getElementById("modal");
  var zoom = document.getElementById("zoom");
  var lastFocus = null;

  function pad2(n) { return (n < 10 ? "0" : "") + n; }

  function fadeClose(el, outClass, done) {
    if (reduce || el.hidden) { done(); return; }
    el.classList.add(outClass);
    var t = setTimeout(finish, 300);
    function finish() { el.removeEventListener("animationend", finish); clearTimeout(t); el.classList.remove(outClass); done(); }
    el.addEventListener("animationend", finish);
  }

  function renderProjectBody(slug) {
    var p = window.MC_PROJECTS && window.MC_PROJECTS[slug];
    if (!p) return false;
    modal.dataset.slug = slug;
    var body = modal.querySelector(".modal__body");
    var head = document.createElement("header");
    head.className = "modal__head";
    var h2 = document.createElement("h2");
    h2.id = "modal-title"; h2.textContent = p.title;
    var meta = document.createElement("p");
    meta.className = "modal__meta";
    meta.textContent = p.cat + (p.year ? ", " + p.year : "");
    head.append(h2, meta);
    (Array.isArray(p.desc) ? p.desc : [p.desc]).forEach(function (para) {
      var d = document.createElement("p");
      d.className = "modal__desc"; d.textContent = para;
      head.appendChild(d);
    });
    body.replaceChildren(head);
    var skip = p.skip || [];
    for (var i = 1; i <= p.n; i++) {
      if (skip.indexOf(i) !== -1) continue;
      var im = document.createElement("img");
      im.loading = "lazy"; im.alt = "";
      im.src = "assets/img/" + slug + "/" + pad2(i) + ".jpg";
      body.appendChild(im);
    }
    modal.querySelector(".modal__card").scrollTop = 0;
    return true;
  }

  function stepProject(dir) {
    var order = window.MC_ORDER || [];
    var idx = order.indexOf(modal.dataset.slug);
    if (idx < 0 || order.length < 2) return;
    renderProjectBody(order[(idx + dir + order.length) % order.length]);
  }

  function openProject(slug) {
    if (!modal || !window.MC_PROJECTS) { location.href = "work/" + slug + ".html"; return; }
    if (!renderProjectBody(slug)) { location.href = "work/" + slug + ".html"; return; }

    lastFocus = document.activeElement;
    modal.classList.remove("modal--out");
    modal.hidden = false;
    root.style.overflow = "hidden";
    if (lenis) lenis.stop();
    requestAnimationFrame(function () {
      var c = modal.querySelector(".modal__close");
      if (c) c.focus();
    });
  }

  function closeProject() {
    if (!modal || modal.hidden) return;
    fadeClose(modal, "modal--out", function () {
      modal.hidden = true;
      root.style.overflow = "";
      if (lenis) lenis.start();
      if (lastFocus && lastFocus.focus) lastFocus.focus();
    });
  }

  var zoomList = [], zoomIdx = 0, zImgs = null, zTop = 0;
  function renderZoom() {
    if (!zImgs) zImgs = zoom.querySelectorAll(".zoom__fig img");
    var cur = zImgs[zTop], nxt = zImgs[zTop ^ 1];
    var apply = function () { nxt.classList.add("shown"); cur.classList.remove("shown"); zTop ^= 1; };
    nxt.onload = apply;
    nxt.src = zoomList[zoomIdx];
    if (nxt.complete) apply();
    var multi = zoomList.length > 1;
    zoom.querySelector(".zoom__prev").hidden = !multi;
    zoom.querySelector(".zoom__next").hidden = !multi;
  }
  function stepZoom(d) {
    if (zoomList.length < 2) return;
    zoomIdx = (zoomIdx + d + zoomList.length) % zoomList.length;
    renderZoom();
  }
  function openZoom(src, imgs) {
    if (!zoom) return;
    zoomList = [].map.call(imgs || [], function (i) { return i.src; });
    zoomIdx = Math.max(0, zoomList.indexOf(src));
    if (!zoomList.length) zoomList = [src];
    zImgs = zoom.querySelectorAll(".zoom__fig img");
    zImgs.forEach(function (i) { i.classList.remove("shown"); i.removeAttribute("src"); });
    zTop = 1;
    renderZoom();
    zoom.classList.remove("zoom--out");
    zoom.hidden = false;
  }
  function closeZoom() {
    if (!zoom || zoom.hidden) return;
    fadeClose(zoom, "zoom--out", function () {
      zoom.hidden = true;
      zoom.querySelector("img").removeAttribute("src");
    });
  }

  if (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target.closest("[data-close]")) { closeProject(); return; }
      var nav = e.target.closest(".modal__nav");
      if (nav) { stepProject(nav.classList.contains("modal__next") ? 1 : -1); return; }
      var img = e.target.closest(".modal__body img");
      if (img && img.src) openZoom(img.src, modal.querySelectorAll(".modal__body img"));
    });
  }

  // project pages: click a shot to zoom, arrows/Esc to step and close
  var shots = document.querySelector(".case__shots");
  if (shots && zoom) {
    shots.addEventListener("click", function (e) {
      var img = e.target.closest("img");
      if (img && img.src) openZoom(img.src, shots.querySelectorAll("img"));
    });
  }

  // a slide slot quietly crossfades through its shots on its own
  if (shots && !reduce) {
    shots.querySelectorAll(".case__slide").forEach(function (slide) {
      var imgs = slide.querySelectorAll("img");
      if (imgs.length < 2) return;
      var i = 0;
      setInterval(function () {
        imgs[i].classList.remove("shown");
        i = (i + 1) % imgs.length;
        imgs[i].classList.add("shown");
      }, 2800);
    });
  }
  if (zoom) {
    zoom.addEventListener("click", function (e) {
      var nav = e.target.closest(".zoom__nav");
      if (nav) { e.stopPropagation(); stepZoom(nav.classList.contains("zoom__next") ? 1 : -1); return; }
      closeZoom();
    });
  }
  document.addEventListener("keydown", function (e) {
    if (zoom && !zoom.hidden) {
      if (e.key === "Escape") closeZoom();
      else if (e.key === "ArrowRight") stepZoom(1);
      else if (e.key === "ArrowLeft") stepZoom(-1);
      return;
    }
    if (!modal || modal.hidden) return;
    if (e.key === "Escape") { closeProject(); return; }
    if (e.key === "ArrowRight") { stepProject(1); return; }
    if (e.key === "ArrowLeft") { stepProject(-1); return; }
    if (e.key === "Tab") {
      var f = modal.querySelectorAll('button, a[href], [tabindex]:not([tabindex="-1"])');
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
    }
  });

  /* ---------------- fades ---------------- */
  var fades = document.querySelectorAll(".fade");
  if (fades.length) {
    if (reduce || !("IntersectionObserver" in window)) {
      fades.forEach(function (el) { el.classList.add("in"); });
    } else {
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (x) { if (x.isIntersecting) { x.target.classList.add("in"); io.unobserve(x.target); } });
      }, { rootMargin: "0px 0px -5% 0px" });
      fades.forEach(function (el) { io.observe(el); });
    }
  }

  /* ---------------- ambient glow in the empty left void ---------------- */
  (function ambient() {
    var el = document.querySelector(".ambient");
    if (!el || reduce || matchMedia("(max-width: 900px), (hover: none)").matches) return;
    var bay = document.querySelector(".bay");
    var tx = window.innerWidth * 0.2, ty = window.innerHeight * 0.4;
    var x = tx, y = ty, raf = null, active = false;

    function voidRight() {
      return bay ? bay.getBoundingClientRect().left : window.innerWidth * 0.4;
    }
    function tick() {
      x += (tx - x) * 0.055;
      y += (ty - y) * 0.055;
      el.style.setProperty("--ax", x + "px");
      el.style.setProperty("--ay", y + "px");
      if (Math.abs(tx - x) > 0.3 || Math.abs(ty - y) > 0.3) raf = requestAnimationFrame(tick);
      else raf = null;
    }
    function kick() { if (!raf) raf = requestAnimationFrame(tick); }

    window.addEventListener("pointermove", function (e) {
      tx = Math.min(e.clientX, voidRight());
      ty = e.clientY;
      if (!active) { active = true; el.classList.add("on"); }
      kick();
    });
    document.addEventListener("mouseleave", function () { el.classList.remove("on"); });
  })();

  /* ---------------- a bunny that peeks up once you reach the bottom ---------------- */
  (function bunny() {
    var el = document.getElementById("bunny");
    var foot = document.querySelector(".foot");
    if (!el || !foot) return;
    function check() {
      var r = foot.getBoundingClientRect();
      el.classList.toggle("show", r.top < window.innerHeight * 0.85 && r.bottom > 0);
    }
    window.addEventListener("scroll", check, { passive: true });
    window.addEventListener("resize", check);
    check();
  })();

  /* ---------------- the basketball under the mark ---------------- */
  (function hoops() {
    var rig = document.getElementById("hoops");
    var mark = document.querySelector(".mark");
    if (!rig || !mark) return;                    // only the home page has it

    var canPlay = !matchMedia("(max-width: 820px), (hover: none)").matches;
    mark.setAttribute("aria-expanded", "false");
    mark.style.cursor = "pointer";
    if (canPlay) mark.title = "shoot some hoops";
    mark.addEventListener("click", function (e) {
      e.preventDefault();                          // mark is the home link; on home it opens the game
      if (canPlay) toggle();
    });
    if (!canPlay) return;

    var ball = document.getElementById("hoopBall");
    var scoreEl = document.getElementById("hoopScore");
    var hint = document.getElementById("hoopHint");
    var rimEl = rig.querySelector(".hoops__rim");
    var netEl = rig.querySelector(".hoops__net");
    var bay = document.querySelector(".bay");
    var aim = document.querySelector("#hoopAim line");

    var GRAV = 0.46, POWER = 0.105, MAXV = 25, DAMP = 0.55;
    var MOVE_AT = 5;
    var st = { x: 0, y: 0, vx: 0, vy: 0 };
    var home = { x: 0, y: 0, r: 22 }, rim = { lx: 0, rx: 0, y: 0 };
    var raf = null, driftRaf = null, driftT0 = 0;
    var active = false, moving = false, scored = false, bounces = 0, score = 0;
    var dragging = false, courtX = 0;

    function setCourt() {
      var left = bay ? bay.getBoundingClientRect().left : window.innerWidth * 0.32;
      courtX = Math.max(70, left / 2);
      rig.style.setProperty("--court-x", courtX + "px");
    }
    function readRim() {
      var r = rimEl.getBoundingClientRect();
      rim = { lx: r.left, rx: r.right, y: r.top + r.height / 2 };
    }
    function measure() {
      setCourt();
      var b = ball.getBoundingClientRect();
      home = { x: b.left + b.width / 2 - st.x, y: b.top + b.height / 2 - st.y, r: b.width / 2 };
      readRim();
    }
    function place() { ball.style.transform = "translate(" + st.x + "px," + st.y + "px)"; }
    function reset() {
      if (raf) { cancelAnimationFrame(raf); raf = null; }
      st = { x: 0, y: 0, vx: 0, vy: 0 };
      scored = false; bounces = 0;
      ball.classList.remove("flying");
      place();
    }

    /* the hoop starts drifting once you sink MOVE_AT shots */
    function driftLoop(now) {
      if (!moving || !active) { driftRaf = null; rig.style.setProperty("--drift", "0px"); return; }
      var range = Math.min(Math.max(courtX - 48, 26), 120);
      rig.style.setProperty("--drift", (Math.sin((now - driftT0) / 1150) * range).toFixed(1) + "px");
      driftRaf = requestAnimationFrame(driftLoop);
    }
    function startDrift() {
      if (driftRaf) return;
      driftT0 = performance.now();
      driftRaf = requestAnimationFrame(driftLoop);
    }

    function tick() {
      readRim();
      var prevY = home.y + st.y;
      st.vy += GRAV; st.x += st.vx; st.y += st.vy;
      var cx = home.x + st.x, cy = home.y + st.y, R = home.r;

      if (!scored) {
        if (st.vy > 0 && prevY <= rim.y && cy >= rim.y &&
            cx > rim.lx + R * 0.4 && cx < rim.rx - R * 0.4) {
          scored = true; onScore();
        } else {
          [[rim.lx, rim.y], [rim.rx, rim.y]].forEach(function (p) {
            var dx = cx - p[0], dy = cy - p[1], d = Math.hypot(dx, dy);
            if (d > 0 && d < R + 2) {
              var nx = dx / d, ny = dy / d, dot = st.vx * nx + st.vy * ny;
              st.vx = (st.vx - 2 * dot * nx) * DAMP;
              st.vy = (st.vy - 2 * dot * ny) * DAMP;
              st.x += nx * 3; st.y += ny * 3;
            }
          });
          var floor = window.innerHeight - 16;
          if (cy + R > floor && st.vy > 0) {
            st.vy = -st.vy * DAMP; st.vx *= 0.72;
            st.y = floor - R - home.y;
            if (++bounces > 2 || Math.abs(st.vy) < 2.6) {
              ball.classList.remove("flying");
              raf = null; setTimeout(reset, 300); return;
            }
          }
        }
      }
      if (cx < -180 || cx > window.innerWidth + 180 || cy > window.innerHeight + 400) { reset(); return; }
      place();
      raf = requestAnimationFrame(tick);
    }

    function onScore() {
      score++;
      scoreEl.textContent = score;
      scoreEl.classList.remove("pop"); void scoreEl.offsetWidth; scoreEl.classList.add("pop");
      netEl.classList.remove("swish"); void netEl.offsetWidth; netEl.classList.add("swish");
      ball.classList.remove("flying");
      if (score >= MOVE_AT && !moving) { moving = true; startDrift(); }
    }

    function shoot(cx, cy) {
      var vx = (home.x + st.x - cx) * POWER;
      var vy = (home.y + st.y - cy) * POWER;
      var m = Math.hypot(vx, vy);
      if (m < 3) return;
      if (m > MAXV) { vx = vx / m * MAXV; vy = vy / m * MAXV; }
      st.vx = vx; st.vy = vy;
      bounces = 0; scored = false;
      ball.classList.add("flying");
      if (hint) hint.classList.add("gone");
      if (raf) cancelAnimationFrame(raf);
      raf = requestAnimationFrame(tick);
    }

    ball.addEventListener("pointerdown", function (e) {
      if (raf || st.vx || st.vy) return;
      dragging = true;
      measure();
      try { ball.setPointerCapture(e.pointerId); } catch (_) {}
      rig.classList.add("aiming");
      aim.setAttribute("x1", home.x + st.x); aim.setAttribute("y1", home.y + st.y);
      aim.setAttribute("x2", e.clientX); aim.setAttribute("y2", e.clientY);
    });
    ball.addEventListener("pointermove", function (e) {
      if (!dragging) return;
      aim.setAttribute("x2", e.clientX); aim.setAttribute("y2", e.clientY);
    });
    function endDrag(e) {
      if (!dragging) return;
      dragging = false;
      rig.classList.remove("aiming");
      try { ball.releasePointerCapture(e.pointerId); } catch (_) {}
      shoot(e.clientX, e.clientY);
    }
    ball.addEventListener("pointerup", endDrag);
    ball.addEventListener("pointercancel", endDrag);

    window.addEventListener("resize", function () {
      if (active && !dragging) { setCourt(); if (!raf) { reset(); measure(); } }
    });

    function toggle() {
      active = !active;
      mark.setAttribute("aria-expanded", active ? "true" : "false");
      if (active) {
        moving = false; score = 0;
        rig.style.setProperty("--drift", "0px");
        rig.hidden = false;
        void rig.offsetWidth;                 // reflow so the fade-in transition runs
        rig.classList.add("on");
        reset(); measure();
        if (hint) hint.classList.remove("gone");
        scoreEl.textContent = "0";
        requestAnimationFrame(measure);        // re-measure once layout settles
      } else {
        rig.classList.remove("on");
        moving = false;
        if (raf) { cancelAnimationFrame(raf); raf = null; }
        if (driftRaf) { cancelAnimationFrame(driftRaf); driftRaf = null; }
        setTimeout(function () { if (!active) rig.hidden = true; }, 420);
      }
    }
  })();
})();
