function setSite(color, font) {
    document.documentElement.style.setProperty('--me-color', color);
    document.documentElement.style.setProperty('--me-font-family', font);
}

$(function () {

        let href = location.href
        let origin = location.origin
        let pathname = location.pathname
        let hostname = location.hostname;
        let siteName = location.hostname.split('.')[0];
        document.title = siteName;

        try {
            document.querySelector('[data-clickout-type="native_table_box_processed"]').remove(); // lower advert
        } catch (err) {
        }

        try {
            document.querySelector("body > div.main > main > section.container-fluid.bg-gradient").remove(); // Guides front page
        } catch (err) {
        }

        try {
            document.querySelector("#style-css-css").remove(); // their's style.css
        } catch (err) {
        }

        try {
            document.querySelector("body > div.main > main > section.container.pb-20.pt-sm-60").remove(); // newsletter
        } catch (err) {
        }

        try {
            document.querySelector(".newsletter.home-newsletter.single").remove(); // newsletter
        } catch (err) {
        }

        try {
            document.querySelector("#widget_container").remove(); // widget Buy/Sell at the best rates
        } catch (err) {
        }

        try {
            document.querySelectorAll(".socials").forEach((e) => { // twitter and others
                e.remove();
            });
        } catch (err) {
        }

        try {
            document.querySelectorAll(".modal").forEach((e) => {
                e.remove();
            });
        } catch (err) {
        }

        try {
            document.querySelectorAll(".article-tag-box").forEach((e) => { // tags
                e.remove();
            });
        } catch (err) {
        }

        try {
            $("a").remove(":contains('Twitter')");
        } catch (err) {
        }

        try {
            $("section").remove(":contains('Videos')");
        } catch (err) {
        }

        try {
            document.querySelector("body > div.main > main > section:nth-child(5)").remove(); // Buy/Sell at the best rates (front page)
        } catch (err) {
        }

        $("head").prepend("<link href=\"/assets/images/favicon.png\" rel=\"shortcut icon\"/>" +
            "<link href=\"https://cdn.jsdelivr.net/gh/orestbida/cookieconsent@v2.9.2/dist/cookieconsent.css\" rel=\"stylesheet\"/>" +
            "<script defer=\"\" src=\"/assets/js/cookieconsent.js\"></script>" +
            "<script defer=\"\" src=\"/assets/js/cookieconsent-init.js\"></script>");

        $("#menu-header > li:nth-child(10) > ul").load("/kak-index.html #menu-header > li:nth-child(9) > ul > li", function () { // fix recommended
            try {
                document.querySelectorAll("a").forEach((e) => { // edit links
                    e.href = e.href.replace("https://cryptonews.com", "");
                });
            } catch (err) {
            }
        });

        $("#menu-item-119744 > ul").load("/kak-index.html #menu-item-119744 > ul > li", function () { // fix recommended footer
            try {
                document.querySelectorAll("a").forEach((e) => { // edit links
                    e.href = e.href.replace("https://cryptonews.com", "");
                });
            } catch (err) {
            }
        });

        // remove links in exchanges, couldn't replace them back to cryptonews
        try {
            let ha = document.querySelectorAll("a.button-more").forEach((e) => {
                e.remove();
            });
        } catch (err) {
        }

        try {
            document.querySelectorAll('.me-mailto').forEach((e) => {
                e.outerHTML = '<a href="mailto:support@' + hostname + '" class="d-inline-block" style="color:#fff">support@' + hostname + '</a>';
            });
        } catch (err) {
        }

        try {
            document.querySelector(".header__logo > img").src = "/assets/images/" + hostname + ".svg";
        } catch (err) {
        }

        if (hostname === 'da-1.com' || hostname === 'intspeed.com' || hostname === 'hindex.amkamdam.com' || hostname === 'xxx.xx') {
            setSite('green', 'Kanit')
        }

        if (hostname === 'huy.com' || hostname === 'xxx.xx' || hostname === 'xxx.xx') {
            setSite('pink', 'Oswald')
        }

        if (hostname === 'huy-1.com' || hostname === 'xxx.xx' || hostname === 'xxx.xx') {
            setSite('red', 'Playfair Display')
        }

        // change to site name
        try {
            document.querySelector(".breadcrumbs").children[0].textContent = siteName
        } catch (err) {

        }

        // change to site name
        try {
            document.querySelector("#copyright").textContent = '© 2023 ' + siteName + '. All rights reserved';
        } catch (err) {

        }

        function setSi(e) {
            e.innerHTML = e.innerHTML.replace(/cryptonews/g, siteName);
            e.innerHTML = e.innerHTML.replace(/Cryptonews/g, siteName);
            e.innerHTML = e.innerHTML.replace(/CryptoNews/g, siteName);
        }

        // change to site name
        try {
            document.body.querySelectorAll('.layout-size').forEach(setSi);
        } catch (err) {
        }

        // insert ads
        // index.html
        $("body > div.main > main > section:nth-child(2) > div > div > div.col-12.col-lg-9 > div.dslot.pb-20.d-md-none").load('/me-index.html [did="16"] > a');
        $("body > div.main > main > section:nth-child(2) > div > div > div.col-12.col-lg-9 > div.dslot.pb-20.d-none.d-md-block").load('/me-index.html [did="11"] > a');
        $("body > div.main > main > section:nth-child(2) > div > div > div.col-12.col-lg-3 > div.dslot").load('/me-index.html [did="1"] > a');
        $("body > div.main > main > section:nth-child(5) > div > div").load('/me-index.html [did="2"] > a');

        //news/index.html
        $("body > div.main > main > div:nth-child(2) > div > div > div.col-12.col-lg-3 > div.dslot").load('/me-index.html [did="4"] > a');

        // news/*.htm
        $("body > div.main > div:nth-child(1) > div:nth-child(2) > main > div > div.col-12.col-md-9.mb-40 > div.article-single__content.category_contents_details > div.dslot.text-right").load('/me-index.html [did="9"] > a');
        $("body > div.main > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(1)").load('/me-index.html [did="6"] > a');
        $("body > div.main > div:nth-child(1) > div:nth-child(2) > main > div > div.col-12.col-md-9.mb-40 > div.article-single__content.category_contents_details > div:nth-child(16)").load('/me-index.html [did="12"] > a');
        $("body > div.main > div:nth-child(2) > div:nth-child(2) > main > div > div.col-12.col-md-9.mb-40 > div.article-single__content.category_contents_details > div:nth-child(15)").load('/me-index.html [did="12"] > a');
        $("body > div.main > div:nth-child(1) > div:nth-child(2) > main > div > div.col-12.col-md-9.mb-40 > div.article-single__content.category_contents_details > div.dslot.row.mb-20").load('/me-index.html [did="5"] > a');
        $("body > div.main > div:nth-child(1) > div:nth-child(2) > div > div:nth-child(4)").load('/me-index.html [did="7"] > a');
        $("body > div.main > main > div > div > div.col-12.col-lg-9 > div.scrollspy > div").load('/me-index.html [did="5"] > a');
        $("#altcoins > div > div.dslot").load('/me-index.html [did="5"] > a');
        $("body > div.main > main > div > div.mb-50.c-black > coinlist > div.mb-60.dslot").load('/me-index.html #1160x90 > a');
        $("body > div.main > div > div > main > div.row > div.scrollspy.col-lg-9.col-md-9.col-sm-12 > div:nth-child(2) > div > div > div").load('/me-index.html [did="5"] > a');
        $('.dslot').removeClass('dslot').addClass('huyslot');

        // disable theirs cookies
        try {
            document.querySelectorAll('script[type="rocketlazyloadscript"]')[3].remove();
        } catch (err) {
        }
    }
);

$(window).load(function () {
    // Animate loader off screen
    $(".se-pre-con").fadeOut("slow");
});
