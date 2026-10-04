/**
 * Jholo University - site behaviour
 *
 * Vanilla JS, no dependencies, no build step. Loaded with `defer`.
 *
 * Every feature is an init function that bails out early if its markup is not
 * on the page. That way one file serves every template, and a page that has no
 * accordion simply skips it.
 */
(function () {
    'use strict';

    /* ----------------------------------------------------------------------
       Shared breakpoint
       Must stay in step with the `@media (max-width: 1199px)` block in
       static/css/main.css - that is the width at which the horizontal bar
       becomes the panel menu.
       ---------------------------------------------------------------------- */
    var DESKTOP_NAV = '(min-width: 1200px)';

    /* ----------------------------------------------------------------------
       Mobile navigation
       Opens/closes the slide-down panel and keeps aria-expanded in sync so
       screen readers announce the state change.
       ---------------------------------------------------------------------- */
    function initNav() {
        var toggle = document.getElementById('nav-toggle');
        var nav = document.getElementById('primary-nav');

        if (!toggle || !nav) {
            return;
        }

        function setOpen(isOpen) {
            nav.classList.toggle('is-open', isOpen);
            toggle.setAttribute('aria-expanded', String(isOpen));
            toggle.setAttribute(
                'aria-label',
                isOpen ? 'Close navigation menu' : 'Open navigation menu'
            );

            if (!isOpen) {
                closeAllDropdowns();
            }
        }

        toggle.addEventListener('click', function () {
            var isOpen = toggle.getAttribute('aria-expanded') === 'true';
            setOpen(!isOpen);
        });

        // Tapping a link should close the panel, not navigate with it open
        nav.addEventListener('click', function (event) {
            if (event.target.closest('.subnav a')) {
                setOpen(false);
            }
        });

        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape') {
                closeAllDropdowns();
                setOpen(false);
                toggle.focus();
            }
        });

        document.addEventListener('click', function (event) {
            if (!nav.classList.contains('is-open')) {
                return;
            }
            if (nav.contains(event.target) || toggle.contains(event.target)) {
                return;
            }
            setOpen(false);
        });

        // Leaving the mobile breakpoint while open would strand the menu
        var desktop = window.matchMedia(DESKTOP_NAV);
        var onChange = function (event) {
            if (event.matches) {
                setOpen(false);
            }
        };

        if (desktop.addEventListener) {
            desktop.addEventListener('change', onChange);
        } else if (desktop.addListener) {
            desktop.addListener(onChange);
        }

        initDropdowns(nav);
    }

    /* ----------------------------------------------------------------------
       Dropdown menus

       Hover and :focus-within already open these through CSS, so this only
       maintains the is-open class and the ARIA state - which is what makes
       them work on touch devices, where there is no hover.

       Closing a sibling on open keeps one menu visible at a time, and the
       small open delay stops a dropdown flashing while the pointer crosses
       the bar on its way to another item.
       ---------------------------------------------------------------------- */
    var OPEN_DELAY = 120;
    var CLOSE_DELAY = 180;

    function initDropdowns(nav) {
        var parents = nav.querySelectorAll('.nav__item--parent');

        if (!parents.length) {
            return;
        }

        var desktop = window.matchMedia(DESKTOP_NAV);
        var closeTimers = [];

        function cancelTimers() {
            closeTimers.forEach(clearTimeout);
            closeTimers = [];
        }

        function openItem(item) {
            cancelTimers();

            parents.forEach(function (other) {
                if (other !== item) {
                    setItemOpen(other, false);
                }
            });

            setItemOpen(item, true);
        }

        function setItemOpen(item, isOpen) {
            var trigger = item.querySelector('[data-nav-toggle]');
            var panel = item.querySelector('[data-nav-panel]');

            item.classList.toggle('is-open', isOpen);
            if (trigger) {
                trigger.setAttribute('aria-expanded', String(isOpen));
            }
            if (panel) {
                panel.classList.toggle('is-open', isOpen);
            }
        }

        function closeItem(item) {
            closeTimers.push(
                setTimeout(function () {
                    setItemOpen(item, false);
                }, CLOSE_DELAY)
            );
        }

        parents.forEach(function (item) {
            var trigger = item.querySelector('[data-nav-toggle]');

            if (!trigger) {
                return;
            }

            // Pointer: hover intent on desktop only
            item.addEventListener('pointerenter', function () {
                if (!desktop.matches) {
                    return;
                }
                openItem(item);
            });

            item.addEventListener('pointerleave', function () {
                if (!desktop.matches) {
                    return;
                }
                closeItem(item);
            });

            // Click / tap / keyboard Enter - works everywhere
            trigger.addEventListener('click', function () {
                var isOpen = trigger.getAttribute('aria-expanded') === 'true';
                cancelTimers();

                if (isOpen) {
                    setItemOpen(item, false);
                } else {
                    openItem(item);
                }
            });

            // Tabbing past the last link in a dropdown should close it
            item.addEventListener('focusout', function (event) {
                if (item.contains(event.relatedTarget)) {
                    return;
                }
                setItemOpen(item, false);
            });
        });

        closeAllDropdowns = function () {
            cancelTimers();
            parents.forEach(function (item) {
                setItemOpen(item, false);
            });
        };
    }

    var closeAllDropdowns = function () {};

    /* ----------------------------------------------------------------------
       Header shadow on scroll - a flat border reads as "pasted on"
       ---------------------------------------------------------------------- */
    function initStickyHeader() {
        var header = document.getElementById('site-header');

        if (!header) {
            return;
        }

        var ticking = false;

        function update() {
            header.classList.toggle('is-stuck', window.scrollY > 8);
            ticking = false;
        }

        window.addEventListener(
            'scroll',
            function () {
                if (ticking) {
                    return;
                }
                ticking = true;
                window.requestAnimationFrame(update);
            },
            { passive: true }
        );

        update();
    }

    /* ----------------------------------------------------------------------
       Accordion
       Uses the grid-template-rows 0fr -> 1fr trick so the panel animates to
       its natural height without JavaScript measuring anything.
       ---------------------------------------------------------------------- */
    function initAccordion() {
        var accordions = document.querySelectorAll('.accordion');

        if (!accordions.length) {
            return;
        }

        accordions.forEach(function (accordion) {
            var triggers = accordion.querySelectorAll('.accordion__trigger');

            triggers.forEach(function (trigger) {
                var panelId = trigger.getAttribute('aria-controls');
                var panel = panelId ? document.getElementById(panelId) : null;

                if (panel) {
                    panel.setAttribute('data-open', String(trigger.getAttribute('aria-expanded') === 'true'));
                }

                trigger.addEventListener('click', function () {
                    var isOpen = trigger.getAttribute('aria-expanded') === 'true';

                    trigger.setAttribute('aria-expanded', String(!isOpen));
                    if (panel) {
                        panel.setAttribute('data-open', String(!isOpen));
                    }
                });
            });
        });
    }

    /* ----------------------------------------------------------------------
       Animated counters
       Counts up once, when the element scrolls into view. Skipped entirely
       for users who prefer reduced motion.
       ---------------------------------------------------------------------- */
    function initCounters() {
        var counters = document.querySelectorAll('[data-count-to]');

        if (!counters.length) {
            return;
        }

        var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

        function renderFinal(element) {
            element.textContent = element.getAttribute('data-count-to') + '+';
        }

        function animate(element) {
            var target = parseInt(element.getAttribute('data-count-to'), 10);
            var duration = 1400;
            var start = null;

            function step(timestamp) {
                if (start === null) {
                    start = timestamp;
                }

                var progress = Math.min((timestamp - start) / duration, 1);
                // easeOutCubic
                var eased = 1 - Math.pow(1 - progress, 3);

                element.textContent = Math.floor(target * eased).toLocaleString();

                if (progress < 1) {
                    window.requestAnimationFrame(step);
                } else {
                    renderFinal(element);
                }
            }

            window.requestAnimationFrame(step);
        }

        counters.forEach(function (element) {
            if (reduceMotion.matches || !('IntersectionObserver' in window)) {
                renderFinal(element);
                return;
            }

            var observer = new IntersectionObserver(function (entries) {
                entries.forEach(function (entry) {
                    if (!entry.isIntersecting) {
                        return;
                    }
                    animate(entry.target);
                    observer.unobserve(entry.target);
                });
            }, { threshold: 0.4 });

            observer.observe(element);
        });
    }

    /* ----------------------------------------------------------------------
       Back to top - shown only once the user is past the hero
       ---------------------------------------------------------------------- */
    function initBackToTop() {
        var button = document.getElementById('back-to-top');

        if (!button) {
            return;
        }

        var ticking = false;

        function update() {
            button.hidden = window.scrollY < 400;
            ticking = false;
        }

        window.addEventListener(
            'scroll',
            function () {
                if (ticking) {
                    return;
                }
                ticking = true;
                window.requestAnimationFrame(update);
            },
            { passive: true }
        );

        button.addEventListener('click', function () {
            var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
            window.scrollTo({ top: 0, behavior: reduceMotion ? 'auto' : 'smooth' });
        });

        update();
    }

    /* ----------------------------------------------------------------------
       Under development notice

       Links that point somewhere real navigate and are left alone. Links with
       no destination yet (href="#" placeholders in the footer) would otherwise
       silently jump the visitor to the top of the page, so they are caught here
       and answered with a short, honest message instead.

       Catch is delegated from document, so a link added to any template later
       works without touching this file.
       ---------------------------------------------------------------------- */
    var TOAST_DURATION = 4000;

    function initDevNotice() {
        var toast = document.getElementById('site-toast');
        var text = document.getElementById('site-toast-text');
        var close = document.getElementById('site-toast-close');

        if (!toast || !text) {
            return;
        }

        var timer = null;

        function hide() {
            window.clearTimeout(timer);
            timer = null;
            toast.classList.remove('is-visible');

            // Keep it in the accessibility tree until the fade finishes.
            window.setTimeout(function () {
                if (!toast.classList.contains('is-visible')) {
                    toast.hidden = true;
                }
            }, 240);
        }

        function show(message) {
            text.textContent = message;
            toast.hidden = false;

            // Force a reflow so the transition runs when the toast is already
            // on screen from a previous click.
            void toast.offsetWidth;
            toast.classList.add('is-visible');

            window.clearTimeout(timer);
            timer = window.setTimeout(hide, TOAST_DURATION);
        }

        document.addEventListener('click', function (event) {
            var target = event.target;

            if (!target || !target.closest) {
                return;
            }

            var link = target.closest('a[href="#"], a:not([href]), a[href=""]');

            if (!link || link.hasAttribute('download')) {
                return;
            }

            event.preventDefault();

            // A link can carry its own wording, e.g. "Privacy is still being
            // written". Otherwise fall back to the generic line.
            show(
                link.getAttribute('data-dev') ||
                'Website is under development'
            );
        });

        if (close) {
            close.addEventListener('click', hide);
        }

        document.addEventListener('keydown', function (event) {
            if (event.key === 'Escape' && !toast.hidden) {
                hide();
            }
        });
    }

    /* ----------------------------------------------------------------------
       Carousel

       Vanilla, no dependencies. Progressive enhancement: the markup is a plain
       stacked list, so this function adds the is-ready class and only then
       takes over. Everything below is driven off data-carousel attributes, so
       the same file serves any template that uses the pattern.

       Non-current slides get aria-hidden and, where the browser supports it,
       inert - otherwise a keyboard user would tab into a message they cannot
       see.

       data-carousel-label on the carousel sets the noun used in the live
       region, so a carousel of photographs announces "Place 2 of 5" rather
       than "Message 2 of 5". It defaults to "Message".
       ---------------------------------------------------------------------- */
    var CAROUSEL_INTERVAL = 7000;
    var SWIPE_THRESHOLD = 45;

    function initCarousel() {
        var carousels = document.querySelectorAll('[data-carousel]');

        carousels.forEach(function (carousel) {
            var viewport = carousel.querySelector('[data-carousel-viewport]');
            var track = carousel.querySelector('[data-carousel-track]');
            var slides = carousel.querySelectorAll('[data-carousel-slide]');
            var dots = carousel.querySelectorAll('[data-carousel-dot]');
            var prev = carousel.querySelector('[data-carousel-prev]');
            var next = carousel.querySelector('[data-carousel-next]');
            var status = carousel.querySelector('[data-carousel-status]');

            if (!track || !viewport || slides.length < 2) {
                return;
            }

            var supportsInert = 'inert' in HTMLElement.prototype;
            var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
            var noun = carousel.getAttribute('data-carousel-label') || 'Message';
            var total = slides.length;
            var index = 0;
            var timer = null;

            function render(announce) {
                track.style.transform = 'translate3d(' + (-index * 100) + '%, 0, 0)';

                slides.forEach(function (slide, i) {
                    var isCurrent = i === index;

                    slide.classList.toggle('is-current', isCurrent);
                    slide.setAttribute('aria-hidden', String(!isCurrent));

                    if (supportsInert) {
                        slide.inert = !isCurrent;
                    }
                });

                dots.forEach(function (dot, i) {
                    dot.setAttribute('aria-current', i === index ? 'true' : 'false');
                });

                if (announce && status) {
                    var label = slides[index].getAttribute('aria-label') || '';
                    var role = slides[index].querySelector('.tag');
                    status.textContent =
                        noun + ' ' + label + (role ? ': ' + role.textContent.trim() : '');
                }
            }

            function goTo(target) {
                // Wrap in both directions so the arrows never dead-end.
                index = ((target % total) + total) % total;
                render(true);
            }

            function stop() {
                if (timer) {
                    window.clearInterval(timer);
                    timer = null;
                }
            }

            function start() {
                stop();

                // Someone who has asked for less motion should get the messages
                // on demand rather than sliding past on a timer.
                if (reduceMotion.matches) {
                    return;
                }

                timer = window.setInterval(function () {
                    goTo(index + 1);
                }, CAROUSEL_INTERVAL);
            }

            if (prev) {
                prev.addEventListener('click', function () {
                    goTo(index - 1);
                    start();
                });
            }

            if (next) {
                next.addEventListener('click', function () {
                    goTo(index + 1);
                    start();
                });
            }

            dots.forEach(function (dot, i) {
                dot.addEventListener('click', function () {
                    goTo(i);
                    start();
                });
            });

            carousel.addEventListener('keydown', function (event) {
                if (event.key === 'ArrowLeft') {
                    event.preventDefault();
                    goTo(index - 1);
                } else if (event.key === 'ArrowRight') {
                    event.preventDefault();
                    goTo(index + 1);
                } else {
                    return;
                }

                start();
            });

            // Pause while the visitor is reading or driving the controls.
            carousel.addEventListener('mouseenter', stop);
            carousel.addEventListener('mouseleave', start);
            carousel.addEventListener('focusin', stop);
            carousel.addEventListener('focusout', start);

            // Swipe. Only a mostly-horizontal drag counts, so a vertical scroll
            // over the card is not hijacked.
            var startX = 0;
            var startY = 0;
            var tracking = false;

            viewport.addEventListener('touchstart', function (event) {
                if (event.touches.length !== 1) {
                    tracking = false;
                    return;
                }

                startX = event.touches[0].clientX;
                startY = event.touches[0].clientY;
                tracking = true;
            }, { passive: true });

            viewport.addEventListener('touchend', function (event) {
                if (!tracking) {
                    return;
                }

                tracking = false;

                var touch = event.changedTouches[0];
                var dx = touch.clientX - startX;
                var dy = touch.clientY - startY;

                if (Math.abs(dx) < SWIPE_THRESHOLD || Math.abs(dx) < Math.abs(dy)) {
                    return;
                }

                goTo(dx < 0 ? index + 1 : index - 1);
                start();
            }, { passive: true });

            carousel.classList.add('is-ready');
            render(false);
            start();
        });
    }

    /* ----------------------------------------------------------------------
       Hero image slider

    The home page hero uses a full-bleed background image carousel.
       ---------------------------------------------------------------------- */
    function initHeroSlider() {
        var slider = document.querySelector('[data-hero-slider]');

        if (!slider) {
            return;
        }

        var slides = slider.querySelectorAll('.hero__slide');
        var track = slider.querySelector('.hero__slide-track');
        var dots = slider.querySelectorAll('[data-hero-dot]');

        if (!slides.length || !track) {
            return;
        }

        var index = 0;
        var timer = null;
        var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');

        function render() {
            track.style.transform = 'translate3d(' + (-index * 100) + '%, 0, 0)';

            slides.forEach(function (slide, i) {
                slide.setAttribute('aria-hidden', String(i !== index));
            });

            dots.forEach(function (dot, i) {
                dot.classList.toggle('is-active', i === index);
                dot.setAttribute('aria-current', i === index ? 'true' : 'false');
            });
        }

        function stop() {
            if (timer) {
                window.clearInterval(timer);
                timer = null;
            }
        }

        function start() {
            stop();

            if (reduceMotion.matches) {
                return;
            }

            timer = window.setInterval(function () {
                index = (index + 1) % slides.length;
                render();
            }, 4500);
        }

        dots.forEach(function (dot, i) {
            dot.addEventListener('click', function () {
                index = i;
                render();
                start();
            });
        });

        slider.addEventListener('focusin', stop);
        slider.addEventListener('focusout', start);

        render();
        start();
    }

    function initGridReveal() {
        var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
        var items = document.querySelectorAll(
            '.grid > li, .quicklinks > li, .stats-band__inner > .stat, .footer__grid > .footer__col'
        );

        if (reduceMotion.matches || !('IntersectionObserver' in window) || !items.length) {
            return;
        }

        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (!entry.isIntersecting) {
                    return;
                }

                entry.target.classList.add('grid-item-reveal');
                observer.unobserve(entry.target);
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -24px 0px' });

        items.forEach(function (item, index) {
            item.style.setProperty('--grid-reveal-delay', (index % 4) * 65 + 'ms');
            observer.observe(item);
        });
    }

    /* ---------------------------------------------------------------------- */

    function init() {
        initNav();
        initStickyHeader();
        initAccordion();
        initCarousel();
        initHeroSlider();
        initGridReveal();
        initCounters();
        initBackToTop();
        initDevNotice();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
